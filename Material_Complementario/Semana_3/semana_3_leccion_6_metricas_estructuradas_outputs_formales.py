# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "matplotlib==3.10.8",
#     "numpy==2.4.2",
#     "pandas==3.0.1",
#     "pytest==9.0.2",
#     "requests==2.32.5",
#     "seaborn==0.13.2",
# ]
# ///

import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")

with app.setup(hide_code=True):
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import seaborn as sns
    import pickle
    import os
    from matplotlib.axes import Axes
    from matplotlib.figure import Figure

    from setup import TipContent, TestContent, find_data_file

    sns.set_theme(style="whitegrid")


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Semana 3 · Lección 6
    ## Métricas estructuradas y outputs formales

    **Propósito de la sesión:** aprender a organizar resultados analíticos de manera formal y reutilizable usando:

    - diccionarios estructurados para métricas,
    - tablas resumen con `pandas`,
    - salidas gráficas organizadas de forma explícita.

    Hasta ahora en la semana 3 trabajaste principalmente dos cosas:

    - cómo construir visualizaciones,
    - y cómo organizar procesos analíticos con mejor diseño.

    En esta lección daremos un paso complementario:

    > pasar de resultados sueltos a **outputs formales**.

    En análisis de datos no basta con calcular una media o producir un gráfico aislado.

    También hay que responder preguntas como:

    - ¿dónde queda guardado el resumen principal?
    - ¿cómo sé qué métricas forman parte del output final?
    - ¿qué tabla sirve como producto reutilizable?
    - ¿cómo organizo las visualizaciones que vale la pena conservar?

    Idea central:

    > **un análisis gana calidad cuando sus resultados quedan estructurados con nombres claros, formatos consistentes y objetos fáciles de reutilizar.**
    """)
    return


@app.cell
def _():
    data_path = find_data_file("public/dataset_clase_semana2_small.csv")
    df = pd.read_csv(data_path)

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    categorical_cols = df.select_dtypes(include="object").columns.tolist()

    assert data_path.exists()
    assert df.shape[0] > 0
    assert set(["age", "sex", "hypertension", "Diabetes"]).issubset(df.columns)

    df.head()
    return categorical_cols, df, numeric_cols


@app.cell(hide_code=True)
def _(df):
    mo.md(f"""
    ## Dataset de trabajo

    Seguiremos trabajando con el mismo dataset clínico de las lecciones anteriores.

    El dataset contiene:

    - **{df.shape[0]} registros**
    - **{df.shape[1]} variables**

    Cada fila representa un individuo con variables demográficas, factores de riesgo y mediciones clínicas.

    En esta sesión nos concentraremos en variables útiles para construir métricas y resúmenes formales:

    - `ID`
    - `age`
    - `sex`
    - `hypertension`
    - `Diabetes`
    - `sbp_mmHg`
    - `glucose_mg_dL`
    - `ldl_mg_dL`
    - `residence_area`
    - `education_grouped`

    La pregunta pedagógica ya no es solo cómo visualizar.

    Ahora es:

    > **cómo organizar resultados para que puedan revisarse, reutilizarse y comunicarse con claridad.**
    """)
    return


@app.cell(hide_code=True)
def _(categorical_cols, df, numeric_cols):
    summary_numeric = df[numeric_cols].describe().round(2)
    summary_categorical = pd.DataFrame(
        {
            "variable": categorical_cols,
            "n_unique": [df[col].nunique(dropna=False) for col in categorical_cols],
            "missing": [int(df[col].isna().sum()) for col in categorical_cols],
        }
    )

    mo.vstack(
        [
            mo.md("### Resumen numérico"),
            summary_numeric,
            mo.md("### Resumen categórico"),
            summary_categorical,
        ]
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 1) Primer principio: una métrica aislada todavía no es un output formal

    En una exploración inicial es muy común calcular valores sueltos como:

    - media de edad,
    - proporción de hipertensión,
    - mediana de glucosa,
    - número total de pacientes.

    El problema es que, si esos resultados quedan repartidos en distintas celdas o variables sin estructura, luego son difíciles de:

    - revisar,
    - comparar,
    - exportar,
    - o integrar a un informe.

    Una solución simple es agrupar métricas relacionadas dentro de un **diccionario**.

    Eso permite que cada resultado tenga:

    - un nombre explícito,
    - un valor asociado,
    - y una posición clara dentro del output.
    """)
    return


