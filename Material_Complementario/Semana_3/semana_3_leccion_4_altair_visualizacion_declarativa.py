# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "altair==6.0.0",
#     "matplotlib==3.10.8",
#     "numpy==2.4.2",
#     "pandas==3.0.1",
#     "pytest==9.0.2",
#     "requests==2.32.5",
#     "typing-extensions==4.15.0",
# ]
# ///

import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")

with app.setup(hide_code=True):
    import marimo as mo
    import altair as alt
    import numpy as np
    import pandas as pd
    from matplotlib.figure import Figure

    from setup import TipContent, TestContent, find_data_file


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Semana 3 · Lección 4
    ## Visualización declarativa con Altair

    **Propósito de la sesión:** aprender a construir visualizaciones declarativas con Altair para comunicar relaciones, comparaciones y patrones matriciales usando una gramática explícita basada en datos, marcas y canales visuales.

    Esta lección funciona como cierre del bloque de visualización de la semana 3.

    La progresión hasta aquí ha sido:

    - **Lección 2:** construir gráficos de forma imperativa con Matplotlib,
    - **Lección 3:** representar relaciones estadísticas con Seaborn,
    - **Lección 4:** expresar la lógica visual con una sintaxis declarativa en Altair.

    Aquí el cambio conceptual es importante:

    > en lugar de describir el dibujo paso a paso, declaramos **qué variables ocupan qué canales visuales**.

    Eso hace especialmente útil a Altair cuando queremos:

    - transformar una tabla resumida en un gráfico claro,
    - mantener una gramática consistente,
    - trabajar con tooltips y paneles múltiples,
    - construir visualizaciones compactas y expresivas con poco código mecánico.

    Idea central:

    > **Altair no dibuja primero y piensa después; primero exige pensar la estructura de la relación que quieres comunicar.**
    """)
    return


@app.cell(hide_code=True)
def _():
    data_path = find_data_file("public/dataset_clase_semana2_small.csv")
    df = pd.read_csv(data_path)

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    categorical_cols = df.select_dtypes(include="object").columns.tolist()

    assert data_path.exists()
    assert df.shape[0] > 0
    assert set(numeric_cols).issubset(df.columns)

    df.head()
    return categorical_cols, df, numeric_cols


@app.cell(hide_code=True)
def _(df):
    mo.md(f"""
    ## Dataset de trabajo

    Mantendremos el mismo dataset clínico de las lecciones anteriores para que el cambio principal sea el **lenguaje de visualización** y no el contexto analítico.

    El dataset contiene:

    - **{df.shape[0]} registros**
    - **{df.shape[1]} variables**

    Cada fila representa un individuo e incluye variables demográficas, factores de riesgo y mediciones clínicas.

    Variables que usaremos con mayor frecuencia:

    - `age`
    - `sbp_mmHg`
    - `glucose_mg_dL`
    - `ldl_mg_dL`
    - `sex`
    - `hypertension`
    - `Diabetes`
    - `bmi_category`
    - `education_grouped`

    Igual que antes, el objetivo no es “graficar por graficar”.

    El objetivo es construir una visualización coherente con preguntas como:

    - ¿qué grupo tiene mayor proporción?
    - ¿cómo cambia un promedio entre categorías?
    - ¿qué patrón aparece en una matriz de grupos?
    - ¿cuándo conviene dividir la comparación en paneles?
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
    ## 1) Gramática declarativa: datos, marca, encoding y propiedades

    En Altair, un gráfico suele construirse a partir de cuatro piezas principales:

    ### Datos

    La tabla que quieres representar.

    ### Marca

    La forma geométrica principal del gráfico.

    Ejemplos:

    - `mark_bar()`
    - `mark_line()`
    - `mark_circle()`
    - `mark_rect()`

    ### Encodings

    La asignación entre variables y canales visuales.

    Ejemplos frecuentes:

    - eje x,
    - eje y,
    - color,
    - tooltip,
    - faceta.

    ### Propiedades

    Ajustes generales como:

    - título,
    - ancho,
    - alto.

    Idea clave:

    > **en Altair, un gráfico es la combinación entre una tabla, una marca y una asignación explícita de variables a canales visuales.**
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 2) Primer patrón: barras para proporciones observadas

    Empezaremos con una pregunta sencilla:

    > ¿cómo cambia la proporción observada de hipertensión entre categorías de sexo?

    La lógica analítica será:

    1. convertir la variable en una bandera booleana,
    2. resumir por grupo,
    3. declarar el gráfico con una barra.

    Igual que en Seaborn o Matplotlib, el pensamiento analítico ocurre antes del gráfico.

    Altair recibe mejor una tabla ya clara y resumida.
    """)
    return


@app.cell
def _(df):
    # Construcción de indicador
    # - assign: crea una nueva columna
    # - eq("Yes"): convierte a booleano (True si hay hipertensión)
    hypertension_by_sex = (
        df.assign(
            hypertension_flag=lambda d: d["hypertension"].eq("Yes")
        )

        # Agrupación por sexo
        # - as_index=False: mantiene formato tabular
        .groupby("sex", as_index=False)

        # Agregaciones
        .agg(
            # Conteo total de personas
            n_people=("ID", "count"),

            # Proporción de hipertensión
            # - mean sobre booleanos → proporción (True=1, False=0)
            prop_hypertension=("hypertension_flag", "mean"),
        )
    )

    # Conversión a porcentaje
    # - escala 0–100
    # - round(1): una cifra decimal para presentación
    hypertension_by_sex["prop_hypertension_pct"] = (
        hypertension_by_sex["prop_hypertension"] * 100
    ).round(1)

    # Resultado final
    hypertension_by_sex
    return (hypertension_by_sex,)


@app.cell
def _(hypertension_by_sex):
    # Crear gráfico con Altair
    # - Chart: define el dataset de entrada
    # - mark_bar: tipo de visualización (barras)
    chart_hypertension_by_sex = (
        alt.Chart(hypertension_by_sex)
        .mark_bar()

        # Codificación de variables
        .encode(
            # Eje X (categórico)
            # - :N indica variable nominal
            x=alt.X("sex:N", title="Sexo"),

            # Eje Y (cuantitativo)
            # - :Q indica variable numérica
            # - scale: fija dominio 0–100 para interpretación como porcentaje
            y=alt.Y(
                "prop_hypertension_pct:Q",
                title="Hipertensión (%)",
                scale=alt.Scale(domain=[0, 70]),
            ),

            # Color por grupo
            # - refuerza diferenciación visual
            color=alt.Color("sex:N", title="Sexo"),

            # Tooltips interactivos
            # - muestran detalles al pasar el cursor
            tooltip=[
                alt.Tooltip("sex:N", title="Sexo"),
                alt.Tooltip("n_people:Q", title="N", format=",.0f"),
                alt.Tooltip(
                    "prop_hypertension_pct:Q",
                    title="Hipertensión (%)",
                    format=".1f",
                ),
            ],
        )

        # Propiedades del gráfico
        # - title: título general
        # - width / height: dimensiones
        .properties(
            title="Proporción de hipertensión por sexo",
            width=420,
            height=320,
        )
    )

    # Mostrar gráfico
    chart_hypertension_by_sex
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 3) Lectura conceptual del gráfico de barras

    Este gráfico ya muestra algo importante de la lógica declarativa.

    No dijimos:

    - dibuja una barra aquí,
    - ahora otra aquí,
    - colorea esta de cierto modo.

    Dijimos:

    - usa una marca de barra,
    - coloca `sex` en x,
    - coloca `prop_hypertension_pct` en y,
    - usa color según `sex`,
    - muestra información adicional en `tooltip`.

    Idea clave:

    > **Altair se apoya en una especificación del gráfico, no en una secuencia manual de dibujo.**
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto 1 — Barras para diabetes por sexo

    Construye un gráfico declarativo llamado `chart_diabetes_by_sex`.

    ### Objetivo analítico

    Comparar el **porcentaje de diabetes** entre categorías de sexo.

    ### Requisitos

    1. crea primero una tabla llamada `diabetes_by_sex`,
    2. usa una barra (`mark_bar()`),
    3. coloca `sex` en el eje x,
    4. coloca el porcentaje en el eje y,
    5. incluye `tooltip`,
    6. asigna el resultado final a `chart_diabetes_by_sex`.

    **Variables esperadas:**

    - `diabetes_by_sex`
    - `chart_diabetes_by_sex`
    """)
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    diabetes_by_sex = None
    chart_diabetes_by_sex = None
    return chart_diabetes_by_sex, diabetes_by_sex


