# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "pandas==3.0.1",
#     "pytest==9.0.2",
#     "requests==2.32.5",
# ]
# ///

import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")

with app.setup(hide_code=True):
    import marimo as mo
    import pandas as pd
    from setup import TipContent, TestContent


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Semana 2 · Lección 4
    ## Pandas como librería de estructura tabular

    **Objetivo conceptual:** introducir `Series` y `DataFrame` como estructuras tabulares para organizar, inspeccionar, seleccionar y filtrar datos clínicos o epidemiológicos.

    En esta lección trabajaremos con:

    - `Series` como estructura unidimensional etiquetada
    - `DataFrame` como estructura tabular bidimensional
    - inspección básica de tablas
    - selección con `loc` e `iloc`
    - filtrado con condiciones booleanas
    - resúmenes simples con `describe`, `min` y `max`

    ---

    ### Motivación en salud pública

    En análisis clínico y epidemiológico, la mayoría de los datos llegan en forma de tabla:

    - cada **fila** representa una observación
    - cada **columna** representa una variable

    Por ejemplo:

    - paciente
    - visita
    - edad
    - sexo
    - presión arterial
    - IMC
    - biomarcadores

    Pandas formaliza este modelo y permite trabajar con él de forma programable.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 1) ¿Qué es Pandas en este curso?

    Pandas es una librería diseñada para trabajar con datos estructurados.

    En esta etapa del curso nos interesan dos objetos principales:

    - **`Series`**: una columna con índice
    - **`DataFrame`**: una tabla con filas y columnas etiquetadas

    En esta lección todavía no vamos a usar herramientas más avanzadas.

    Nos enfocaremos en cinco acciones fundamentales:

    1. crear estructuras tabulares,
    2. inspeccionarlas,
    3. seleccionar partes específicas,
    4. filtrar filas según criterios,
    5. resumir variables rápidamente.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 2) `Series`: una variable clínica como vector etiquetado

    Una `Series` puede entenderse como una sola variable observada en múltiples casos.

    Por ejemplo:

    - frecuencia cardiaca
    - glucosa
    - presión arterial sistólica
    - edad

    La diferencia respecto a una lista simple es que una `Series` no solo contiene valores: también contiene un **índice**.

    Ese índice permite que cada observación quede etiquetada.
    """)
    return


@app.cell
def _():
    # Creamos una serie que representa frecuencia cardiaca en varios pacientes
    frecuencia_cardiaca = pd.Series(
        [72, 88, 64, 91, 77],
        name="frecuencia_cardiaca_bpm",
    )

    frecuencia_cardiaca
    return (frecuencia_cardiaca,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Una vez creada una `Series`, podemos aplicar operaciones simples para obtener un primer resumen.

    Por ejemplo:

    - el valor mínimo
    - el valor máximo

    Esto es útil para una inspección rápida de la variable.
    """)
    return


