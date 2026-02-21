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
    # 02 — Pseudocódigo y utilidades para programar con rigor

    ## Propósito de la sección

    Antes de aprender más sintaxis, es fundamental adquirir un método de trabajo. En esta sección se introduce el uso de **pseudocódigo** como herramienta para:

    - estructurar el pensamiento antes de escribir código,
    - explicitar entradas, procesos y salidas,
    - reducir errores por “improvisación”,
    - documentar decisiones de manera reproducible.

    Además, se presentan utilidades básicas del ecosistema Python para inspección, documentación y depuración inicial:

    - `print` y f-strings (salida y reporte de resultados),
    - `type`, `isinstance` (inspección de tipos),
    - `len`, `sum`, `min`, `max`, `sorted` (utilidades comunes),
    - `help`, `dir` (documentación e introspección),
    - `enumerate`, `zip` (soporte para iteraciones claras),
    - `assert` (verificaciones simples y tests mínimos).

    ## Idea central

    La programación en ciencia de datos no es “escribir código”; es **especificar un procedimiento** (con claridad), implementarlo, y verificar que produce resultados correctos.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1) Pseudocódigo como especificación (inputs → proceso → outputs)

    Un formato útil y universal es escribir, primero, la especificación:

    - **Entrada (inputs):** qué información recibe el algoritmo.
    - **Proceso:** pasos ordenados (reglas) que se aplican.
    - **Salida (outputs):** qué retorna o produce el algoritmo.

    ### Ejemplo 1: “Promedio de una lista”

    **Pseudocódigo**
    1. Recibir una lista de números `x`.
    2. Si la lista está vacía, detener o reportar error.
    3. Sumar los valores.
    4. Dividir por el número de elementos.
    5. Retornar el resultado.

    Ahora implementaremos esto y compararemos versiones.
    """)
    return


@app.cell
def _():
    def promedio_v1(x):
        """Calcula el promedio de una secuencia numérica no vacía."""
        if len(x) == 0:
            raise ValueError("La secuencia está vacía; no existe promedio.")
        return sum(x) / len(x)

    print(promedio_v1([10, 20, 30]))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Observación: especificación explícita reduce ambigüedad

    El pseudocódigo obliga a decidir qué hacer con entradas “problemáticas” (por ejemplo: lista vacía).
    En ciencia de datos, estas decisiones son parte del rigor del análisis (y deben documentarse).

    A continuación, la misma función con validación de tipos y mensajes más claros.
    """)
    return