@app.cell
def _(df):
    overview_metrics = {
        "n_patients": int(df.shape[0]),
        "n_variables": int(df.shape[1]),
        "mean_age": round(float(df["age"].mean()), 2),
        "mean_sbp": round(float(df["sbp_mmHg"].mean()), 2),
        "prop_hypertension": round(float(df["hypertension"].eq("Yes").mean()), 4),
        "prop_diabetes": round(float(df["Diabetes"].eq("Yes").mean()), 4),
    }

    pd.Series(overview_metrics, name="value")
    return (overview_metrics,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    En este punto ya tenemos una salida más formal:

    - cada métrica tiene una **clave** clara,
    - los valores pueden recuperarse fácilmente,
    - y el resumen queda concentrado en un único objeto.

    Idea clave:

    > **nombrar bien las métricas es parte del análisis, no un detalle cosmético.**
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto 1 — Diccionario clínico básico

    Construye un diccionario llamado `metrics_clinical` con exactamente estas claves:

    - `total_patients`
    - `mean_glucose`
    - `mean_ldl`
    - `hypertension_count`

    Reglas:

    - usa el dataset `df`,
    - redondea las medias a 2 cifras decimales,
    - el conteo debe ser entero.

    Piensa en este objeto como un **output mínimo de perfil clínico general**.
    """)
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    metrics_clinical = None
    return (metrics_clinical,)


@app.cell(hide_code=True)
def _():
    _tip_content = TipContent(
        items_raw=[
            r"""
    <Idea>
    Un diccionario agrupa resultados bajo nombres explícitos.
    """,
            r"""
    <Cálculos>
    Las medias salen de columnas numéricas y el conteo puede construirse con una comparación booleana.
    """,
            r"""
    <Formato>
    Usa `round(..., 2)` para medias y `int(...)` para conteos.
    """,
            r"""
    <solucion>
    ```python
    metrics_clinical = {
    "total_patients": int(df.shape[0]),
    "mean_glucose": round(float(df["glucose_mg_dL"].mean()), 2),
    "mean_ldl": round(float(df["ldl_mg_dL"].mean()), 2),
    "hypertension_count": int(df["hypertension"].eq("Yes").sum()),
    }
    ```
    """,
        ]
    )
    _tip_content.render()
    return


@app.cell(hide_code=True)
def _(metrics_clinical):
    _test_content = TestContent(
        items_raw=[
            r"""
    <Existencia>
    ```python
    assert metrics_clinical is not None
    assert isinstance(metrics_clinical, dict)
    print("El output existe y es un diccionario.")
    ```
    """,
            r"""
    <Claves esperadas>
    ```python
    assert list(metrics_clinical.keys()) == [
    "total_patients",
    "mean_glucose",
    "mean_ldl",
    "hypertension_count",
    ]
    print("Las claves son correctas.")
    ```
    """,
            r"""
    <Valores básicos>
    ```python
    assert metrics_clinical["total_patients"] == int(df.shape[0])
    assert metrics_clinical["hypertension_count"] == int(df["hypertension"].eq("Yes").sum())
    print("Los valores básicos son consistentes.")
    ```
    """,
        ],
        namespace=globals(),
    )

    if metrics_clinical is not None:
        pd.Series(metrics_clinical, name="value")
    _test_content.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 2) Segundo principio: una tabla resumen también es un output formal

    Muchas preguntas no se responden con un solo número, sino con una tabla reutilizable.

    Por ejemplo, puede ser útil conservar una tabla por subgrupos que incluya:

    - tamaño del grupo,
    - edad promedio,
    - PAS promedio,
    - proporción de diabetes.

    Una tabla resumen bien nombrada puede funcionar como:

    - base para un gráfico,
    - insumo para un reporte,
    - evidencia analítica intermedia,
    - o salida final en sí misma.
    """)
    return


