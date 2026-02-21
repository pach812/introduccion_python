import marimo

__generated_with = "0.20.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 01 — Semántica del lenguaje Python

    ## Propósito de la sección

    Esta sección introduce principios semánticos fundamentales de Python: cómo se ejecuta el código, cómo se relacionan los nombres (variables) con los objetos en memoria, y qué implicaciones prácticas tiene esto al escribir programas correctos y reproducibles.

    A lo largo del notebook encontrarás:

    - Explicaciones conceptuales en lenguaje académico, acompañadas de demostraciones ejecutables.
    - Ejemplos diseñados para formar intuición (por ejemplo: identidad vs igualdad, mutabilidad, tipado dinámico).
    - Un mini-reto al final, con verificaciones automáticas (tests) para validar el aprendizaje.

    ## Contenidos

    1. Flujo de ejecución y orden de evaluación.
    2. Nombres, objetos y asignación (name binding).
    3. Identidad (`is`) vs igualdad (`==`).
    4. Sentencias (statements) vs expresiones (expressions).
    5. Tipado dinámico e inspección de tipos.
    6. Mutabilidad e implicaciones en estructuras de datos.
    7. Errores semánticos frecuentes y lectura de trazas.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1) Flujo de ejecución y orden de evaluación

    En un script de Python, el intérprete ejecuta el código en orden (de arriba hacia abajo). En un entorno tipo notebook (como marimo), cada celda se ejecuta cuando el usuario la dispara, pero **dentro de cada celda** el orden sigue siendo secuencial.

    Esto tiene consecuencias directas:

    - Si una variable se usa antes de definirse, ocurre un `NameError`.
    - Si una línea falla, la ejecución se detiene en ese punto (y las líneas posteriores no se ejecutan).
    - El “estado” del programa depende de qué celdas se ejecutaron y en qué orden (marimo ayuda a gestionar este estado con dependencias explícitas).

    A continuación se muestra un ejemplo simple de ejecución secuencial.
    """)
    return


@app.cell
def _():
    print("Paso 1: antes de calcular")
    _x = 10
    print("Paso 2: x =", _x)
    _x = _x + 5
    print("Paso 3: x =", _x)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2) Nombres y objetos: asignación no implica copia

    En Python, una asignación como `b = a` no significa “copiar” el valor de `a` en `b`. En general significa:

    - `a` es un **nombre** (una etiqueta).
    - Existe un **objeto** en memoria (por ejemplo, una lista).
    - El nombre `a` referencia (apunta a) ese objeto.
    - Al hacer `b = a`, el nombre `b` referencia **el mismo objeto**.

    Esta idea se denomina con frecuencia *name binding* y es esencial para entender efectos colaterales en estructuras **mutables**.

    Para observar esto, se puede usar:
    - `id(obj)`: un identificador del objeto (útil para exploración).
    - `is`: operador de identidad (verifica si dos nombres refieren al mismo objeto).
    """)
    return


@app.cell
def _():
    _a = [1, 2, 3]
    _b = _a  # b referencia el mismo objeto que a

    print("id(a):", id(_a))
    print("id(b):", id(_b))
    print("a is b:", _a is _b)

    # Mutación: se modifica el objeto en memoria; ambos nombres observan el cambio
    _b.append(4)
    print("a después de b.append(4):", _a)
    print("b:", _b)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3) Identidad (`is`) vs igualdad (`==`)

    Dos conceptos diferentes:

    - **Igualdad (`==`)**: compara contenido/valor lógico.
    - **Identidad (`is`)**: compara si es el mismo objeto en memoria.

    Es perfectamente posible que dos listas tengan el mismo contenido (igualdad), pero sean objetos distintos (no identidad).
    """)
    return


@app.cell
def _():
    u = [1, 2, 3]
    v = [1, 2, 3]

    print("u == v:", u == v)  # igualdad de contenido
    print("u is v:", u is v)  # identidad (mismo objeto)
    print("id(u):", id(u))
    print("id(v):", id(v))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4) Sentencias (statements) vs expresiones (expressions)

    - Una **expresión** es una construcción que se evalúa y produce un valor (por ejemplo: `2 + 2`, `len(lista)`).
    - Una **sentencia** es una instrucción que controla el flujo o define estructura del programa (por ejemplo: `if`, `for`, `def`, `import`).

    En práctica:
    - Las expresiones “calculan”.
    - Las sentencias “organizan” y “dirigen” la ejecución.

    Ejemplos de expresiones:
    """)
    return


@app.cell
def _():
    expr_1 = 2 + 2
    expr_2 = "a" * 3
    expr_3 = len([10, 20, 30])

    print("expr_1:", expr_1)
    print("expr_2:", expr_2)
    print("expr_3:", expr_3)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Ejemplo de sentencia (`if`): decide qué bloque se ejecuta según una condición booleana.
    """)
    return


@app.cell
def _():
    edad = 17

    if edad >= 18:
        mensaje = "Eres mayor de edad."
    else:
        mensaje = "Aún no eres mayor de edad."

    print(mensaje)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5) Tipado dinámico e inspección de tipos

    Python utiliza **tipado dinámico**: un nombre puede referirse a objetos de distintos tipos a lo largo de la ejecución. El tipo está asociado al **objeto**, no al nombre.

    Herramientas útiles:
    - `type(obj)` para inspección rápida.
    - `isinstance(obj, Tipo)` para verificación de tipo en lógica de control (cuando es pertinente).

    Este comportamiento es potente, pero exige disciplina: los errores por incompatibilidad de tipos aparecen en tiempo de ejecución.
    """)
    return


