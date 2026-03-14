# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo>=0.20.0",
#     "numpy==2.4.2",
#     "pandas==3.0.1",
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
    import pandas as pd
    import pytest
    import requests
    from setup import TipContent, TestContent


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Semana 2 · Lección 8
    ## Reestructuración y combinación avanzada de tablas en pandas

    En sesiones anteriores trabajaste principalmente con **resúmenes y agregaciones**.

    En esta lección nos moveremos a un paso anterior, pero igual de importante: **darle a la tabla la forma correcta antes del resumen**.

    Trabajaremos con cuatro operaciones muy frecuentes en análisis de datos en salud:

    - **reestructurar tablas** con `melt`
    - **combinar tablas equivalentes** con `concat`
    - **unir tablas con validación de llaves** con `merge`
    - **calcular métricas por grupo sin perder filas** con `transform`

    Además, cerraremos con dos patrones muy usados en análisis clínico real:

    - obtener la **última medición por paciente**
    - construir un **ranking dentro de hospital**

    La idea central es esta:

    > una tabla clínica casi nunca llega en la forma exacta en que se necesita para analizarla.

    Por eso, el *data wrangling* consiste en transformar la estructura de los datos sin perder su significado clínico o epidemiológico.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Propósito analítico

    Usaremos datos sintéticos de un programa ambulatorio de riesgo cardiometabólico.

    Cada tabla representa una parte distinta del sistema:

    - una tabla de pacientes,
    - una tabla de laboratorios,
    - una tabla de instituciones,
    - y una tabla longitudinal de presión arterial.

    El objetivo no es solo “mover columnas”, sino responder preguntas como:

    - ¿qué instituciones atienden pacientes de mayor edad?
    - ¿cómo reorganizar una tabla ancha para resumir por tiempo?
    - ¿cómo validar una unión para no duplicar pacientes por error?
    - ¿cómo calcular métricas por hospital sin colapsar la tabla?
    - ¿cómo quedarnos con la medición más reciente de cada paciente?
    - ¿cómo comparar pacientes dentro de su mismo hospital?
    """)
    return


@app.cell(hide_code=True)
def _():
    generador = np.random.default_rng(20260313)

    n_pacientes = 24
    patient_id = np.arange(1001, 1001 + n_pacientes)
    sex = generador.choice(
        np.array(["female", "male"]),
        size=n_pacientes,
        p=[0.58, 0.42],
    )
    hospital_code = generador.choice(
        np.array(["H1", "H2", "H3"]),
        size=n_pacientes,
        p=[0.35, 0.40, 0.25],
    )
    age = generador.integers(35, 81, size=n_pacientes)
    diabetes = generador.choice(
        np.array(["yes", "no"]),
        size=n_pacientes,
        p=[0.38, 0.62],
    )

    patients = pd.DataFrame(
        {
            "patient_id": patient_id,
            "sex": sex,
            "age": age,
            "hospital_code": hospital_code,
            "diabetes": diabetes,
        }
    ).sort_values("patient_id").reset_index(drop=True)

    labs = pd.DataFrame(
        {
            "patient_id": patient_id,
            "sbp": generador.normal(132, 16, size=n_pacientes).round(0).astype(int),
            "ldl": generador.normal(121, 28, size=n_pacientes).round(0).astype(int),
            "bmi": generador.normal(28, 4.5, size=n_pacientes).round(1),
        }
    ).sort_values("patient_id").reset_index(drop=True)

    hospitals = pd.DataFrame(
        {
            "hospital_code": ["H1", "H2", "H3"],
            "hospital_name": [
                "Hospital Central",
                "Hospital del Norte",
                "Hospital Comunitario",
            ],
            "region": ["urban", "urban", "rural"],
        }
    )

    monthly_bp = pd.DataFrame(
        {
            "patient_id": patient_id,
            "sbp_baseline": generador.normal(136, 15, size=n_pacientes).round(0).astype(int),
            "sbp_month_1": generador.normal(132, 15, size=n_pacientes).round(0).astype(int),
            "sbp_month_3": generador.normal(128, 14, size=n_pacientes).round(0).astype(int),
        }
    ).sort_values("patient_id").reset_index(drop=True)

    assert patients["patient_id"].is_unique
    assert labs["patient_id"].is_unique
    assert hospitals["hospital_code"].is_unique
    assert monthly_bp["patient_id"].is_unique
    return hospitals, labs, monthly_bp, patients


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Tablas base

    Comenzamos con cuatro tablas separadas.

    Desde el punto de vista conceptual, esto refleja una situación común en salud:

    - los datos demográficos están en una tabla,
    - los resultados clínicos en otra,
    - los metadatos institucionales en otra,
    - y algunas mediciones longitudinales en formato ancho.

    Antes de unir o resumir, siempre conviene inspeccionar cada estructura por separado y preguntarse:

    - ¿qué representa cada fila?
    - ¿qué representa cada columna?
    - ¿qué llave permite conectar esta tabla con otras?
    """)
    return


