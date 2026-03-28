# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "pytest==9.0.2",
#     "requests==2.32.5",
# ]
# ///

import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")

with app.setup(hide_code=True):
    from dataclasses import dataclass, field
    from pathlib import Path
    from typing import Iterator
    from urllib.parse import unquote, urlparse
    import re
    import io
    import contextlib
    import traceback

    import marimo as mo
    import requests


    def debug_print(debug: bool, *args) -> None:
        """Print debug messages when debug=True."""
        if debug:
            print("[DEBUG]", *args)


    @dataclass(frozen=True)
    class GitHubTreeTarget:
        owner: str
        repo: str
        ref: str
        path: str


    def get_local_base_dir(debug: bool = False) -> Path:
        """
        Resolve a reliable local base directory for file writes.

        Preferred order:
        1. mo.notebook_dir()
        2. file:// path from mo.notebook_location()
        3. Path.cwd()
        """
        debug_print(debug, "Entering get_local_base_dir()")

        try:
            base_dir = Path(mo.notebook_dir())
            debug_print(debug, "Using mo.notebook_dir() =", base_dir)
            return base_dir
        except Exception as exc:
            debug_print(debug, "mo.notebook_dir() failed:", repr(exc))

        try:
            location = str(mo.notebook_location())
            parsed = urlparse(location)

            debug_print(debug, "mo.notebook_location() =", location)

            if parsed.scheme == "file":
                base_dir = Path(unquote(parsed.path)).parent
                debug_print(debug, "Using file:// notebook parent =", base_dir)
                return base_dir
        except Exception as exc:
            debug_print(debug, "mo.notebook_location() failed:", repr(exc))

        base_dir = Path.cwd()
        debug_print(debug, "Falling back to Path.cwd() =", base_dir)
        return base_dir


    def parse_github_tree_url(
        tree_url: str,
        debug: bool = False,
    ) -> GitHubTreeTarget:
        """
        Parse a GitHub tree URL of the form:
        https://github.com/<owner>/<repo>/tree/<ref>/<path>
        """
        debug_print(debug, "Entering parse_github_tree_url()")
        debug_print(debug, "tree_url =", tree_url)

        parsed = urlparse(tree_url)

        if parsed.netloc.lower() != "github.com":
            raise ValueError("Expected a github.com URL.")

        parts = [part for part in parsed.path.split("/") if part]
        debug_print(debug, "URL parts =", parts)

        if len(parts) < 4 or parts[2] != "tree":
            raise ValueError(
                "Expected URL format: https://github.com/<owner>/<repo>/tree/<ref>/<path>"
            )

        target = GitHubTreeTarget(
            owner=parts[0],
            repo=parts[1],
            ref=parts[3],
            path=unquote("/".join(parts[4:])) if len(parts) > 4 else "",
        )

        debug_print(debug, "Parsed target =", target)
        return target


    def github_contents(
        session: requests.Session,
        target: GitHubTreeTarget,
        path: str,
        debug: bool = False,
    ) -> list[dict]:
        """
        Return directory contents using the GitHub Contents API.
        """
        api_url = (
            f"https://api.github.com/repos/"
            f"{target.owner}/{target.repo}/contents/{path}"
        )

        debug_print(debug, "Entering github_contents()")
        debug_print(debug, "api_url =", api_url)
        debug_print(debug, "ref =", target.ref)

        response = session.get(api_url, params={"ref": target.ref}, timeout=30)

        debug_print(debug, "response.status_code =", response.status_code)
        debug_print(debug, "response.url =", response.url)

        response.raise_for_status()
        data = response.json()

        if isinstance(data, dict):
            raise ValueError(f"Path '{path}' is a file, expected a directory.")

        debug_print(debug, "Number of items returned =", len(data))
        return data


    def walk_github_dir(
        session: requests.Session,
        target: GitHubTreeTarget,
        base_path: str,
        debug: bool = False,
    ) -> Iterator[dict]:
        """
        Recursively yield file entries from a GitHub directory.
        """
        debug_print(debug, "Entering walk_github_dir()")
        debug_print(debug, "base_path =", base_path)

        items = github_contents(
            session=session,
            target=target,
            path=base_path,
            debug=debug,
        )

        for item in items:
            item_type = item.get("type")
            item_path = item.get("path")

            debug_print(debug, "Inspecting item:", {"type": item_type, "path": item_path})

            if item_type == "file":
                debug_print(debug, "Yielding file:", item_path)
                yield item
                continue

            if item_type == "dir":
                debug_print(debug, "Descending into directory:", item_path)
                yield from walk_github_dir(
                    session=session,
                    target=target,
                    base_path=item_path,
                    debug=debug,
                )
                continue

            debug_print(debug, "Skipping unsupported item type:", item_type)

        debug_print(debug, "Leaving walk_github_dir() for base_path =", base_path)


