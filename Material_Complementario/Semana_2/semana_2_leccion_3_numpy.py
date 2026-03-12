# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "numpy==2.4.2",
#     "requests==2.32.5",
#     "pytest==9.0.2",
# ]
# ///

import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")

with app.setup(hide_code=True):
    import marimo as mo
    import numpy as np
    from setup import TipContent, TestContent


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Semana 2 · Lección 3 — NumPy: arrays y vectorización

    **Objetivo conceptual:** pasar de colecciones Python como las listas a **arrays NumPy**, para expresar operaciones numéricas sobre muchos valores al mismo tiempo, sin escribir ciclos explícitos.

    En analítica de salud, esto es especialmente útil porque muchas variables aparecen naturalmente como vectores:

    - peso
    - talla
    - presión arterial
    - biomarcadores
    - edad
    - resultados de laboratorio

    En esta lección trabajaremos con:

    - `ndarray` como estructura central
    - propiedades básicas como `shape` y `dtype`
    - creación de arrays
    - operaciones vectorizadas
    - indexación y slicing
    - máscaras booleanas
    - agregaciones rápidas como `mean`, `sum`, `min` y `max`
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 1) ¿Por qué NumPy en analítica de salud?

    En analítica clínica o epidemiológica, rara vez trabajamos con un solo número.

    Lo habitual es trabajar con **muchas observaciones a la vez**:

    - pesos de una cohorte,
    - tallas de una población,
    - valores de laboratorio de múltiples pacientes,
    - mediciones fisiológicas repetidas.

    Si usamos listas de Python, muchas operaciones requieren:

    - ciclos `for`,
    - acumuladores,
    - o transformaciones manuales más largas.

    Con NumPy, en cambio, podemos escribir una sola expresión que se aplica sobre todo el conjunto de datos.

    **Idea clave:** la **vectorización** consiste en expresar una operación sobre un array completo, en lugar de recorrer elemento por elemento de forma explícita.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 2) `ndarray`: el objeto central de NumPy

    La estructura básica de NumPy es el **array** (`ndarray`).

    Un array NumPy suele contener datos del mismo tipo y permite realizar operaciones numéricas de forma más directa y eficiente.

    Dos propiedades importantes son:

    - `dtype`: el tipo de dato almacenado
    - `shape`: la forma del array, es decir, sus dimensiones

    En salud, esto facilita tareas como:

    - calcular IMC para una cohorte,
    - transformar biomarcadores,
    - resumir variables fisiológicas,
    - seleccionar subgrupos con criterios clínicos.
    """)
    return


@app.cell
def _():
    # Datos clínicos sintéticos pequeños, pero útiles para aprender la lógica
    # Peso en kilogramos y talla en metros de varios pacientes
    peso_kg = np.array([72.0, 85.5, 60.2, 95.0, 68.0, 77.3, 110.4, 49.8])
    talla_m = np.array([1.75, 1.80, 1.62, 1.70, 1.68, 1.72, 1.78, 1.55])

    # Presión arterial sistólica en mmHg
    pas_mmHg = np.array([118, 135, 110, 142, 128, 125, 160, 105])

    peso_kg, talla_m, pas_mmHg
    return pas_mmHg, peso_kg, talla_m


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Antes de operar con los datos, conviene inspeccionar dos propiedades básicas del array:

    - su **forma** (`shape`), para saber cuántos elementos o dimensiones tiene,
    - y su **tipo de dato** (`dtype`), para entender qué clase de valores contiene.

    Esto ayuda a confirmar que estamos trabajando con la estructura esperada.
    """)
    return