@app.cell(hide_code=True)
def _():
    _tip_content = TipContent(
        items_raw=[
            r"""
            <Transformación>
            Convierte `Diabetes` en una bandera booleana usando `.eq("Yes")`.
            """,
            r"""
            <Resumen>
            El promedio de una variable booleana puede interpretarse como proporción.
            """,
            r"""
            <Porcentaje>
            Multiplica por 100 antes de graficar para que el eje sea más interpretable.
            """,
            r"""
            <solucion>
            ```python
            diabetes_by_sex = (
                df.assign(diabetes_flag=lambda d: d["Diabetes"].eq("Yes"))
                .groupby("sex", as_index=False)
                .agg(
                    n_people=("ID", "count"),
                    prop_diabetes=("diabetes_flag", "mean"),
                )
            )

            diabetes_by_sex["prop_diabetes_pct"] = (
                diabetes_by_sex["prop_diabetes"] * 100
            ).round(1)

            chart_diabetes_by_sex = (
                alt.Chart(diabetes_by_sex)
                .mark_bar()
                .encode(
                    x=alt.X("sex:N", title="Sexo"),
                    y=alt.Y("prop_diabetes_pct:Q", title="Diabetes (%)"),
                    color=alt.Color("sex:N", title="Sexo"),
                    tooltip=[
                        alt.Tooltip("sex:N", title="Sexo"),
                        alt.Tooltip("n_people:Q", title="N", format=",.0f"),
                        alt.Tooltip("prop_diabetes_pct:Q", title="Diabetes (%)", format=".1f"),
                    ],
                )
                .properties(
                    title="Proporción de diabetes por sexo",
                    width=420,
                    height=320,
                )
            )
            ```
            """,
        ]
    )
    _tip_content.render()
    return


