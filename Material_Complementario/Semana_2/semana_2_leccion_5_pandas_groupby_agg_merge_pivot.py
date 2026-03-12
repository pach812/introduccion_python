# /// script
# requires-python = ">=3.14"
# dependencies = [
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
    from setup import TipContent, TestContent


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Semana 2 · Lección 5
    ## Métodos avanzados de agrupación y resumen en pandas

    **Propósito de la sesión:** aprender a construir resúmenes descriptivos reproducibles a partir de datos clínicos tabulares usando cuatro herramientas centrales de pandas:

    - `groupby` para segmentar datos en subgrupos
    - `agg` para calcular varias métricas por grupo
    - `merge` para enriquecer tablas con información adicional
    - `pivot_table` para construir tablas resumen tipo matriz

    ### Regla de oro de la sesión

    Antes de resumir una tabla, conviene definir tres cosas:

    1. **unidad de análisis**
       Por ejemplo: paciente, visita, prueba de laboratorio.

    2. **variables de estratificación**
       Por ejemplo: sexo, hospital, condición, región.

    3. **métrica de interés**
       Por ejemplo: conteo, promedio, mediana, proporción.

    A lo largo de la lección seguiremos esta secuencia conceptual:

    **datos → agrupar → resumir → interpretar**
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 1) Dataset de ejemplo: visitas ambulatorias

    Trabajaremos con un dataset sintético de **visitas ambulatorias**.

    Cada fila representa una visita de un paciente, no un paciente único.

    Las variables del dataset son:

    - `patient_id`: identificador del paciente
    - `visit_id`: identificador único de la visita
    - `hospital`: institución donde ocurrió la visita
    - `sex`: sexo reportado
    - `age`: edad en años
    - `condition`: condición principal de la visita
    - `sbp`: presión arterial sistólica
    - `ldl`: colesterol LDL
    - `days_to_next`: días hasta la siguiente visita

    ### Objetivo analítico

    Construir resúmenes por hospital, sexo, condición o región para describir:

    - volumen de visitas,
    - perfil clínico,
    - y posibles señales de severidad o seguimiento.
    """)
    return


@app.cell
def _():
    rng = np.random.default_rng(20260228)

    n_patients = 180
    visits_per_patient = rng.integers(1, 6, size=n_patients)
    patient_ids = np.arange(1, n_patients + 1)

    hospitals = np.array(["HOSP_A", "HOSP_B", "HOSP_C"])
    conditions = np.array(["HTA", "T2D", "EPOC", "ASMA"])
    sexes = np.array(["female", "male"])

    rows = []
    visit_counter = 1

    for pid, k in zip(patient_ids, visits_per_patient):
        sex = rng.choice(sexes, p=[0.55, 0.45])
        age = int(rng.normal(loc=52, scale=16))
        age = int(np.clip(age, 18, 90))
        hospital = rng.choice(hospitals, p=[0.4, 0.35, 0.25])

        for _ in range(int(k)):
            condition = rng.choice(conditions, p=[0.35, 0.30, 0.20, 0.15])

            # Simplificación didáctica:
            # la "severidad" se refleja en distribuciones distintas de PAS y LDL
            base_sbp = {"HTA": 145, "T2D": 135, "EPOC": 128, "ASMA": 124}[condition]
            sbp = float(rng.normal(loc=base_sbp, scale=12))

            base_ldl = {"HTA": 125, "T2D": 135, "EPOC": 120, "ASMA": 118}[condition]
            ldl = float(rng.normal(loc=base_ldl, scale=22))

            days_to_next = int(np.clip(rng.gamma(shape=2.2, scale=18), 1, 180))

            rows.append(
                {
                    "patient_id": int(pid),
                    "visit_id": int(visit_counter),
                    "hospital": hospital,
                    "sex": sex,
                    "age": age,
                    "condition": condition,
                    "sbp": round(sbp, 1),
                    "ldl": round(ldl, 1),
                    "days_to_next": int(days_to_next),
                }
            )
            visit_counter += 1

    visits = pd.DataFrame(rows)

    # Validaciones mínimas del dataset
    assert visits["patient_id"].nunique() == n_patients
    assert visits["visit_id"].is_unique
    assert set(visits["sex"].unique()).issubset({"female", "male"})
    assert visits["age"].between(18, 90).all()

    visits.head(10)
    return (visits,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 2) `groupby`: segmentar la tabla en subgrupos

    `groupby` puede leerse así:

    > “separo la tabla por una o más columnas y luego calculo un resumen dentro de cada grupo”.

    Ejemplos típicos en salud:

    - promedio de PAS por sexo,
    - conteo de visitas por hospital,
    - promedio de LDL por condición,
    - seguimiento medio por región.

    La idea central es que primero defines **cómo partir la tabla**, y después **qué resumen calcular dentro de cada parte**.
    """)
    return