@app.cell
def _(peso_kg, talla_m):
    # Observamos forma y tipo de dato de los arrays
    info_peso = (peso_kg.shape, peso_kg.dtype)
    info_talla = (talla_m.shape, talla_m.dtype)

    info_peso, info_talla
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 3) Operación vectorizada: cálculo de IMC

    Una de las ventajas más visibles de NumPy es que podemos aplicar una fórmula directamente sobre arrays completos.

    La fórmula del IMC es:

    \[
    IMC = \frac{\text{peso (kg)}}{\text{talla (m)}^2}
    \]

    Cuando `peso_kg` y `talla_m` son arrays, esta operación se aplica **elemento a elemento** de manera automática.

    Observa que no necesitamos escribir ningún `for`.
    """)
    return


@app.cell
def _(peso_kg, talla_m):
    # Cálculo vectorizado de IMC para todos los pacientes
    imc = peso_kg / (talla_m**2)

    # Redondeamos para facilitar la lectura
    imc_2_dec = np.round(imc, 2)

    imc_2_dec
    return imc, imc_2_dec


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 4) Indexación y slicing en arrays 1D

    Una vez tenemos un array, también podemos inspeccionar partes específicas.

    Reglas básicas:

    - `arr[i]` selecciona un elemento concreto
    - `arr[a:b]` selecciona un rango
    - el índice inicial se incluye, el final no

    Esto es útil, por ejemplo, cuando queremos revisar rápidamente algunos pacientes o un pequeño subconjunto del vector.
    """)
    return


@app.cell
def _(imc_2_dec):
    # Seleccionamos el primer valor del array
    primer_paciente = imc_2_dec[0]

    # Seleccionamos los tres primeros valores
    primeros_tres = imc_2_dec[:3]

    primer_paciente, primeros_tres
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 5) Máscaras booleanas: selección por criterio clínico

    Una máscara booleana es un array del mismo tamaño que los datos originales, pero formado por valores `True` y `False`.

    Estas máscaras permiten expresar preguntas como:

    - ¿qué pacientes tienen IMC elevado?
    - ¿qué pacientes podrían tener hipertensión?
    - ¿qué observaciones cumplen un criterio específico?

    La lógica general es:

    1. construir una condición,
    2. obtener una máscara booleana,
    3. usar esa máscara para seleccionar valores.
    """)
    return


@app.cell
def _(imc, pas_mmHg):
    def _():
        # Criterios clínicos simples expresados como máscaras booleanas
        obesidad = imc >= 30
        probable_hta = pas_mmHg >= 140

        # Seleccionamos solo los valores que cumplen cada criterio
        imc_obesidad = np.round(imc[obesidad], 2)
        pas_probable_hta = pas_mmHg[probable_hta]
    
        return obesidad, probable_hta, imc_obesidad, pas_probable_hta

    _()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 6) Agregaciones básicas: resumen rápido del vector

    NumPy también permite obtener resúmenes descriptivos de forma inmediata.

    Algunas operaciones frecuentes son:

    - `mean()`
    - `sum()`
    - `min()`
    - `max()`

    Esto resulta útil para obtener una primera visión rápida de una cohorte sin construir todavía una tabla más compleja.
    """)
    return