@app.cell(hide_code=True)
def _(chart_diabetes_by_sex, diabetes_by_sex):
    _test_content = TestContent(
        items_raw=[
            r"""
            <Existencia>
            ```python
    assert diabetes_by_sex is not None
    assert chart_diabetes_by_sex is not None
            ```
            """,
            r"""
            <Columnas esperadas>
            ```python
    assert list(diabetes_by_sex.columns) == [
                "sex",
                "n_people",
                "prop_diabetes",
                "prop_diabetes_pct",
            ]
            ```
            """,
            r"""
            <Objeto Altair>
            ```python
    assert hasattr(chart_diabetes_by_sex, "to_dict")
            spec = chart_diabetes_by_sex.to_dict()
    assert spec["mark"]["type"] == "bar"
    assert spec["encoding"]["x"]["field"] == "sex"
    assert spec["encoding"]["y"]["field"] == "prop_diabetes_pct"
            ```
            """,
        ],
        namespace=globals(),
    )

    if diabetes_by_sex is not None:
        diabetes_by_sex
    if chart_diabetes_by_sex is not None:
        chart_diabetes_by_sex
    _test_content.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 4) Segunda marca nueva: `mark_line()` para evolución resumida

    Otra pregunta frecuente es:

    > ¿cómo cambia un promedio a través de una variable ordenada?

    Aquí construiremos una línea para representar la PAS media por grupo de edad.

    Igual que antes, la línea no surge directamente del dataset crudo.

    Primero necesitamos una tabla resumida y ordenada.
    """)
    return


@app.cell
def _(df):
    # Crear grupos de edad
    # - pd.cut: discretiza variable continua en intervalos
    # - bins: define límites de los grupos
    # - right=False: intervalos incluyen el límite izquierdo [ )
    # - labels: nombres legibles para cada grupo
    age_groups = pd.cut(
        df["age"],
        bins=[40, 50, 60, 70, 80, np.inf],
        right=False,
        labels=["40-49", "50-59", "60-69", "70-79", "80+"],
    )

    # Agregación por grupo de edad
    # - assign: añade columna age_group
    # - dropna: elimina filas sin edad o PAS
    # - groupby: agrupa por categoría
    # - mean: calcula promedio de PAS
    sbp_by_age_group = (
        df.assign(age_group=age_groups)
        .dropna(subset=["age_group", "sbp_mmHg"])
        .groupby("age_group", as_index=False)
        .agg(mean_sbp=("sbp_mmHg", "mean"))
    )

    # Formato de salida
    # - astype(str): convierte categorías a texto (útil para visualización)
    # - round(1): redondea a 1 decimal
    sbp_by_age_group["age_group"] = sbp_by_age_group["age_group"].astype(str)
    sbp_by_age_group["mean_sbp"] = sbp_by_age_group["mean_sbp"].round(1)

    # Resultado final
    sbp_by_age_group
    return (sbp_by_age_group,)


@app.cell
def _(sbp_by_age_group):
    # Crear gráfico de línea con Altair
    # - mark_line(point=True): línea + puntos en cada categoría
    chart_line_sbp = (
        alt.Chart(sbp_by_age_group)
        .mark_line(point=True)

        # Codificación de variables
        .encode(
            # Eje X (categórico ordenado)
            # - sort: define orden lógico de los grupos de edad
            x=alt.X(
                "age_group:N",
                title="Grupo de edad",
                sort=["40-49", "50-59", "60-69", "70-79", "80+"],
            ),

            # Eje Y (cuantitativo)
            # - valores promedio de PAS
            y=alt.Y(
                "mean_sbp:Q",
                title="PAS media (mmHg)"
            ),

            # Tooltips interactivos
            # - muestran valores exactos al pasar el cursor
            tooltip=[
                alt.Tooltip("age_group:N", title="Grupo de edad"),
                alt.Tooltip(
                    "mean_sbp:Q",
                    title="PAS media",
                    format=".1f"
                ),
            ],
        )

        # Propiedades del gráfico
        .properties(
            title="PAS media por grupo de edad",
            width=420,
            height=320,
        )
    )

    # Mostrar gráfico
    chart_line_sbp
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 5) Nueva visualización del módulo final: heatmaps con `mark_rect()`

    Hasta ahora ya usaste barras, líneas, histogramas, boxplots y scatter plots en lecciones anteriores.

    Aquí introduciremos una visualización nueva para esta secuencia:

    > **heatmaps**

    Un heatmap es útil cuando queremos mostrar una magnitud resumen en una matriz de categorías.

    Pregunta de ejemplo:

    > ¿cómo cambia la PAS media según categoría de IMC y estado de diabetes?

    En Altair, el heatmap no es una función especial aislada.

    Se construye declarando:

    - una marca rectangular,
    - una categoría en x,
    - una categoría en y,
    - una variable cuantitativa en color.
    """)
    return


