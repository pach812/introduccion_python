import marimo

__generated_with = "0.20.2"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 02 — Variables, semántica y expresiones

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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1.1) Valores y tipos (antes de profundizar en variables)

    Un **valor** es “una cosa básica” con la que trabaja un programa: números, texto, etc.
    Cada valor pertenece a un **tipo** (`int`, `float`, `str`, `bool`, ...).

    Ideas clave:
    - El **tipo de una variable** es el tipo del **valor** al que referencia.
    - Puedes inspeccionarlo con `type(...)`.
    - Ojo: `'17'` (con comillas) **no es** un número, es `str`.

    Ejemplos típicos:
    - `17` → `int`
    - `3.2` → `float`
    - `"Hola"` → `str`
    - `True/False` → `bool`
    """)
    return


@app.cell
def _():
    print(type(17), 17)
    print(type(3.2), 3.2)
    print(type("17"), "17")
    print(type(True), True)
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
    ## 2.1) Expresiones vs sentencias (statements)

    - **Expresión**: algo que Python puede *evaluar* y produce un valor (ej: `2 + 2`, `x * 3`).
    - **Sentencia**: una instrucción que Python *ejecuta* (ej: asignación `x = 5`, `print(...)`, `if ...`).

    En el intérprete (REPL), escribir una expresión suele mostrar su valor.
    En un script/notebook, una expresión aislada **no imprime nada**: si quieres ver el valor, usa `print(...)`.
    """)
    return


@app.cell
def _():
    x_ev = 5
    x_ev + 1  # no imprime nada por sí solo
    print(x_ev + 1)  # esto sí muestra el resultado
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2.2) Strings: `+` no siempre es suma

    - Con números, `+` suma.
    - Con strings, `+` concatena (pega textos).
    - Con strings, `*` repite.

    Esto puede producir **errores semánticos**: el programa corre, pero hace algo distinto a lo que creías.
    """)
    return


@app.cell
def _():
    print(100 + 150)  # suma numérica
    print("100" + "150")  # concatenación
    print("Test " * 3)  # repetición
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
    print("bool([1]):", bool(1))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5.1) `and` / `or` / `not`: corto-circuito (short-circuit)

    Python evalúa `and` / `or` **de izquierda a derecha** y puede detenerse temprano:

    - En `A and B`: si `A` es `False`, Python **no evalúa** `B`.
    - En `A or B`: si `A` es `True`, Python **no evalúa** `B`.

    Esto permite patrones de "guardia" (evitar errores), pero también puede confundir si esperas
    que todo se evalúe siempre.
    """)
    return


@app.cell
def _():
    x_sc = 0
    seguro = (x_sc != 0) and (10 / x_sc > 1)
    print("seguro:", seguro)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6) Entrada del usuario: `input()` siempre devuelve `str`

    - `input(...)` siempre retorna texto (`str`), aunque el usuario “digite un número”.
    - Para números, conviertes con `int(...)` o `float(...)`.
    - Si el texto no es convertible, aparece `ValueError`.

    Más adelante, verás cómo manejarlo con `try/except`.
    """)
    return


@app.cell
def _():
    texto = "17"
    print("texto:", texto, type(texto))
    numero = int(texto)
    print("numero:", numero, type(numero))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7) Comentarios y nombres mnemónicos (legibilidad)

    **Comentarios (`#`)**
    - Úsalos para explicar *por qué* existe un bloque, decisiones, supuestos.
    - Evita comentarios redundantes que repiten el código.

    **Nombres mnemónicos**
    - Prefiere `horas`, `tasa`, `pago` sobre `a`, `b`, `c` cuando importa entender el contexto.
    - Buen naming reduce la necesidad de comentarios.
    """)
    return