@app.cell
def _(imc, pas_mmHg):
    # Resumen simple de dos variables clínicas
    resumen = {
        "imc_media": float(imc.mean()),
        "imc_minimo": float(imc.min()),
        "imc_maximo": float(imc.max()),
        "pas_media": float(pas_mmHg.mean()),
        "pas_minima": int(pas_mmHg.min()),
        "pas_maxima": int(pas_mmHg.max()),
    }

    resumen
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---

    # Mini-retos (3)

    Hasta aquí viste varias ideas fundamentales:

    - cómo crear arrays,
    - cómo inspeccionar su estructura,
    - cómo aplicar operaciones vectorizadas,
    - cómo seleccionar con máscaras,
    - y cómo resumir rápidamente un conjunto de valores.

    Ahora vas a pasar de observar ejemplos a construir tus propias soluciones con NumPy.

    En cada reto tendrás que decidir:

    - qué operación vectorizada usar,
    - qué salida debe producirse,
    - y cómo mantener toda la lógica sin recurrir a ciclos.

    En cada reto encontrarás:

    - un contexto breve,
    - una celda editable,
    - tips progresivos,
    - y tests para verificar tu solución.

    Recomendación de trabajo:

    1. lee el reto completo,
    2. identifica qué estructuras ya están dadas,
    3. piensa qué transformación NumPy necesitas,
    4. implementa primero una versión simple,
    5. usa los tips solo si te bloqueas,
    6. interpreta los tests como retroalimentación.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto 1 — Cohorte: IMC vectorizado

    **Dominio:** clínica / salud pública

    En este primer reto trabajarás con una cohorte pequeña de pacientes representada por dos arrays:

    - `peso_kg_r1`
    - `talla_m_r1`

    El objetivo es practicar la idea más importante de esta lección:

    **usar una operación vectorizada para transformar dos arrays en un resultado nuevo**.

    Tu tarea será obtener un array con los IMC y luego construir una versión redondeada.

    Antes de programar, piensa:

    - qué operación debe aplicarse entre ambos arrays,
    - qué tipo de objeto debe salir,
    - y cómo generar una versión más legible del resultado sin cambiar su estructura.
    """)
    return


@app.cell
def _():
    # Datos del reto (no modificar)
    peso_kg_r1 = np.array([50.0, 64.2, 72.0, 80.0, 92.5])
    talla_m_r1 = np.array([1.55, 1.68, 1.75, 1.80, 1.70])

    # === TU TURNO (EDITA ESTA CELDA) ===
    # TODO: calcular el array principal
    imc_r1 = None

    # TODO: construir la versión redondeada
    imc_r1_1d = None

    print("IMC (1 decimal):", imc_r1_1d)
    return imc_r1, imc_r1_1d


@app.cell(hide_code=True)
def _():
    _tip_content = TipContent(
        items_raw=[
            r"""
    <Relación entre los arrays>
    Ambos arrays representan medidas correspondientes a los mismos pacientes.

    Antes de escribir código, identifica qué operación clínica conecta esas dos variables.
    """,
            r"""
    <Operación vectorizada>
    No necesitas recorrer paciente por paciente.

    Si aplicas correctamente una operación entre arrays NumPy compatibles, el resultado se calculará elemento a elemento.
    """,
            r"""
    <Versión más legible>
    Después de obtener el resultado principal, conviene construir una versión redondeada para mostrarla con más claridad.

    Piensa qué función de NumPy permite redondear un array completo sin usar ciclos.
    """,
            r"""
    <solucion>

    ```python
    imc_r1 = peso_kg_r1 / (talla_m_r1 ** 2)
    imc_r1_1d = np.round(imc_r1, 1)
    ```
    """,
        ]
    )

    _tip_content.render()
    return


@app.cell(hide_code=True)
def _(imc_r1, imc_r1_1d):
    _test_content = TestContent(
        items_raw=[
            r"""
    <Tipo de salida>
    Verifica que ambas salidas sean arrays NumPy.

    ```python
    assert isinstance(imc_r1, np.ndarray), "imc_r1 debe ser un array NumPy."
    assert isinstance(imc_r1_1d, np.ndarray), "imc_r1_1d debe ser un array NumPy."
    print("Tipo de salida correcto.")
    ```
    """,
            r"""
    <Forma del resultado>
    Verifica que el resultado conserve la misma longitud de la cohorte original.

    ```python
    assert imc_r1.shape == peso_kg_r1.shape, (
        "El array de IMC debe tener la misma forma que los datos de entrada."
    )
    print("Forma del resultado correcta.")
    ```
    """,
            r"""
    <Cálculo vectorizado>
    Verifica que el cálculo principal coincida con el resultado esperado.

    ```python
    imc_ref = peso_kg_r1 / (talla_m_r1 ** 2)

    assert np.allclose(imc_r1, imc_ref, rtol=0, atol=1e-12), (
        "El cálculo de IMC no coincide con el valor esperado."
    )
    print("Cálculo principal correcto.")
    ```
    """,
            r"""
    <Versión redondeada>
    Verifica que la versión redondeada sea correcta.

    ```python
    imc_ref = peso_kg_r1 / (talla_m_r1 ** 2)
    imc_ref_1d = np.round(imc_ref, 1)

    assert np.allclose(imc_r1_1d, imc_ref_1d, rtol=0, atol=1e-12), (
        "La versión redondeada no coincide con el valor esperado."
    )
    print("Versión redondeada correcta.")
    ```
    """,
        ],
        namespace=globals(),
    )

    imc_r1, imc_r1_1d
    _test_content.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 7) Estandarización sin ciclos: z-score

    En análisis de cohortes es frecuente transformar una variable para expresar cuánto se aleja cada observación respecto al promedio.

    Una forma clásica de hacerlo es el **z-score**:

    \[
    z = \frac{x - \mu}{\sigma}
    \]

    Aquí ocurre algo importante:

    - `x` es un array,
    - `\mu` y `\sigma` son escalares,
    - pero la operación sigue siendo vectorizada.

    Es decir, podemos restar y dividir todo el array sin escribir ciclos explícitos.
    """)
    return