@app.cell
def _(df):
    summary_by_sex = (
        df.assign(diabetes_flag=lambda d: d["Diabetes"].eq("Yes"))
        .groupby("sex", as_index=False)
        .agg(
            n_people=("ID", "count"),
            mean_age=("age", "mean"),
            mean_sbp=("sbp_mmHg", "mean"),
            prop_diabetes=("diabetes_flag", "mean"),
        )
        .round(2)
        .sort_values("sex")
    )

    summary_by_sex
    return (summary_by_sex,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Esta tabla ya es un output formal porque:

    - tiene una unidad de agregación clara,
    - cada columna representa una métrica interpretable,
    - y puede reutilizarse directamente en otra etapa del análisis.

    Idea clave:

    > **una buena tabla resumen no es un borrador; puede ser un producto analítico legítimo.**
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto 2 — Tabla resumen por residencia

    Construye una tabla llamada `summary_by_residence` que agrupe por `residence_area` y calcule:

    - `n_people`
    - `mean_age`
    - `mean_glucose`
    - `prop_high_cholesterol`

    Reglas:

    - crea primero una bandera booleana de colesterol alto,
    - ordena la tabla por `residence_area`,
    - redondea a 2 cifras decimales.

    Esta tabla debe quedar lista para ser reutilizada en un gráfico posterior.
    """)
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    summary_by_residence = None
    return (summary_by_residence,)


@app.cell(hide_code=True)
def _():
    _tip_content = TipContent(
        items_raw=[
            r"""
    <Preparación>
    Antes del `groupby`, crea una bandera booleana que identifique colesterol alto.
    """,
            r"""
    <Resumen>
    La proporción de una bandera booleana se obtiene con la media.
    """,
            r"""
    <Orden>
    Usa `.sort_values(...)` al final para dejar la salida estable.
    """,
            r"""
    <solucion>
    ```python
    summary_by_residence = (
    df.assign(high_cholesterol_flag=lambda d: d["high_cholesterol"].eq("Yes"))
    .groupby("residence_area", as_index=False)
    .agg(
        n_people=("ID", "count"),
        mean_age=("age", "mean"),
        mean_glucose=("glucose_mg_dL", "mean"),
        prop_high_cholesterol=("high_cholesterol_flag", "mean"),
    )
    .round(2)
    .sort_values("residence_area")
    )
    ```
    """,
        ]
    )
    _tip_content.render()
    return


@app.cell(hide_code=True)
def _(summary_by_residence):
    _test_content = TestContent(
        items_raw=[
            r"""
    <Existencia>
    ```python
    assert summary_by_residence is not None
    assert isinstance(summary_by_residence, pd.DataFrame)
    print("La tabla resumen existe.")
    ```
    """,
            r"""
    <Columnas esperadas>
    ```python
    assert list(summary_by_residence.columns) == [
    "residence_area",
    "n_people",
    "mean_age",
    "mean_glucose",
    "prop_high_cholesterol",
    ]
    print("Las columnas son correctas.")
    ```
    """,
            r"""
    <Rango válido>
    ```python
    assert summary_by_residence["prop_high_cholesterol"].between(0, 1).all()
    print("Las proporciones están en rango válido.")
    ```
    """,
        ],
        namespace=globals(),
    )

    if summary_by_residence is not None:
        summary_by_residence
    _test_content.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 3) Tercer principio: un gráfico útil también puede formar parte del output formal

    En sesiones previas el foco estaba en construir buenas visualizaciones.

    Aquí la pregunta cambia un poco:

    > ¿qué visualizaciones vale la pena conservar como parte explícita del resultado?

    Una forma simple de hacerlo es guardar objetos gráficos dentro de una estructura organizada.

    Por ejemplo, una lista de figuras o ejes puede servir para:

    - revisar outputs al final,
    - devolver varios gráficos desde una función,
    - o mantener una colección visual asociada a un análisis.
    """)
    return


