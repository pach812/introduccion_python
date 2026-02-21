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
    # Clase 01 — Introducción a Python para Ciencia de Datos (sesión guiada)

    ## Qué buscamos hoy (visión del docente)

    Esta sesión está diseñada para crear **base conceptual sólida** sobre cómo “piensa” Python y cómo esa forma de pensar se traduce en buenas prácticas para ciencia de datos.

    ### Al final de la clase, el estudiante debería poder:
    - Explicar qué significa “una variable” en Python (no es una caja: es un **nombre** que referencia un **objeto**).
    - Distinguir entre **mutación** y **reasignación**, y por qué eso importa en análisis reproducibles.
    - Implementar funciones pequeñas con:
      - validación de tipo (`TypeError`)
      - validación de dominio/rango (`ValueError`)
      - retornos claros y testeables.
    - Usar estructuras básicas (listas, diccionarios, conjuntos) para simular mini-EDA.
    - Leer código y predecir resultados antes de ejecutar (habilidad crítica).

    ### Cómo usar este notebook en clase
    - **Celdas del docente** (Markdown largo): úsalo como “diapositivas integradas”.
    - **Live coding**: detente antes de ejecutar y pide predicciones.
    - **Ejercicios**: los estudiantes editan una celda, luego revisan tips/solución, y por último corren asserts.

    > Regla de oro: **predecir → ejecutar → observar → explicar → generalizar**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Plan sugerido (bloques)

    1. Semántica: ejecución, nombres, objetos, mutabilidad (10–15 min)
    2. Pseudocódigo y utilidades estándar (10–15 min)
    3. Variables y expresiones: precedencia, comparaciones (10–15 min)
    4. Condicionales: reglas de decisión (10–15 min)
    5. Secuencias: indexación y slicing (10–15 min)
    6. Funciones: docstrings, validaciones, contratos (15–20 min)
    7. Iteraciones: patrón acumulador (15–20 min)
    8. Diccionarios y conjuntos: conteos y únicos (10–15 min)
    9. Comprensiones: pipelines cortos (10–15 min)
    10. Mini-reto integrador (15–25 min)

    ### Señales que indican que vamos bien
    - El grupo explica *por qué* algo pasa, no solo *qué* pasa.
    - Los estudiantes usan asserts como verificación, no como “decoración”.
    - Las validaciones se vuelven un hábito: tipo → rango → lógica.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # 1) Semántica: ejecución, nombres, objetos, mutabilidad

    ## Conceptos clave (para explicar como diapositiva)

    ### 1) Python evalúa código y produce objetos
    En Python, casi todo lo que “existe” es un **objeto**: números, strings, listas, funciones, etc.

    ### 2) Asignación no copia: enlaza nombres con objetos
    Cuando escribes:

    ```python
    x = 10
    ```

    No significa “guardar 10 dentro de una caja llamada x”.
    Significa: el nombre `x` ahora **referencia** el objeto `10`.

    ### 3) Mutación vs reasignación
    - **Reasignar**: `x = x + 1` hace que `x` apunte a un nuevo objeto resultado.
    - **Mutar**: modificar un objeto existente (ej. lista con `.append()`).

    Esto es importante en ciencia de datos porque:
    - Copias vs referencias pueden cambiar datasets sin darte cuenta.
    - Algunas operaciones producen objetos nuevos; otras alteran el mismo.

    ### Preguntas para activar el pensamiento
    - Si `b = a`, ¿se crea copia o referencia?
    - ¿Qué diferencia hay entre `==` e `is`?
    - ¿Por qué `append()` puede “cambiar dos variables” al mismo tiempo?

    ### Error típico
    Creer que “asignar” significa “copiar”.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Live coding 1.1 — Orden de ejecución y reasignación

    **Antes de ejecutar:**
    1) ¿Qué imprime primero?
    2) ¿Cuál es el valor de `x_sem_lc1` en cada print?
    3) ¿Qué significa “nuevo” en `x_sem_lc1 (nuevo)`?

    **Idea docente:**
    - Dentro de una celda, la ejecución es secuencial.
    - Cada línea puede depender del estado previo.
    """)
    return


@app.cell
def _():
    print("Inicio")

    x_sem_lc1 = 10
    print("x_sem_lc1 =", x_sem_lc1)

    x_sem_lc1 = x_sem_lc1 + 5
    print("x_sem_lc1 (nuevo) =", x_sem_lc1)

    print("Fin")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Live coding 1.2 — Identidad vs igualdad; mutabilidad

    ### Diferencia operativa
    - `==` pregunta: “¿tienen el mismo contenido/valor?”
    - `is` pregunta: “¿son exactamente el mismo objeto?”

    ### Por qué importa
    - En listas/dicts, si dos nombres apuntan al mismo objeto y uno muta, el otro “ve” el cambio.
    - Esto explica bugs como: “¿por qué cambió mi lista original si solo modifiqué otra variable?”

    ### Pregunta clave
    Si `b = a`, ¿qué crees que vale `a` después de hacer `b.append(...)`?

    ### Concepto adicional útil
    `id(obj)` devuelve un identificador del objeto (útil para mostrar identidad en clase).
    """)
    return