@app.cell
def _(df):
    # Agregación para heatmap
    # - groupby: combina dos variables categóricas (IMC y diabetes)
    # - as_index=False: mantiene formato tabular
    heatmap_table = (
        df.groupby(["bmi_category", "Diabetes"], as_index=False)

            # Agregación
            # - mean: calcula la PAS promedio en cada combinación de grupos
            .agg(mean_sbp=("sbp_mmHg", "mean"))

            # Redondeo
            # - mejora legibilidad para visualización
            .round({"mean_sbp": 1})
    )

    # Resultado final
    heatmap_table
    return (heatmap_table,)


@app.cell
def _(heatmap_table):
    # Crear heatmap con Altair
    # - mark_rect: representa cada celda como un rectángulo coloreado
    chart_heatmap_sbp = (
        alt.Chart(heatmap_table)
        .mark_rect()

        # Codificación de variables
        .encode(
            # Eje X (categórico)
            # - estado de diabetes
            x=alt.X("Diabetes:N", title="Diabetes"),

            # Eje Y (categórico)
            # - categorías de IMC
            y=alt.Y("bmi_category:N", title="Categoría de IMC"),

            # Color (variable cuantitativa)
            # - intensidad representa la PAS media
            color=alt.Color(
                "mean_sbp:Q",
                title="PAS media (mmHg)"
            ),

            # Tooltips interactivos
            # - muestran detalle por celda
            tooltip=[
                alt.Tooltip("bmi_category:N", title="IMC"),
                alt.Tooltip("Diabetes:N", title="Diabetes"),
                alt.Tooltip(
                    "mean_sbp:Q",
                    title="PAS media",
                    format=".1f"
                ),
            ],
        )

        # Propiedades del gráfico
        .properties(
            title="PAS media por IMC y diabetes",
            width=260,
            height=450,
        )
    )

    # Mostrar gráfico
    chart_heatmap_sbp
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 6) Capa adicional útil en heatmaps: texto sobre celdas

    Un heatmap comunica mucho por color, pero a veces conviene mostrar también el valor numérico dentro de cada celda.

    En Altair esto puede hacerse superponiendo una capa de texto.

    Esa es una idea importante del enfoque declarativo:

    > **los gráficos pueden componerse sumando especificaciones compatibles.**
    """)
    return


@app.cell
def _(heatmap_table):
    # Base común
    # - define ejes compartidos para múltiples capas
    base_heatmap = alt.Chart(heatmap_table).encode(
        x=alt.X("Diabetes:N", title="Diabetes"),
        y=alt.Y("bmi_category:N", title="Categoría de IMC"),
    )

    # Capa de rectángulos (heatmap)
    # - mark_rect: cada celda representa una combinación de grupos
    # - color: intensidad según PAS media
    # - scale: esquema de color continuo (blues)
    heat_rect = base_heatmap.mark_rect().encode(
        color=alt.Color(
            "mean_sbp:Q",
            title="PAS media (mmHg)",
            scale=alt.Scale(scheme="blues"),
        )
    )

    # Capa de texto
    # - mark_text: añade etiquetas dentro de cada celda
    # - text: muestra valor numérico formateado
    # - color condicional:
    #   - blanco si PAS ≥ 130 (mejor contraste en fondos oscuros)
    #   - negro en caso contrario
    heat_text = base_heatmap.mark_text(
        baseline="middle"
    ).encode(
        text=alt.Text("mean_sbp:Q", format=".1f"),
        color=alt.condition(
            alt.datum.mean_sbp >= 130,
            alt.value("white"),
            alt.value("black"),
        ),
    )

    # Composición final
    # - suma de capas: heat_rect + heat_text
    # - properties: título y tamaño del gráfico
    chart_heatmap_text = (
        (heat_rect + heat_text)
        .properties(
            title="PAS media por IMC y diabetes con etiquetas",
            width=360,
            height=250,
        )
    )

    # Mostrar gráfico
    chart_heatmap_text
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto 2 — Heatmap de LDL por educación y colesterol alto

    Construye un heatmap llamado `chart_heatmap_ldl`.

    ### Objetivo analítico

    Visualizar el **LDL promedio** según:

    - `education_grouped`
    - `high_cholesterol`

    ### Requisitos

    1. crea primero una tabla llamada `heatmap_ldl_table`,
    2. usa `mark_rect()`,
    3. coloca `high_cholesterol` en x,
    4. coloca `education_grouped` en y,
    5. coloca el LDL promedio en color,
    6. agrega `tooltip`,
    7. asigna el resultado a `chart_heatmap_ldl`.

    **Variables esperadas:**

    - `heatmap_ldl_table`
    - `chart_heatmap_ldl`
    """)
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    heatmap_ldl_table = None
    chart_heatmap_ldl = None
    return chart_heatmap_ldl, heatmap_ldl_table