@app.cell
def _(df):
    figures_overview = []

    fig_age, ax_age = plt.subplots(figsize=(6.5, 4))
    sns.histplot(data=df, x="age", bins=15, ax=ax_age)
    ax_age.set_title("Distribución de edad")
    ax_age.set_xlabel("Edad")
    ax_age.set_ylabel("Frecuencia")
    fig_age.tight_layout()
    figures_overview.append(fig_age)

    fig_sbp, ax_sbp = plt.subplots(figsize=(6.5, 4))
    sns.boxplot(data=df, x="sex", y="sbp_mmHg", ax=ax_sbp)
    ax_sbp.set_title("PAS por sexo")
    ax_sbp.set_xlabel("Sexo")
    ax_sbp.set_ylabel("PAS (mmHg)")
    fig_sbp.tight_layout()
    figures_overview.append(fig_sbp)

    figures_overview[0], figures_overview[1]
    return (figures_overview,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    La estructura anterior no guarda solo imágenes “porque sí”.

    Guarda objetos que representan outputs visuales con sentido analítico.

    Idea clave:

    > **un output formal puede ser numérico, tabular o gráfico; lo importante es que quede organizado y recuperable.**
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto 3 — Lista formal de gráficos

    Construye una lista llamada `figures_clinical` que contenga exactamente dos figuras, en este orden:

    1. un histograma de `glucose_mg_dL`,
    2. un boxplot de `ldl_mg_dL` por `sex`.

    Requisitos:

    - cada gráfico debe tener título,
    - ambos deben quedar guardados como objetos `Figure`,
    - la lista final debe contener solo esas dos figuras.

    Piensa este ejercicio como una versión mínima de un output visual organizado.
    """)
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    figures_clinical = None
    return (figures_clinical,)


@app.cell(hide_code=True)
def _():
    _tip_content = TipContent(
        items_raw=[
            r"""
    <Estructura>
    Empieza creando una lista vacía y luego agrega cada figura con `.append(...)`.
    """,
            r"""
    <Primera figura>
    Necesitas un histograma de glucosa.
    """,
            r"""
    <Segunda figura>
    Necesitas un boxplot de LDL por sexo.
    """,
            r"""
    <solucion>
    ```python
    figures_clinical = []

    fig_glucose, ax_glucose = plt.subplots(figsize=(6.5, 4))
    sns.histplot(data=df, x="glucose_mg_dL", bins=15, ax=ax_glucose)
    ax_glucose.set_title("Distribución de glucosa")
    ax_glucose.set_xlabel("Glucosa (mg/dL)")
    ax_glucose.set_ylabel("Frecuencia")
    fig_glucose.tight_layout()
    figures_clinical.append(fig_glucose)

    fig_ldl, ax_ldl = plt.subplots(figsize=(6.5, 4))
    sns.boxplot(data=df, x="sex", y="ldl_mg_dL", ax=ax_ldl)
    ax_ldl.set_title("LDL por sexo")
    ax_ldl.set_xlabel("Sexo")
    ax_ldl.set_ylabel("LDL (mg/dL)")
    fig_ldl.tight_layout()
    figures_clinical.append(fig_ldl)
    ```
    """,
        ]
    )
    _tip_content.render()
    return


@app.cell(hide_code=True)
def _(figures_clinical):
    _test_content = TestContent(
        items_raw=[
            r"""
    <Existencia>
    ```python
    assert figures_clinical is not None
    assert isinstance(figures_clinical, list)
    print("La colección visual existe.")
    ```
    """,
            r"""
    <Longitud>
    ```python
    assert len(figures_clinical) == 2
    print("La lista contiene exactamente dos figuras.")
    ```
    """,
            r"""
    <Tipos correctos>
    ```python
    assert all(isinstance(fig, Figure) for fig in figures_clinical)
    print("Todos los elementos son figuras.")
    ```
    """,
        ],
        namespace=globals(),
    )

    if figures_clinical is not None and len(figures_clinical) == 2:
        figures_clinical[0], figures_clinical[1]
    _test_content.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 4) Unificar outputs: una estructura compuesta

    Cuando un análisis empieza a consolidarse, conviene agrupar sus salidas principales dentro de una sola estructura.

    Una posibilidad simple es un diccionario maestro con entradas como:

    - `metrics`
    - `tables`
    - `figures`

    Eso permite dejar explícito:

    - qué resultados forman parte del análisis,
    - dónde está cada tipo de output,
    - y cómo recuperarlo después.
    """)
    return