@app.cell
def _():
    a_sem_lc2 = [1, 2, 3]
    b_sem_lc2 = a_sem_lc2

    print("a_sem_lc2 is b_sem_lc2:", a_sem_lc2 is b_sem_lc2)
    print("id(a):", id(a_sem_lc2))
    print("id(b):", id(b_sem_lc2))

    b_sem_lc2.append(4)
    print("a después de mutar b:", a_sem_lc2)

    u_sem_lc2 = [1, 2, 3]
    v_sem_lc2 = [1, 2, 3]
    print("u == v:", u_sem_lc2 == v_sem_lc2)
    print("u is v:", u_sem_lc2 is v_sem_lc2)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejercicio 1 — Referencias y copia

    **Objetivo:** practicar la diferencia entre:
    - referenciar el mismo objeto (`ref = lista`)
    - copiar contenido en un objeto nuevo (`lista.copy()`)

    **Tu tarea:**
    1) Define `lista_ex1` como `[10, 20]`
    2) Define `ref_ex1` apuntando al mismo objeto que `lista_ex1`
    3) Agrega `30` usando `ref_ex1`
    4) Define `copia_ex1` como una copia (objeto distinto) con el mismo contenido final

    Luego ejecuta los asserts.
    """)
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===

    # 1) Define lista_ex1 como [10, 20]
    # TODO:
    pass

    # 2) Define ref_ex1 apuntando al mismo objeto
    # TODO:
    pass

    # 3) Agrega 30 usando ref_ex1
    # TODO:
    pass

    # 4) Define copia_ex1 como copia (objeto distinto)
    # TODO:
    pass
    return


@app.cell(hide_code=True)
def _(mo):
    _tip_content = mo.md(
        r"""
    ### Tip

    - Si haces `ref = lista`, **no copias**: creas otra referencia al mismo objeto.
    - Para copiar una lista puedes usar:
      - `lista.copy()`
      - `list(lista)`
    - Para comprobar si es copia real:
      - `a == b` (contenido)
      - `a is b` (misma identidad)
    """
    )

    _solution_content = mo.md(
        r"""
    ### Solución (referencia)

    ```python
    lista_ex1 = [10, 20]
    ref_ex1 = lista_ex1
    ref_ex1.append(30)
    copia_ex1 = lista_ex1.copy()
    ```

    Notas:
    - `ref_ex1` y `lista_ex1` apuntan al mismo objeto.
    - `copia_ex1` tiene el mismo contenido, pero otro objeto.
    """
    )

    mo.accordion(
        {
            "Tip (referencias y copia)": _tip_content,
            "Solución (referencia)": _solution_content,
        }
    )
    return


@app.cell
def _(copia_ex1, lista_ex1, mo, ref_ex1):
    assert lista_ex1 == [10, 20, 30]
    assert ref_ex1 == [10, 20, 30]
    assert lista_ex1 is ref_ex1
    assert copia_ex1 == [10, 20, 30]
    assert copia_ex1 is not lista_ex1
    mo.md("✅ Ejercicio 1: OK")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # 2) Pseudocódigo y utilidades

    ## Idea central (para explicar)

    En ciencia de datos rara vez arrancas con código perfecto.
    Arrancas con una especificación:

    - ¿Qué entra? (inputs)
    - ¿Qué haces? (proceso)
    - ¿Qué sale? (outputs)

    ### Por qué el pseudocódigo es potente
    - Obliga a pensar validaciones (casos borde).
    - Reduce ambigüedad.
    - Facilita tests: si sabes “qué debe salir”, puedes comprobarlo.

    ### Diferencia importante
    - **Validación de tipo**: “¿es el tipo correcto?”
    - **Validación de dominio**: “¿está dentro de valores permitidos?”
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Live coding 2.1 — Del pseudocódigo al código (promedio)

    **Pseudocódigo:**
    1) Recibir una secuencia numérica (lista o tupla)
    2) Validar que no esté vacía
    3) Calcular `sum(x) / len(x)`
    4) Retornar el promedio

    **Puntos para explicar:**
    - `raise` detiene el programa con un mensaje útil (mejor que fallar silenciosamente).
    - Validar temprano simplifica el resto del código.
    """)
    return


@app.cell
def _():
    def promedio_lc2(x_lc2):
        if len(x_lc2) == 0:
            raise ValueError("Secuencia vacía.")
        return sum(x_lc2) / len(x_lc2)

    print(promedio_lc2([10, 20, 30]))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Live coding 2.2 — Utilidades estándar (`type`, `isinstance`, `len`, `sorted`, `help`)

    ### Mensaje docente (diapositiva)
    - `type(x)` te dice qué es.
    - `isinstance(x, (tipos...))` te permite validar entradas con rigor.
    - `len(x)` es universal para secuencias/colecciones.
    - `sorted(x)` ordena y devuelve un nuevo objeto.
    - `help(func)` es una herramienta real de trabajo: leer documentación es parte del oficio.

    **Mini-pregunta:**
    - ¿`sorted` muta la lista original o retorna otra?
    """)
    return


@app.cell
def _():
    datos_lc2b = [3, 1, 2]
    print("type(datos):", type(datos_lc2b))
    print("len(datos):", len(datos_lc2b))
    print("sorted(datos):", sorted(datos_lc2b))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejercicio 2 — Resumen numérico (dict)

    Implementa `resumen_numerico_ex2(x)`:

    **Requisitos**
    - `x` debe ser lista/tupla **no vacía**
    - todos los elementos deben ser `int` o `float`

    **Salida**
    Retorna un `dict` con llaves:
    - `n`, `minimo`, `maximo`, `suma`, `promedio`
    """)
    return