@app.function(hide_code=True)
def download_github_folder(
    tree_url: str,
    dest_dir: str | Path = "public",
    *,
    github_token: str | None = None,
    overwrite: bool = False,
    prefix: str | None = None,
    debug: bool = False,
) -> Path:
    """
    Download files from a GitHub folder using the Trees API (fast).

    This performs a single GitHub API request and filters files locally.

    Parameters
    ----------
    tree_url
        GitHub tree URL.

    dest_dir
        Local destination directory.

    github_token
        Optional GitHub token.

    overwrite
        Overwrite existing files.

    prefix
        Only download files whose name starts with this prefix.

    debug
        Enable debug logging.
    """

    debug_print(debug, "Entering download_github_folder()")
    debug_print(debug, "tree_url =", tree_url)

    base_dir = get_local_base_dir(debug)
    dest_path = base_dir / Path(dest_dir)
    dest_path.mkdir(parents=True, exist_ok=True)

    target = parse_github_tree_url(tree_url, debug)

    headers = {"Accept": "application/vnd.github+json"}

    if github_token:
        headers["Authorization"] = f"Bearer {github_token}"

    tree_api = f"https://api.github.com/repos/{target.owner}/{target.repo}/git/trees/{target.ref}"

    debug_print(debug, "tree_api =", tree_api)

    with requests.Session() as session:

        session.headers.update(headers)

        r = session.get(tree_api, params={"recursive": "1"}, timeout=30)
        r.raise_for_status()

        tree = r.json()["tree"]

        debug_print(debug, "Total objects in repo tree =", len(tree))

        files = [
            item
            for item in tree
            if item["type"] == "blob"
            and item["path"].startswith(target.path)
        ]

        debug_print(debug, "Files in target folder =", len(files))

        downloaded = 0

        for item in files:

            rel_path = item["path"]
            filename = Path(rel_path).name

            if prefix and not filename.startswith(prefix):
                debug_print(debug, "Skipping (prefix mismatch):", filename)
                continue

            rel_under_root = rel_path.removeprefix(target.path).lstrip("/")

            local_path = dest_path / rel_under_root
            local_path.parent.mkdir(parents=True, exist_ok=True)

            if local_path.exists() and not overwrite:
                debug_print(debug, "Skipping existing:", local_path)
                continue

            download_url = (
                f"https://raw.githubusercontent.com/"
                f"{target.owner}/{target.repo}/{target.ref}/{rel_path}"
            )

            debug_print(debug, "Downloading:", download_url)

            r = session.get(download_url, timeout=60)
            r.raise_for_status()

            local_path.write_bytes(r.content)

            downloaded += 1

    debug_print(debug, "Downloaded files =", downloaded)

    return dest_path


@app.cell
def _():
    # # ---------------------------------------------------------------------
    # # Run
    # # ---------------------------------------------------------------------

    # tree_url = "https://github.com/pach812/introduccion_python/tree/master/Material_Complementario/Semana_1/scr"

    # local_public = download_github_folder(
    #     tree_url=tree_url,
    #     dest_dir="public",
    #     overwrite=True,
    #     prefix="L1_"
    # )

    # img_path = local_public

    # print("\nRESULTS")
    # print("base_dir =", get_local_base_dir())
    # print("local_public =", local_public)
    # print("local_public.exists() =", local_public.exists())

    # print("\nFiles:")
    # for p in list(local_public.rglob("*"))[:20]:
    #     if p.is_file():
    #         print(f" - {p} | size={p.stat().st_size} bytes")
    #     else:
    #         print(f" - {p}")
    return


@app.class_definition(hide_code=True)
@dataclass
class AccordionBlock:
    """Represent a single parsed accordion block."""

    title: str | None
    content: str


