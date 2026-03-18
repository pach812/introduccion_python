# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "matplotlib==3.10.8",
#     "numpy==2.4.2",
#     "pandas==3.0.1",
#     "pytest==9.0.2",
#     "requests==2.32.5",
# ]
# ///

import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")

with app.setup(hide_code=True):
    import os

    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import seaborn as sns
    from matplotlib.figure import Figure


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Semana 3 · Lección 6
    ## Métricas estructuradas y outputs formales

    **Propósito de la sesión:** aprender a organizar resultados analíticos de forma reproducible usando:

    - **diccionarios estructurados** para métricas y metadatos,
    - **tablas resumen** construidas con `pandas`,
    - **listas de objetos gráficos** para conservar visualizaciones de forma ordenada.

    En análisis de datos clínicos no basta con calcular números o producir gráficos aislados.

    También es necesario responder una pregunta práctica:

    > **¿Cómo guardo mis resultados de manera clara para poder revisarlos, comunicarlos y reutilizarlos?**

    La idea central de esta lección es pasar de resultados dispersos a **salidas formales y organizadas**.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 1) Dataset de trabajo

    Usaremos un dataset tabular con variables demográficas, clínicas y sociales en población adulta mayor.

    Algunas columnas relevantes para la sesión son:

    - `age`: edad
    - `sex`: sexo
    - `hypertension`: hipertensión reportada
    - `Diabetes`: diabetes reportada
    - `sbp_mmHg`: presión arterial sistólica
    - `glucose_mg_dL`: glucosa
    - `ldl_mg_dL`: colesterol LDL
    - `residence_area`: área de residencia
    - `education_grouped`: nivel educativo agrupado

    Nuestro objetivo será construir salidas que respondan preguntas descriptivas simples en salud pública, por ejemplo:

    - ¿cuántos pacientes hay en la base?,
    - ¿cuál es el perfil etario y clínico general?,
    - ¿qué tablas resumen conviene conservar?,
    - ¿qué visualizaciones deben quedar organizadas como parte del resultado analítico?
    """)
    return


@app.cell
def _():
    candidate_paths = [
        "dataset_clase_semana2_small.csv",
        "./dataset_clase_semana2_small.csv",
        "/mnt/data/dataset_clase_semana2_small.csv",
    ]

    data_path = None
    for path in candidate_paths:
        if os.path.exists(path):
            data_path = path
            break

    assert data_path is not None, "No se encontró el archivo dataset_clase_semana2_small.csv."

    df = pd.read_csv(data_path)

    expected_columns = {
        "age",
        "sex",
        "hypertension",
        "Diabetes",
        "sbp_mmHg",
        "glucose_mg_dL",
        "ldl_mg_dL",
        "residence_area",
        "education_grouped",
    }
    assert expected_columns.issubset(df.columns)

    df.head(10)
    return data_path, df


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 2) Primer principio: una métrica aislada no es todavía un output formal

    En una exploración inicial es normal hacer cálculos sueltos como:

    - media de edad,
    - número de personas con hipertensión,
    - mediana de LDL,
    - proporción de diabetes.

    El problema es que, si estos resultados quedan dispersos en distintas celdas, luego son difíciles de:

    - revisar,
    - reutilizar,
    - comparar,
    - o integrar en un informe analítico.

    Una solución simple y poderosa es usar un **diccionario** para agrupar métricas relacionadas bajo nombres explícitos.
    """)
    return