@app.function
# === TU TURNO (EDITA ESTA CELDA) ===
def resumen_numerico_ex2(x_ex2):
    # 1) Validar que x sea lista o tupla
    # TODO:
    pass

    # 2) Validar no vacío
    # TODO:
    pass

    # 3) Validar elementos numéricos (usa enumerate para mensajes claros)
    # TODO:
    pass

    # 4) Calcular métricas y retornar dict con llaves exactas
    # TODO:
    return None


@app.cell(hide_code=True)
def _(mo):
    _tip_content = mo.md(
        r"""
    ### Tip

    Una implementación rigurosa típicamente sigue:

    1) Validar contenedor:
       - `isinstance(x, (list, tuple))`

    2) Validar no vacío:
       - `len(x) > 0`

    3) Validar elementos:
       - Recorre con `enumerate(x)` y revisa `isinstance(v, (int, float))`

    4) Calcular:
       - `n = len(x)`, `min(x)`, `max(x)`, `sum(x)`, `sum(x)/n`
    """
    )

    _solution_content = mo.md(
        r"""
    ### Solución (referencia)

    ```python
    def resumen_numerico_ex2(x):
    if not isinstance(x, (list, tuple)):
        raise TypeError("x debe ser lista o tupla.")
    if len(x) == 0:
        raise ValueError("x no puede estar vacío.")

    for i, v in enumerate(x):
        if not isinstance(v, (int, float)):
            raise TypeError(f"Elemento no numérico en {i}: {v!r}")

    n = len(x)
    minimo = min(x)
    maximo = max(x)
    suma = sum(x)
    promedio = suma / n

    return {
        "n": n,
        "minimo": minimo,
        "maximo": maximo,
        "suma": suma,
        "promedio": promedio,
    }
    ```
    """
    )

    mo.accordion(
        {
            "Tip (validación y métricas)": _tip_content,
            "Solución (referencia)": _solution_content,
        }
    )
    return


@app.cell
def _(mo):
    out_ex2 = resumen_numerico_ex2([10, 20, 30])
    assert out_ex2["n"] == 3
    assert out_ex2["minimo"] == 10
    assert out_ex2["maximo"] == 30
    assert out_ex2["suma"] == 60
    assert out_ex2["promedio"] == 20.0
    mo.md("✅ Ejercicio 2: OK")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # 3) Variables y expresiones

    ## Conceptos clave (diapositiva)

    ### Expresiones
    Una expresión es algo que Python puede evaluar para producir un valor:
    - `2 + 3 * 4`
    - `x > 0`
    - `a and b`

    ### Precedencia
    Python sigue reglas de precedencia (como matemáticas):
    - multiplicación antes que suma
    - paréntesis forzan orden

    **En ciencia de datos**:
    - Fórmulas mal parentizadas dan resultados incorrectos (y a veces “parecen” correctos).

    ### Pregunta guía
    - ¿Cuándo usar paréntesis aunque “no sea necesario”?
      - Respuesta esperada: cuando mejora claridad y evita errores.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Live coding 3.1 — Precedencia y paréntesis

    **Predice:**
    - `2 + 3 * 4`
    - `(2 + 3) * 4`

    **Después de ver resultados:**
    - explica la regla de precedencia
    - refuerza: paréntesis = claridad
    """)
    return


@app.cell
def _():
    res_lc3a = 2 + 3 * 4
    res_lc3b = (2 + 3) * 4
    print("2 + 3 * 4 =", res_lc3a)
    print("(2 + 3) * 4 =", res_lc3b)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejercicio 3 — Clasificador de signo

    Implementa `clasificar_signo_ex3(x)`:

    - `TypeError` si `x` no es numérico (`int` o `float`)
    - Retorna:
      - `"positivo"` si `x > 0`
      - `"negativo"` si `x < 0`
      - `"cero"` si `x == 0`
    """)
    return


@app.function
# === TU TURNO (EDITA ESTA CELDA) ===
def clasificar_signo_ex3(x_ex3):

    # 1) Validar que x sea numérico
    # TODO:
    pass

    # 2) Retornar etiqueta según el signo
    # TODO:
    return None


@app.cell(hide_code=True)
def _(mo):
    _tip_content = mo.md(
        r"""
    ### Tip

    - La validación de tipo debe ocurrir al inicio.
    - Luego decide con comparaciones:
      - `> 0`
      - `< 0`
      - caso contrario (`0`)
    """
    )

    _solution_content = mo.md(
        r"""
    ### Solución (referencia)

    ```python
    def clasificar_signo_ex3(x):
    if not isinstance(x, (int, float)):
        raise TypeError("x debe ser numérico.")
    if x > 0:
        return "positivo"
    if x < 0:
        return "negativo"
    return "cero"
    ```
    """
    )

    mo.accordion(
        {"Tip (lógica y validación)": _tip_content, "Solución (referencia)": _solution_content}
    )
    return