@app.class_definition(hide_code=True)
@dataclass
class BaseAccordionContent:
    """
    Base class for accordion-style educational content.

    Supported format
    ----------------
    <Title>Content...
    <solucion>Content...
    """

    items_raw: list[str]
    prefix: str = "Item"

    _blocks: list[AccordionBlock] = field(
        default_factory=list, init=False, repr=False
    )
    _solution: AccordionBlock | None = field(
        default=None, init=False, repr=False
    )

    def __post_init__(self) -> None:
        self._validate_items()
        self._parse_items()

    def _validate_items(self) -> None:
        """Validate raw input items."""
        if not isinstance(self.items_raw, list):
            raise TypeError("items_raw must be a list of strings.")

        if len(self.items_raw) == 0:
            raise ValueError("items_raw must contain at least one item.")

        if not all(isinstance(item, str) for item in self.items_raw):
            raise TypeError("Each item must be a string.")

        if not all(item.strip() for item in self.items_raw):
            raise ValueError("Items cannot be empty strings.")

        if not isinstance(self.prefix, str) or not self.prefix.strip():
            raise ValueError("prefix must be a non-empty string.")

    @staticmethod
    def _parse_item(item: str) -> AccordionBlock:
        """
        Parse a raw item with optional embedded title.

        Accepted format:
            <Title>Content...
        """
        item = item.strip()

        match = re.match(r"^\s*<([^<>]+)>\s*(.*)$", item, flags=re.DOTALL)

        if match:
            title = match.group(1).strip()
            content = match.group(2).strip()

            if not title:
                raise ValueError(
                    "Item title inside angle brackets cannot be empty."
                )

            if not content:
                raise ValueError(
                    f"Item with title '{title}' must include content after the title."
                )

            return AccordionBlock(title=title, content=content)

        return AccordionBlock(title=None, content=item)

    def _parse_items(self) -> None:
        """Parse all raw items and separate optional solution block."""
        parsed_blocks = [self._parse_item(item) for item in self.items_raw]

        regular_blocks = []
        solution_block = None

        for block in parsed_blocks:
            if block.title and block.title.strip().lower() == "solucion":
                solution_block = block
            else:
                regular_blocks.append(block)

        self._blocks = regular_blocks
        self._solution = solution_block

    def _build_key(self, index: int, title: str | None) -> str:
        """Build the accordion key."""
        if title:
            return f"{self.prefix} {index}: {title}"
        return f"{self.prefix} {index}"

    @property
    def blocks(self) -> list[AccordionBlock]:
        """Return parsed regular blocks."""
        return self._blocks

    @property
    def solution(self) -> AccordionBlock | None:
        """Return optional solution block."""
        return self._solution


@app.class_definition(hide_code=True)
@dataclass
class MarkdownAccordionContent(BaseAccordionContent):
    """Accordion content rendered directly as markdown."""

    def _render_block(self, block: AccordionBlock):
        """Render one block as markdown."""
        return mo.md(block.content)

    @property
    def items(self) -> dict[str, mo.Html]:
        """Return accordion items."""
        accordion = {
            self._build_key(index=i, title=block.title): self._render_block(
                block
            )
            for i, block in enumerate(self.blocks, start=1)
        }

        if self.solution is not None:
            accordion["Solución"] = mo.md(self.solution.content)

        return accordion

    def render(self):
        """Render accordion."""
        return mo.accordion(self.items)


@app.class_definition
@dataclass
class TipContent(MarkdownAccordionContent):
    """Accordion content specialized for tips."""

    prefix: str = "Tip"


@app.cell(hide_code=True)
def _():
    _tip_content = TipContent(
        items_raw=[
            r"""
    <Validación de tipos>
    Recuerda que puedes usar:

    `isinstance(x, (int, float))`
    """,
            r"""
    <Positividad>
    Piensa si en este contexto clínico tiene sentido aceptar valores negativos.
    """,
            r"""
    <Redondeo seguro>
    Consulta la documentación del módulo `math` para encontrar una función
    que redondee hacia arriba.
    """,
        ]
    )

    mo.accordion(_tip_content.items)
    return


@app.class_definition(hide_code=True)
@dataclass
class TestResult:
    """Store the result of a single executed test block."""

    title: str | None
    description: str
    code: str
    passed: bool
    output: str
    error_type: str | None = None
    error_message: str | None = None
    traceback_text: str | None = None