@app.cell
def _(df):
    overview_metrics = {
        "n_patients": int(df.shape[0]),
        "n_variables": int(df.shape[1]),
        "mean_age": round(float(df["age"].mean()), 2),
        "mean_sbp": round(float(df["sbp_mmHg"].mean()), 2),
        "prop_hypertension": round(float((df["hypertension"] == "Yes").mean()), 4),
        "prop_diabetes": round(float((df["Diabetes"] == "Yes").mean()), 4),
    }

    pd.Series(overview_metrics, name="value")
    return (overview_metrics,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    En este punto ya tenemos una salida más formal:

    - cada métrica tiene una **clave** clara,
    - los valores pueden recuperarse fácilmente,
    - y todo el resumen queda concentrado en un único objeto.

    Esta forma de trabajo mejora la trazabilidad del análisis.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto 1 — Construir un diccionario demográfico mínimo

    **Dominio:** resumen poblacional inicial

    Construye un diccionario llamado `metrics_demography` con exactamente estas claves:

    - `total_patients`
    - `mean_age`
    - `female_count`
    - `male_count`

    Reglas:

    - Usa el dataset `df`.
    - Conserva `mean_age` como número decimal redondeado a 2 cifras.
    - Los conteos deben ser enteros.

    Antes de programar, piensa:

    - qué columna contiene el sexo,
    - qué operación produce un conteo,
    - y cómo asegurar nombres claros para cada métrica.
    """)
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    metrics_demography = None
    return (metrics_demography,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Tips — Mini-reto 1

    **Tip 1.** Un diccionario se construye con pares `clave: valor`.

    **Tip 2.** Para contar categorías de sexo puedes comparar la columna `sex` contra cada valor esperado.

    **Tip 3.** Si quieres un promedio más legible, usa `round(..., 2)`.

    **Solución posible:**

    ```python
    metrics_demography = {
        "total_patients": int(df.shape[0]),
        "mean_age": round(float(df["age"].mean()), 2),
        "female_count": int((df["sex"] == "Female").sum()),
        "male_count": int((df["sex"] == "Male").sum()),
    }
    ```
    """)
    return


@app.cell(hide_code=True)
def _(df, metrics_demography):
    assert metrics_demography is not None, "Debes asignar un diccionario a `metrics_demography`."
    assert isinstance(metrics_demography, dict), "`metrics_demography` debe ser un diccionario."
    assert list(metrics_demography.keys()) == [
        "total_patients",
        "mean_age",
        "female_count",
        "male_count",
    ], "Las claves no coinciden con las solicitadas."
    assert metrics_demography["total_patients"] == int(df.shape[0])
    assert metrics_demography["female_count"] + metrics_demography["male_count"] == int(df.shape[0])

    print("Mini-reto 1: tests superados.")
    pd.Series(metrics_demography, name="value")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 3) Segundo principio: una tabla resumen también es un output formal

    En salud pública, muchas preguntas descriptivas no se responden con un único número sino con una **tabla resumen reproducible**.

    Por ejemplo, puede ser útil guardar una tabla por subgrupos que contenga:

    - tamaño del grupo,
    - edad promedio,
    - presión arterial promedio,
    - proporción de diabetes.

    Este tipo de salida puede construirse con `groupby` + `agg` y quedar lista para inspección o comunicación.
    """)
    return


@app.cell
def _(df):
    summary_by_sex_area = (
        df.groupby(["sex", "residence_area"], as_index=False)
        .agg(
            n_patients=("ID", "count"),
            mean_age=("age", "mean"),
            mean_sbp=("sbp_mmHg", "mean"),
            prop_diabetes=("Diabetes", lambda s: (s == "Yes").mean()),
        )
        .sort_values(["sex", "residence_area"])
    )

    summary_by_sex_area = summary_by_sex_area.assign(
        mean_age=lambda d: d["mean_age"].round(2),
        mean_sbp=lambda d: d["mean_sbp"].round(2),
        prop_diabetes=lambda d: d["prop_diabetes"].round(4),
    )

    summary_by_sex_area
    return (summary_by_sex_area,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Aquí la idea importante es que **no todo output formal debe ser un diccionario**.

    Según la pregunta analítica, puede convenir conservar:

    - diccionarios para métricas globales,
    - DataFrames para resúmenes tabulares,
    - listas para secuencias ordenadas de resultados.

    El formato correcto depende del tipo de salida que se quiere preservar.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 4) Tercer principio: una visualización también puede almacenarse como objeto

    En las lecciones anteriores construiste gráficos con `matplotlib` y `seaborn`.

    Ahora daremos un paso adicional: en lugar de pensar el gráfico solo como algo que “se muestra”, lo trataremos como un **objeto** que puede guardarse dentro de una variable.

    Esto permite:

    - conservar varias figuras en orden,
    - devolverlas como parte del resultado analítico,
    - y separarlas conceptualmente del cálculo de métricas.
    """)
    return