@app.cell
def _():
    def promedio_v2(x):
        """
        Calcula el promedio de una secuencia numérica.

        Reglas:
        - x debe ser iterable (por ejemplo list/tuple) con longitud > 0
        - todos los elementos deben ser int o float (para este ejemplo)
        """
        if not hasattr(x, "__iter__"):
            raise TypeError("x debe ser una secuencia (iterable).")

        if len(x) == 0:
            raise ValueError("La secuencia está vacía; no existe promedio.")

        for i, v in enumerate(x):
            if not isinstance(v, (int, float)):
                raise TypeError(
                    f"Elemento no numérico en posición {i}: {v!r} (tipo {type(v).__name__})"
                )

        return sum(x) / len(x)

    print(promedio_v2([1, 2, 3, 4]))
    return (promedio_v2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2) Utilidades esenciales: inspección y documentación

    ### `type()` e `isinstance()`
    - `type(obj)` devuelve el tipo del objeto.
    - `isinstance(obj, Tipo)` permite verificar tipos en tiempo de ejecución.

    ### `help()`
    - `help(obj)` muestra documentación (docstring) y firma.
    - Muy útil para aprendizaje autónomo y lectura de APIs.

    ### `dir()`
    - `dir(obj)` lista atributos/métodos disponibles (introspección).

    Ejemplo práctico con utilidades numéricas comunes:
    """)
    return


@app.cell
def _():
    x = [10, 20, 30]
    print("type(x):", type(x))
    print("isinstance(x, list):", isinstance(x, list))
    print("len(x):", len(x))
    print("sum(x):", sum(x))
    print("min(x):", min(x))
    print("max(x):", max(x))
    print("sorted(x, reverse=True):", sorted(x, reverse=True))
    return


@app.cell
def _(mo, promedio_v2):
    mo.md(
        r"""
    Ejemplo: consultar documentación de una función.

    En marimo, `help()` puede imprimir salida extensa. Aquí mostramos:
    - un extracto de docstring (`__doc__`) y
    - los nombres de parámetros a partir del objeto `__code__`.

    Esto no reemplaza `help()`, pero ilustra la introspección básica.
    """
    )

    doc = promedio_v2.__doc__ or ""
    args = promedio_v2.__code__.co_varnames[: promedio_v2.__code__.co_argcount]

    mo.md(
        "Docstring (extracto):\n\n"
        + "\n".join([f"- {line.strip()}" for line in doc.strip().splitlines() if line.strip()][:8])
        + "\n\n"
        + f"Parámetros: {', '.join(args)}"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3) “Utilidades de control”: `enumerate` y `zip`

    Estas herramientas ayudan a escribir código más claro y menos propenso a errores.

    ### `enumerate(iterable)`
    Itera con índice y valor, sin manejar contadores manuales.

    ### `zip(a, b, ...)`
    Recorre varias secuencias en paralelo (por posición).
    """)
    return


@app.cell
def _():
    nombres = ["Ana", "Luis", "Sofía"]
    notas = [4.5, 3.8, 4.9]

    print("Usando enumerate:")
    for i, nombre in enumerate(nombres):
        print(i, nombre)

    print("\nUsando zip (nombre, nota):")
    for nombre, nota in zip(nombres, notas):
        print(f"{nombre}: {nota}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4) Reporte de resultados: `print` y f-strings

    Para reportar resultados con claridad se usan f-strings:

    ```python
    valor = 3.14159
    print(f"Pi aproximado: {valor:.2f}")
    ```

    Donde `:.2f` indica “2 decimales”.
    """)
    return


@app.cell
def _():
    valor = 3.14159
    n = 1234567
    print(f"Pi aproximado: {valor:.2f}")
    print(f"Entero con separador de miles: {n:,}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5) Verificación mínima: `assert` como tests simples

    En contextos académicos y de ciencia de datos, es recomendable construir **verificaciones automáticas** para partes críticas del análisis.

    `assert` exige que una condición sea verdadera; si no lo es, detiene la ejecución y muestra un mensaje.

    A continuación, definimos una función y la verificamos con asserts.
    """)
    return