@app.class_definition
@dataclass
class TestContent(BaseAccordionContent):
    """
    Accordion content specialized for executable tests.

    Supported code block formats
    ----------------------------
    ``-python ... ``-
    ``python ... ``
    """

    prefix: str = "Test"
    namespace: dict | None = None

    _results: list[TestResult] = field(default_factory=list, init=False, repr=False)

    def __post_init__(self) -> None:
        super().__post_init__()
        self._results = self._run_tests()

    @staticmethod
    def _extract_code_block(content: str) -> tuple[str, str]:
        """
        Extract one supported Python code block from the content.

        Returns
        -------
        tuple[str, str]
            description_without_code, code
        """
        patterns = [
            r"``-python\s*(.*?)\s*``-",
            r"``python\s*(.*?)\s*``",
        ]

        match = None
        matched_pattern = None

        for pattern in patterns:
            match = re.search(pattern, content, flags=re.DOTALL)
            if match:
                matched_pattern = pattern
                break

        if not match or matched_pattern is None:
            raise ValueError(
                "Each test block must include one code block using "
                "``-python ... ``- or ``python ... ``."
            )

        code = match.group(1).strip()
        description = re.sub(
            matched_pattern,
            "",
            content,
            flags=re.DOTALL
        ).strip()

        return description, code

    def _run_single_test(self, block: AccordionBlock) -> TestResult:
        """Execute a single parsed test block."""
        description, code = self._extract_code_block(block.content)

        stdout_buffer = io.StringIO()
        namespace = self.namespace if self.namespace is not None else globals()

        try:
            with contextlib.redirect_stdout(stdout_buffer):
                exec(code, namespace, namespace)

            return TestResult(
                title=block.title,
                description=description,
                code=code,
                passed=True,
                output=stdout_buffer.getvalue().strip(),
            )

        except Exception as exc:
            return TestResult(
                title=block.title,
                description=description,
                code=code,
                passed=False,
                output=stdout_buffer.getvalue().strip(),
                error_type=type(exc).__name__,
                error_message=str(exc),
                traceback_text=traceback.format_exc(),
            )

    def _run_tests(self) -> list[TestResult]:
        """Execute all parsed test blocks."""
        return [self._run_single_test(block) for block in self.blocks]

    @property
    def passed_count(self) -> int:
        """Return the number of passed tests."""
        return sum(result.passed for result in self._results)

    @property
    def failed_count(self) -> int:
        """Return the number of failed tests."""
        return len(self._results) - self.passed_count

    @property
    def total_count(self) -> int:
        """Return total number of tests."""
        return len(self._results)

    @property
    def summary_markdown(self) -> str:
        """Return a compact summary in markdown."""
        if self.total_count == 0:
            return "No tests were executed."

        if self.failed_count == 0:
            return (
                f"### Tests summary\n\n"
                f"**PASS:** {self.passed_count} / {self.total_count} tests passed."
            )

        return (
            f"### Tests summary\n\n"
            f"**PASS:** {self.passed_count} / {self.total_count} tests passed.\n\n"
            f"**FAIL:** {self.failed_count} test(s) need attention."
        )

    def _build_result_key(self, index: int, result: TestResult) -> str:
        """Build the accordion key for a test result."""
        status = "PASS" if result.passed else "FAIL"

        if result.title:
            return f"{self.prefix} {index}: {result.title} — {status}"
        return f"{self.prefix} {index} — {status}"

    @staticmethod
    def _last_traceback_line(traceback_text: str | None) -> str | None:
        """Extract the last non-empty line from a traceback."""
        if not traceback_text:
            return None

        lines = [line.strip() for line in traceback_text.splitlines() if line.strip()]
        if not lines:
            return None

        return lines[-1]

    def _format_error_message(self, result: TestResult) -> str:
        """Return a clean error message."""
        last_line = self._last_traceback_line(result.traceback_text)

        if last_line:
            return last_line

        if result.error_type and result.error_message:
            return f"{result.error_type}: {result.error_message}"

        if result.error_type:
            return result.error_type

        return "Unknown error."

    def _render_result(self, result: TestResult):
        """Render a single test result."""
        parts = []

        if result.description:
            parts.append(result.description)

        parts.append("### Result")
        parts.append(f"**Status:** {'PASS' if result.passed else 'FAIL'}")

        if result.output:
            parts.append("### Output")
            parts.append(f"```\n{result.output}\n```")

        if not result.passed:
            parts.append("### Error")
            parts.append(f"**{self._format_error_message(result)}**")

        return mo.md("\n\n".join(parts))

    @property
    def items(self) -> dict[str, mo.Html]:
        """Return test results as accordion items."""
        accordion = {
            self._build_result_key(index=i, result=result): self._render_result(result)
            for i, result in enumerate(self._results, start=1)
        }

        if self.solution is not None:
            accordion["Qué son los test?"] = mo.md(self.solution.content)

        return accordion

    def render(self):
        """Render summary + accordion."""
        return mo.vstack(
            [
                mo.md(self.summary_markdown),
                mo.accordion(self.items),
            ]
        )


@app.function
def find_data_file(filename: str) -> Path:
    """Locate a data file in common execution directories."""
    candidates = [
        Path.cwd() / filename,
        Path(__file__).resolve().parent / filename,
        Path("/mnt/data") / filename,
    ]
    for path in candidates:
        if path.exists():
            return path
    raise FileNotFoundError(f"No se encontró el archivo: {filename}")


if __name__ == "__main__":
    app.run()