@app.cell
def _(visits):
    visits_by_sex = (
        visits.groupby("sex", as_index=False)
        .agg(
            n_visits=("visit_id", "count"),
            mean_sbp=("sbp", "mean"),
            mean_ldl=("ldl", "mean"),
        )
        .sort_values("sex")
    )

    assert visits_by_sex.shape[0] == 2

    visits_by_sex
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    En este ejemplo, cada fila del resultado representa un sexo, y las columnas resumen lo que ocurre dentro de ese grupo.

    Observa que `groupby` no produce por sí solo el resumen final.

    Para eso necesitamos una segunda parte: **definir qué métricas queremos calcular**.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto 1 — PAS promedio por hospital

    **Dominio:** servicios de salud / resumen institucional

    En este primer reto vas a construir un resumen por hospital.

    La meta es producir una tabla en la que cada fila represente una institución y las columnas contengan métricas descriptivas simples.

    Este ejercicio busca reforzar dos ideas:

    - cómo agrupar una tabla por una variable categórica,
    - y cómo calcular varias métricas dentro de cada grupo.

    Antes de programar, piensa:

    - qué variable define los grupos,
    - qué columna sirve para contar visitas,
    - y qué columnas deben resumirse con promedio o extremos.
    """)
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    # TODO: construir el resumen pedido
    summary_hospital = None
    return (summary_hospital,)


@app.cell(hide_code=True)
def _():
    _tip_content = TipContent(
        items_raw=[
            r"""
    <Variable de agrupación>
    El resultado debe tener una fila por institución.

    Piensa cuál columna define naturalmente esos grupos.
    """,
            r"""
    <Múltiples métricas>
    Necesitas construir varias columnas resumen al mismo tiempo.

    Revisa cómo `agg` permite asignar nombres nuevos a distintas métricas calculadas sobre columnas específicas.
    """,
            r"""
    <Formato del resultado>
    Conviene mantener la variable de agrupación como columna explícita y no como índice.

    También puede ser útil ordenar el resultado para que quede más estable y legible.
    """,
            r"""
    <solucion>

    ```python
    summary_hospital = (
        visits.groupby("hospital", as_index=False)
        .agg(
            n_visits=("visit_id", "count"),
            mean_sbp=("sbp", "mean"),
            min_age=("age", "min"),
            max_age=("age", "max"),
        )
        .sort_values("hospital")
    )
    ```
    """,
        ]
    )

    _tip_content.render()
    return


@app.cell(hide_code=True)
def _(summary_hospital):
    _test_content = TestContent(
        items_raw=[
            r"""
    <Existencia del resultado>
    Verifica que `summary_hospital` haya sido definido.

    ```python
    assert summary_hospital is not None, (
        "Debes asignar un DataFrame a `summary_hospital`."
    )
    print("Objeto definido correctamente.")
    ```
    """,
            r"""
    <Columnas esperadas>
    Verifica que el resultado tenga exactamente las columnas pedidas.

    ```python
    assert list(summary_hospital.columns) == [
        "hospital",
        "n_visits",
        "mean_sbp",
        "min_age",
        "max_age",
    ], (
        "Las columnas esperadas son: hospital, n_visits, mean_sbp, min_age, max_age."
    )
    print("Columnas correctas.")
    ```
    """,
            r"""
    <Una fila por hospital>
    Verifica que el resumen tenga una sola fila por institución.

    ```python
    assert summary_hospital["hospital"].nunique() == summary_hospital.shape[0], (
        "Debe haber exactamente una fila por hospital."
    )
    print("Estructura por hospital correcta.")
    ```
    """,
            r"""
    <Conteo total consistente>
    Verifica que la suma de visitas por hospital coincida con el total de filas del dataset original.

    ```python
    assert summary_hospital["n_visits"].sum() == visits.shape[0], (
        "La suma de `n_visits` debe coincidir con el número total de visitas."
    )
    print("Conteo total consistente.")
    ```
    """,
        ],
        namespace=globals(),
    )

    summary_hospital
    _test_content.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 3) `agg`: varias métricas por grupo

    En un análisis descriptivo real, rara vez basta con una sola métrica.

    Con frecuencia queremos combinar en un mismo reporte:

    - tamaño muestral,
    - media o mediana,
    - medidas extremas,
    - proporciones,
    - y otras métricas derivadas.

    `agg` permite declarar explícitamente:

    - qué columna resumir,
    - qué función aplicar,
    - y cómo llamar la nueva columna en la tabla final.
    """)
    return