@app.cell
def _(figures_overview, overview_metrics, summary_by_sex):
    analysis_outputs = {
        "metrics": overview_metrics,
        "tables": {
            "summary_by_sex": summary_by_sex,
        },
        "figures": figures_overview,
    }

    analysis_outputs["metrics"], analysis_outputs["tables"]["summary_by_sex"]
    return (analysis_outputs,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto final — Construir un output maestro

    Construye un diccionario llamado `final_outputs` con esta estructura:

    - clave `"metrics"` → debe contener `metrics_clinical`
    - clave `"tables"` → debe contener otro diccionario con una clave `"residence"` que apunte a `summary_by_residence`
    - clave `"figures"` → debe apuntar a `figures_clinical`

    Este ejercicio resume toda la lógica de la lección:

    - producir métricas,
    - producir tablas,
    - producir gráficos,
    - y organizarlos dentro de una sola salida formal.
    """)
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    final_outputs = None
    return (final_outputs,)


@app.cell(hide_code=True)
def _():
    _tip_content = TipContent(
        items_raw=[
            r"""
    <Estructura general>
    Aquí necesitas un diccionario principal que contenga tres claves de primer nivel.
    """,
            r"""
    <Tabla anidada>
    Dentro de `"tables"` necesitas otro diccionario.
    """,
            r"""
    <Referencia>
    No recalcules objetos; reutiliza los outputs ya construidos.
    """,
            r"""
    <solucion>
    ```python
    final_outputs = {
    "metrics": metrics_clinical,
    "tables": {
        "residence": summary_by_residence,
    },
    "figures": figures_clinical,
    }
    ```
    """,
        ]
    )
    _tip_content.render()
    return


@app.cell(hide_code=True)
def _(final_outputs):
    _test_content = TestContent(
        items_raw=[
            r"""
    <Existencia>
    ```python
    assert final_outputs is not None
    assert isinstance(final_outputs, dict)
    print("El output maestro existe.")
    ```
    """,
            r"""
    <Claves principales>
    ```python
    assert set(final_outputs.keys()) == {"metrics", "tables", "figures"}
    print("Las claves principales son correctas.")
    ```
    """,
            r"""
    <Estructura interna>
    ```python
    assert isinstance(final_outputs["metrics"], dict)
    assert isinstance(final_outputs["tables"], dict)
    assert "residence" in final_outputs["tables"]
    assert isinstance(final_outputs["figures"], list)
    print("La estructura interna es válida.")
    ```
    """,
        ],
        namespace=globals(),
    )

    if final_outputs is not None:
        final_outputs
    _test_content.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 5) De output formal a output persistente

    Hasta aquí organizaste el análisis dentro de una estructura clara:

    - métricas en diccionarios,
    - tablas en `DataFrame`,
    - figuras como objetos de Matplotlib,
    - y un output maestro que reúne todo.

    El siguiente paso es decidir **cómo conservar cada resultado** según su uso posterior.

    Antes de guardar, conviene distinguir tres preguntas:

    1. ¿qué resultado quiero volver a cargar dentro de Python?
    2. ¿qué resultado quiero compartir como tabla?
    3. ¿qué resultado quiero exportar como figura para un informe o presentación?

    No todos los outputs se guardan del mismo modo, porque no todos cumplen la misma función.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 5.1) Elegir el formato según el propósito

    Un mismo análisis puede producir varios tipos de salida, pero cada una responde a una necesidad distinta.

    ### Cuando quieres conservar el objeto completo del análisis

    Conviene usar un formato que preserve la estructura de Python.

    Esto permite recuperar después:

    - diccionarios,
    - tablas,
    - listas,
    - y otros objetos compuestos.

    ### Cuando quieres compartir una tabla

    Conviene usar formatos tabulares intercambiables, por ejemplo:

    - CSV,
    - Excel,
    - Stata,
    - Parquet.

    Aquí el objetivo no es preservar toda la estructura del análisis, sino dejar una tabla legible y reutilizable.

    ### Cuando quieres comunicar una visualización

    Conviene exportar la figura como archivo gráfico, por ejemplo:

    - PNG para uso general,
    - PDF cuando interesa una salida de alta calidad para documento o informe.

    La elección del formato debe ser coherente con el uso esperado del output.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 5.2) Guardar el output maestro como objeto de Python

    Si quieres recuperar más adelante la estructura completa del análisis, una opción simple es usar `pickle`.

    Esto resulta útil cuando el interés principal es:

    - reabrir el análisis en Python,
    - inspeccionar nuevamente el diccionario maestro,
    - o continuar una etapa posterior sin reconstruir todos los objetos.

    En este caso, el objeto que conviene guardar es el **output maestro**, porque allí ya quedó organizada la salida principal del análisis.
    """)
    return