@app.cell
def _(patients):
    patients
    return


@app.cell
def _(labs):
    labs
    return


@app.cell
def _(hospitals):
    hospitals
    return


@app.cell
def _(monthly_bp):
    monthly_bp.head()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 1) `merge`: unir tablas por una llave común

    `merge` permite enlazar filas de dos tablas usando una o más claves.

    En términos analíticos, esto equivale a **enriquecer una tabla** con información disponible en otra.

    En nuestro caso:

    - `patients` contiene características demográficas,
    - `labs` contiene biomarcadores,
    - `hospitals` contiene metadatos institucionales.

    La secuencia será:

    1. unir pacientes con laboratorios usando `patient_id`,
    2. unir ese resultado con hospitales usando `hospital_code`.
    """)
    return


@app.cell
def _(labs, patients):
    perfil_paciente = patients.merge(labs, on="patient_id", how="inner")

    assert perfil_paciente.shape[0] == patients.shape[0]
    assert "sbp" in perfil_paciente.columns
    assert "ldl" in perfil_paciente.columns

    perfil_paciente.head()
    return (perfil_paciente,)


@app.cell
def _(hospitals, perfil_paciente):
    perfil_paciente_completo = perfil_paciente.merge(
        hospitals,
        on="hospital_code",
        how="left",
    )

    assert perfil_paciente_completo.shape[0] == perfil_paciente.shape[0]
    assert perfil_paciente_completo["hospital_name"].isna().sum() == 0

    perfil_paciente_completo.head()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Interpretación

    Después del `merge`, cada fila sigue representando un paciente, pero ahora contiene más contexto.

    Eso es importante: **la unidad de análisis no cambió**.

    Lo que cambió fue la cantidad de información disponible por fila.

    Esta idea es fundamental, porque una unión bien hecha agrega contexto sin alterar indebidamente el significado de cada observación.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto 1

    Construye una tabla llamada `pacientes_mayores` a partir de `perfil_paciente_completo` con estas condiciones:

    - incluir solo pacientes de **60 años o más**,
    - conservar únicamente las columnas:
      `patient_id`, `age`, `sex`, `hospital_name`, `sbp`, `ldl`,
    - ordenar por `age` de mayor a menor.

    Este reto refuerza dos ideas previas de pandas:

    - selección por condición,
    - selección explícita de columnas.
    """)
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    pacientes_mayores = None
    return


@app.cell(hide_code=True)
def _():
    tip_content_reto_1 = TipContent(
        items_raw=[
            r"""
    <Filtrado por condición>
    Primero identifica qué filas cumplen el criterio de edad.

    Esa condición debe aplicarse antes o al mismo tiempo que la selección de columnas.
    """,
            r"""
    <Columnas finales>
    La tabla no debe conservar todas las variables del dataset enriquecido.

    Debes dejar solo el subconjunto explícitamente pedido.
    """,
            r"""
    <Orden del resultado>
    La salida final debe quedar ordenada por edad de mayor a menor.

    Eso forma parte del contrato del mini-reto, no es un detalle opcional.
    """,
            r"""
    <solucion>

    ```python
    pacientes_mayores = (
    perfil_paciente_completo.loc[
        perfil_paciente_completo["age"] >= 60,
        ["patient_id", "age", "sex", "hospital_name", "sbp", "ldl"],
    ]
    .sort_values("age", ascending=False)
    .reset_index(drop=True)
    )
    ```
    """,
        ]
    )

    tip_content_reto_1.render()
    return


