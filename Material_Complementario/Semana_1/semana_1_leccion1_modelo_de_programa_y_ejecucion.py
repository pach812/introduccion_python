# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo>=0.20.2",
#     "requests==2.32.5",
# ]
# ///

import marimo

__generated_with = "0.20.4"
app = marimo.App(
    width="medium",
    css_file="/usr/local/_marimo/custom.css",
    auto_download=["html"],
)


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    from __future__ import annotations

    from dataclasses import dataclass
    from typing import Iterable
    from urllib.parse import unquote, urlparse

    import requests

    from pathlib import Path

    img_path = mo.notebook_location() / "public"

    @dataclass(frozen=True)
    class GitHubTreeTarget:
        owner: str
        repo: str
        ref: str
        path: str  # repo-relative path (can be empty)


    def parse_github_tree_url(tree_url: str) -> GitHubTreeTarget:
        """
        Parse a GitHub 'tree' URL like:
        https://github.com/<owner>/<repo>/tree/<ref>/<path>

        Returns owner, repo, ref and decoded path.
        """
        parsed = urlparse(tree_url)
        if parsed.netloc.lower() != "github.com":
            raise ValueError("Expected a github.com URL.")

        parts = [p for p in parsed.path.split("/") if p]
        # Expected: owner / repo / tree / ref / (path...)
        if len(parts) < 4 or parts[2] != "tree":
            raise ValueError("Expected a URL of the form https://github.com/<owner>/<repo>/tree/<ref>/<path>")

        owner = parts[0]
        repo = parts[1]
        ref = parts[3]
        path = "/".join(parts[4:]) if len(parts) > 4 else ""
        path = unquote(path)

        return GitHubTreeTarget(owner=owner, repo=repo, ref=ref, path=path)


    def _github_contents(
        session: requests.Session,
        target: GitHubTreeTarget,
        path: str,
    ) -> list[dict]:
        """
        Call GitHub REST API 'Get repository content' for a directory path.
        For public repos, auth is optional (but rate-limits are stricter).
        """
        api_url = f"https://api.github.com/repos/{target.owner}/{target.repo}/contents/{path}"
        r = session.get(api_url, params={"ref": target.ref}, timeout=30)
        r.raise_for_status()

        data = r.json()
        if isinstance(data, dict):
            # This means the path is a file, not a directory
            raise ValueError(f"Path '{path}' is a file, expected a directory.")
        return data


    def _walk_github_dir(
        session: requests.Session,
        target: GitHubTreeTarget,
        base_path: str,
    ) -> Iterable[dict]:
        """
        Recursively yield file entries from a GitHub directory using the Contents API.
        Each yielded dict corresponds to a file item with 'path' and 'download_url'.
        """
        items = _github_contents(session=session, target=target, path=base_path)

        for item in items:
            item_type = item.get("type")
            if item_type == "file":
                yield item
            elif item_type == "dir":
                yield from _walk_github_dir(session=session, target=target, base_path=item["path"])
            else:
                # skip symlinks/submodules or unexpected types
                continue


    def download_github_folder_if_public_missing(
        tree_url: str,
        dest_dir: str | Path = "public",
        *,
        github_token: str | None = None,
    ) -> Path:
        """
        If dest_dir does not exist in the current working directory, create it and
        download all files from the GitHub folder specified by tree_url.

        Parameters
        ----------
        tree_url:
            GitHub folder URL in 'tree' form.
        dest_dir:
            Local destination folder (created only if missing).
        github_token:
            Optional GitHub token to increase rate limits.

        Returns
        -------
        Path to the local dest_dir.
        """
        dest_dir = mo.notebook_location() / dest_dir
        if dest_dir.exists():
            return dest_dir

        dest_dir.mkdir(parents=True, exist_ok=True)

        target = parse_github_tree_url(tree_url)

        headers = {"Accept": "application/vnd.github+json"}
        if github_token:
            headers["Authorization"] = f"Bearer {github_token}"

        with requests.Session() as session:
            session.headers.update(headers)

            for item in _walk_github_dir(session=session, target=target, base_path=target.path):
                download_url = item.get("download_url")
                rel_path = item["path"]

                if not download_url:
                    continue

                # Preserve folder structure relative to the chosen GitHub folder root
                if target.path:
                    rel_under_root = Path(rel_path).as_posix().replace(target.path.rstrip("/") + "/", "", 1)
                else:
                    rel_under_root = rel_path

                local_path = dest_dir / rel_under_root
                local_path.parent.mkdir(parents=True, exist_ok=True)

                if local_path.exists():
                    continue

                r = session.get(download_url, timeout=60)
                r.raise_for_status()
                local_path.write_bytes(r.content)

        return dest_dir

    tree_url = "https://github.com/pach812/introduccion_python/tree/master/Material%20Complementario/Semana%201/public"
    local_public = download_github_folder_if_public_missing(tree_url=tree_url, dest_dir="public")
    _var = 0
    return (img_path,)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    from pathlib import Path

    img_path = Path("https://github.com/pach812/introduccion_python/blob/master/pre-session/Semana%201/public/")
    img_path = mo.notebook_dir() / "public"
    return img_path, mo


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Semana 1 · Lección 1 — Modelo de programa y ejecución (Python)

    ## Propósito

    En esta lección se construye una idea operativa y verificable de qué es un *programa* en Python y qué significa que el intérprete lo ejecute **de forma secuencial**.

    El objetivo no es memorizar comandos, sino comprender el modelo mental mínimo para:

    - Escribir instrucciones en un orden lógico.
    - Predecir qué ocurrirá cuando el intérprete “lea” el código.
    - Interpretar errores como parte del proceso formal de depuración.
    """)
    return


@app.cell(hide_code=True)
def _(img_path, mo):
    mo.md(rf"""
    ## 1) ¿Qué es un programa?

    Un **programa** es una *secuencia* de instrucciones escritas en un lenguaje que el computador puede ejecutar.

    En Python:

    - Un archivo con extensión `.py` suele llamarse **script**.
    - El **intérprete** de Python ejecuta el programa instrucción por instrucción.
    - En un notebook (como marimo), se ejecutan celdas; **dentro de cada celda**, la ejecución también es secuencial.

    {mo.image(src=img_path/"Gemini_Generated_Image_q81h44q81h44q81h-2.png")}
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2) La idea clave: ejecución secuencial

    La ejecución secuencial significa:

    1. Python empieza arriba.
    2. Ejecuta la primera instrucción.
    3. Continúa con la siguiente, en orden, hasta terminar el archivo (o la celda).

    Esto es crucial para salud pública, porque análisis reproducibles (por ejemplo, un resumen diario de vigilancia epidemiológica) dependen de que el flujo sea:

    **entrada → procesamiento → salida**, en un orden estable y auditable.
    """)
    return


@app.cell
def _():
    # Demostración mínima de ejecución secuencial (salud pública)
    print("Informe de vigilancia — ejemplo mínimo")
    print("1) Recolección: consolidar notificaciones del día")
    print("2) Procesamiento: verificar consistencia básica de los registros")
    print("3) Salida: preparar resumen para el equipo de respuesta")
    return


@app.cell(hide_code=True)
def _(img_path, mo):
    mo.md(rf"""
    ## 3) Dos modos comunes de ejecutar Python

    ### 3.1 Modo interactivo (conversación)
    En el intérprete (por ejemplo, al ejecutar `python` en una terminal), aparece un prompt `>>>`.
    Ese prompt se puede leer como: **“¿qué quieres que ejecute ahora?”**.

    Este modo se usa para probar ideas rápidamente.

    {mo.image(src=img_path/"interpreter.png",height=300)}


    ### 3.2 Modo script (archivo `.py`)
    En lugar de escribir una línea a la vez, se ejecuta un archivo completo:

    - Escribes el código en un `.py`.
    - Ejecutas el archivo con Python.
    - Python recorre el archivo de arriba hacia abajo.

    {mo.image(src=img_path/"script.png")}

    **Marimo** es un entorno intermedio: combina un documento explicativo con celdas ejecutables para aprendizaje y demostración.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4) ¿Qué puede salir mal?

    En esta etapa inicial, lo más importante es reconocer que los errores **no** son un fracaso: son señales del intérprete para que ajustemos el código.

    Tres categorías útiles:

    - **Errores de sintaxis (SyntaxError):** la “gramática” del código no es válida.
    - **Errores en tiempo de ejecución (Runtime error):** el código es “legible” pero algo falla al ejecutarlo.
    - **Errores semánticos o lógicos:** el programa corre, pero produce un resultado distinto al que querías.

    En esta lección nos concentramos en el modelo de ejecución; los mecanismos formales de manejo de errores se abordarán más adelante.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejemplo conceptual de error de sintaxis (NO ejecutar)

    Si se escribe mal una instrucción, el intérprete no puede continuar.

    ```python
    pritn("Hola")  # error: nombre mal escrito
    ```

    La idea pedagógica aquí es simple:

    - Python necesita instrucciones **precisas**.
    - Un detalle pequeño puede detener la ejecución del programa.

    (En la práctica, aprenderemos a leer cuidadosamente el mensaje de error).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5) Mini-laboratorio guiado: “tres líneas, una historia”

    La meta es practicar el modelo mental:

    - Cada línea se ejecuta en orden.
    - El orden define el “relato” del programa.

    ### Actividad A (demostración)
    En el siguiente bloque, observa cómo el programa produce una narrativa ordenada sobre una jornada de vacunación.
    """)
    return


@app.cell
def _():
    print("Jornada de vacunación — narrativa secuencial")
    print("Paso 1: Recepción de biológicos y verificación de cadena de frío")
    print("Paso 2: Registro de personas vacunadas en el sistema")
    print("Paso 3: Cierre: consolidación y reporte de dosis aplicadas")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Actividad B (TU TURNO)

    **Instrucciones:**

    1. Crea un bloque de *tres* `print(...)`.
    2. Cada línea debe corresponder a una fase típica de un proceso de salud pública.
    3. El orden debe ser coherente y sin saltos.

    Sugerencias de temas (elige uno):
    - Triage en urgencias
    - Toma y transporte de muestras
    - Investigación de brotes (búsqueda activa, verificación, informe)

    **Regla didáctica:** no uses variables ni estructuras de control todavía; solo secuencia.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "Guía (una posible solución)": mo.md(
                r"""
    ```python
    print("Investigación de brote — ejemplo")
    print("Paso 1: Identificar y listar casos sospechosos")
    print("Paso 2: Verificar definición de caso y recolectar datos básicos")
    print("Paso 3: Elaborar un resumen preliminar para intervención")
    ```

    **Criterio de calidad:** si cambias el orden de los pasos, el relato pierde coherencia.
    """
            )
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6) Mini-reto final

    **Reto:** Crea una nueva celda y redacta un “micro-programa” de 5 líneas (5 `print(...)`) que simule la salida textual de un reporte breve de vigilancia semanal.

    Debe incluir (en orden):

    1. Título del reporte.
    2. Periodo (por ejemplo, “Semana epidemiológica 08”).
    3. Evento (por ejemplo, IRA, dengue, COVID-19, EDA).
    4. Resumen narrativo (una línea).
    5. Cierre (por ejemplo, “Fin del reporte”).
    """)
    return


@app.cell
def _():
    # Ejemplo de mini-reto (modelo)
    print("Ejemplo!")
    print("Reporte de vigilancia semanal")
    print("Periodo: Semana epidemiológica 08")
    print("Evento: Infección respiratoria aguda (IRA)")
    print("Resumen: Se observa estabilidad general con aumento leve en consultas.")
    print("Fin del reporte")
    return


if __name__ == "__main__":
    app.run()