@app.cell
def _(mo):
    assert clasificar_signo_ex3(10) == "positivo"
    assert clasificar_signo_ex3(-1.5) == "negativo"
    assert clasificar_signo_ex3(0) == "cero"
    mo.md("✅ Ejercicio 3: OK")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # 4) Ejecución condicional

    ## Diapositiva conceptual

    ### `if / elif / else` como reglas de decisión
    En analítica (y clínica) muchas decisiones son reglas:

    - Si cumple criterio A → acción A
    - Si no, pero cumple criterio B → acción B
    - Si no cumple ninguno → acción por defecto

    ### Orden importa
    Las condiciones se evalúan en orden.
    La primera verdadera “gana”.

    ### Validaciones y reglas
    Un patrón profesional:
    1) Validar entradas (tipo/rango)
    2) Aplicar reglas con `if/elif/else`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Live coding 4.1 — Categorizar una nota

    **Regla:**
    - `>= 4.5`: Excelente
    - `>= 3.5`: Aprobado
    - else: Reprobado

    **Pregunta docente:**
    - ¿Por qué no ponemos primero `>= 3.5`?
    """)
    return


@app.cell
def _():
    nota_lc4 = 3.7
    if nota_lc4 >= 4.5:
        cat_lc4 = "Excelente"
    elif nota_lc4 >= 3.5:
        cat_lc4 = "Aprobado"
    else:
        cat_lc4 = "Reprobado"
    print(cat_lc4)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejercicio 4 — Clasificar IMC

    Implementa `clasificar_imc_ex4(peso_kg, altura_m)`:

    **Validaciones**
    - `TypeError` si entradas no numéricas
    - `ValueError` si `altura_m <= 0`

    **Cálculo**
    - `imc = peso_kg / altura_m**2`

    **Categorías**
    - `< 18.5`: Bajo peso
    - `< 25`: Normal
    - `< 30`: Sobrepeso
    - `>= 30`: Obesidad
    """)
    return


@app.function
# === TU TURNO (EDITA ESTA CELDA) ===
def clasificar_imc_ex4(peso_kg_ex4, altura_m_ex4):

    # 1) Validar tipos numéricos
    # TODO:
    pass

    # 2) Validar altura > 0
    # TODO:
    pass

    # 3) Calcular IMC
    # TODO:
    pass

    # 4) Clasificar por rangos y retornar categoría
    # TODO:
    return None


@app.cell(hide_code=True)
def _(mo):
    _tip_content = mo.md(
        r"""
    ### Tip

    - Valida tipo primero:
      - `isinstance(peso_kg, (int, float))`
      - `isinstance(altura_m, (int, float))`
    - Valida dominio:
      - `altura_m > 0`
    - Luego calcula IMC y aplica rangos en orden.
    """
    )

    _solution_content = mo.md(
        r"""
    ### Solución (referencia)

    ```python
    def clasificar_imc_ex4(peso_kg, altura_m):
    if not isinstance(peso_kg, (int, float)) or not isinstance(altura_m, (int, float)):
        raise TypeError("Peso y altura deben ser numéricos.")
    if altura_m <= 0:
        raise ValueError("La altura debe ser mayor que 0.")

    imc = peso_kg / (altura_m ** 2)

    if imc < 18.5:
        return "Bajo peso"
    if imc < 25:
        return "Normal"
    if imc < 30:
        return "Sobrepeso"
    return "Obesidad"
    ```
    """
    )

    mo.accordion(
        {"Tip (validación y rangos)": _tip_content, "Solución (referencia)": _solution_content}
    )
    return


@app.cell
def _(mo):
    assert clasificar_imc_ex4(50, 1.70) == "Bajo peso"
    assert clasificar_imc_ex4(65, 1.70) == "Normal"
    assert clasificar_imc_ex4(80, 1.70) == "Sobrepeso"
    assert clasificar_imc_ex4(95, 1.70) == "Obesidad"
    mo.md("✅ Ejercicio 4: OK")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # 5) Secuencias (list, tuple, str)

    ## Diapositiva conceptual

    ### Qué es una secuencia
    Una secuencia es una colección ordenada:
    - lista (`list`) — mutable
    - tupla (`tuple`) — inmutable
    - string (`str`) — inmutable (pero indexable)

    ### Por qué importa en ciencia de datos
    - Columnas (antes de pandas) se representan como listas.
    - Tokenización produce secuencias (NLP).
    - Series temporales se recorren como secuencias.

    ### Indexación y slicing
    - índices inician en 0
    - `-1` es el último
    - `a:b` incluye a, excluye b
    - `[::-1]` invierte
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Live coding 5.1 — Slicing como herramienta de exploración

    **Qué mostrar:**
    - `seq[0]`, `seq[-1]`
    - `seq[1:5]`
    - `seq[::-1]`

    **Pregunta docente:**
    - ¿Por qué `seq[1:5]` no incluye el índice 5?
    """)
    return


@app.cell
def _():
    seq_lc5 = [0, 1, 2, 3, 4, 5, 6]
    print("seq[0]:", seq_lc5[0])
    print("seq[-1]:", seq_lc5[-1])
    print("seq[1:5]:", seq_lc5[1:5])
    print("seq[::-1]:", seq_lc5[::-1])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejercicio 5 — Analizar secuencia

    Implementa `analizar_secuencia_ex5(seq)`:

    - Acepta `list` o `tuple` no vacía
    - Retorna dict con:
      - `longitud`
      - `primer_elemento`
      - `ultimo_elemento`
      - `invertida`
    """)
    return