@app.cell
def _(analysis_outputs):
    os.makedirs("./outputs", exist_ok=True)

    pickle_path = "./outputs/final_outputs.pkl"

    # Crear una versión serializable del output
    final_outputs_pickle = {
        "metrics": analysis_outputs["metrics"],
        "tables": analysis_outputs["tables"],
    }

    # Guardar el diccionario sin figuras
    with open(pickle_path, "wb") as f:
        pickle.dump(final_outputs_pickle, f)

    assert os.path.exists(pickle_path)

    pickle_path
    return (pickle_path,)


@app.cell(hide_code=True)
def _(pickle_path):
    mo.md(rf"""
    El output maestro quedó guardado en:

    ```text
    {pickle_path}
    ```

    Este archivo permite recuperar posteriormente la estructura completa del análisis dentro de Python.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 5.3) Recuperar el objeto guardado

    Guardar un objeto tiene valor real solo si después puede recuperarse de forma consistente.

    Por eso conviene comprobar inmediatamente que el archivo creado puede volver a cargarse.

    Esta verificación funciona como una validación mínima de persistencia.
    """)
    return


@app.cell
def _(pickle_path):
    # Cargar archivo pickle correctamente
    with open(pickle_path, "rb") as _f:
        reloaded_outputs = pickle.load(_f)

    # Validaciones
    assert isinstance(reloaded_outputs, dict)
    assert set(reloaded_outputs.keys()) == {"metrics", "tables"}

    # Acceso a métricas
    reloaded_outputs["metrics"]
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 5.4) Guardar tablas como outputs compartibles

    Cuando el interés no está en reabrir toda la estructura en Python, sino en **compartir una tabla**, conviene exportar el `DataFrame` en formatos tabulares.

    Aquí ya no estamos pensando en persistencia interna del análisis, sino en circulación del resultado.

    Una misma tabla puede necesitar distintos formatos según el contexto:

    - **CSV** si buscas interoperabilidad simple,
    - **Excel** si la tabla será revisada o comentada manualmente,
    - **Stata** si el output irá a un flujo estadístico clásico,
    - **Parquet** si interesa almacenamiento más eficiente y reutilización computacional.

    El tipo de archivo también forma parte del diseño del output.
    """)
    return


@app.cell
def _(summary_by_residence):
    table_export_paths = {}
    try: 
        table_export_paths["csv"] = "outputs/summary_by_residence.csv"
        summary_by_residence.to_csv(table_export_paths["csv"], index=False)
    
        table_export_paths["excel"] = "outputs/summary_by_residence.xlsx"
        summary_by_residence.to_excel(table_export_paths["excel"], index=False)
    
        table_export_paths["stata"] = "outputs/summary_by_residence.dta"
        summary_by_residence.to_stata(table_export_paths["stata"], write_index=False)
    
        table_export_paths["parquet"] = "outputs/summary_by_residence.parquet"
        summary_by_residence.to_parquet(table_export_paths["parquet"], index=False)
    
        assert all(os.path.exists(path) for path in table_export_paths.values())
    
        pd.Series(table_export_paths, name="path")
    except Exception as e:
        print(f"Error al exportar tablas: {e}")
    return (table_export_paths,)


@app.cell(hide_code=True)
def _(table_export_paths):
    mo.md(rf"""
    La misma tabla puede quedar disponible en varios formatos.

    Esto permite adaptar la salida a distintos contextos de uso sin modificar su contenido analítico.

    {table_export_paths["csv"]}
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 5.5) Guardar figuras como productos comunicables

    Las figuras cumplen una función distinta a la de las tablas.

    No suelen guardarse para volver a manipularlas como tablas, sino para:

    - incluirlas en un informe,
    - insertarlas en una presentación,
    - compartirlas como producto visual,
    - o documentar una salida analítica seleccionada.

    En este caso, la pregunta central es:

    **¿cómo dejar esta visualización disponible para comunicación posterior?**
    """)
    return


@app.cell
def _(figures_clinical):
    figure_export_paths = {}
    try: 
        first_figure = figures_clinical[0]
    
        figure_export_paths["png"] = "outputs/glucose_distribution.png"
        first_figure.savefig(figure_export_paths["png"], dpi=300, bbox_inches="tight")
    
        figure_export_paths["pdf"] = "outputs/glucose_distribution.pdf"
        first_figure.savefig(figure_export_paths["pdf"], bbox_inches="tight")
    
        assert all(os.path.exists(path) for path in figure_export_paths.values())
    
        pd.Series(figure_export_paths, name="path")
    except Exception as e:
        print(f"Error al exportar figuras: {e}")
    return (figure_export_paths,)


@app.cell(hide_code=True)
def _(figure_export_paths):
    mo.md(r"""
    Aquí se exportó una figura en dos formatos porque los contextos de uso pueden ser distintos.

    - **PNG** suele ser práctico para presentaciones o documentos breves.
    - **PDF** suele ser útil cuando se desea una salida estable para informe o impresión.
    """)
    mo.md(
        f"""
    ```python
    {figure_export_paths}
    ```
    """
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 5.6) Resumen de persistencia del análisis

    A esta altura ya no tienes solo resultados calculados.

    Tienes además una estrategia mínima de persistencia organizada en tres niveles:

    - el **objeto maestro** para reabrir el análisis como estructura de Python,
    - la **tabla resumen** para compartir un output tabular,
    - la **figura exportada** para comunicación visual.

    Esta secuencia resume un recorrido completo:

    **producir → organizar → guardar**
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto de cierre — Diseñar un plan de exportación

    Construye un diccionario llamado `export_plan` con exactamente estas claves:

    - `python_object`
    - `table_share_format`
    - `figure_report_format`

    Reglas:

    - cada valor debe ser un texto breve,
    - `python_object` debe indicar qué objeto conviene guardar para continuar el análisis en Python,
    - `table_share_format` debe indicar un formato adecuado para compartir la tabla resumen,
    - `figure_report_format` debe indicar un formato adecuado para incluir una figura en un informe.

    Este ejercicio evalúa si lograste distinguir correctamente **qué tipo de output conviene preservar y en qué formato**.
    """)
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    export_plan = None
    return (export_plan,)


