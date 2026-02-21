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
    # 03 — Variables, semántica y expresiones

    ## Propósito de la sección

    En esta sección se profundiza en:

    - El concepto formal de variable como nombre ligado a un objeto.
    - Reglas de nombrado y convenciones.
    - Expresiones aritméticas, comparativas y lógicas.
    - Precedencia de operadores.
    - Evaluación booleana.

    El objetivo es comprender cómo Python evalúa expresiones y cómo construirlas con precisión.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1) Variables: reglas y convenciones

    Una variable es un nombre que referencia un objeto.

    Reglas:
    - Debe iniciar con letra o guion bajo.
    - No puede iniciar con número.
    - Es sensible a mayúsculas/minúsculas.
    - No puede usar palabras reservadas.

    Convención recomendada:
    - snake_case
    - nombres semánticamente informativos
    """)
    return


@app.cell
def _():
    edad_paciente = 45
    peso_kg = 72.5
    activo = True

    print("edad_paciente:", edad_paciente)
    print("peso_kg:", peso_kg)
    print("activo:", activo)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2) Expresiones aritméticas

    Operadores:
    \+  \-  \*  /  //  %  **
    """)
    return


@app.cell
def _():
    a = 10
    b = 3

    print("a + b =", a + b)
    print("a - b =", a - b)
    print("a * b =", a * b)
    print("a / b =", a / b)
    print("a // b =", a // b)
    print("a % b =", a % b)
    print("a ** b =", a ** b)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Precedencia

    Multiplicación y división tienen mayor precedencia que suma y resta.
    Siempre usar paréntesis cuando la intención no sea evidente.
    """)
    return


@app.cell
def _():
    resultado_1 = 2 + 3 * 4
    resultado_2 = (2 + 3) * 4

    print("2 + 3 * 4 =", resultado_1)
    print("(2 + 3) * 4 =", resultado_2)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3) Expresiones comparativas

    Operadores:
    ==  !=  <  >  <=  >=

    Producen valores booleanos.
    """)
    return


@app.cell
def _():
    x = 10
    y = 5

    print("x > y:", x > y)
    print("x == y:", x == y)
    print("x != y:", x != y)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4) Expresiones lógicas

    Operadores lógicos:
    - and
    - or
    - not

    Se usan para combinar condiciones.
    """)
    return


@app.cell
def _():
    edad = 25
    tiene_permiso = True

    condicion = (edad >= 18) and tiene_permiso
    print("Puede acceder:", condicion)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5) Evaluación booleana implícita

    En Python, ciertos valores se consideran False:

    - 0
    - None
    - Secuencias vacías
    - False

    El resto se evalúa como True.
    """)
    return


@app.cell
def _():
    print("bool(0):", bool(0))
    print("bool([]):", bool([]))
    print("bool(1):", bool(1))
    print("bool([1]):", bool([1]))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    # Mini-reto (Sección 3)

    Construye una función `clasificar_valor(x)` que:

    1. Retorne "positivo" si x > 0
    2. Retorne "negativo" si x < 0
    3. Retorne "cero" si x == 0
    4. Lance TypeError si x no es numérico
    """)
    return


@app.function
def clasificar_valor(x):

    # 1) Validar que x sea numérico
    # TODO:
    pass

    # 2) Clasificar según su valor
    # TODO:
    if False:
        return None
    elif False:
        return None
    else:
        return None


@app.cell(hide_code=True)
def _(mo):
    tip_content = mo.md(
    """
    ### Tip

    Para implementar `clasificar_valor(x)` con claridad lógica:

    1. Valida primero el tipo:
       - `isinstance(x, (int, float))`
    2. Luego evalúa condiciones en este orden:
       - `x > 0`
       - `x < 0`
       - caso restante (`else`) será 0
    3. El orden importa: evita condiciones redundantes.
    """
    )

    solution_content = mo.md(
    """
    ### Solución (referencia)

    ````python
    def clasificar_valor(x):
        if not isinstance(x, (int, float)):
            raise TypeError("x debe ser numérico.")

        if x > 0:
            return "positivo"
        elif x < 0:
            return "negativo"
        else:
            return "cero"
    ```

    Notas:
    - La validación ocurre antes de cualquier comparación.
    - El else captura el caso x == 0.
    - La estructura es exhaustiva y mutuamente excluyente.
    """
    )
    mo.accordion(
    {
    "Tip (estructura lógica)": tip_content,
    "Solución (referencia)": solution_content,
    }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    assert clasificar_valor(10) == "positivo"
    assert clasificar_valor(-5) == "negativo"
    assert clasificar_valor(0) == "cero"

    mo.md(
        r"""
    ✅ Reto superado.
    Has aplicado correctamente expresiones comparativas y lógicas.
    """
    )
    return


if __name__ == "__main__":
    app.run()