@app.cell
def _(visits):
    def prop_high_sbp(s: pd.Series) -> float:
        # Proporción de visitas con PAS elevada
        return float((s >= 140).mean())

    report_condition_sex = (
        visits.groupby(["condition", "sex"], as_index=False)
        .agg(
            n_visits=("visit_id", "count"),
            mean_age=("age", "mean"),
            median_sbp=("sbp", "median"),
            prop_high_sbp=("sbp", prop_high_sbp),
            mean_ldl=("ldl", "mean"),
        )
        .sort_values(["condition", "sex"])
    )

    report_condition_sex.head(12)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 4) `pivot_table`: resúmenes tipo matriz

    `pivot_table` es útil cuando quieres organizar un resumen con dos ejes visibles:

    - filas = una dimensión
    - columnas = otra dimensión
    - celdas = una métrica

    Esto se parece mucho a una tabla resumen de Excel.

    En salud pública, este tipo de estructura aparece en preguntas como:

    - cuántos casos hay por hospital y condición,
    - cuál es el promedio de una medición por institución y sexo,
    - cómo se distribuye una métrica entre dos dimensiones categóricas.
    """)
    return


@app.cell
def _(visits):
    pivot_counts = pd.pivot_table(
        visits,
        index="hospital",
        columns="condition",
        values="visit_id",
        aggfunc="count",
        fill_value=0,
        margins=True,
        margins_name="TOTAL",
    )

    assert "TOTAL" in pivot_counts.index
    assert "TOTAL" in pivot_counts.columns

    pivot_counts
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto 2 — PAS promedio por hospital y sexo

    **Dominio:** estructura tabular / comparación entre subgrupos

    En este reto construirás una tabla resumen con dos ejes:

    - hospitales en las filas,
    - sexo en las columnas,
    - y el promedio de PAS dentro de cada subgrupo.

    Este ejercicio busca reforzar:

    - cómo definir filas y columnas en una tabla pivote,
    - qué variable debe resumirse,
    - y cómo hacer el resultado más legible.

    Antes de programar, piensa:

    - qué dimensión irá en el índice,
    - qué dimensión irá en las columnas,
    - y qué métrica debe ocupar las celdas.
    """)
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    # TODO: construir la tabla pivote pedida
    pivot_sbp = None
    return (pivot_sbp,)


@app.cell(hide_code=True)
def _():
    _tip_content = TipContent(
        items_raw=[
            r"""
    <Estructura de la tabla>
    Una tabla pivote se define separando claramente qué variable irá por filas y cuál por columnas.

    Aquí necesitas una dimensión institucional y una dimensión demográfica.
    """,
            r"""
    <Métrica en las celdas>
    Las celdas no deben contener conteos, sino una medida resumen de una variable clínica.

    Revisa cuál es la columna a resumir y qué función de agregación corresponde.
    """,
            r"""
    <Presentación del resultado>
    Después de construir la tabla, puede ser útil redondear para facilitar la lectura.

    Hazlo sin cambiar la estructura principal de la tabla.
    """,
            r"""
    <solucion>

    ```python
    pivot_sbp = pd.pivot_table(
        visits,
        index="hospital",
        columns="sex",
        values="sbp",
        aggfunc="mean",
    ).round(1)
    ```
    """,
        ]
    )

    _tip_content.render()
    return


