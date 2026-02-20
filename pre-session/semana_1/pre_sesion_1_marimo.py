import marimo

__generated_with = "0.19.11"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _():
    import platform
    import sys
    from dataclasses import dataclass

    return platform, sys


@app.cell(hide_code=True)
def _(platform, sys):
    class EnvironmentInfo:
        python_version: str
        python_executable: str
        os: str
        machine: str
        processor: str

        def __init__ (self, python_version: str, python_executable: str, os: str, machine: str, processor: str):
            self.python_version = python_version
            self.python_executable = python_executable
            self.os = os
            self.machine = machine
            self.processor = processor

    def get_environment_info() -> EnvironmentInfo:
        return EnvironmentInfo(
            python_version=sys.version.split()[0],
            python_executable=sys.executable,
            os=platform.system(),
            machine=platform.machine(),
            processor=platform.processor(),
        )

    env_info = get_environment_info()
    return (env_info,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Pre–Sesión 1 — Primer contacto con Python (marimo)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Objetivos de aprendizaje

    Al finalizar esta pre–sesión, podrás:

    - Explicar qué es un programa y qué significa que Python sea un lenguaje interpretado.
    - Verificar tu entorno local: versión de Python y sistema operativo.
    - Ejecutar instrucciones básicas en Python (variables, tipos, operaciones, `print()`).
    - Producir un resultado verificable en la variable `pre_session_1_result`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Introducción conceptual

    Un **programa** es una secuencia de instrucciones que describe *qué hacer* con datos, de forma que una computadora pueda ejecutarlo de manera determinística.

    - **Hardware**: componentes físicos (CPU, memoria, disco, periféricos).
    - **Software**: instrucciones (programas) que controlan el hardware y transforman datos.

    Python es un lenguaje **interpretado**: el código se ejecuta mediante un intérprete que lee y ejecuta instrucciones. Esto facilita experimentar y aprender iterativamente.

    En esta pre–sesión, el énfasis no es “memorizar”, sino **comprender el flujo mínimo**: escribir → ejecutar → observar → ajustar.
    """)
    return


@app.cell(hide_code=True)
def _(env_info, mo):
    mo.md(rf"""
    ## Verificación del entorno actual (evidencia técnica)

    **Python version:** `{env_info.python_version}`  
    **Python executable:** `{env_info.python_executable}`  
    **OS:** `{env_info.os}`  
    **Machine:** `{env_info.machine}`  
    **Processor:** `{env_info.processor}`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Lenguaje mínimo: valores, tipos y variables

    Ideas clave:

    - Un **valor** es un dato (por ejemplo, `3`, `"hola"`, `True`).
    - Un **tipo** describe la naturaleza del valor (por ejemplo, `int`, `float`, `str`, `bool`).
    - Una **variable** es un nombre que referencia un valor.

    En Python, puedes inspeccionar el tipo con `type()`.
    """)
    return


@app.cell
def _():
    example_int = 7
    example_float = 3.14
    example_str = "salud pública"
    example_bool = True
    tu_ejemplo = "cualquier valor que quieras!"
    return example_bool, example_float, example_int, example_str, tu_ejemplo


@app.cell(hide_code=True)
def _(example_bool, example_float, example_int, example_str, mo, tu_ejemplo):
    mo.md(rf"""
    | Variable | Valor | type(...) |
    |---|---:|---|
    | `example_int` | `{example_int}` | `{type(example_int).__name__}` |
    | `example_float` | `{example_float}` | `{type(example_float).__name__}` |
    | `example_str` | `{example_str}` | `{type(example_str).__name__}` |
    | `example_bool` | `{example_bool}` | `{type(example_bool).__name__}` |
    | `tu_ejemplo` | `{tu_ejemplo}` | `{type(tu_ejemplo).__name__}` |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Operaciones básicas y evaluación

    Python permite expresar operaciones aritméticas directamente:

    - Suma: `+`
    - Resta: `-`
    - Multiplicación: `*`
    - División: `/`

    En analítica, estas operaciones son la base para construir transformaciones más complejas.
    """)
    return


@app.cell
def _():
    a = 14
    b = 5
    sum_ab = a + b
    diff_ab = a - b
    prod_ab = a * b
    div_ab = a / b
    return a, b, diff_ab, div_ab, prod_ab, sum_ab


@app.cell(hide_code=True)
def _(a, b, diff_ab, div_ab, mo, prod_ab, sum_ab):
    mo.md(rf"""
    Con `a = {a}` y `b = {b}`:

    - `a + b = {sum_ab}`
    - `a - b = {diff_ab}`
    - `a * b = {prod_ab}`
    - `a / b = {div_ab}`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Micro–ejercicio guiado (interactivo)

    Objetivo: construir **tres variables**, aplicar una operación y producir un **resultado final verificable** en:

    - `pre_session_1_result`

    Instrucciones:

    1. Elige valores para `x`, `y`, `z`.
    2. Elige una operación para combinar `x` y `y`.
    3. Calcula un valor final: `(x ⊗ y) + z`
    4. Genera un texto final formateado con el detalle del cálculo.
    """)
    return


@app.cell
def _(mo):
    x_slider = mo.ui.slider(start=0, stop=100, step=1, value=10, label="x")
    y_slider = mo.ui.slider(start=0, stop=100, step=1, value=20, label="y")
    z_slider = mo.ui.slider(start=0, stop=100, step=1, value=5, label="z")

    operation_dropdown = mo.ui.dropdown(
        options=["+", "-", "*", "/"],
        value="+",
        label="Operación para combinar x y y",
    )

    mo.vstack(
        [
            mo.md("### Controles"),
            x_slider,
            y_slider,
            z_slider,
            operation_dropdown,
        ]
    )
    return operation_dropdown, x_slider, y_slider, z_slider


@app.cell
def _(mo, operation_dropdown, x_slider, y_slider, z_slider):
    x = int(x_slider.value)
    y = int(y_slider.value)
    z = int(z_slider.value)
    op = str(operation_dropdown.value)

    def safe_combine(left: float, right: float, operation: str) -> float:
        if operation == "+":
            return left + right
        if operation == "-":
            return left - right
        if operation == "*":
            return left * right
        if operation == "/":
            return left / right if right != 0 else float("nan")
        raise ValueError(f"Unsupported operation: {operation}")

    combined_xy = safe_combine(x, y, op)
    final_value = combined_xy + z

    pre_session_1_result = (
        "Pre–Sesión 1 OK | "
        f"x={x}, y={y}, z={z}, op='{op}' | "
        f"(x {op} y) + z = ({combined_xy}) + {z} = {final_value}"
    )

    mo.md(
            f"""
    ### Resultado

    `pre_session_1_result`:

    `{pre_session_1_result}`
    """
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Evidencia requerida (para entregar)

    Entrega **4 evidencias**:

    1. Captura de pantalla (o texto copiado) mostrando:
       - `Python version`
       - `OS`
    2. El código (archivo o notebook) con:
       - Definición de `x`, `y`, `z`
       - Cálculo y formateo del resultado
    3. Evidencia de ejecución correcta del micro–ejercicio (captura del resultado en pantalla).
    4. El valor final de:
       - `pre_session_1_result`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Criterios de validación (checklist técnico)

    Se considera “completado” si:

    - Se reporta una versión de Python válida (se ve en la sección de entorno).
    - Se demuestra el uso de `type()` en al menos 2 variables.
    - Se ejecuta al menos una operación aritmética.
    - Existe la variable `pre_session_1_result` y contiene:
      - Valores de `x`, `y`, `z`
      - Operación usada
      - Resultado final
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Ejercicios (sin solución)

    1. Cambia el cálculo para que el valor final sea: `(x ⊗ y) * z`
       - ¿Cómo cambia el resultado al variar `z`?
    2. Haz que el resultado sea `int` si la operación es división y el resultado es entero exacto.
       - Pista: compara `final_value` con `int(final_value)`.
    3. Agrega una validación: si `op == "/"` y `y == 0`, muestra un mensaje de error en vez de `nan`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Cierre

    En esta pre–sesión consolidaste el “ciclo mínimo” de programación:

    - definir variables → operar → inspeccionar tipos → imprimir / reportar resultados

    Esto prepara el terreno para la Sesión 1, donde formalizaremos:

    - sintaxis básica
    - estructuras de control iniciales
    - disciplina de ejecución reproducible
    - cómo leer y entender errores de forma sistemática
    """)
    return


if __name__ == "__main__":
    app.run()