@app.cell(hide_code=True)
def _():
    _tip_content = TipContent(
        items_raw=[
            r"""
            <Tabla previa>
            Resume primero con `groupby` y `agg`; el gráfico no debe calcular la tabla por ti en este ejercicio.
            """,
            r"""
            <Variable cuantitativa>
            La variable resumen aquí es `ldl_mg_dL`.
            """,
            r"""
            <Marca correcta>
            Un heatmap en Altair se construye con `mark_rect()`.
            """,
            r"""
            <solucion>
            ```python
            heatmap_ldl_table = (
                df.groupby(["education_grouped", "high_cholesterol"], as_index=False)
                .agg(mean_ldl=("ldl_mg_dL", "mean"))
                .round({"mean_ldl": 1})
            )

            chart_heatmap_ldl = (
                alt.Chart(heatmap_ldl_table)
                .mark_rect()
                .encode(
                    x=alt.X("high_cholesterol:N", title="Colesterol alto"),
                    y=alt.Y("education_grouped:N", title="Educación"),
                    color=alt.Color("mean_ldl:Q", title="LDL medio (mg/dL)"),
                    tooltip=[
                        alt.Tooltip("education_grouped:N", title="Educación"),
                        alt.Tooltip("high_cholesterol:N", title="Colesterol alto"),
                        alt.Tooltip("mean_ldl:Q", title="LDL medio", format=".1f"),
                    ],
                )
                .properties(
                    title="LDL medio por educación y colesterol alto",
                    width=360,
                    height=250,
                )
            )
            ```
            """,
        ]
    )
    _tip_content.render()
    return