@app.function
# === TU TURNO (EDITA ESTA CELDA) ===
def analizar_secuencia_ex5(seq_ex5):

    # 1) Validar tipo (list/tuple)
    # TODO:
    pass

    # 2) Validar no vacío
    # TODO:
    pass

    # 3) Retornar dict con llaves exactas
    # TODO:
    return None


@app.cell(hide_code=True)
def _(mo):
    _tip_content = mo.md(
        r"""
    ### Tip

    - `len(seq)` para longitud
    - `seq[0]` primer elemento
    - `seq[-1]` último elemento
    - `seq[::-1]` invertida
    """
    )

    _solution_content = mo.md(
        r"""
    ### Solución (referencia)

    ```python
    def analizar_secuencia_ex5(seq):
    if not isinstance(seq, (list, tuple)):
        raise TypeError("seq debe ser lista o tupla.")
    if len(seq) == 0:
        raise ValueError("seq no puede estar vacía.")
    return {
        "longitud": len(seq),
        "primer_elemento": seq[0],
        "ultimo_elemento": seq[-1],
        "invertida": seq[::-1],
    }
    ```
    """
    )

    mo.accordion(
        {"Tip (indexación y slicing)": _tip_content, "Solución (referencia)": _solution_content}
    )
    return


@app.cell
def _(mo):
    out_ex5 = analizar_secuencia_ex5([10, 20, 30])
    assert out_ex5["longitud"] == 3
    assert out_ex5["primer_elemento"] == 10
    assert out_ex5["ultimo_elemento"] == 30
    assert out_ex5["invertida"] == [30, 20, 10]
    mo.md("✅ Ejercicio 5: OK")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # 6) Funciones

    ## Diapositiva conceptual

    ### Por qué funciones
    En proyectos reales, si no encapsulas lógica en funciones:
    - se repite código,
    - se vuelve difícil de probar,
    - los notebooks se vuelven frágiles.

    ### Contrato de una función
    Una función bien diseñada tiene:
    1) **Entrada** clara (tipos y supuestos)
    2) **Validación** (TypeError / ValueError)
    3) **Proceso** (lógica)
    4) **Salida** (retorno consistente)
    5) Idealmente un **docstring**.

    ### Errores comunes
    - Retornar tipos distintos según casos (difícil de usar).
    - No validar y dejar que el error ocurra lejos del origen.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Live coding 6.1 — Función con docstring y validación

    Ejemplo: normalización a [0, 1].

    **Puntos para explicar:**
    - Docstring: describe qué hace la función.
    - Validación de rango: evita divisiones por cero o resultados incoherentes.
    - Retorno numérico interpretable.
    """)
    return


@app.cell
def _():
    def normalizar_0_1_lc6(x_min_lc6, x_max_lc6, x_lc6):
        """Normaliza x al rango [0, 1] dados x_min y x_max."""
        if x_max_lc6 <= x_min_lc6:
            raise ValueError("x_max debe ser mayor que x_min.")
        if not (x_min_lc6 <= x_lc6 <= x_max_lc6):
            raise ValueError("x debe estar dentro de [x_min, x_max].")
        return (x_lc6 - x_min_lc6) / (x_max_lc6 - x_min_lc6)

    print(normalizar_0_1_lc6(0, 10, 5))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejercicio 6 — Evaluación de aprobación

    Implementa `evaluar_aprobacion(nota)`:

    **Validaciones**
    1) `TypeError` si `nota` no es numérica
    2) `ValueError` si `nota` está fuera de `0–5`

    **Clasificación**
    - `>= 3` → `"Aprobado"`
    - `< 3` → `"Reprobado"`

    Luego ejecuta los asserts.
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
    _tip_content = mo.md(
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

    _solution_content = mo.md(
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
            "Tip (validación y lógica)": _tip_content,
            "Solución (referencia)": _solution_content,
        }
    )
    return


@app.cell
def _(mo):
    assert evaluar_aprobacion(4) == "Aprobado"
    assert evaluar_aprobacion(2.5) == "Reprobado"
    mo.md("✅ Ejercicio 6: OK")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # 7) Iteraciones

    ## Diapositiva conceptual

    ### Por qué loops importan
    Aunque existan funciones como `sum`, `min`, `max`, los loops son la base para:
    - construir métricas personalizadas,
    - limpiar datos con reglas,
    - recorrer registros (pacientes),
    - generar features.

    ### Patrón acumulador
    Un patrón universal:

    1) inicializar acumulador
    2) recorrer elementos
    3) actualizar acumulador
    4) usar el resultado

    Ejemplos de acumuladores:
    - suma (inicia en 0)
    - producto (inicia en 1)
    - conteo (inicia en 0)
    - listas de resultados (inicia en [])
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Live coding 7.1 — Patrón acumulador (suma manual)

    **Mensaje docente:**
    - `sum()` es conveniente, pero entender el patrón te permite inventar algoritmos.
    - Si puedes sumar con un loop, puedes contar categorías, calcular métricas, etc.

    **Pregunta:**
    - ¿Qué cambia si inicializas la suma en 1?
    """)
    return