@app.cell
def _(frecuencia_cardiaca):
    # Calculamos el mínimo y el máximo de la serie
    fc_min = frecuencia_cardiaca.min()
    fc_max = frecuencia_cardiaca.max()

    fc_min, fc_max
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 3) Filtrado básico en `Series`

    Una operación muy importante en Pandas es construir criterios lógicos.

    Cuando comparamos una serie con una condición, obtenemos una **máscara booleana**.

    Esa máscara:

    - tiene el mismo tamaño que la serie original,
    - contiene valores `True` y `False`,
    - y puede usarse para filtrar solo los casos que cumplen el criterio.

    Ejemplo clínico:

    seleccionar observaciones con frecuencia cardiaca mayor de 90 bpm.
    """)
    return


@app.cell
def _(frecuencia_cardiaca):
    # Creamos una máscara booleana para identificar taquicardia simple
    mascara_taquicardia = frecuencia_cardiaca > 90

    # Usamos la máscara para filtrar la serie
    valores_taquicardia = frecuencia_cardiaca[mascara_taquicardia]

    mascara_taquicardia, valores_taquicardia
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---

    # Mini-retos (3)

    Hasta aquí viste tres ideas importantes:

    - una `Series` como una variable etiquetada,
    - un `DataFrame` como una tabla,
    - y el filtrado como una forma de seleccionar observaciones según criterios.

    Ahora vas a pasar de observar ejemplos a construir tus propias soluciones con Pandas.

    En cada reto tendrás que decidir:

    - qué estructura usar,
    - qué operación aplicar,
    - y qué resultado debe producirse.

    En cada reto encontrarás:

    - un contexto breve,
    - una celda editable,
    - tips progresivos,
    - y tests para verificar tu implementación.

    Recomendación de trabajo:

    1. lee primero el reto completo,
    2. identifica qué estructura se espera,
    3. implementa una solución simple,
    4. usa los tips solo si te bloqueas,
    5. y revisa los tests como retroalimentación.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto 1 — `Series` y criterio clínico simple

    **Dominio:** clínica / presión arterial

    En este primer reto vas a construir una `Series` que represente presiones arteriales sistólicas observadas en varios pacientes.

    El objetivo es reforzar tres ideas básicas:

    - crear una `Series`,
    - obtener un resumen simple,
    - y filtrar observaciones según un umbral clínico.

    Antes de programar, piensa:

    - qué estructura representa una sola variable,
    - cómo obtener extremos de esa variable,
    - y cómo seleccionar únicamente los valores que cumplan un criterio definido.
    """)
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    # TODO: crear la serie principal
    sbp = None

    # TODO: calcular extremos
    sbp_min = None
    sbp_max = None

    # TODO: filtrar los valores que cumplan el criterio pedido
    high_sbp = None
    return high_sbp, sbp, sbp_max, sbp_min


@app.cell(hide_code=True)
def _():
    _tip_content = TipContent(
        items_raw=[
            r"""
    <Estructura esperada>
    En este reto necesitas representar una sola variable observada en varios casos.

    Piensa cuál es el objeto de Pandas diseñado para guardar una sola columna con índice.
    """,
            r"""
    <Resumen simple>
    Una vez creada la estructura principal, puedes obtener rápidamente sus valores extremos.

    Revisa qué métodos permiten calcular el mínimo y el máximo directamente sobre una serie.
    """,
            r"""
    <Filtro por umbral>
    El último paso consiste en seleccionar solo las observaciones que cumplen una condición clínica.

    Primero construye una comparación booleana y luego úsala para filtrar la propia serie.
    """,
            r"""
    <solucion>

    ```python
    sbp = pd.Series([118, 135, 142, 126, 160], name="sbp")
    sbp_min = sbp.min()
    sbp_max = sbp.max()
    high_sbp = sbp[sbp >= 140]
    ```
    """,
        ]
    )

    _tip_content.render()
    return