@app.cell(hide_code=True)
def _(pivot_sbp):
    _test_content = TestContent(
        items_raw=[
            r"""
    <Existencia del resultado>
    Verifica que `pivot_sbp` haya sido definido.

    ```python
    assert pivot_sbp is not None, "Debes asignar una tabla a `pivot_sbp`."
    print("Objeto definido correctamente.")
    ```
    """,
            r"""
    <Índice correcto>
    Verifica que el índice represente hospitales.

    ```python
    assert pivot_sbp.index.name == "hospital", (
        "El índice debe llamarse `hospital`."
    )
    print("Índice correcto.")
    ```
    """,
            r"""
    <Columnas esperadas>
    Verifica que las columnas correspondan a categorías de sexo.

    ```python
    assert set(pivot_sbp.columns).issubset({"female", "male"}), (
        "Las columnas esperadas son `female` y/o `male`."
    )
    print("Columnas correctas.")
    ```
    """,
            r"""
    <Tipo de resumen>
    Verifica que el resultado mantenga estructura tabular.

    ```python
    assert hasattr(pivot_sbp, "loc"), (
        "`pivot_sbp` debe comportarse como un DataFrame."
    )
    print("Estructura tabular correcta.")
    ```
    """,
        ],
        namespace=globals(),
    )

    pivot_sbp
    _test_content.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 5) `merge`: enriquecer una tabla con metadatos

    En muchos análisis de servicios de salud, la información está separada en varias tablas.

    Por ejemplo:

    - una tabla de visitas o eventos,
    - y otra tabla con metadatos de las instituciones.

    `merge` permite unir ambas usando una llave común, como `hospital`.

    La utilidad de esto es que, una vez enriquecida la tabla principal, podemos resumir por variables nuevas que antes no estaban disponibles, como:

    - región,
    - nivel de complejidad,
    - tipo de institución.
    """)
    return


@app.cell
def _():
    hospitales_meta = pd.DataFrame(
        {
            "hospital": ["HOSP_A", "HOSP_B", "HOSP_C"],
            "region": ["Urbana", "Urbana", "Rural"],
            "level": ["Alta complejidad", "Media complejidad", "Baja complejidad"],
        }
    )

    assert hospitales_meta["hospital"].is_unique

    hospitales_meta
    return (hospitales_meta,)


@app.cell
def _(hospitales_meta, visits):
    # Unimos visitas con metadatos institucionales
    visits_enriched = visits.merge(hospitales_meta, on="hospital", how="left")

    assert visits_enriched.shape[0] == visits.shape[0]
    assert visits_enriched["region"].isna().sum() == 0

    visits_enriched.head(10)
    return (visits_enriched,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 6) Caso aplicado: seguimiento temprano por región y condición

    Una vez enriquecida la tabla, podemos derivar indicadores nuevos y luego resumirlos.

    Definiremos un indicador simple de ejemplo:

    - **seguimiento temprano** = próxima visita en 30 días o menos

    Después estimaremos su proporción por:

    - región,
    - condición.

    Observa la secuencia:

    1. crear una bandera booleana,
    2. agrupar por subgrupos,
    3. resumir con conteo y proporción.
    """)
    return