@app.cell(hide_code=True)
def _():
    test_content_reto_1 = TestContent(
        items_raw=[
            r"""
    <Objeto definido>

    ```python
    assert pacientes_mayores is not None
    print("Tabla definida correctamente.")
    ```
    """,
            r"""
    <Columnas correctas>

    ```python
    assert list(pacientes_mayores.columns) == [
    "patient_id",
    "age",
    "sex",
    "hospital_name",
    "sbp",
    "ldl",
    ]
    print("Columnas correctas.")
    ```
    """,
            r"""
    <Regla de edad y orden>

    ```python
    assert (pacientes_mayores["age"] >= 60).all()
    assert pacientes_mayores["age"].is_monotonic_decreasing
    print("Filtro y orden correctos.")
    ```
    """,
        ],
        namespace=globals(),
    )

    test_content_reto_1.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 2) `concat`: combinar tablas con la misma estructura

    Mientras `merge` une columnas usando llaves, `concat` apila o concatena objetos a lo largo de un eje.

    Una situación frecuente en salud pública es tener la misma estructura separada por sedes, periodos o cohortes.

    Aquí simularemos dos tablas de tamizaje provenientes de dos jornadas distintas.

    La pregunta conceptual es:

    **si las columnas representan las mismas variables, podemos apilar las filas para formar una sola tabla de eventos.**
    """)
    return


@app.cell
def _():
    jornada_tamizaje_1 = pd.DataFrame(
        {
            "screening_id": ["S01", "S02", "S03", "S04"],
            "hospital_code": ["H1", "H2", "H1", "H3"],
            "n_screened": [40, 32, 28, 22],
            "day": ["day_1", "day_1", "day_1", "day_1"],
        }
    )

    jornada_tamizaje_2 = pd.DataFrame(
        {
            "screening_id": ["S05", "S06", "S07", "S08"],
            "hospital_code": ["H2", "H3", "H1", "H2"],
            "n_screened": [35, 21, 31, 30],
            "day": ["day_2", "day_2", "day_2", "day_2"],
        }
    )
    return jornada_tamizaje_1, jornada_tamizaje_2


@app.cell
def _(jornada_tamizaje_1, jornada_tamizaje_2):
    tamizaje_total = pd.concat(
        [jornada_tamizaje_1, jornada_tamizaje_2],
        ignore_index=True,
    )

    assert tamizaje_total.shape[0] == (
        jornada_tamizaje_1.shape[0] + jornada_tamizaje_2.shape[0]
    )
    assert tamizaje_total.shape[1] == jornada_tamizaje_1.shape[1]

    tamizaje_total
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Interpretación

    En `tamizaje_total`, cada fila sigue representando una jornada institucional de tamizaje.

    La lógica de `concat` es útil cuando las tablas comparten el mismo diccionario de variables.

    En otras palabras:

    - **mismas columnas**,
    - **más filas**,
    - **misma semántica observacional**.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 3) `melt`: pasar de formato ancho a formato largo

    Muchos sistemas clínicos almacenan mediciones repetidas en columnas diferentes:

    - `sbp_baseline`
    - `sbp_month_1`
    - `sbp_month_3`

    Ese formato es cómodo para lectura humana, pero no siempre es el mejor para resumir por tiempo.

    `melt` transforma una tabla **ancha** en una tabla **larga**.

    Esto permite que una variable como el tiempo quede representada explícitamente en una columna.
    """)
    return