@app.cell
def _():
    # Useful: explains units (not obvious from the code)
    velocidad_m_s = 5  # meters/second

    # Redundant: does not add information
    x_naming = 5  # assigns 5 to x_naming

    print("velocidad_m_s:", velocidad_m_s, "| x_naming:", x_naming)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    # Mini-retos

    En los siguientes retos solo usarás:
    - asignación a variables
    - operadores aritméticos
    - comparaciones
    - lógica booleana (`and`, `or`, `not`)

    Completa los `# TODO` (to do en inglés) para que los test (`assert`) pasen y recibas un mensaje de pasado.
    Si tienes problemas, revisa los tips debajo de cada ejercicio.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Mini-reto 1 — Salud clínica

    **Dominio:** Salud / clínica

    Tareas:
    1) Calcula el **BMI**: `peso_kg_r1 / (altura_m_r1 ** 2)`
    2) Define `es_adulto_r1`: `edad_r1 >= 18`
    3) Define `bmi_en_rango_r1`: True si `18.5 <= bmi_r1 < 30`
    4) Define `apto_r1`: True solo si es adulto, BMI en rango y **no** tiene fiebre
    """)
    return


@app.cell
def _():
    # Datos (no cambiar)
    edad_r1 = 25
    peso_kg_r1 = 72.0
    altura_m_r1 = 1.80
    tiene_fiebre_r1 = False

    # TODO: calcula el BMI (float)
    bmi_r1 = None

    # TODO: define es_adulto (bool)
    es_adulto_r1 = None

    # TODO: define bmi_en_rango (bool)
    bmi_en_rango_r1 = None

    # TODO: define apto (bool)
    apto_r1 = None

    print("R1 -> bmi:", bmi_r1, "| es_adulto:", es_adulto_r1, "| apto:", apto_r1)
    return (
        altura_m_r1,
        apto_r1,
        bmi_en_rango_r1,
        bmi_r1,
        es_adulto_r1,
        peso_kg_r1,
    )


@app.cell(hide_code=True)
def _(mo):
    __tip_content = mo.md(
        """
    ### Tip

    Para resolver este reto:

    1) Calcula BMI con potencia:
       - `bmi_r1 = peso_kg_r1 / (altura_m_r1 ** 2)`

    2) Adulto:
       - `es_adulto_r1 = edad_r1 >= 18`

    3) Rango (comparación encadenada):
       - `bmi_en_rango_r1 = 18.5 <= bmi_r1 < 30`

    4) Combina condiciones:
       - `apto_r1 = es_adulto_r1 and bmi_en_rango_r1 and (not tiene_fiebre_r1)`
    """
    )

    _solution_content = mo.md(
        """
    ### Solución (referencia)

    ```python
    bmi_r1 = peso_kg_r1 / (altura_m_r1 ** 2)
    es_adulto_r1 = edad_r1 >= 18
    bmi_en_rango_r1 = 18.5 <= bmi_r1 < 30
    apto_r1 = es_adulto_r1 and bmi_en_rango_r1 and (not tiene_fiebre_r1)
    ```

    Notas:
    - La comparación encadenada es la forma más limpia para rangos.
    - `not tiene_fiebre_r1` exige que la fiebre sea False.
    """
    )

    mo.accordion(
        {
            "Tip (estructura lógica)": __tip_content,
            "Solución (referencia)": _solution_content,
        }
    )
    return


@app.cell(hide_code=True)
def _(
    altura_m_r1,
    apto_r1,
    bmi_en_rango_r1,
    bmi_r1,
    es_adulto_r1,
    mo,
    peso_kg_r1,
):
    bmi_ref_r1 = peso_kg_r1 / (altura_m_r1 ** 2)

    assert abs(bmi_r1 - bmi_ref_r1) < 1e-12
    assert es_adulto_r1 is True
    assert bmi_en_rango_r1 is True
    assert apto_r1 is True

    mo.md("✅ Mini-reto 1 superado.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Mini-reto 2 — Finanzas personales

    **Dominio:** Finanzas / vida diaria

    Tareas:
    1) `gastos_totales_r2`: suma de gastos necesarios + deseos
    2) `balance_r2`: `ingresos_r2 - gastos_totales_r2`
    3) `puede_ahorrar_r2`: True si `balance_r2 > 0`
    4) `ahorro_r2`: si `balance_r2 > 0` entonces `balance_r2`, si no `0.0`
       (usa operador condicional: `x if condicion else y`)
    5) `regla_50_30_20_ok_r2`: True si:
       - `gastos_necesarios_r2 <= 0.50 * ingresos_r2`
       - `gastos_deseos_r2 <= 0.30 * ingresos_r2`
       - `ahorro_r2 >= 0.20 * ingresos_r2`
    """)
    return