@app.cell
def _(df):
    sns.set_theme(style="whitegrid")

    fig_age, ax_age = plt.subplots(figsize=(6, 4))
    sns.histplot(data=df, x="age", bins=15, ax=ax_age)
    ax_age.set_title("Distribución de edad")
    ax_age.set_xlabel("Edad")
    ax_age.set_ylabel("Frecuencia")

    fig_sbp, ax_sbp = plt.subplots(figsize=(6, 4))
    sns.boxplot(data=df, x="sex", y="sbp_mmHg", ax=ax_sbp)
    ax_sbp.set_title("PAS por sexo")
    ax_sbp.set_xlabel("Sexo")
    ax_sbp.set_ylabel("PAS (mmHg)")

    example_figures = [fig_age, fig_sbp]

    fig_age
    return example_figures, fig_age, fig_sbp


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    En este ejemplo, la lista `example_figures` mantiene una secuencia ordenada de figuras.

    Eso significa que ya podemos concebir una salida formal del análisis como algo del tipo:

    - métricas globales,
    - tablas resumen,
    - y una lista de figuras clínicas.

    La estructura deja de depender de celdas sueltas y se vuelve más explícita.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto 2 — Construir una lista de figuras clínicas

    **Dominio:** visualización descriptiva en salud

    Crea una lista llamada `clinical_figures` que contenga exactamente **2 figuras** en este orden:

    1. una figura con un histograma de `glucose_mg_dL`,
    2. una figura con un boxplot de `ldl_mg_dL` por `hypertension`.

    Reglas:

    - Usa `matplotlib` y `seaborn`.
    - Guarda cada figura en una variable antes de construir la lista.
    - La lista final debe conservar el orden indicado.

    Antes de programar, piensa:

    - qué objeto devuelve `plt.subplots()`,
    - sobre qué eje debe dibujar `seaborn`,
    - y cómo reunir al final ambas figuras dentro de una sola lista.
    """)
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    clinical_figures = None
    return (clinical_figures,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Tips — Mini-reto 2

    **Tip 1.** Cada gráfico debe empezar con `fig, ax = plt.subplots(...)`.

    **Tip 2.** Para el histograma puedes usar `sns.histplot(...)`.

    **Tip 3.** Para el boxplot necesitas una variable categórica en `x` y una numérica en `y`.

    **Solución posible:**

    ```python
    fig_glucose, ax_glucose = plt.subplots(figsize=(6, 4))
    sns.histplot(data=df, x="glucose_mg_dL", bins=15, ax=ax_glucose)
    ax_glucose.set_title("Distribución de glucosa")

    fig_ldl, ax_ldl = plt.subplots(figsize=(6, 4))
    sns.boxplot(data=df, x="hypertension", y="ldl_mg_dL", ax=ax_ldl)
    ax_ldl.set_title("LDL por hipertensión")

    clinical_figures = [fig_glucose, fig_ldl]
    ```
    """)
    return