@app.cell
def _(visits_enriched):
    visits_flags = visits_enriched.assign(
        early_follow_up=lambda d: d["days_to_next"] <= 30
    )

    followup_by_region_condition = (
        visits_flags.groupby(["region", "condition"], as_index=False)
        .agg(
            n_visits=("visit_id", "count"),
            prop_early_follow_up=("early_follow_up", "mean"),
        )
        .sort_values(["region", "condition"])
    )

    assert followup_by_region_condition["prop_early_follow_up"].between(0, 1).all()

    followup_by_region_condition
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto 3 — Riesgo alto por región con `merge` + `groupby`

    **Dominio:** servicios de salud / priorización poblacional

    En este reto final integrarás varias ideas de la sesión en una sola secuencia de trabajo.

    Ya dispones de `visits_enriched`, es decir, una tabla de visitas que ya fue enriquecida con metadatos institucionales.

    Debes definir una bandera de **alto riesgo cardiometabólico** usando un criterio simple y luego resumirla por región.

    Este ejercicio integra:

    - derivación de una variable booleana,
    - agrupación por subgrupo,
    - cálculo de proporciones,
    - y ordenamiento del resultado para priorización.

    Antes de programar, piensa:

    - qué condición lógica define alto riesgo,
    - cómo crear esa nueva columna sin modificar manualmente fila por fila,
    - y qué métricas resumen deben quedar finalmente por región.
    """)
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    # TODO: construir el resumen final pedido
    risk_by_region = None
    return (risk_by_region,)


@app.cell(hide_code=True)
def _():
    _tip_content = TipContent(
        items_raw=[
            r"""
    <Bandera booleana>
    El primer paso no es agrupar, sino derivar una variable nueva que identifique alto riesgo.

    Esa variable debe construirse combinando dos condiciones clínicas con un operador lógico.
    """,
            r"""
    <De la bandera al resumen>
    Una vez creada la nueva columna, debes agrupar por región y calcular varias métricas.

    Recuerda que el promedio de una columna booleana puede interpretarse como proporción.
    """,
            r"""
    <Orden del resultado>
    El resultado final debe ayudar a priorizar regiones con mayor carga de riesgo.

    Por eso conviene ordenar por la proporción calculada, de mayor a menor.
    """,
            r"""
    <solucion>

    ```python
    risk_by_region = (
        visits_enriched.assign(
            high_risk=lambda d: (d["sbp"] >= 140) | (d["ldl"] >= 160)
        )
        .groupby("region", as_index=False)
        .agg(
            n_visits=("visit_id", "count"),
            prop_high_risk=("high_risk", "mean"),
            mean_age=("age", "mean"),
        )
        .sort_values("prop_high_risk", ascending=False)
    )
    ```
    """,
        ]
    )

    _tip_content.render()
    return


@app.cell(hide_code=True)
def _(risk_by_region):
    _test_content = TestContent(
        items_raw=[
            r"""
    <Existencia del resultado>
    Verifica que `risk_by_region` haya sido definido.

    ```python
    assert risk_by_region is not None, (
        "Debes asignar un DataFrame a `risk_by_region`."
    )
    print("Objeto definido correctamente.")
    ```
    """,
            r"""
    <Columnas esperadas>
    Verifica que el resultado tenga exactamente las columnas solicitadas.

    ```python
    assert list(risk_by_region.columns) == [
        "region",
        "n_visits",
        "prop_high_risk",
        "mean_age",
    ], (
        "Las columnas esperadas son: region, n_visits, prop_high_risk, mean_age."
    )
    print("Columnas correctas.")
    ```
    """,
            r"""
    <Rango de proporciones>
    Verifica que la proporción se mantenga entre 0 y 1.

    ```python
    assert risk_by_region["prop_high_risk"].between(0, 1).all(), (
        "`prop_high_risk` debe estar entre 0 y 1."
    )
    print("Rango de proporciones correcto.")
    ```
    """,
            r"""
    <Consistencia del conteo>
    Verifica que la suma de visitas por región coincida con el total del dataset enriquecido.

    ```python
    assert risk_by_region["n_visits"].sum() == visits_enriched.shape[0], (
        "La suma de `n_visits` debe coincidir con el total de visitas."
    )
    print("Conteo total consistente.")
    ```
    """,
        ],
        namespace=globals(),
    )

    risk_by_region
    _test_content.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Cierre conceptual

    En análisis tabular en salud, estas operaciones forman el núcleo de muchos reportes descriptivos reproducibles:

    - `groupby` define los **estratos** o subgrupos,
    - `agg` define las **métricas** por estrato,
    - `pivot_table` organiza comparaciones en forma de matriz,
    - `merge` integra contexto adicional antes del resumen.

    La idea más importante de esta sesión es que resumir bien no significa solo “calcular números”.

    También implica decidir con claridad:

    - qué unidad estás resumiendo,
    - qué grupos quieres comparar,
    - y qué métrica responde realmente a tu pregunta analítica.
    """)
    return


if __name__ == "__main__":
    app.run()