@app.cell
def _():
    # Datos (no cambiar)
    ingresos_r2 = 2500.0
    gastos_necesarios_r2 = 1100.0
    gastos_deseos_r2 = 600.0

    # TODO: gastos_totales (float)
    gastos_totales_r2 = None

    # TODO: balance (float)
    balance_r2 = None

    # TODO: puede_ahorrar (bool)
    puede_ahorrar_r2 = None

    # TODO: ahorro (float) usando operador condicional
    ahorro_r2 = None

    # TODO: regla_50_30_20_ok (bool)
    regla_50_30_20_ok_r2 = None

    print(
        "R2 -> gastos_totales:", gastos_totales_r2,
        "| balance:", balance_r2,
        "| ahorro:", ahorro_r2,
        "| regla_ok:", regla_50_30_20_ok_r2,
    )
    return (
        ahorro_r2,
        balance_r2,
        gastos_deseos_r2,
        gastos_necesarios_r2,
        gastos_totales_r2,
        ingresos_r2,
        puede_ahorrar_r2,
        regla_50_30_20_ok_r2,
    )


@app.cell(hide_code=True)
def _(mo, tip_content):
    _tip_content = mo.md(
        """
    ### Tip

    1) Suma:
       - `gastos_totales_r2 = gastos_necesarios_r2 + gastos_deseos_r2`

    2) Balance:
       - `balance_r2 = ingresos_r2 - gastos_totales_r2`

    3) Booleano:
       - `puede_ahorrar_r2 = balance_r2 > 0`

    4) Operador condicional (sin funciones):
       - `ahorro_r2 = balance_r2 if balance_r2 > 0 else 0.0`

    5) Regla 50/30/20:
       - compara cada gasto y el ahorro contra proporciones del ingreso
       - combina todo con `and`
    """
    )

    _solution_content = mo.md(
        """
    ### Solución (referencia)

    ```python
    gastos_totales_r2 = gastos_necesarios_r2 + gastos_deseos_r2
    balance_r2 = ingresos_r2 - gastos_totales_r2
    puede_ahorrar_r2 = balance_r2 > 0
    ahorro_r2 = balance_r2 if balance_r2 > 0 else 0.0
    regla_50_30_20_ok_r2 = (
    (gastos_necesarios_r2 <= 0.50 * ingresos_r2)
    and (gastos_deseos_r2 <= 0.30 * ingresos_r2)
    and (ahorro_r2 >= 0.20 * ingresos_r2)
    )
    ```

    Notas:
    - El operador condicional es una expresión (no es una función).
    - La regla final es una sola expresión booleana.
    """
    )

    mo.accordion(
        {
            "Tip (estructura lógica)": tip_content,
            "Solución (referencia)": _solution_content,
        }
    )
    return