@app.cell
def _(monthly_bp):
    presion_long = monthly_bp.melt(
        id_vars="patient_id",
        value_vars=["sbp_baseline", "sbp_month_1", "sbp_month_3"],
        var_name="timepoint",
        value_name="sbp",
    )

    assert presion_long.shape[0] == monthly_bp.shape[0] * 3
    assert set(presion_long.columns) == {"patient_id", "timepoint", "sbp"}

    presion_long.head(9)
    return (presion_long,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## ¿Por qué este cambio importa?

    Cuando el tiempo está codificado como nombres de columnas, es más difícil:

    - agrupar,
    - resumir,
    - comparar,
    - o construir tablas por momento de medición.

    Después de `melt`, el tiempo se convierte en una variable explícita.

    Eso prepara la tabla para operaciones posteriores como `groupby`, `agg` y `pivot_table`.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto 2

    A partir de `presion_long`, construye una tabla llamada `media_sbp_tiempo` que:

    - agrupe por `timepoint`,
    - calcule la **media** de `sbp`,
    - devuelva el resultado con `as_index=False`,
    - ordene las filas siguiendo este orden lógico:
      `sbp_baseline`, `sbp_month_1`, `sbp_month_3`.

    Este ejercicio enlaza directamente el cambio de estructura con el resumen analítico.
    """)
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    media_sbp_tiempo = None
    return


@app.cell(hide_code=True)
def _():
    tip_content_reto_2 = TipContent(
        items_raw=[
            r"""
    <Agrupación>
    El resumen debe producir una fila por momento de medición.

    Eso define directamente la variable de agrupación.
    """,
            r"""
    <Métrica>
    La salida requiere una sola medida resumen sobre la presión arterial sistólica.

    Piensa qué función de agregación corresponde.
    """,
            r"""
    <Orden lógico>
    El orden final no es alfabético, sino clínico-temporal.

    Necesitas una forma explícita de imponer ese orden.
    """,
            r"""
    <solucion>

    ```python
    media_sbp_tiempo = (
    presion_long.groupby("timepoint", as_index=False)
    .agg(mean_sbp=("sbp", "mean"))
    .assign(
        timepoint=lambda d: pd.Categorical(
            d["timepoint"],
            categories=["sbp_baseline", "sbp_month_1", "sbp_month_3"],
            ordered=True,
        )
    )
    .sort_values("timepoint")
    .reset_index(drop=True)
    )
    ```
    """,
        ]
    )

    tip_content_reto_2.render()
    return


@app.cell(hide_code=True)
def _():
    test_content_reto_2 = TestContent(
        items_raw=[
            r"""
    <Objeto definido>

    ```python
    assert media_sbp_tiempo is not None
    print("Tabla definida correctamente.")
    ```
    """,
            r"""
    <Columnas correctas>

    ```python
    assert list(media_sbp_tiempo.columns) == ["timepoint", "mean_sbp"]
    print("Columnas correctas.")
    ```
    """,
            r"""
    <Contenido válido>

    ```python
    assert media_sbp_tiempo.shape[0] == 3
    assert media_sbp_tiempo["mean_sbp"].notna().all()
    print("Resumen correcto.")
    ```
    """,
        ],
        namespace=globals(),
    )

    test_content_reto_2.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 4) `merge` con validación de llaves

    Un error muy común es hacer joins incorrectos.

    Cuando cada paciente aparece **una sola vez** en una tabla de referencia, podemos validar esa relación al unir.

    Esto evita duplicaciones silenciosas y ayuda a detectar errores de estructura.
    """)
    return


@app.cell
def _(patients, presion_long):
    presion_enriquecida = presion_long.merge(
        patients,
        on="patient_id",
        how="left",
        validate="many_to_one",
    )

    presion_enriquecida.head()
    return (presion_enriquecida,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 5) `transform`: métricas por grupo sin colapsar filas

    `groupby().agg()` produce una tabla agregada.

    Pero a veces queremos calcular métricas **por grupo manteniendo cada fila original**.

    Para eso usamos **`transform`**.

    Esto es útil, por ejemplo, cuando quieres comparar cada observación con el comportamiento típico de su hospital.
    """)
    return


@app.cell
def _(presion_enriquecida):
    presion_enriquecida["media_sbp_hospital"] = (
        presion_enriquecida.groupby("hospital_code")["sbp"].transform("mean")
    )

    presion_enriquecida.head()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto 3

    Crea una columna llamada `z_sbp_hospital` que represente el **z-score de SBP dentro de cada hospital**.

    Es decir, cada observación debe compararse con:

    - la media de su hospital,
    - y la desviación estándar de su hospital.

    La tabla final debe seguir teniendo el mismo número de filas que `presion_enriquecida`.
    """)
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    z_sbp_hospital = None
    return