@app.cell(hide_code=True)
def _(high_sbp, sbp, sbp_max, sbp_min):
    _test_content = TestContent(
        items_raw=[
            r"""
    <Creación de la serie>
    Verifica que `sbp` exista y contenga los valores esperados.

    ```python
    assert sbp is not None, "Debes definir `sbp`."
    assert isinstance(sbp, pd.Series), "`sbp` debe ser una `pd.Series`."
    assert list(sbp.values) == [118, 135, 142, 126, 160], (
        "Los valores de `sbp` no son correctos."
    )
    print("Serie creada correctamente.")
    ```
    """,
            r"""
    <Extremos de la variable>
    Verifica que el mínimo y el máximo sean correctos.

    ```python
    assert sbp_min == 118, "`sbp_min` es incorrecto."
    assert sbp_max == 160, "`sbp_max` es incorrecto."
    print("Extremos correctos.")
    ```
    """,
            r"""
    <Filtro clínico>
    Verifica que el filtrado conserve solo los valores esperados.

    ```python
    assert isinstance(high_sbp, pd.Series), "`high_sbp` debe ser una `pd.Series`."
    assert list(high_sbp.values) == [142, 160], (
        "El filtrado de `high_sbp` no es correcto."
    )
    print("Filtrado correcto.")
    ```
    """,
        ],
        namespace=globals(),
    )

    sbp, sbp_min, sbp_max, high_sbp
    _test_content.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 4) `DataFrame`: una tabla clínica mínima

    Si una `Series` representa una sola variable, un `DataFrame` representa una tabla completa.

    En un `DataFrame`:

    - cada fila suele corresponder a una observación,
    - cada columna corresponde a una variable.

    Por ejemplo, una tabla clínica simple puede incluir:

    - identificador del paciente,
    - edad,
    - sexo,
    - presión arterial sistólica,
    - IMC.

    Esta es la estructura más habitual cuando trabajamos con bases de datos en salud.
    """)
    return


@app.cell
def _():
    # Creamos una tabla clínica pequeña de ejemplo
    pacientes = pd.DataFrame(
        {
            "patient_id": [101, 102, 103, 104, 105],
            "age": [34, 58, 45, 67, 29],
            "sex": ["F", "M", "F", "M", "F"],
            "sbp": [118, 141, 132, 155, 110],
            "bmi": [22.4, 29.1, 31.8, 27.5, 24.0],
        }
    )

    pacientes
    return (pacientes,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 5) Inspección rápida del `DataFrame`

    Antes de analizar una tabla, conviene inspeccionar su estructura.

    Algunas preguntas básicas son:

    - ¿cuántas filas y columnas tiene?
    - ¿cómo se llaman las variables?
    - ¿qué tipos de dato se infirieron?
    - ¿cómo se ven las primeras filas?

    Esta revisión inicial ayuda a detectar problemas o simplemente a familiarizarse con el dataset.
    """)
    return


@app.cell
def _(pacientes):
    # Inspección estructural del DataFrame
    pacientes.shape, pacientes.columns.tolist(), pacientes.dtypes
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 6) Selección: `loc` e `iloc`

    Pandas ofrece dos formas importantes de seleccionar partes de una tabla:

    - **`loc`**: selecciona por etiquetas
    - **`iloc`**: selecciona por posiciones

    Esta diferencia es muy importante.

    Usa `loc` cuando quieres pedir columnas por nombre.
    Usa `iloc` cuando quieres pedir filas o columnas por su posición.

    En práctica:

    - “quiero las columnas `age` y `sbp`”
    - “quiero las primeras filas y primeras columnas”
    """)
    return


@app.cell
def _(pacientes):
    # Selección por nombre de columnas usando loc
    pacientes.loc[:, ["age", "sbp"]]
    return


@app.cell
def _(pacientes):
    # Selección por posiciones usando iloc
    pacientes.iloc[0:3, 0:3]
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 7) Filtrado de filas con criterios clínicos

    Una de las tareas más frecuentes en Pandas es filtrar filas según condiciones.

    Por ejemplo:

    - presión sistólica elevada,
    - obesidad,
    - edad mayor o igual a cierto umbral.

    Cuando combinamos condiciones, debemos usar operadores lógicos apropiados:

    - `&` para AND
    - `|` para OR

    Y es importante rodear cada condición con paréntesis.
    """)
    return


@app.cell
def _(pacientes):
    # Ejemplo de filtrado combinado
    alto_riesgo = pacientes[(pacientes["sbp"] >= 140) & (pacientes["age"] >= 60)]

    alto_riesgo
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 8) Resúmenes simples: `describe`, `min` y `max`

    Antes de modelar o profundizar en una base de datos, suele hacerse un primer resumen descriptivo.

    Algunas operaciones útiles son:

    - `describe()`
    - `min()`
    - `max()`

    Estas funciones permiten obtener un panorama inicial de las variables numéricas.
    """)
    return


@app.cell
def _(pacientes):
    # Resumen descriptivo de variables numéricas seleccionadas
    pacientes[["age", "sbp", "bmi"]].describe()
    return


@app.cell
def _(pacientes):
    # Extremos de una variable concreta
    pacientes["bmi"].min(), pacientes["bmi"].max()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto 2 — Selección con `loc` e `iloc`

    **Dominio:** estructura tabular / selección básica

    En este reto trabajarás directamente sobre el `DataFrame` `pacientes`.

    El objetivo es reforzar dos ideas distintas:

    - selección por etiquetas,
    - selección por posiciones.

    Tu solución debe construir dos objetos nuevos a partir de la misma tabla original.

    Antes de programar, piensa:

    - cuándo conviene seleccionar por nombres,
    - cuándo conviene seleccionar por posiciones,
    - y qué forma final debería tener cada resultado.
    """)
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    # TODO: seleccionar por etiquetas
    demo = None

    # TODO: seleccionar por posiciones
    first_two_rows = None
    return demo, first_two_rows