@app.cell(hide_code=True)
def _(chart_heatmap_ldl, heatmap_ldl_table):
    _test_content = TestContent(
        items_raw=[
            r"""
            <Existencia>
            ```python
    assert heatmap_ldl_table is not None
    assert chart_heatmap_ldl is not None
            ```
            """,
            r"""
            <Columnas esperadas>
            ```python
    assert list(heatmap_ldl_table.columns) == [
                "education_grouped",
                "high_cholesterol",
                "mean_ldl",
            ]
            ```
            """,
            r"""
            <Especificación>
            ```python
            spec = chart_heatmap_ldl.to_dict()
    assert spec["mark"]["type"] == "rect"
    assert spec["encoding"]["x"]["field"] == "high_cholesterol"
    assert spec["encoding"]["y"]["field"] == "education_grouped"
    assert spec["encoding"]["color"]["field"] == "mean_ldl"
            ```
            """,
        ],
        namespace=globals(),
    )

    if heatmap_ldl_table is not None:
        heatmap_ldl_table
    if chart_heatmap_ldl is not None:
        chart_heatmap_ldl
    _test_content.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 7) Otra capacidad útil: scatter declarativo con color y tooltip

    Altair también puede expresar relaciones entre variables numéricas, igual que Seaborn.

    La diferencia está en el estilo de especificación y en la facilidad para añadir `tooltip` de forma natural.

    Aquí construiremos un scatter plot con una tercera variable categórica en color.
    """)
    return


@app.cell
def _(df):
    # Scatter plot con Altair
    # - mark_circle: puntos con tamaño y transparencia definidos
    chart_scatter_altair = (
        alt.Chart(df)
        .mark_circle(
            size=70,     # tamaño de los puntos
            opacity=0.6  # transparencia para manejar solapamiento
        )

        # Codificación de variables
        .encode(
            # Eje X (cuantitativo)
            x=alt.X("sbp_mmHg:Q", title="PAS (mmHg)"),

            # Eje Y (cuantitativo)
            y=alt.Y("glucose_mg_dL:Q", title="Glucosa (mg/dL)"),

            # Color por grupo
            # - permite identificar patrones según diabetes
            color=alt.Color("Diabetes:N", title="Diabetes"),

            # Tooltips interactivos
            # - muestran información individual por punto
            tooltip=[
                alt.Tooltip("ID:Q", title="ID"),
                alt.Tooltip("sex:N", title="Sexo"),
                alt.Tooltip("sbp_mmHg:Q", title="PAS", format=".1f"),
                alt.Tooltip("glucose_mg_dL:Q", title="Glucosa", format=".1f"),
                alt.Tooltip("Diabetes:N", title="Diabetes"),
            ],
        )

        # Propiedades del gráfico
        .properties(
            title="Relación entre PAS y glucosa según diabetes",
            width=420,
            height=320,
        )
    )

    # Mostrar gráfico
    chart_scatter_altair
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 8) Paneles múltiples declarativos: faceting

    En las lecciones anteriores ya trabajaste facets como idea.

    En Altair también es posible faceteando una variable categórica.

    Esto resulta útil cuando:

    - una sola figura acumula demasiadas capas,
    - quieres comparar el mismo patrón en subgrupos,
    - quieres mantener la misma gramática visual en todos los paneles.

    En este ejemplo veremos glucosa por sexo en paneles separados.
    """)
    return


