import marimo

__generated_with = "0.20.1"
app = marimo.App(width="medium")



@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 06 — Funciones

    ## Propósito de la sección

    Las funciones permiten:

    - Encapsular lógica.
    - Reutilizar código.
    - Separar especificación de implementación.
    - Facilitar pruebas y validación.

    En programación científica, las funciones constituyen la unidad básica de modularidad.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1) Definición básica

    Sintaxis:

    ```python
    def nombre(parametros):
        cuerpo
        return valor
    ```

    Una función puede:
    - Recibir argumentos.
    - Realizar cálculos.
    - Retornar un valor.
    """)
    return


@app.cell
def _():
    def cuadrado_fn1(x_fn1):
        return x_fn1 ** 2

    resultado_fn1 = cuadrado_fn1(5)
    print("Cuadrado:", resultado_fn1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2) Parámetros y argumentos

    Los parámetros se definen en la firma.
    Los argumentos se pasan al llamar la función.

    Se recomienda nombrar parámetros de forma semánticamente clara.
    """)
    return


@app.cell
def _():
    def area_rectangulo_fn2(base_fn2, altura_fn2):
        return base_fn2 * altura_fn2

    area_fn2 = area_rectangulo_fn2(10, 3)
    print("Área:", area_fn2)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3) Valores por defecto

    Se pueden definir valores por defecto en parámetros.
    """)
    return


@app.cell
def _():
    def potencia_fn3(base_fn3, exponente_fn3=2):
        return base_fn3 ** exponente_fn3

    print("Potencia por defecto:", potencia_fn3(4))
    print("Potencia personalizada:", potencia_fn3(4, 3))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4) Retorno múltiple

    Una función puede retornar múltiples valores (como tupla).
    """)
    return


@app.cell
def _():
    def estadisticas_fn4(x_fn4):
        return min(x_fn4), max(x_fn4)

    minimo_fn4, maximo_fn4 = estadisticas_fn4([3, 7, 1, 9])
    print("Min:", minimo_fn4, "Max:", maximo_fn4)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5) Ámbito (scope)

    Las variables definidas dentro de la función no existen fuera de ella.
    """)
    return


@app.cell
def _():
    def ejemplo_scope_fn5():
        variable_interna_fn5 = 10
        return variable_interna_fn5

    valor_scope_fn5 = ejemplo_scope_fn5()
    print("Valor interno:", valor_scope_fn5)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6) Documentación (docstrings)

    Las funciones deben documentarse formalmente.
    """)
    return


@app.cell
def _():
    def promedio_fn6(x_fn6):
        """Calcula el promedio de una secuencia numérica."""
        return sum(x_fn6) / len(x_fn6)

    print(promedio_fn6([1, 2, 3]))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    # Mini-reto (Sección 6)

    Construye una función `evaluar_aprobacion(nota)` que:

    1. Lance TypeError si la nota no es numérica.
    2. Lance ValueError si la nota está fuera del rango 0–5.
    3. Retorne "Aprobado" si nota >= 3.
    4. Retorne "Reprobado" si nota < 3.
    """)
    return


@app.function
# === TU TURNO (EDITA ESTA CELDA) ===

def evaluar_aprobacion(nota):

    # 1) Validar que la nota sea numérica
    # TODO:
    pass

    # 2) Validar que esté en el rango 0–5
    # TODO:
    pass

    # 3) Retornar "Aprobado" o "Reprobado"
    # TODO:
    return None


@app.cell(hide_code=True)
def _(mo):
    tip_content = mo.md(
    """
    ### Tip

    Para implementar `evaluar_aprobacion(nota)` con rigor:

    1. Valida tipo primero:
       - `isinstance(nota, (int, float))`
    2. Valida dominio:
       - La nota debe estar en el rango cerrado `[0, 5]`
    3. Luego clasifica:
       - `>= 3` → "Aprobado"
       - `< 3` → "Reprobado"
    4. Puedes usar un `if/else` tradicional o una expresión condicional en una línea.
    """
    )

    solution_content = mo.md(
    """
    ### Solución (referencia)

    ```python
    def evaluar_aprobacion(nota):

        if not isinstance(nota, (int, float)):
            raise TypeError("La nota debe ser numérica.")

        if not (0 <= nota <= 5):
            raise ValueError("La nota debe estar entre 0 y 5.")

        return "Aprobado" if nota >= 3 else "Reprobado"
    ```

    Notas:
    - La validación de tipo ocurre antes de evaluar el rango.
    - El rango incluye los extremos 0 y 5.
    - La expresión condicional simplifica la clasificación.
    """
    )

    mo.accordion(
        {
            "Tip (validación y lógica)": tip_content,
            "Solución (referencia)": solution_content,
        }
    )
    return


@app.cell
def _(mo):

    assert evaluar_aprobacion(4) == "Aprobado"
    assert evaluar_aprobacion(2.5) == "Reprobado"

    mo.md("Reto superado.")
    return


if __name__ == "__main__":
    app.run()