@app.cell
def _():
    def normalizar_a_0_1(x_min, x_max, x):
        """
        Normaliza x al rango [0, 1] dados x_min y x_max.

        Reglas:
        - x_max debe ser mayor que x_min
        - x debe estar dentro de [x_min, x_max]
        """
        if x_max <= x_min:
            raise ValueError("x_max debe ser mayor que x_min.")

        if not (x_min <= x <= x_max):
            raise ValueError("x debe estar dentro del rango [x_min, x_max].")

        return (x - x_min) / (x_max - x_min)

    # Tests mínimos
    assert normalizar_a_0_1(0, 10, 0) == 0.0
    assert normalizar_a_0_1(0, 10, 10) == 1.0
    assert normalizar_a_0_1(0, 10, 5) == 0.5

    print("Tests básicos: OK")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    # Mini-reto (Sección 2): Pseudocódigo + utilidades

    ## Enunciado

    Construye una función `resumen_numerico(x)` siguiendo este pseudocódigo:

    **Entrada**
    - `x`: lista o tupla de números (`int`/`float`), no vacía.

    **Proceso**
    1. Verificar que `x` sea una secuencia con longitud > 0.
    2. Verificar que todos los elementos sean numéricos (usar `enumerate`).
    3. Calcular: `n`, `minimo`, `maximo`, `suma`, `promedio`.
    4. Retornar un diccionario con esas llaves exactas.

    **Salida**
    - `dict` con llaves: `n`, `minimo`, `maximo`, `suma`, `promedio`.

    Completa la siguiente celda y luego ejecuta los tests.
    """)
    return


@app.function
# === TU TURNO (EDITA ESTA CELDA) ===
def resumen_numerico(x):
    # 1) Validar que x sea iterable
    # TODO:
    pass

    # 2) Validar que x no esté vacío
    # TODO:
    pass

    # 3) Validar que todos los elementos sean numéricos (int/float)
    #    usando enumerate para reportar posición.
    # TODO:
    pass

    # 4) Calcular n, minimo, maximo, suma, promedio
    # TODO:
    n = None
    minimo = None
    maximo = None
    suma = None
    promedio = None

    # 5) Retornar dict con llaves exactas
    # TODO:
    return {
        "n": n,
        "minimo": minimo,
        "maximo": maximo,
        "suma": suma,
        "promedio": promedio,
    }


@app.cell(hide_code=True)
def _(mo):
    tip_content = mo.md(
    """
    ### Tip

    Para implementar `resumen_numerico(x)` con rigor:

    - Valida que `x` sea **iterable**: `hasattr(x, "__iter__")`
    - Valida que **no esté vacío**: `len(x) == 0`
    - Recorre con `enumerate(x)` para detectar:
      - posición (`i`)
      - valor (`v`)
    - Verifica tipos con `isinstance(v, (int, float))`
    - Calcula métricas con utilidades estándar:
      - `n = len(x)`
      - `minimo = min(x)`
      - `maximo = max(x)`
      - `suma = sum(x)`
      - `promedio = suma / n`
    - Retorna un `dict` con llaves exactas:
      `{"n", "minimo", "maximo", "suma", "promedio"}`
    """
    )

    solution_content = mo.md(
    """
    ### Solución (referencia)

    ```python
    def resumen_numerico(x):
        if not hasattr(x, "__iter__"):
            raise TypeError("x debe ser una secuencia (iterable).")

        if len(x) == 0:
            raise ValueError("x no puede estar vacío.")

        for i, v in enumerate(x):
            if not isinstance(v, (int, float)):
                raise TypeError(
                    f"Elemento no numérico en posición {i}: {v!r} (tipo {type(v).__name__})"
                )

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

        Notas:
    - hasattr(x, "__iter__") es una validación simple para este curso.
    - enumerate te permite reportar el índice exacto cuando encuentras un valor inválido.
    """
    )

    mo.accordion(
    {
    "Tip (cómo pensarlo)": tip_content,
    "Solución (referencia)": solution_content,
    }
    )

    return


@app.cell
def _(mo):
    # === TESTS (NO EDITAR) ===
    out = resumen_numerico([10, 20, 30])

    assert isinstance(out, dict), "Debe retornar un diccionario."
    assert set(out.keys()) == {"n", "minimo", "maximo", "suma", "promedio"}, "Llaves incorrectas."
    assert out["n"] == 3, "n debería ser 3."
    assert out["minimo"] == 10, "minimo debería ser 10."
    assert out["maximo"] == 30, "maximo debería ser 30."
    assert out["suma"] == 60, "suma debería ser 60."
    assert out["promedio"] == 20.0, "promedio debería ser 20.0."

    out2 = resumen_numerico((1.5, 2.5))
    assert out2["n"] == 2
    assert out2["suma"] == 4.0
    assert out2["promedio"] == 2.0

    mo.md(
        r"""
    ✅ **Reto superado.**  
    Has transformado un pseudocódigo en una implementación verificable, usando utilidades estándar de Python.
    """
    )
    return


if __name__ == "__main__":
    app.run()