@app.cell
def _():
    datos_lc7 = [2, 4, 6, 8]
    suma_lc7 = 0
    for v_lc7 in datos_lc7:
        suma_lc7 += v_lc7
    print("Suma acumulada:", suma_lc7)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejercicio 7 — Factorial (iterativo)

    Implementa `factorial_ex7(n)`:

    - `TypeError` si `n` no es `int`
    - `ValueError` si `n < 0`
    - Calcula factorial con un loop `for`
    """)
    return


@app.function
# === TU TURNO (EDITA ESTA CELDA) ===
def factorial_ex7(n_ex7):

    # 1) Validar tipo (int)
    # TODO:
    pass

    # 2) Validar n >= 0
    # TODO:
    pass

    # 3) Calcular factorial con acumulador multiplicativo
    # TODO:
    return None


@app.cell(hide_code=True)
def _(mo):
    _tip_content = mo.md(
        r"""
    ### Tip

    - Factorial usa producto:
      - acumulador inicial = 1
    - Rango típico:
      - `for i in range(1, n + 1):`
    """
    )

    _solution_content = mo.md(
        r"""
    ### Solución (referencia)

    ```python
    def factorial_ex7(n):
    if not isinstance(n, int):
        raise TypeError("n debe ser entero.")
    if n < 0:
        raise ValueError("n debe ser no negativo.")
    out = 1
    for i in range(1, n + 1):
        out *= i
    return out
    ```
    """
    )

    mo.accordion(
        {"Tip (acumulador multiplicativo)": _tip_content, "Solución (referencia)": _solution_content}
    )
    return


@app.cell
def _(mo):
    assert factorial_ex7(0) == 1
    assert factorial_ex7(5) == 120
    mo.md("✅ Ejercicio 7: OK")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # 8) Diccionarios y conjuntos

    ## Diapositiva conceptual

    ### `dict` (mapeo clave → valor)
    Es la estructura natural para:
    - conteos de categorías
    - mapeos (id → valor)
    - agregaciones simples tipo EDA

    ### `set` (conjunto de únicos)
    Útil para:
    - deduplicación
    - obtener categorías únicas
    - comparar conjuntos (intersección, unión)

    ### Patrón clásico de conteo
    ```python
    conteo[clave] = conteo.get(clave, 0) + 1
    ```

    Esto evita `KeyError` y es muy común en analítica.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Live coding 8.1 — Conteo con diccionarios

    **Qué explicar:**
    - `conteo = {}` inicializa diccionario vacío
    - `.get(clave, 0)` devuelve 0 si la clave no existe
    - Actualizamos por cada etiqueta

    **Conexión a ciencia de datos:**
    - Esto es equivalente conceptual a `value_counts` en pandas (pero a mano).
    """)
    return


@app.cell
def _():
    etiquetas_lc8 = ["HTA", "DM2", "HTA", "EPOC", "HTA"]
    conteo_lc8 = {}
    for e_lc8 in etiquetas_lc8:
        conteo_lc8[e_lc8] = conteo_lc8.get(e_lc8, 0) + 1
    print(conteo_lc8)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejercicio 8 — Resumen categórico (dict + set)

    Implementa `resumen_categorico_ex8(lista_etiquetas)`:

    **Validaciones**
    - Debe ser list/tuple no vacío
    - Todos los elementos deben ser `str`

    **Salida**
    Retorna dict con:
    - `unicos` (set)
    - `conteo` (dict)
    """)
    return


@app.function
# === TU TURNO (EDITA ESTA CELDA) ===
def resumen_categorico_ex8(lista_etiquetas_ex8):

    # 1) Validar contenedor (list/tuple) y no vacío
    # TODO:
    pass

    # 2) Validar que todos los elementos sean strings
    # TODO:
    pass

    # 3) Construir unicos (set) y conteo (dict)
    # TODO:
    return None


@app.cell(hide_code=True)
def _(mo):
    _tip_content = mo.md(
        r"""
    ### Tip

    - Únicos: `set(lista_etiquetas)`
    - Conteo:
      - inicializa `conteo = {}`
      - actualiza con `conteo.get(etiqueta, 0) + 1`
    """
    )

    _solution_content = mo.md(
        r"""
    ### Solución (referencia)

    ```python
    def resumen_categorico_ex8(lista_etiquetas):
    if not isinstance(lista_etiquetas, (list, tuple)):
        raise TypeError("La entrada debe ser una lista o tupla.")
    if len(lista_etiquetas) == 0:
        raise ValueError("La secuencia no puede estar vacía.")

    for i, v in enumerate(lista_etiquetas):
        if not isinstance(v, str):
            raise TypeError(f"Elemento no string en {i}: {v!r}")

    unicos = set(lista_etiquetas)

    conteo = {}
    for v in lista_etiquetas:
        conteo[v] = conteo.get(v, 0) + 1

    return {"unicos": unicos, "conteo": conteo}
    ```
    """
    )

    mo.accordion(
        {"Tip (únicos y conteo)": _tip_content, "Solución (referencia)": _solution_content}
    )
    return


@app.cell
def _(mo):
    out_ex8 = resumen_categorico_ex8(["a", "b", "a", "c", "b", "a"])
    assert out_ex8["unicos"] == {"a", "b", "c"}
    assert out_ex8["conteo"]["a"] == 3
    assert out_ex8["conteo"]["b"] == 2
    assert out_ex8["conteo"]["c"] == 1
    mo.md("✅ Ejercicio 8: OK")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # 9) Comprensiones

    ## Diapositiva conceptual

    ### Qué son
    Las comprehensions son una forma compacta de construir colecciones:
    - list comprehension
    - dict comprehension
    - set comprehension

    ### Por qué importan
    Permiten expresar en una línea:
    - recorrer
    - filtrar
    - transformar

    ### Regla de legibilidad
    Si la comprensión se vuelve difícil de leer:
    - usar un `for` explícito es mejor (claridad > concisión).

    ### Lectura “en voz alta”
    ```python
    [v for v in x si condición]
    ```
    Se lee: “toma v para cada v en x, si cumple condición”.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Live coding 9.1 — List comprehension con filtro

    **Objetivo:**
    - extraer pares
    - transformar impares

    **Preguntas:**
    - ¿Qué parte es filtro? (`if ...`)
    - ¿Qué parte es transformación? (`v**2`)
    """)
    return