@app.cell(hide_code=True)
def _(clinical_figures):
    assert clinical_figures is not None, "Debes asignar una lista a `clinical_figures`."
    assert isinstance(clinical_figures, list), "`clinical_figures` debe ser una lista."
    assert len(clinical_figures) == 2, "La lista debe contener exactamente 2 figuras."
    assert all(isinstance(fig, Figure) for fig in clinical_figures), (
        "Cada elemento de `clinical_figures` debe ser un objeto Figure."
    )

    print("Mini-reto 2: tests superados.")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 5) Integración: construir un paquete de resultados

    Cuando un análisis ya tiene varias salidas, conviene reunirlas en una estructura principal.

    Un patrón simple consiste en usar un diccionario superior con secciones como:

    - `metadata`
    - `metrics`
    - `tables`
    - `figures`

    Esto no introduce una librería nueva ni una arquitectura compleja.

    Solo aplica de manera explícita estructuras ya conocidas: **diccionarios, listas y DataFrames**.
    """)
    return


@app.cell
def _(data_path, example_figures, overview_metrics, summary_by_sex_area):
    teacher_bundle = {
        "metadata": {
            "dataset_name": os.path.basename(data_path),
            "analysis_unit": "persona",
        },
        "metrics": overview_metrics,
        "tables": {
            "summary_by_sex_area": summary_by_sex_area,
        },
        "figures": example_figures,
    }

    teacher_bundle.keys()
    return (teacher_bundle,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Observa que este patrón produce una salida mucho más formal que una secuencia de prints o gráficos aislados.

    Ahora todo el análisis puede consultarse por componentes:

    - `teacher_bundle["metrics"]`
    - `teacher_bundle["tables"]`
    - `teacher_bundle["figures"]`

    La ventaja conceptual es que el análisis queda organizado como un conjunto coherente de resultados.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto 3 — Reto final: construir un output analítico completo

    **Dominio:** resumen clínico estructurado

    Construye un diccionario llamado `analysis_output` con exactamente estas claves principales:

    - `metadata`
    - `metrics`
    - `tables`
    - `figures`

    Reglas del reto:

    1. `metadata` debe ser un diccionario con:
       - `dataset_name`
       - `n_rows`

    2. `metrics` debe ser exactamente el diccionario `metrics_demography`.

    3. `tables` debe ser un diccionario con una sola entrada:
       - clave: `summary_by_hypertension`
       - valor: un DataFrame resumen por `hypertension` con las columnas:
         - `hypertension`
         - `n_patients`
         - `mean_age`
         - `mean_sbp`
         - `prop_diabetes`

    4. `figures` debe ser exactamente la lista `clinical_figures`.

    Antes de programar, piensa:

    - qué partes del resultado ya existen y pueden reutilizarse,
    - qué parte nueva debes construir con `groupby` y `agg`,
    - y cómo ensamblar todo en un único diccionario final.
    """)
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    analysis_output = None
    return (analysis_output,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Tips — Mini-reto 3

    **Tip 1.** La tabla nueva debe construirse primero y luego incorporarse al diccionario final.

    **Tip 2.** Para `prop_diabetes`, recuerda que el promedio de una condición booleana funciona como proporción.

    **Tip 3.** `analysis_output` no debe mezclar nombres arbitrarios: debe respetar exactamente la estructura pedida.

    **Solución posible:**

    ```python
    summary_by_hypertension = (
        df.groupby("hypertension", as_index=False)
        .agg(
            n_patients=("ID", "count"),
            mean_age=("age", "mean"),
            mean_sbp=("sbp_mmHg", "mean"),
            prop_diabetes=("Diabetes", lambda s: (s == "Yes").mean()),
        )
        .assign(
            mean_age=lambda d: d["mean_age"].round(2),
            mean_sbp=lambda d: d["mean_sbp"].round(2),
            prop_diabetes=lambda d: d["prop_diabetes"].round(4),
        )
    )

    analysis_output = {
        "metadata": {
            "dataset_name": os.path.basename(data_path),
            "n_rows": int(df.shape[0]),
        },
        "metrics": metrics_demography,
        "tables": {
            "summary_by_hypertension": summary_by_hypertension,
        },
        "figures": clinical_figures,
    }
    ```
    """)
    return


@app.cell(hide_code=True)
def _(analysis_output, clinical_figures, data_path, df, metrics_demography):
    assert analysis_output is not None, "Debes asignar un diccionario a `analysis_output`."
    assert isinstance(analysis_output, dict), "`analysis_output` debe ser un diccionario."
    assert list(analysis_output.keys()) == ["metadata", "metrics", "tables", "figures"], (
        "Las claves principales deben ser: metadata, metrics, tables, figures."
    )

    assert analysis_output["metadata"]["dataset_name"] == os.path.basename(data_path)
    assert analysis_output["metadata"]["n_rows"] == int(df.shape[0])
    assert analysis_output["metrics"] == metrics_demography
    assert analysis_output["figures"] == clinical_figures

    assert "summary_by_hypertension" in analysis_output["tables"], (
        "Dentro de `tables` debe existir la clave `summary_by_hypertension`."
    )

    summary_table = analysis_output["tables"]["summary_by_hypertension"]
    assert isinstance(summary_table, pd.DataFrame), (
        "`summary_by_hypertension` debe ser un DataFrame."
    )
    assert list(summary_table.columns) == [
        "hypertension",
        "n_patients",
        "mean_age",
        "mean_sbp",
        "prop_diabetes",
    ], "Las columnas de la tabla resumen no coinciden con las solicitadas."
    assert summary_table["n_patients"].sum() == df.shape[0]
    assert summary_table["prop_diabetes"].between(0, 1).all()

    print("Mini-reto 3: tests superados.")
    analysis_output["tables"]["summary_by_hypertension"]
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Cierre conceptual

    La idea más importante de esta sesión es que un análisis reproducible no solo calcula métricas: también **organiza sus salidas**.

    En esta lección viste tres formatos centrales:

    - **diccionarios** para métricas y metadatos,
    - **DataFrames** para tablas resumen,
    - **listas** para conservar figuras en orden.

    Cuando estos componentes se integran en una estructura explícita, el resultado analítico se vuelve más fácil de:

    - interpretar,
    - comunicar,
    - revisar,
    - y reutilizar.

    En términos prácticos, pasar de resultados dispersos a outputs formales significa pasar de un análisis improvisado a un análisis mejor organizado.
    """)
    return


if __name__ == "__main__":
    app.run()