@app.cell(hide_code=True)
def _():
    tip_content_reto_3 = TipContent(
        items_raw=[
            r"""
    <Paso conceptual>
    Primero necesitas la media y la desviación estándar dentro de cada hospital.

    Luego debes aplicar esas cantidades a cada fila sin colapsar la tabla.
    """,
            r"""
    <Pista operativa>
    `transform` permite devolver una serie con la misma longitud que la tabla original.
    """,
            r"""
    <solucion>

    ```python
    z_sbp_hospital = (
    presion_enriquecida.groupby("hospital_code")["sbp"]
    .transform(lambda x: (x - x.mean()) / x.std())
    )
    ```
    """,
        ]
    )

    tip_content_reto_3.render()
    return


@app.cell(hide_code=True)
def _():
    test_content_reto_3 = TestContent(
        items_raw=[
            r"""
    <Objeto definido>

    ```python
    assert z_sbp_hospital is not None
    print("Serie definida correctamente.")
    ```
    """,
            r"""
    <Longitud correcta>

    ```python
    assert len(z_sbp_hospital) == len(presion_enriquecida)
    print("Longitud correcta.")
    ```
    """,
        ],
        namespace=globals(),
    )

    test_content_reto_3.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 6) Patrón útil en análisis clínico: última medición por paciente

    En datos longitudinales es muy común que cada paciente tenga varias observaciones.

    A veces el análisis no requiere todas, sino solo la **más reciente**.

    Un patrón práctico para resolver esto es:

    1. ordenar por paciente y tiempo,
    2. quedarte con la última fila de cada paciente.

    Este patrón aparece constantemente en cohortes clínicas y estudios observacionales.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto 4 — Última medición por paciente

    A partir de `presion_long`, construye una tabla llamada `ultima_medicion_paciente` que:

    - conserve una sola fila por `patient_id`,
    - represente la medición más reciente según este orden temporal:
      `sbp_baseline` → `sbp_month_1` → `sbp_month_3`,
    - conserve las columnas `patient_id`, `timepoint`, `sbp`,
    - y quede ordenada por `patient_id`.

    Este es uno de los patrones más útiles en análisis longitudinal.
    """)
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    ultima_medicion_paciente = None
    return


@app.cell(hide_code=True)
def _():
    tip_content_reto_4 = TipContent(
        items_raw=[
            r"""
    <Orden temporal explícito>
    Aquí no basta con ordenar alfabéticamente los momentos.

    Necesitas imponer un orden clínico real entre baseline, mes 1 y mes 3.
    """,
            r"""
    <Una fila por paciente>
    Después de ordenar correctamente, debes quedarte con una sola observación por paciente.

    Piensa qué combinación de funciones ya conoces que permite lograr eso.
    """,
            r"""
    <solucion>

    ```python
    ultima_medicion_paciente = (
    presion_long.assign(
        timepoint=pd.Categorical(
            presion_long["timepoint"],
            categories=["sbp_baseline", "sbp_month_1", "sbp_month_3"],
            ordered=True,
        )
    )
    .sort_values(["patient_id", "timepoint"])
    .drop_duplicates(subset="patient_id", keep="last")
    .loc[:, ["patient_id", "timepoint", "sbp"]]
    .sort_values("patient_id")
    .reset_index(drop=True)
    )
    ```
    """,
        ]
    )

    tip_content_reto_4.render()
    return


@app.cell(hide_code=True)
def _():
    test_content_reto_4 = TestContent(
        items_raw=[
            r"""
    <Objeto definido>

    ```python
    assert ultima_medicion_paciente is not None
    print("Tabla definida correctamente.")
    ```
    """,
            r"""
    <Una fila por paciente>

    ```python
    assert ultima_medicion_paciente["patient_id"].is_unique
    print("Una fila por paciente correcta.")
    ```
    """,
            r"""
    <Estructura esperada>

    ```python
    assert list(ultima_medicion_paciente.columns) == ["patient_id", "timepoint", "sbp"]
    assert ultima_medicion_paciente["patient_id"].is_monotonic_increasing
    print("Estructura y orden correctos.")
    ```
    """,
        ],
        namespace=globals(),
    )

    test_content_reto_4.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 7) Otro patrón útil: ranking dentro de hospital

    Además de resumir por grupo, a veces queremos comparar individuos **dentro del mismo grupo**.

    Por ejemplo:

    - ¿qué paciente tiene la SBP más alta dentro de su hospital?
    - ¿quién ocupa el primer, segundo o tercer lugar?

    Para eso podemos construir rankings por grupo.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto 5 — Ranking de SBP dentro de hospital

    A partir de `perfil_paciente_completo`, construye una tabla llamada `ranking_sbp_hospital` que:

    - incluya las columnas:
      `patient_id`, `hospital_name`, `sbp`,
    - agregue una columna `rank_sbp_hospital`,
    - donde el paciente con mayor `sbp` dentro de cada hospital tenga rango `1`,
    - y el resultado final quede ordenado por `hospital_name` y `rank_sbp_hospital`.

    Este patrón es muy útil para priorización clínica y revisión de casos extremos.
    """)
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    ranking_sbp_hospital = None
    return