@app.cell
def _():
    x_lc9 = [1, 2, 3, 4, 5, 6]
    pares_lc9 = [v_lc9 for v_lc9 in x_lc9 if v_lc9 % 2 == 0]
    cuadrados_impares_lc9 = [v_lc9 ** 2 for v_lc9 in x_lc9 if v_lc9 % 2 != 0]
    print("pares:", pares_lc9)
    print("cuadrados_impares:", cuadrados_impares_lc9)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejercicio 9 — Pipeline simple con comprehensions

    Implementa `pipeline_simple_ex9(x)`:

    **Validaciones**
    - `x` debe ser list/tuple
    - todos los elementos deben ser enteros

    **Salida**
    Retorna dict con:
    - `pares` (list comprehension)
    - `cuadrados_impares` (list comprehension)
    - `mapa_paridad` (dict comprehension: número → "par"/"impar")
    """)
    return


@app.function
# === TU TURNO (EDITA ESTA CELDA) ===
def pipeline_simple_ex9(x_ex9):

    # 1) Validar contenedor y tipos internos (int)
    # TODO:
    pass

    # 2) Construir pares y cuadrados_impares con list comprehensions
    # TODO:
    pass

    # 3) Construir mapa_paridad con dict comprehension
    # TODO:
    return None


@app.cell(hide_code=True)
def _(mo):
    _tip_content = mo.md(
        r"""
    ### Tip

    - Pares:
      - `[v for v in x if v % 2 == 0]`
    - Cuadrados de impares:
      - `[v**2 for v in x if v % 2 != 0]`
    - Mapa paridad:
      - `{v: ("par" if v % 2 == 0 else "impar") for v in x}`
    """
    )

    _solution_content = mo.md(
        r"""
    ### Solución (referencia)

    ```python
    def pipeline_simple_ex9(x):
    if not isinstance(x, (list, tuple)):
        raise TypeError("x debe ser lista o tupla.")
    for i, v in enumerate(x):
        if not isinstance(v, int):
            raise TypeError(f"Elemento no entero en {i}: {v!r}")

    pares = [v for v in x if v % 2 == 0]
    cuadrados_impares = [v**2 for v in x if v % 2 != 0]
    mapa_paridad = {v: ("par" if v % 2 == 0 else "impar") for v in x}

    return {
        "pares": pares,
        "cuadrados_impares": cuadrados_impares,
        "mapa_paridad": mapa_paridad,
    }
    ```
    """
    )

    mo.accordion(
        {"Tip (comprehensions)": _tip_content, "Solución (referencia)": _solution_content}
    )
    return


@app.cell
def _(mo):
    out_ex9 = pipeline_simple_ex9([1, 2, 3, 4, 5])
    assert out_ex9["pares"] == [2, 4]
    assert out_ex9["cuadrados_impares"] == [1, 9, 25]
    assert out_ex9["mapa_paridad"][1] == "impar"
    assert out_ex9["mapa_paridad"][2] == "par"
    assert out_ex9["mapa_paridad"][5] == "impar"
    mo.md("✅ Ejercicio 9: OK")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Mini-reto integrador (final)

    ## Enunciado (diapositiva)

    Implementa una función `perfil_paciente(registros)`.

    ### Entrada
    - `registros`: lista de diccionarios; cada dict representa un paciente con llaves:
      - `id` (str, requerida)
      - `edad` (int/float, requerida)
      - `dx` (str, requerida)
      - `peso_kg` (int/float, opcional)
      - `altura_m` (int/float, opcional)

    ### Proceso (arquitectura)
    1) Validar que `registros` sea lista no vacía.
    2) Validar que cada registro sea dict y tenga `id`, `edad`, `dx` con tipos correctos.
    3) Construir y retornar un dict con:
       - `n`: número de pacientes
       - `dx_unicos`: set de dx únicos
       - `conteo_dx`: dict de frecuencias por dx
       - `ids_mayores`: lista de ids con edad >= 65 (list comprehension)
       - `imc_por_id`: dict {id: imc} solo si hay peso y altura válidos (altura>0)

    ### Mensaje docente de cierre
    Este reto integra:
    - validación de datos (lo más común en datos reales)
    - iteraciones
    - dict/set
    - comprehensions
    - salida estructurada (lista para convertirse en tabla más adelante)
    """)
    return


