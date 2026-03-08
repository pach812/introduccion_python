import marimo

__generated_with = "0.20.2"
app = marimo.App(width="medium")

with app.setup:
    from dataclasses import dataclass
    from pathlib import Path
    from typing import Iterator
    from urllib.parse import unquote, urlparse

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


@app.function
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
    # ---------------------------------------------------------------------
    # Run
    # ---------------------------------------------------------------------

    tree_url = "https://github.com/pach812/introduccion_python/tree/master/Material_Complementario/Semana_1/scr"

    local_public = download_github_folder(
        tree_url=tree_url,
        dest_dir="public",
        overwrite=True,
        prefix="L1_"
    )

    img_path = local_public

    print("\nRESULTS")
    print("base_dir =", get_local_base_dir())
    print("local_public =", local_public)
    print("local_public.exists() =", local_public.exists())

    print("\nFiles:")
    for p in list(local_public.rglob("*"))[:20]:
        if p.is_file():
            print(f" - {p} | size={p.stat().st_size} bytes")
        else:
            print(f" - {p}")
    return


if __name__ == "__main__":
    app.run()