@app.cell(hide_code=True)
def _(
    ahorro_r2,
    balance_r2,
    gastos_deseos_r2,
    gastos_necesarios_r2,
    gastos_totales_r2,
    ingresos_r2,
    mo,
    puede_ahorrar_r2,
    regla_50_30_20_ok_r2,
):
    gastos_totales_ref_r2 = gastos_necesarios_r2 + gastos_deseos_r2
    balance_ref_r2 = ingresos_r2 - gastos_totales_ref_r2
    puede_ahorrar_ref_r2 = balance_ref_r2 > 0
    ahorro_ref_r2 = balance_ref_r2 if balance_ref_r2 > 0 else 0.0
    regla_ref_r2 = (
        (gastos_necesarios_r2 <= 0.50 * ingresos_r2)
        and (gastos_deseos_r2 <= 0.30 * ingresos_r2)
        and (ahorro_ref_r2 >= 0.20 * ingresos_r2)
    )

    assert abs(gastos_totales_r2 - gastos_totales_ref_r2) < 1e-12
    assert abs(balance_r2 - balance_ref_r2) < 1e-12
    assert puede_ahorrar_r2 is puede_ahorrar_ref_r2
    assert abs(ahorro_r2 - ahorro_ref_r2) < 1e-12
    assert regla_50_30_20_ok_r2 is regla_ref_r2

    mo.md("✅ Mini-reto 2 superado.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Mini-reto 3 — Tecnología (seguridad básica)

    **Dominio:** Tecnología / seguridad

    Contexto:
    - La longitud real de una contraseña vendrá después (strings).
      Por ahora, `longitud_r3` ya es un número dado.

    Tareas:
    1) `tiene_longitud_ok_r3`: True si `longitud_r3 >= 8`
    2) `password_fuerte_r3`: True si:
       - tiene_longitud_ok_r3
       - y tiene_mayuscula_r3
       - y (tiene_numero_r3 o tiene_simbolo_r3)
    """)
    return


@app.cell
def _():
    # Datos (no cambiar)
    longitud_r3 = 10
    tiene_mayuscula_r3 = True
    tiene_numero_r3 = False
    tiene_simbolo_r3 = True

    # TODO: tiene_longitud_ok (bool)
    tiene_longitud_ok_r3 = None

    # TODO: password_fuerte (bool)
    password_fuerte_r3 = None

    print(
        "R3 -> longitud_ok:", tiene_longitud_ok_r3,
        "| password_fuerte:", password_fuerte_r3,
    )
    return (
        longitud_r3,
        password_fuerte_r3,
        tiene_longitud_ok_r3,
        tiene_mayuscula_r3,
        tiene_numero_r3,
        tiene_simbolo_r3,
    )


@app.cell(hide_code=True)
def _(mo):
    _tip_content = mo.md(
        """
    ### Tip

    1) Longitud:
       - `tiene_longitud_ok_r3 = longitud_r3 >= 8`

    2) Combina reglas con `and` y `or`:
       - `password_fuerte_r3 = tiene_longitud_ok_r3 and tiene_mayuscula_r3 and (tiene_numero_r3 or tiene_simbolo_r3)`

    Importante:
    - Usa paréntesis alrededor del `or` para que se lea claramente la intención.
    """
    )

    _solution_content = mo.md(
        """
    ### Solución (referencia)

    ```python
    tiene_longitud_ok_r3 = longitud_r3 >= 8
    password_fuerte_r3 = (
    tiene_longitud_ok_r3
    and tiene_mayuscula_r3
    and (tiene_numero_r3 or tiene_simbolo_r3)
    )
    ```

    Notas:
    - `and` y `or` producen valores booleanos cuando sus operandos son booleanos.
    - El paréntesis hace explícita la precedencia y mejora la legibilidad.
    """
    )

    mo.accordion(
        {
            "Tip (estructura lógica)": _tip_content,
            "Solución (referencia)": _solution_content,
        }
    )
    return


@app.cell(hide_code=True)
def _(
    longitud_r3,
    mo,
    password_fuerte_r3,
    tiene_longitud_ok_r3,
    tiene_mayuscula_r3,
    tiene_numero_r3,
    tiene_simbolo_r3,
):
    longitud_ok_ref_r3 = longitud_r3 >= 8
    password_ref_r3 = (
        longitud_ok_ref_r3
        and tiene_mayuscula_r3
        and (tiene_numero_r3 or tiene_simbolo_r3)
    )

    assert tiene_longitud_ok_r3 is longitud_ok_ref_r3
    assert password_fuerte_r3 is password_ref_r3

    mo.md("✅ Mini-reto 3 superado.")
    return


if __name__ == "__main__":
    app.run()