@app.function
# === TU TURNO (EDITA ESTA CELDA) ===
def perfil_paciente_ex_final(registros_ex_final):

    # 1) Validar contenedor principal: list no vacía
    # TODO:
    pass

    # 2) Validar cada registro (dict) y llaves requeridas con tipos adecuados
    # TODO:
    pass

    # 3) Construir dx_unicos, conteo_dx, ids_mayores, imc_por_id
    #    - ids_mayores: list comprehension
    #    - imc_por_id: dict comprehension (omitir pacientes sin datos completos)
    # TODO:
    return None


@app.cell(hide_code=True)
def _(mo):
    _tip_content = mo.md(
        r"""
    ### Tip

    Arquitectura recomendada:

    1) Validaciones globales:
       - `isinstance(registros, list)` y `len(registros) > 0`

    2) Validaciones por registro:
       - cada elemento es dict
       - llaves `id`, `edad`, `dx` presentes
       - tipos correctos

    3) Agregaciones:
       - `dx_unicos = set(...)`
       - `conteo_dx` con patrón `.get(..., 0) + 1`

    4) Comprehensions:
       - `ids_mayores = [r["id"] for r in registros if r["edad"] >= 65]`
       - `imc_por_id = { ... for r in registros if ... }`
    """
    )

    _solution_content = mo.md(
        r"""
    ### Solución (referencia)

    ```python
    def perfil_paciente_ex_final(registros):
    if not isinstance(registros, list):
        raise TypeError("registros debe ser una lista.")
    if len(registros) == 0:
        raise ValueError("registros no puede estar vacío.")

    dx_list = []
    for i, r in enumerate(registros):
        if not isinstance(r, dict):
            raise TypeError(f"Registro no dict en posición {i}.")
        if "id" not in r or "edad" not in r or "dx" not in r:
            raise ValueError(f"Faltan llaves requeridas en posición {i}.")
        if not isinstance(r["id"], str):
            raise TypeError(f"id debe ser str en posición {i}.")
        if not isinstance(r["edad"], (int, float)):
            raise TypeError(f"edad debe ser numérica en posición {i}.")
        if not isinstance(r["dx"], str):
            raise TypeError(f"dx debe ser str en posición {i}.")
        dx_list.append(r["dx"])

    conteo_dx = {}
    for dx in dx_list:
        conteo_dx[dx] = conteo_dx.get(dx, 0) + 1

    dx_unicos = set(dx_list)

    ids_mayores = [r["id"] for r in registros if r["edad"] >= 65]

    def _imc_valido(r):
        return (
            "peso_kg" in r
            and "altura_m" in r
            and isinstance(r["peso_kg"], (int, float))
            and isinstance(r["altura_m"], (int, float))
            and r["altura_m"] > 0
        )

    imc_por_id = {
        r["id"]: (r["peso_kg"] / (r["altura_m"] ** 2))
        for r in registros
        if _imc_valido(r)
    }

    return {
        "n": len(registros),
        "dx_unicos": dx_unicos,
        "conteo_dx": conteo_dx,
        "ids_mayores": ids_mayores,
        "imc_por_id": imc_por_id,
    }
    ```
    """
    )

    mo.accordion(
        {"Tip (arquitectura)": _tip_content, "Solución (referencia)": _solution_content}
    )
    return


@app.cell
def _(mo):
    registros_t_final = [
        {"id": "P1", "edad": 70, "dx": "HTA", "peso_kg": 80, "altura_m": 1.70},
        {"id": "P2", "edad": 40, "dx": "DM2"},
        {"id": "P3", "edad": 66, "dx": "HTA", "peso_kg": 65, "altura_m": 1.60},
    ]

    out_t_final = perfil_paciente_ex_final(registros_t_final)

    assert out_t_final["n"] == 3
    assert out_t_final["dx_unicos"] == {"HTA", "DM2"}
    assert out_t_final["conteo_dx"]["HTA"] == 2
    assert out_t_final["conteo_dx"]["DM2"] == 1
    assert out_t_final["ids_mayores"] == ["P1", "P3"]
    assert "P2" not in out_t_final["imc_por_id"]
    assert round(out_t_final["imc_por_id"]["P1"], 6) == round(80 / (1.70 ** 2), 6)
    assert round(out_t_final["imc_por_id"]["P3"], 6) == round(65 / (1.60 ** 2), 6)

    mo.md(
        r"""
    ✅ Mini-reto integrador: OK

    Cierre sugerido (docente):
    - ¿Qué validaciones faltan si esto fuera “datos reales”?
    - ¿Cómo convertiríamos la salida a una tabla (pandas) la próxima semana?
    - ¿Qué otras variables clínicas añadirías y cómo cambiarían las validaciones?
    """
    )
    return


if __name__ == "__main__":
    app.run()