@app.cell
def _(df):
    # Histograma facetado con Altair
    # - mark_bar: representa frecuencias por intervalos (bins)
    chart_facet_glucose = (
        alt.Chart(df)
        .mark_bar()

        # Codificación de variables
        .encode(
            # Eje X (cuantitativo con binning)
            # - bin: agrupa valores continuos en intervalos
            # - maxbins: controla resolución del histograma
            x=alt.X(
                "glucose_mg_dL:Q",
                bin=alt.Bin(maxbins=15),
                title="Glucosa (mg/dL)"
            ),

            # Eje Y (conteo)
            # - count(): número de observaciones por bin
            y=alt.Y(
                "count():Q",
                title="Frecuencia"
            ),

            # Tooltip
            # - muestra frecuencia por barra
            tooltip=[
                alt.Tooltip("count():Q", title="Frecuencia")
            ],
        )

        # Propiedades base
        # - tamaño por faceta
        .properties(
            width=280,
            height=220,
            title="Distribución de glucosa por sexo",
        )

        # Facetado
        # - column: crea una columna por categoría (sexo)
        .facet(
            column=alt.Column("sex:N", title="Sexo")
        )
    )

    # Mostrar gráfico
    chart_facet_glucose
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 9) Cuándo conviene usar cada librería

    En este punto ya trabajaste con tres enfoques distintos de visualización.
    No son “competidores directos”, sino herramientas con modelos mentales diferentes.

    La decisión no es estética: es **epistemológica y operativa**.
    Depende de cómo estás pensando el problema.

    ---

    ## Matplotlib — Control imperativo y bajo nivel

    Matplotlib sigue un enfoque **imperativo**:

    > defines explícitamente cada elemento del gráfico paso a paso.

    Esto implica que tú controlas directamente:

    - ejes (`axes`)
    - figuras (`figure`)
    - escalas
    - anotaciones
    - elementos gráficos individuales (“artists”)

    ### Cuándo usarlo

    - Cuando necesitas **control total del layout**
    - Cuando el gráfico requiere **ajustes muy específicos o no estándar**
    - Cuando estás construyendo:
      - figuras complejas para papers
      - dashboards estáticos altamente personalizados
    - Cuando necesitas **optimizar cada detalle visual**

    ### Limitaciones

    - Código más **verborreico**
    - Mayor carga cognitiva
    - No está optimizado para exploración rápida

    ---

    ## Seaborn — Abstracción estadística sobre Matplotlib

    Seaborn introduce un enfoque **de alto nivel orientado a relaciones estadísticas**.

    No defines “cómo dibujar”, sino **qué relación quieres ver**:

    - distribución
    - correlación
    - comparación entre grupos

    Internamente usa Matplotlib, pero simplifica su uso.

    ### Cuándo usarlo

    - Exploración inicial de datos (EDA)
    - Visualización de:
      - distribuciones (`histplot`, `kdeplot`)
      - relaciones (`scatterplot`, `regplot`)
      - comparaciones (`boxplot`, `violinplot`)
    - Cuando quieres:
      - menos código
      - defaults estadísticamente razonables

    ### Ventaja clave

    > Reduce fricción entre **pregunta estadística** y **visualización**

    ### Limitaciones

    - Menor control fino que Matplotlib
    - Personalización avanzada puede volverse confusa
    - Menos expresivo para composiciones complejas

    ---

    ## Altair — Especificación declarativa (grammar of graphics)

    Altair sigue un enfoque **declarativo** basado en el *Grammar of Graphics*:

    > describes el gráfico como una **transformación de datos a representación visual**

    En lugar de decir “dibuja esto”, defines:

    - **datos**
    - **marca (mark)**
    - **canales (encodings)** → x, y, color, tamaño, etc.
    - **transformaciones**

    El sistema se encarga del renderizado.

    ### Cuándo usarlo

    - Cuando quieres **claridad estructural en el código**
    - Cuando trabajas con:
      - múltiples variables
      - facetas
      - capas
    - Cuando necesitas:
      - interactividad (tooltips, selección)
      - reproducibilidad clara del gráfico
    - Exploración visual estructurada

    ### Ventaja clave

    > El gráfico es una **declaración explícita del modelo visual**

    ### Limitaciones

    - Menos control pixel-perfect
    - Puede ser restrictivo en layouts muy personalizados
    - Requiere cambiar el modelo mental (no es imperativo)

    ---

    ## Comparación conceptual

    | Dimensión                  | Matplotlib              | Seaborn                         | Altair                              |
    |--------------------------|------------------------|----------------------------------|--------------------------------------|
    | Paradigma                | Imperativo             | Imperativo (alto nivel)          | Declarativo                          |
    | Nivel de abstracción     | Bajo                   | Medio                            | Alto                                 |
    | Control fino             | Máximo                 | Medio                            | Limitado                             |
    | Velocidad de uso         | Baja                   | Alta                             | Alta                                 |
    | Expresividad estructural | Baja                   | Media                            | Muy alta                             |
    | Interactividad           | Limitada               | Limitada                         | Nativa                               |
    | Curva mental             | Técnica                | Intuitiva                        | Conceptual (requiere adaptación)     |

    ---

    ## Casos de uso típicos

    ### Matplotlib

    - Figuras para publicaciones científicas
    - Gráficos altamente personalizados
    - Ajustes finos de ejes, escalas y anotaciones

    ---

    ### Seaborn

    - Análisis exploratorio rápido (EDA)
    - Visualización de patrones estadísticos comunes
    - Reportes preliminares

    ---

    ### Altair

    - Visualización reproducible y clara
    - Dashboards ligeros e interactivos
    - Análisis multivariable con facetas y capas
    - Enseñanza (porque hace explícita la estructura)

    ---

    ## Idea clave

    > No eliges la librería por “potencia”,
    > sino por **alineación entre el modelo mental de la herramienta y tu problema analítico**.

    - Si piensas en **dibujar → Matplotlib**
    - Si piensas en **relaciones estadísticas → Seaborn**
    - Si piensas en **mapear datos a estética → Altair**
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto final — Facets declarativos de PAS por hipertensión

    Construye una visualización declarativa llamada `chart_facet_sbp`.

    ### Objetivo analítico

    Comparar la distribución de `sbp_mmHg` en paneles separados según `hypertension`.

    ### Requisitos

    1. usa `mark_bar()`,
    2. crea bins en el eje x,
    3. usa conteo en el eje y,
    4. facetéa por `hypertension`,
    5. añade un título general.

    **Variable esperada:**

    - `chart_facet_sbp`
    """)
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    chart_facet_sbp = None
    return (chart_facet_sbp,)


@app.cell(hide_code=True)
def _():
    _tip_content = TipContent(
        items_raw=[
            r"""
            <Base>
            Empieza con `alt.Chart(df).mark_bar()`.
            """,
            r"""
            <Distribución>
            Usa una variable binarizada en x con `bin=alt.Bin(maxbins=...)`.
            """,
            r"""
            <Faceta>
            La separación en paneles se construye con `.facet(...)`.
            """,
            r"""
            <solucion>
            ```python
            chart_facet_sbp = (
                alt.Chart(df)
                .mark_bar()
                .encode(
                    x=alt.X(
                        "sbp_mmHg:Q",
                        bin=alt.Bin(maxbins=15),
                        title="PAS (mmHg)",
                    ),
                    y=alt.Y("count():Q", title="Frecuencia"),
                    tooltip=[alt.Tooltip("count():Q", title="Frecuencia")],
                )
                .properties(
                    width=180,
                    height=220,
                    title="Distribución de PAS por hipertensión",
                )
                .facet(column=alt.Column("hypertension:N", title="Hipertensión"))
            )
            ```
            """,
        ]
    )
    _tip_content.render()
    return


@app.cell(hide_code=True)
def _(chart_facet_sbp):
    _test_content = TestContent(
        items_raw=[
            r"""
            <Existencia>
            ```python
    assert chart_facet_sbp is not None
            ```
            """,
            r"""
            <Objeto declarativo>
            ```python
    assert hasattr(chart_facet_sbp, "to_dict")
            ```
            """,
            r"""
            <Facet esperado>
            ```python
            spec = chart_facet_sbp.to_dict()
    assert "facet" in spec
    assert spec["facet"]["column"]["field"] == "hypertension"
            ```
            """,
        ],
        namespace=globals(),
    )

    if chart_facet_sbp is not None:
        chart_facet_sbp
    _test_content.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 10) Cierre conceptual

    En esta lección trabajaste el enfoque declarativo con Altair como cierre del módulo.

    Construiste y analizaste:

    - barras para proporciones,
    - líneas para evolución resumida,
    - heatmaps con `mark_rect()`,
    - etiquetas sobre celdas con `mark_text()`,
    - scatter plots con color y tooltip,
    - facets para comparación estructurada.

    La progresión de la semana queda así:

    - **Matplotlib:** cómo construir manualmente,
    - **Seaborn:** cómo expresar relaciones estadísticas frecuentes,
    - **Altair:** cómo especificar gráficamente una relación de forma declarativa e interactiva.

    Idea final:

    > **las librerías cambian, pero la lógica central se mantiene: elegir la representación correcta según la pregunta, la estructura de los datos y el mensaje que se quiere comunicar.**
    """)
    return


if __name__ == "__main__":
    app.run()