@app.cell(hide_code=True)
def _():
    _tip_content = TipContent(
        items_raw=[
            r"""
    <Propósito>
    No todas las salidas cumplen la misma función.
    Primero decide qué quieres reabrir en Python, qué quieres compartir como tabla y qué quieres usar como figura final.
    """,
            r"""
    <Objeto de Python>
    Para continuar el análisis más adelante, conviene guardar la estructura que reúne los outputs principales.
    """,
            r"""
    <Formatos>
    Piensa en un formato tabular para compartir datos y en un formato gráfico apropiado para un informe.
    """,
            r"""
    <solucion>
    ```python
    export_plan = {
    "python_object": "final_outputs",
    "table_share_format": "csv",
    "figure_report_format": "pdf",
    }
    ```
    """,
        ]
    )
    _tip_content.render()
    return


@app.cell(hide_code=True)
def _(export_plan):
    _test_content = TestContent(
        items_raw=[
            r"""
    <Existencia>
    ```python
    assert export_plan is not None
    assert isinstance(export_plan, dict)
    print("El plan de exportación existe.")
    ```
    """,
            r"""
    <Claves esperadas>
    ```python
    assert list(export_plan.keys()) == [
    "python_object",
    "table_share_format",
    "figure_report_format",
    ]
    print("Las claves del plan son correctas.")
    ```
    """,
            r"""
    <Tipos de salida>
    ```python
    assert all(isinstance(value, str) for value in export_plan.values())
    print("Todos los valores están expresados como texto.")
    ```
    """,
        ],
        namespace=globals(),
    )

    if export_plan is not None:
        pd.Series(export_plan, name="decision")
    _test_content.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 6) Cierre conceptual

    El recorrido de esta sesión puede resumirse así:

    1. producir métricas, tablas y figuras,
    2. organizarlas dentro de un output maestro,
    3. distinguir qué tipo de resultado necesita cada forma de guardado,
    4. y dejar persistencia explícita de las salidas principales.

    Esto permite pasar de una lógica de análisis disperso a una lógica de outputs formales.

    La idea central que conviene retener es la siguiente:

    > **un buen output no solo se calcula bien; también queda nombrado, organizado y guardado de forma coherente con su uso posterior.**
    """)
    return


if __name__ == "__main__":
    app.run()