@app.cell
def _():
    # Biomarcador ficticio en varias observaciones
    biomarcador = np.array([2.1, 2.4, 1.9, 3.2, 2.8, 2.0, 3.6, 1.7])

    # Calculamos media y desviación estándar
    media = biomarcador.mean()
    desviacion = biomarcador.std()

    # Estandarización vectorizada
    z = (biomarcador - media) / desviacion

    np.round(z, 2)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---

    # Mini-reto 2 — Laboratorio: z-score y umbral

    **Dominio:** laboratorio / epidemiología

    En este reto trabajarás con un biomarcador medido en varios pacientes.

    La meta es construir una pequeña secuencia analítica con NumPy:

    - resumir la variable,
    - transformarla,
    - y luego definir un criterio de selección.

    Tu solución debe producir:

    1. una transformación estandarizada,
    2. una máscara booleana,
    3. y un conteo final.

    Antes de programar, piensa:

    - qué escalares necesitas obtener primero,
    - cómo transformar el array completo,
    - y cómo pasar de una condición booleana a un conteo.
    """)
    return


@app.cell
def _():
    # Datos del reto (no modificar)
    biomarcador_r2 = np.array([10.0, 9.5, 12.2, 11.1, 8.9, 9.8, 13.0, 10.4])

    # === TU TURNO (EDITA ESTA CELDA) ===
    # TODO: calcular los escalares necesarios
    mu_r2 = None
    sigma_r2 = None

    # TODO: construir la transformación principal
    z_r2 = None

    # TODO: construir la máscara booleana
    alto_riesgo_r2 = None

    # TODO: obtener el conteo final
    n_alto_riesgo_r2 = None

    print("z:", z_r2)
    print("alto_riesgo:", alto_riesgo_r2)
    print("n_alto_riesgo:", n_alto_riesgo_r2)
    return alto_riesgo_r2, n_alto_riesgo_r2, z_r2


@app.cell(hide_code=True)
def _():
    _tip_content = TipContent(
        items_raw=[
            r"""
    <Resumen previo>
    Antes de transformar el array, necesitas obtener dos cantidades que resumen su distribución.

    Ambas se calculan directamente a partir del propio array.
    """,
            r"""
    <Transformación vectorizada>
    Una vez tengas esos escalares, la estandarización se puede aplicar sobre todo el array en una sola expresión.

    No necesitas trabajar observación por observación.
    """,
            r"""
    <Criterio booleano>
    Después de transformar, debes construir una condición que clasifique qué observaciones cumplen el umbral definido.

    Esa condición debe producir un array booleano.
    """,
            r"""
    <Del booleano al conteo>
    El último paso consiste en resumir cuántos valores `True` aparecen en la máscara.

    Piensa qué propiedad de NumPy permite contar directamente esos valores.
    """,
            r"""
    <solucion>

    ```python
    mu_r2 = biomarcador_r2.mean()
    sigma_r2 = biomarcador_r2.std()
    z_r2 = (biomarcador_r2 - mu_r2) / sigma_r2
    alto_riesgo_r2 = z_r2 >= 1.0
    n_alto_riesgo_r2 = int(alto_riesgo_r2.sum())
    ```
    """,
        ]
    )

    _tip_content.render()
    return


@app.cell(hide_code=True)
def _(alto_riesgo_r2, n_alto_riesgo_r2, z_r2):
    _test_content = TestContent(
        items_raw=[
            r"""
    <Escalares de resumen>
    Verifica que la media y la desviación estándar sean correctas.

    ```python
    mu_ref = biomarcador_r2.mean()
    sigma_ref = biomarcador_r2.std()

    assert abs(mu_r2 - mu_ref) < 1e-12, "La media no es correcta."
    assert abs(sigma_r2 - sigma_ref) < 1e-12, "La desviación estándar no es correcta."
    print("Resumen previo correcto.")
    ```
    """,
            r"""
    <Transformación principal>
    Verifica que el z-score haya sido calculado correctamente.

    ```python
    mu_ref = biomarcador_r2.mean()
    sigma_ref = biomarcador_r2.std()
    z_ref = (biomarcador_r2 - mu_ref) / sigma_ref

    assert isinstance(z_r2, np.ndarray), "z_r2 debe ser un array NumPy."
    assert z_r2.shape == biomarcador_r2.shape, "z_r2 debe conservar la forma del array original."
    assert np.allclose(z_r2, z_ref, rtol=0, atol=1e-12), "El z-score no es correcto."
    print("Transformación principal correcta.")
    ```
    """,
            r"""
    <Máscara booleana>
    Verifica que la selección por umbral sea correcta.

    ```python
    mu_ref = biomarcador_r2.mean()
    sigma_ref = biomarcador_r2.std()
    z_ref = (biomarcador_r2 - mu_ref) / sigma_ref
    mask_ref = z_ref >= 1.0

    assert isinstance(alto_riesgo_r2, np.ndarray), "alto_riesgo_r2 debe ser un array."
    assert alto_riesgo_r2.dtype == bool, "alto_riesgo_r2 debe ser booleano."
    assert np.array_equal(alto_riesgo_r2, mask_ref), "La máscara no coincide con el criterio esperado."
    print("Máscara booleana correcta.")
    ```
    """,
            r"""
    <Conteo final>
    Verifica que el conteo de pacientes en alto riesgo sea correcto.

    ```python
    mu_ref = biomarcador_r2.mean()
    sigma_ref = biomarcador_r2.std()
    z_ref = (biomarcador_r2 - mu_ref) / sigma_ref
    mask_ref = z_ref >= 1.0
    n_ref = int(mask_ref.sum())

    assert int(n_alto_riesgo_r2) == n_ref, "El conteo final no es correcto."
    print("Conteo final correcto.")
    ```
    """,
        ],
        namespace=globals(),
    )

    z_r2, alto_riesgo_r2, n_alto_riesgo_r2
    _test_content.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 8) Arrays 2D: pacientes × variables

    Hasta ahora trabajaste con arrays unidimensionales.

    Pero muchas veces los datos clínicos pueden organizarse como una **matriz**, donde:

    - las filas representan pacientes,
    - y las columnas representan variables.

    Por ejemplo:

    - presión sistólica,
    - presión diastólica,
    - frecuencia cardiaca.

    En NumPy, esta estructura 2D permite seleccionar filas, columnas o bloques completos con slicing.
    """)
    return