@app.cell(hide_code=True)
def _():
    tip_content_reto_5 = TipContent(
        items_raw=[
            r"""
    <Ranking por grupo>
    Aquí no quieres un ranking global, sino un ranking separado dentro de cada hospital.

    Eso significa que la operación debe respetar la agrupación.
    """,
            r"""
    <Dirección del ranking>
    Como los valores más altos de SBP deben tener rango 1, el ranking debe construirse en orden descendente.
    """,
            r"""
    <solucion>

    ```python
    ranking_sbp_hospital = (
    perfil_paciente_completo.loc[:, ["patient_id", "hospital_name", "sbp"]]
    .assign(
        rank_sbp_hospital=lambda d: d.groupby("hospital_name")["sbp"].rank(
            method="dense",
            ascending=False,
        )
    )
    .sort_values(["hospital_name", "rank_sbp_hospital", "patient_id"])
    .reset_index(drop=True)
    )
    ```
    """,
        ]
    )

    tip_content_reto_5.render()
    return


@app.cell(hide_code=True)
def _():
    test_content_reto_5 = TestContent(
        items_raw=[
            r"""
    <Objeto definido>

    ```python
    assert ranking_sbp_hospital is not None
    print("Tabla definida correctamente.")
    ```
    """,
            r"""
    <Columna de ranking presente>

    ```python
    assert "rank_sbp_hospital" in ranking_sbp_hospital.columns
    print("Columna de ranking creada correctamente.")
    ```
    """,
            r"""
    <Rangos válidos>

    ```python
    assert (ranking_sbp_hospital["rank_sbp_hospital"] >= 1).all()
    print("Ranking válido.")
    ```
    """,
        ],
        namespace=globals(),
    )

    test_content_reto_5.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Cierre

    En análisis de datos en salud, transformar la estructura de una tabla es parte del razonamiento estadístico, no solo una tarea técnica.

    Una buena práctica de *data wrangling* exige responder siempre tres preguntas:

    1. ¿cuál es la unidad de análisis?
    2. ¿qué estructura facilita la pregunta analítica?
    3. ¿qué transformación preserva mejor el significado clínico o poblacional?

    Cuando esas preguntas están claras, herramientas como `merge`, `concat`, `melt`, `transform`, `drop_duplicates` y `rank` dejan de ser comandos aislados y se convierten en parte de un flujo analítico coherente.
    """)
    return


if __name__ == "__main__":
    app.run()