@app.cell(hide_code=True)
def _():
    _tip_content = TipContent(
        items_raw=[
            r"""
    <Selección por etiquetas>
    Uno de los resultados debe construirse eligiendo columnas por su nombre.

    Revisa cuál es el indexador de Pandas pensado para trabajar con etiquetas.
    """,
            r"""
    <Selección por posiciones>
    El segundo resultado requiere elegir una región de la tabla según sus posiciones.

    Piensa qué indexador permite seleccionar filas y columnas usando rangos numéricos.
    """,
            r"""
    <Forma esperada>
    Antes de terminar, conviene revisar cuántas filas y columnas debería tener cada objeto resultante.

    Esto te puede ayudar a detectar errores de selección incluso antes de correr los tests.
    """,
            r"""
    <solucion>

    ```python
    demo = pacientes.loc[:, ["patient_id", "sex", "age"]]
    first_two_rows = pacientes.iloc[0:2, 0:3]
    ```
    """,
        ]
    )

    _tip_content.render()
    return


@app.cell(hide_code=True)
def _(demo, first_two_rows):
    _test_content = TestContent(
        items_raw=[
            r"""
    <Selección por columnas>
    Verifica que `demo` contenga las columnas esperadas en el orden correcto.

    ```python
    assert demo is not None, "Debes definir `demo`."
    assert list(demo.columns) == ["patient_id", "sex", "age"], (
        "Las columnas de `demo` no son correctas."
    )
    assert demo.shape == (pacientes.shape[0], 3), (
        "La dimensión de `demo` no es correcta."
    )
    print("Selección por etiquetas correcta.")
    ```
    """,
            r"""
    <Selección por posiciones>
    Verifica que `first_two_rows` tenga el tamaño esperado.

    ```python
    assert first_two_rows is not None, "Debes definir `first_two_rows`."
    assert first_two_rows.shape == (2, 3), (
        "La dimensión de `first_two_rows` no es correcta."
    )
    print("Dimensión por posiciones correcta.")
    ```
    """,
            r"""
    <Coincidencia con la tabla original>
    Verifica que el contenido seleccionado coincida con el `DataFrame` original.

    ```python
    assert first_two_rows.iloc[0, 0] == pacientes.iloc[0, 0], (
        "El contenido de `first_two_rows` no coincide con el esperado."
    )
    print("Contenido seleccionado correctamente.")
    ```
    """,
        ],
        namespace=globals(),
    )

    demo, first_two_rows
    _test_content.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 9) Transformaciones simples: crear columnas nuevas

    Un patrón muy común en Pandas es derivar nuevas variables a partir de las ya existentes.

    Por ejemplo:

    - una categoría de obesidad,
    - una bandera de tamizaje,
    - un puntaje simple,
    - una transformación de laboratorio.

    Crear una columna nueva consiste en asignar un resultado a una nueva etiqueta dentro del `DataFrame`.
    """)
    return


@app.cell
def _(pacientes):
    # Hacemos una copia para no modificar la tabla original
    pacientes2 = pacientes.copy()

    # Creamos una nueva variable derivada
    pacientes2["obesity"] = pacientes2["bmi"] >= 30

    pacientes2
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto 3 — Tamizaje básico con IMC y presión arterial

    **Dominio:** clínica / salud pública

    En este último reto integrarás varias ideas vistas en la lección:

    - filtrado de filas,
    - combinación de criterios booleanos,
    - y resumen descriptivo de un subconjunto.

    Trabajarás con `pacientes2`, que ya contiene una columna derivada llamada `obesity`.

    Tu tarea será:

    1. construir un subconjunto de pacientes que cumpla el criterio de tamizaje,
    2. y luego resumir algunas variables numéricas solo dentro de ese subconjunto.

    Antes de programar, piensa:

    - qué condición compuesta define el tamizaje,
    - cómo construir un `DataFrame` filtrado,
    - y cómo aplicar `describe()` solo a las columnas relevantes.
    """)
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    # TODO: construir el subconjunto filtrado
    screened = None

    # TODO: construir el resumen descriptivo
    summary = None
    return screened, summary