@app.cell
def _():
    # Matriz clínica: columnas = PAS, PAD, FC
    X_vitales = np.array(
        [
            [118, 76, 70],
            [135, 85, 78],
            [110, 72, 66],
            [142, 90, 88],
            [128, 82, 74],
            [125, 80, 72],
            [160, 95, 92],
            [105, 68, 60],
        ],
        dtype=float,
    )

    X_vitales.shape, X_vitales.dtype
    return (X_vitales,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Cuando un array es bidimensional, también podemos resumirlo por ejes.

    Por ejemplo, si queremos obtener el promedio de cada variable clínica, debemos resumir por columnas.

    Esto produce un vector con un valor por variable.
    """)
    return


@app.cell
def _(X_vitales):
    # Calculamos el promedio por columna: PAS, PAD y FC
    media_por_variable = X_vitales.mean(axis=0)

    np.round(media_por_variable, 2)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 9) Composición de criterios con máscaras

    Una de las ideas más potentes de NumPy es que las máscaras también pueden combinarse.

    Para arrays booleanos usamos:

    - `&` para AND
    - `|` para OR

    Esto permite expresar reglas clínicas compuestas de forma clara.

    Ejemplo:

    “probable hipertensión” si:

    - PAS >= 140
    - **o** PAD >= 90

    Observa que con arrays booleanos no se debe usar `and` / `or`, sino `&` y `|`.
    """)
    return