@app.cell
def _():
    x = 42
    print("x =", x, "| type:", type(x))

    x = "ahora soy texto"
    print("x =", x, "| type:", type(x))

    print("isinstance(x, str):", isinstance(x, str))
    print("isinstance(x, int):", isinstance(x, int))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6) Mutabilidad: objetos mutables vs inmutables

    La **mutabilidad** describe si un objeto puede cambiar internamente sin “dejar de ser el mismo objeto”.

    - **Inmutables** (no cambian internamente): `int`, `float`, `bool`, `str`, `tuple`.
      - Si “modificas” un inmutable, Python crea un objeto nuevo y el nombre se enlaza a ese nuevo objeto.
    - **Mutables** (sí cambian internamente): `list`, `dict`, `set`.
      - Operaciones como `.append()` modifican el mismo objeto en memoria.

    Esto es particularmente relevante al trabajar con estructuras de datos y al pasar objetos a funciones.
    """)
    return


@app.cell
def _():
    # Inmutable: str
    s = "hola"
    print("s:", s, "| id:", id(s))
    s = s + " mundo"  # crea un nuevo objeto str
    print("s:", s, "| id:", id(s))

    # Mutable: list
    L = [1, 2, 3]
    print("L:", L, "| id:", id(L))
    L.append(4)  # modifica la misma lista
    print("L:", L, "| id:", id(L))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7) Errores semánticos frecuentes y lectura de trazas

    Tres errores comunes al iniciar:

    ### `NameError`
    Se intenta usar un nombre que no está definido (por ejemplo, por orden de ejecución o por un error tipográfico).

    ### `TypeError`
    Se aplica una operación a tipos incompatibles (por ejemplo, intentar sumar un entero con un texto).

    ### `ValueError`
    El tipo puede ser válido, pero el valor no se puede interpretar/convertir (por ejemplo, `int("abc")`).

    En entornos interactivos, aprender a leer la traza (traceback) es una competencia básica:
    - Identificar el tipo de error.
    - Ubicar la línea exacta donde ocurre.
    - Interpretar el mensaje para corregir la causa.

    A continuación se muestran ejemplos en forma de bloque (no ejecutados para evitar detener el notebook).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Ejemplos (solo como referencia):

    ```python
    # NameError
    print(variable_que_no_existe)

    # TypeError
    3 + "4"

    # ValueError
    int("abc")
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    # Mini-reto (Sección 1): Semántica

    ## Objetivo

    Aplicar de forma verificable los conceptos de:

    1) Identidad vs igualdad (`is` vs `==`)
    2) Mutabilidad
    3) Name binding (dos nombres referenciando el mismo objeto)

    ## Instrucciones

    Completa el código de la siguiente celda (donde dice `TODO`).
    Luego ejecuta la celda de **tests**. Si no aparece ningún error, el reto está resuelto.
    """)
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===

    # 1) Crea una lista llamada a con los valores [10, 20]
    # TODO:


    # 2) Asigna b para que referencia el MISMO objeto que a
    # TODO:


    # 3) Agrega el número 30 a b (mutando la lista)
    # TODO:


    # 4) Crea una NUEVA lista c con el mismo contenido que a,
    #    pero que NO sea el mismo objeto.
    #    Pista: a.copy(), list(a), o a[:]
    # TODO:


    # 5) Define dos variables booleanas:
    #    - eq_1 debe ser True si a y c tienen igual contenido
    #    - same_1 debe ser True si a y b son el mismo objeto
    # TODO:


    return


@app.cell(hide_code=True)
def _(mo):
    tip_content = mo.md(
    """
    ### Tip

    Recuerda:

    - `=` no crea una copia, crea una referencia al mismo objeto.
    - Las listas son **mutables**.
    - `is` compara identidad (mismo objeto en memoria).
    - `==` compara contenido.
    - Para copiar una lista puedes usar:
      - `a.copy()`
      - `list(a)`
      - `a[:]`
    """
    )

    solution_content = mo.md(
    """
    ### Solución explicada

    ```python
    a = [10, 20]
    b = a
    b.append(30)

    c = a.copy()

    eq_1 = (a == c)
    same_1 = (a is b)
    ```
    - b = a hace que ambos apunten al mismo objeto.
    - b.append(30) modifica también a.
    - c = a.copy() crea un nuevo objeto con el mismo contenido.
    - a == c → True (mismo contenido)
    - a is b → True (misma referencia)
    """)

    mo.accordion(
        {
            "Tip conceptual": tip_content,
            "Solución comentada": solution_content,
        }
    )
    return


@app.cell
def _(a, b, c, eq_1, mo, same_1):
    # === TESTS (NO EDITAR) ===
    assert a == [10, 20, 30], "a debería ser [10, 20, 30]"
    assert b == [10, 20, 30], "b debería reflejar la mutación: [10, 20, 30]"
    assert a is b, "a y b deberían ser el mismo objeto (name binding)"
    assert c == a, "c debería tener el mismo contenido que a"
    assert c is not a, "c NO debería ser el mismo objeto que a (copia)"
    assert eq_1 is True, "eq_1 debería ser True (igualdad de contenido)"
    assert same_1 is True, "same_1 debería ser True (misma identidad)"

    mo.md(
        r"""
    ✅ **Reto superado.**  
    Si estás leyendo esto sin errores, has verificado correctamente identidad, igualdad, mutabilidad y asignación por referencia.
    """
    )
    return


if __name__ == "__main__":
    app.run()