@app.cell(hide_code=True)
def _():
    _tip_content = TipContent(
        items_raw=[
            r"""
    <Criterio de tamizaje>
    El primer paso es construir una condición lógica compuesta.

    Revisa con cuidado si el criterio requiere que se cumplan ambas condiciones o si basta con que se cumpla una de ellas.
    """,
            r"""
    <Subconjunto filtrado>
    Una vez tengas la condición booleana, debes usarla para filtrar el `DataFrame`.

    El resultado esperado sigue siendo una tabla, no una serie.
    """,
            r"""
    <Resumen final>
    El último paso consiste en aplicar un resumen descriptivo solo a algunas columnas numéricas del subconjunto filtrado.

    Antes de hacerlo, identifica exactamente qué columnas deben incluirse.
    """,
            r"""
    <solucion>

    ```python
    screened = pacientes2[
        (pacientes2["obesity"] == True) | (pacientes2["sbp"] >= 140)
    ]
    summary = screened[["age", "sbp", "bmi"]].describe()
    ```
    """,
        ]
    )

    _tip_content.render()
    return


@app.cell(hide_code=True)
def _(screened, summary):
    _test_content = TestContent(
        items_raw=[
            r"""
    <Existencia de objetos>
    Verifica que ambos resultados hayan sido definidos.

    ```python
    assert screened is not None, "Debes definir `screened`."
    assert summary is not None, "Debes definir `summary`."
    print("Objetos definidos correctamente.")
    ```
    """,
            r"""
    <Estructura del subconjunto>
    Verifica que el subconjunto conserve las columnas esperadas.

    ```python
    assert all(c in screened.columns for c in ["age", "sbp", "bmi", "obesity"]), (
        "Faltan columnas esperadas en `screened`."
    )
    print("Estructura del subconjunto correcta.")
    ```
    """,
            r"""
    <Casos retenidos>
    Verifica que el filtro conserve al menos los pacientes esperados.

    ```python
    kept_ids = set(screened["patient_id"].tolist())

    assert {102, 103, 104}.issubset(kept_ids), (
        "El filtro no está reteniendo todos los casos esperados."
    )
    print("Filtrado correcto.")
    ```
    """,
            r"""
    <Resumen descriptivo>
    Verifica que `summary` tenga la estructura típica de `describe()`.

    ```python
    assert hasattr(summary, "loc"), "`summary` debe comportarse como un DataFrame."
    for idx in ["count", "mean", "std", "min", "25%", "50%", "75%", "max"]:
        assert idx in summary.index, "`summary` no parece provenir de `describe()`."
    print("Resumen descriptivo correcto.")
    ```
    """,
        ],
        namespace=globals(),
    )

    screened, summary
    _test_content.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Cierre conceptual

    En esta lección aprendiste a trabajar con las dos estructuras tabulares fundamentales de Pandas:

    - **`Series`**, para representar una variable etiquetada,
    - **`DataFrame`**, para representar una tabla completa.

    A lo largo de la lección viste cómo:

    - crear estas estructuras,
    - inspeccionar su forma y contenido,
    - seleccionar partes específicas,
    - filtrar según criterios clínicos,
    - resumir variables numéricas,
    - y crear columnas derivadas simples.

    Esta base será muy importante para la siguiente etapa, donde las tablas dejarán de ser solo objetos para inspeccionar y pasarán a ser herramientas para análisis más completos.
    """)
    return


if __name__ == "__main__":
    app.run()