@app.cell
def _(X_vitales):
    # Extraemos las columnas de presión arterial
    pas = X_vitales[:, 0]
    pad = X_vitales[:, 1]

    # Construimos una regla compuesta
    probable_hta = (pas >= 140) | (pad >= 90)

    probable_hta, probable_hta.sum()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---

    # Mini-reto 3 — Tamizaje clínico vectorizado

    **Dominio:** clínica / salud pública

    En este último reto integrarás varias ideas vistas en la lección:

    - slicing sobre arrays 2D,
    - construcción de máscaras,
    - combinación de criterios,
    - y conteo final.

    Trabajarás con una matriz donde cada fila representa un paciente y cada columna una variable clínica.

    Tu tarea consiste en pasar de esa matriz a una regla de clasificación compuesta.

    Antes de programar, piensa:

    - cómo extraer cada variable desde la matriz,
    - cómo construir primero una condición intermedia,
    - y cómo combinar luego varios criterios clínicos.
    """)
    return


@app.cell
def _():
    # Datos del reto (no modificar)
    # columnas: PAS, PAD, IMC
    X_r3 = np.array(
        [
            [118, 76, 23.5],
            [145, 92, 31.2],
            [132, 88, 29.8],
            [160, 95, 34.1],
            [138, 85, 30.0],
            [150, 89, 28.4],
            [128, 82, 35.0],
            [142, 91, 27.9],
        ],
        dtype=float,
    )

    # === TU TURNO (EDITA ESTA CELDA) ===
    # TODO: extraer los arrays principales
    pas_r3 = None
    pad_r3 = None
    imc_r3 = None

    # TODO: construir las máscaras necesarias
    hta_r3 = None
    alto_riesgo_r3 = None

    # TODO: obtener el conteo final
    n_alto_riesgo_r3 = None

    print("hta:", hta_r3)
    print("alto_riesgo:", alto_riesgo_r3)
    print("n_alto_riesgo:", n_alto_riesgo_r3)
    return alto_riesgo_r3, hta_r3, imc_r3, n_alto_riesgo_r3, pad_r3, pas_r3


@app.cell(hide_code=True)
def _():
    _tip_content = TipContent(
        items_raw=[
            r"""
    <Extracción desde la matriz>
    Antes de construir criterios clínicos, necesitas separar las columnas relevantes.

    Piensa cómo obtener una columna completa desde un array bidimensional usando slicing.
    """,
            r"""
    <Primer criterio>
    La primera condición es una regla de probable hipertensión construida a partir de dos variables distintas.

    Revisa qué operador lógico permite unir dos comparaciones con sentido de “o”.
    """,
            r"""
    <Segundo criterio compuesto>
    Después de construir la primera máscara, debes combinarla con una condición adicional sobre IMC.

    Aquí ya no basta con OR: debes identificar qué operador lógico expresa mejor la regla compuesta.
    """,
            r"""
    <Conteo final>
    Una vez construida la máscara final, solo falta resumir cuántos pacientes cumplen el criterio.

    Piensa cómo convertir esa suma en un entero explícito.
    """,
            r"""
    <solucion>

    ```python
    pas_r3 = X_r3[:, 0]
    pad_r3 = X_r3[:, 1]
    imc_r3 = X_r3[:, 2]

    hta_r3 = (pas_r3 >= 140) | (pad_r3 >= 90)
    alto_riesgo_r3 = hta_r3 & (imc_r3 >= 30)
    n_alto_riesgo_r3 = int(alto_riesgo_r3.sum())
    ```
    """,
        ]
    )

    _tip_content.render()
    return


@app.cell(hide_code=True)
def _(alto_riesgo_r3, hta_r3, imc_r3, n_alto_riesgo_r3, pad_r3, pas_r3):
    _test_content = TestContent(
        items_raw=[
            r"""
    <Extracción de columnas>
    Verifica que las tres variables hayan sido extraídas correctamente desde la matriz original.

    ```python
    pas_ref = X_r3[:, 0]
    pad_ref = X_r3[:, 1]
    imc_ref = X_r3[:, 2]

    assert isinstance(pas_r3, np.ndarray) and np.array_equal(pas_r3, pas_ref), (
        "La extracción de PAS no es correcta."
    )
    assert isinstance(pad_r3, np.ndarray) and np.array_equal(pad_r3, pad_ref), (
        "La extracción de PAD no es correcta."
    )
    assert isinstance(imc_r3, np.ndarray) and np.array_equal(imc_r3, imc_ref), (
        "La extracción de IMC no es correcta."
    )

    print("Extracción de columnas correcta.")
    ```
    """,
            r"""
    <Primera máscara clínica>
    Verifica que la regla de probable hipertensión sea correcta.

    ```python
    pas_ref = X_r3[:, 0]
    pad_ref = X_r3[:, 1]
    hta_ref = (pas_ref >= 140) | (pad_ref >= 90)

    assert isinstance(hta_r3, np.ndarray), "hta_r3 debe ser un array."
    assert hta_r3.dtype == bool, "hta_r3 debe ser booleano."
    assert np.array_equal(hta_r3, hta_ref), "La máscara de HTA no es correcta."

    print("Primera máscara correcta.")
    ```
    """,
            r"""
    <Máscara compuesta>
    Verifica que la regla final de alto riesgo cardiometabólico sea correcta.

    ```python
    pas_ref = X_r3[:, 0]
    pad_ref = X_r3[:, 1]
    imc_ref = X_r3[:, 2]
    hta_ref = (pas_ref >= 140) | (pad_ref >= 90)
    alto_ref = hta_ref & (imc_ref >= 30)

    assert isinstance(alto_riesgo_r3, np.ndarray), "alto_riesgo_r3 debe ser un array."
    assert alto_riesgo_r3.dtype == bool, "alto_riesgo_r3 debe ser booleano."
    assert np.array_equal(alto_riesgo_r3, alto_ref), "La máscara final no es correcta."

    print("Máscara compuesta correcta.")
    ```
    """,
            r"""
    <Conteo final>
    Verifica que el número de pacientes clasificados como alto riesgo sea correcto.

    ```python
    pas_ref = X_r3[:, 0]
    pad_ref = X_r3[:, 1]
    imc_ref = X_r3[:, 2]
    hta_ref = (pas_ref >= 140) | (pad_ref >= 90)
    alto_ref = hta_ref & (imc_ref >= 30)
    n_ref = int(alto_ref.sum())

    assert int(n_alto_riesgo_r3) == n_ref, "El conteo final no es correcto."

    print("Conteo final correcto.")
    ```
    """,
        ],
        namespace=globals(),
    )

    pas_r3, pad_r3, imc_r3, hta_r3, alto_riesgo_r3, n_alto_riesgo_r3
    _test_content.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Cierre conceptual

    Hoy construiste un puente importante:

    **listas → arrays → operaciones vectorizadas**

    A lo largo de la lección viste que NumPy permite:

    - representar datos numéricos de forma estructurada,
    - aplicar transformaciones sobre muchos valores al mismo tiempo,
    - expresar criterios clínicos mediante máscaras booleanas,
    - y producir resúmenes rápidos y reproducibles.

    Esta forma de trabajar será la base para pasar después a estructuras tabulares más ricas y análisis más complejos.
    """)
    return


if __name__ == "__main__":
    app.run()
