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
    import marimo as mo
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from pathlib import Path
    from matplotlib.axes import Axes
    from matplotlib.figure import Figure

    from setup import TipContent, TestContent, find_data_file


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Semana 3 · Lección 2
    ## Visualización imperativa con Matplotlib

    **Propósito de la sesión:** construir visualizaciones clínicas paso a paso utilizando el modelo imperativo de Matplotlib.

    En esta lección trabajaremos con una idea central:

    > primero se crea la figura y sus ejes, y después se agregan explícitamente los elementos gráficos y semánticos del gráfico.

    Esta lógica es especialmente útil en análisis de datos en salud porque permite controlar con precisión:

    - qué variable se representa,
    - cómo se codifica visualmente,
    - qué elementos se enfatizan,
    - y qué etiquetas ayudan a la interpretación clínica.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 1) Marco conceptual

    En el enfoque imperativo, el gráfico se construye como una secuencia de instrucciones.

    La estructura mínima suele ser:

    1. crear una figura y uno o más ejes,
    2. agregar una geometría (`plot`, `bar`, `hist`, `scatter`),
    3. definir título y etiquetas,
    4. ajustar leyenda, límites o cuadrícula,
    5. interpretar el resultado.

    Esto contrasta con una lógica más automática, donde la librería decide parte importante de la representación.

    Aquí el objetivo es comprender que **el gráfico es un objeto construido explícitamente**.
    """)
    return


@app.cell
def _():
    data_path = find_data_file("public/dataset_clase_semana2_small.csv")
    df = pd.read_csv(data_path)

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    categorical_cols = df.select_dtypes(include="str").columns.tolist()

    assert data_path.exists()
    assert df.shape[0] > 0
    assert set(numeric_cols).issubset(df.columns)

    df.head()
    return categorical_cols, df, numeric_cols


@app.cell(hide_code=True)
def _(df):
    mo.md(f"""
    ## 2) Dataset de trabajo

    Utilizaremos un subset de la Encuesta sobre Salud, Bienestar y Envejecimiento (SABE) con **{df.shape[0]} registros** y **{df.shape[1]} variables**.

    Cada fila representa un individuo y contiene variables demográficas, factores de riesgo y mediciones clínicas.

    En esta sesión nos concentraremos en variables adecuadas para visualización básica con Matplotlib:

    - `age`
    - `sbp_mmHg`
    - `glucose_mg_dL`
    - `ldl_mg_dL`
    - `sex`
    - `hypertension`
    - `Diabetes`
    - `bmi_category`

    El propósito no es solo “dibujar”, sino elegir una representación coherente con la pregunta analítica.
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

    mo.vstack([
        mo.md("### Resumen numérico"),
        summary_numeric,
        mo.md("### Resumen categórico"),
        summary_categorical,
    ])
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 3) Anatomía mínima de un gráfico en Matplotlib

    El patrón básico que repetiremos es:

    ```python
    fig, ax = plt.subplots()
    ax.plot(...)
    ax.set_title(...)
    ax.set_xlabel(...)
    ax.set_ylabel(...)
    ```

    - `fig` representa la figura completa.
    - `ax` representa el área concreta donde se dibuja el gráfico.

    Esta separación es importante porque permite añadir control local sobre cada visualización.

    Es preferible **trabajar con métodos del objeto `Axes`** para controlar directamente cada componente del gráfico.
    """)
    return


@app.cell
def _(df):
    # Para mostrar la evolución de PAS media por edad sin grupos etarios, se puede usar el siguiente código:
    sbp_by_age = (
        df.groupby("age", as_index=False)
        .agg(mean_sbp=("sbp_mmHg", "mean"))
        .sort_values("age")
    )

    # Gráfico de línea para PAS media por edad
    fig_line, ax_line = plt.subplots(figsize=(8, 4.5))

    # La función `plot` de Matplotlib se utiliza para crear un gráfico de línea. Aquí se especifica el eje x con las edades y el eje y con la PAS media correspondiente a cada edad. Se añaden marcadores para resaltar cada punto de datos y se ajusta el grosor de la línea para mejorar la visualización.
    ax_line.plot(
        sbp_by_age["age"],
        sbp_by_age["mean_sbp"],
        marker="o",
        linewidth=1.8,
        label="PAS media por edad",
    )

    # Se establecen el título del gráfico y las etiquetas de los ejes para proporcionar contexto clínico. 
    ax_line.set_title("Presión arterial sistólica media por edad")
    ax_line.set_xlabel("Edad (años)")
    ax_line.set_ylabel("PAS media (mmHg)")

    # La leyenda se activa para identificar la serie de datos representada, y se añade una cuadrícula suave para facilitar la lectura de los valores. 
    ax_line.legend()
    ax_line.grid(True, alpha=0.3)

    # Finalmente, `tight_layout()` se llama para ajustar automáticamente los márgenes y evitar que los elementos del
    fig_line.tight_layout()
    fig_line
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    En este primer ejemplo se observa claramente la lógica imperativa en la que se basa Matplotlib:

    - se crea el espacio gráfico,
    - se agrega una línea,
    - se nombran ejes,
    - se añade leyenda,
    - y se mejora la legibilidad con cuadrícula suave.

    Matplotlib permite añadir leyendas, etiquetas de ejes y títulos mediante métodos explícitos del objeto `Axes`, lo que hace visible la construcción paso a paso del gráfico.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 4) Histograma: distribución de una variable clínica

    El histograma responde preguntas como:

    - ¿la variable está concentrada en pocos valores o dispersa?,
    - ¿hay sesgo hacia valores altos o bajos?,
    - ¿la distribución parece simétrica?,
    - ¿existen posibles valores extremos?

    En clínica y salud pública, este tipo de gráfico es útil para inspeccionar variables numéricas como edad, glucosa, presión arterial o colesterol.
    """)
    return


@app.cell
def _(df):
    # Crear figura y eje
    fig_hist, ax_hist = plt.subplots(figsize=(7, 4.5))

    # Histograma
    # - Datos: df["glucose_mg_dL"].dropna() -> elimina valores faltantes
    # - bins: 18 -> número de intervalos
    # - edgecolor: "black" -> bordes para mejor lectura
    ax_hist.hist(
        df["glucose_mg_dL"].dropna(),
        bins=18,
        edgecolor="black"
    )

    # Título y etiquetas
    ax_hist.set_title("Distribución de glucosa en sangre")
    ax_hist.set_xlabel("Glucosa (mg/dL)")
    ax_hist.set_ylabel("Frecuencia")

    # Ajuste de layout
    fig_hist.tight_layout()

    # Mostrar figura
    fig_hist
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto 1 — Histograma de edad

    Construye un histograma para la variable `age`.

    El objetivo es practicar la secuencia básica del enfoque imperativo:

    - crear figura y eje,
    - dibujar el histograma,
    - nombrar título y ejes.

    **Variables esperadas:**

    - `fig_reto1`
    - `ax_reto1`
    """)
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    fig_reto1, ax_reto1 = None, None
    return (fig_reto1,)


@app.cell(hide_code=True)
def _():
    _tip_content = TipContent(
        items_raw=[
            r"""
            <Crear figura y eje>
            Comienza con `plt.subplots()` y asigna el resultado a dos objetos.
            """,
            r"""
            <Geometría correcta>
            Para una sola variable numérica, el método adecuado es `ax.hist(...)`.
            """,
            r"""
            <Semántica mínima>
            Asegúrate de incluir un título y etiquetas para ambos ejes.
            """,
            r"""
            <solucion>
            ```python
            fig_reto1, ax_reto1 = plt.subplots(figsize=(7, 4.5))
            ax_reto1.hist(df["age"].dropna(), bins=15, edgecolor="black")
            ax_reto1.set_title("Distribución de edad en la cohorte")
            ax_reto1.set_xlabel("Edad (años)")
            ax_reto1.set_ylabel("Frecuencia")
            fig_reto1.tight_layout()
            ```
            """,
        ]
    )
    _tip_content.render()
    return


@app.cell(hide_code=True)
def _(fig_reto1):
    _test_content = TestContent(
        items_raw=[
            r"""
            <Existencia de objetos>
            ```python
            assert fig_reto1 is not None and ax_reto1 is not None
            ```
            """,
            r"""
            <Tipos correctos>
            ```python
            assert isinstance(fig_reto1, Figure)
            assert isinstance(ax_reto1, Axes)
            ```
            """,
            r"""
            <Etiquetas básicas>
            ```python
            assert ax_reto1.get_title() != ""
            assert ax_reto1.get_xlabel() != ""
            assert ax_reto1.get_ylabel() != ""
            ```
            """,
        ],
        namespace=globals(),
    )

    if fig_reto1 is not None:
        fig_reto1
    _test_content.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 5) Gráfico de barras: comparación entre categorías

    El gráfico de barras es apropiado cuando queremos comparar magnitudes entre grupos discretos.

    En salud, esto permite mostrar por ejemplo:

    - número de personas por categoría de IMC,
    - prevalencia de hipertensión por sexo,
    - recuento de casos por área de residencia.

    Desde una perspectiva de diseño, conviene reducir elementos innecesarios del gráfico y dejar que la comparación entre alturas sea el foco principal. En *Storytelling with Data* se insiste en eliminar clutter, remover elementos que distraen y dejar una jerarquía visual clara. fileciteturn2file2turn2file8
    """)
    return


@app.cell
def _(df):
    bmi_counts = (
        df["bmi_category"]
        .value_counts(dropna=False)
        .rename_axis("bmi_category")
        .reset_index(name="n")
    )

    fig_bar, ax_bar = plt.subplots(figsize=(8, 4.5))
    ax_bar.bar(bmi_counts["bmi_category"], bmi_counts["n"])
    ax_bar.set_title("Número de personas por categoría de IMC")
    ax_bar.set_xlabel("Categoría de IMC")
    ax_bar.set_ylabel("Número de personas")
    ax_bar.tick_params(axis="x", rotation=30)
    fig_bar.tight_layout()
    fig_bar
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 6) Scatter plot: relación entre dos variables numéricas

    El gráfico de dispersión es útil cuando la pregunta analítica se refiere a asociación o patrón conjunto entre dos variables cuantitativas.

    Aquí exploraremos la relación entre:

    - presión arterial sistólica (`sbp_mmHg`)
    - glucosa (`glucose_mg_dL`)

    Este gráfico no prueba causalidad ni ajuste estadístico; su propósito inmediato es **exploratorio**.
    """)
    return


@app.cell
def _(df):
    df_scatter = df[["sbp_mmHg", "glucose_mg_dL", "Diabetes"]].dropna().copy()
    diabetes_map = {"Yes": "Diabetes", "No": "No diabetes", "yes": "Diabetes", "no": "No diabetes"}
    df_scatter["Diabetes_plot"] = df_scatter["Diabetes"].map(diabetes_map).fillna(df_scatter["Diabetes"])

    fig_scatter, ax_scatter = plt.subplots(figsize=(7, 4.5))
    for label, subset in df_scatter.groupby("Diabetes_plot"):
        ax_scatter.scatter(
            subset["sbp_mmHg"],
            subset["glucose_mg_dL"],
            alpha=0.6,
            label=label,
        )

    ax_scatter.set_title("Presión arterial y glucosa según estado de diabetes")
    ax_scatter.set_xlabel("PAS (mmHg)")
    ax_scatter.set_ylabel("Glucosa (mg/dL)")
    ax_scatter.legend()
    ax_scatter.grid(True, alpha=0.2)
    fig_scatter.tight_layout()
    fig_scatter
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto 2 — Barras de hipertensión por sexo

    Construye un gráfico de barras que compare el **número de personas con hipertensión** entre categorías de `sex`.

    Sugerencia analítica: primero debes resumir la tabla y luego representar el resultado.

    **Variables esperadas:**

    - `hypertension_by_sex`
    - `fig_reto2`
    - `ax_reto2`
    """)
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    hypertension_by_sex = None
    fig_reto2, ax_reto2 = None, None
    return fig_reto2, hypertension_by_sex


@app.cell(hide_code=True)
def _():
    _tip_content = TipContent(
        items_raw=[
            r"""
            <Paso tabular previo>
            Filtra primero las filas donde `hypertension` represente presencia de hipertensión y luego resume por `sex`.
            """,
            r"""
            <Estructura del resumen>
            El DataFrame final debe tener una columna para sexo y otra para el conteo.
            """,
            r"""
            <Representación>
            Usa `ax.bar(...)` con el sexo en el eje x y el conteo en el eje y.
            """,
            r"""
            <solucion>
            ```python
            hypertension_by_sex = (
                df.loc[df["hypertension"].astype(str).str.lower().eq("yes")]
                .groupby("sex", as_index=False)
                .agg(n_hypertension=("ID", "count"))
                .sort_values("sex")
            )

            fig_reto2, ax_reto2 = plt.subplots(figsize=(6.5, 4))
            ax_reto2.bar(hypertension_by_sex["sex"], hypertension_by_sex["n_hypertension"])
            ax_reto2.set_title("Número de personas con hipertensión por sexo")
            ax_reto2.set_xlabel("Sexo")
            ax_reto2.set_ylabel("Número de personas")
            fig_reto2.tight_layout()
            ```
            """,
        ]
    )
    _tip_content.render()
    return


@app.cell(hide_code=True)
def _(fig_reto2, hypertension_by_sex):
    _test_content = TestContent(
        items_raw=[
            r"""
            <Objeto resumen>
            ```python
            assert hypertension_by_sex is not None
            assert isinstance(hypertension_by_sex, pd.DataFrame)
            ```
            """,
            r"""
            <Columnas esperadas>
            ```python
            assert list(hypertension_by_sex.columns) == ["sex", "n_hypertension"]
            ```
            """,
            r"""
            <Objetos de gráfico>
            ```python
            assert isinstance(fig_reto2, Figure)
            assert isinstance(ax_reto2, Axes)
            ```
            """,
        ],
        namespace=globals(),
    )

    if hypertension_by_sex is not None:
        hypertension_by_sex
    if fig_reto2 is not None:
        fig_reto2
    _test_content.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 7) Subplots: comparación coordinada

    Cuando dos gráficos comparten propósito analítico, puede ser útil colocarlos en una misma figura.

    Matplotlib permite crear cuadrículas de ejes mediante `plt.subplots(...)`. Este enfoque es útil cuando queremos comparar distribuciones clínicas con la misma escala visual o con una narrativa coordinada. El texto de referencia de McKinney muestra justamente `plt.subplots` como una forma más conveniente de organizar varios ejes en una misma figura. fileciteturn2file5
    """)
    return


@app.cell
def _(df):
    fig_grid, axes_grid = plt.subplots(1, 2, figsize=(11, 4))

    axes_grid[0].hist(df["sbp_mmHg"].dropna(), bins=18, edgecolor="black")
    axes_grid[0].set_title("Distribución de PAS")
    axes_grid[0].set_xlabel("PAS (mmHg)")
    axes_grid[0].set_ylabel("Frecuencia")

    axes_grid[1].hist(df["ldl_mg_dL"].dropna(), bins=18, edgecolor="black")
    axes_grid[1].set_title("Distribución de LDL")
    axes_grid[1].set_xlabel("LDL (mg/dL)")
    axes_grid[1].set_ylabel("Frecuencia")

    fig_grid.tight_layout()
    fig_grid
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 8) Buenas prácticas mínimas en visualización imperativa

    En este punto ya podemos extraer algunas reglas operativas:

    - elegir el tipo de gráfico según la pregunta,
    - no usar elementos decorativos innecesarios,
    - titular con precisión clínica,
    - nombrar unidades cuando existan,
    - evitar ambigüedad en leyendas y ejes,
    - mantener consistencia visual entre gráficos comparables.

    En *Storytelling with Data* se enfatiza que un buen gráfico no es el más cargado de elementos, sino el que comunica con menor fricción cognitiva. fileciteturn2file9turn2file2
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto 3 — Evolución de PAS media por grupos de edad

    Construye un gráfico de línea que represente la **presión arterial sistólica media** por **grupo etario**.

    Requisitos:

    1. crear una nueva columna `age_group` con estas bandas:
       - 40–49
       - 50–59
       - 60–69
       - 70–79
       - 80+
    2. calcular la PAS media por `age_group`,
    3. construir un gráfico de línea con marcadores.

    **Variables esperadas:**

    - `sbp_by_age_group`
    - `fig_reto3`
    - `ax_reto3`

    Este mini-reto final integra contenidos ya trabajados: transformación tabular con pandas y construcción imperativa del gráfico con Matplotlib.
    """)
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    sbp_by_age_group = None
    fig_reto3, ax_reto3 = None, None
    return fig_reto3, sbp_by_age_group


@app.cell(hide_code=True)
def _():
    _tip_content = TipContent(
        items_raw=[
            r"""
            <Construcción de bandas>
            Puedes usar `pd.cut(...)` para transformar una variable numérica continua en categorías ordenadas.
            """,
            r"""
            <Orden correcto>
            Para que la línea tenga sentido, el resumen final debe respetar el orden natural de los grupos etarios.
            """,
            r"""
            <Gráfico final>
            Usa `ax.plot(...)` con marcador y agrega etiquetas semánticas claras.
            """,
            r"""
            <solucion>
            ```python
            age_groups = pd.cut(
                df["age"],
                bins=[40, 50, 60, 70, 80, np.inf],
                right=False,
                labels=["40-49", "50-59", "60-69", "70-79", "80+"],
            )

            sbp_by_age_group = (
                df.assign(age_group=age_groups)
                .dropna(subset=["age_group", "sbp_mmHg"])
                .groupby("age_group", as_index=False)
                .agg(mean_sbp=("sbp_mmHg", "mean"))
            )

            fig_reto3, ax_reto3 = plt.subplots(figsize=(7.5, 4.5))
            ax_reto3.plot(
                sbp_by_age_group["age_group"].astype(str),
                sbp_by_age_group["mean_sbp"],
                marker="o",
                linewidth=1.8,
            )
            ax_reto3.set_title("PAS media por grupo de edad")
            ax_reto3.set_xlabel("Grupo de edad")
            ax_reto3.set_ylabel("PAS media (mmHg)")
            ax_reto3.grid(True, alpha=0.3)
            fig_reto3.tight_layout()
            ```
            """,
        ]
    )
    _tip_content.render()
    return


@app.cell(hide_code=True)
def _(fig_reto3, sbp_by_age_group):
    _test_content = TestContent(
        items_raw=[
            r"""
            <Resumen tabular>
            ```python
            assert sbp_by_age_group is not None
            assert isinstance(sbp_by_age_group, pd.DataFrame)
            ```
            """,
            r"""
            <Columnas esperadas>
            ```python
            assert list(sbp_by_age_group.columns) == ["age_group", "mean_sbp"]
            ```
            """,
            r"""
            <Gráfico creado>
            ```python
            assert isinstance(fig_reto3, Figure)
            assert isinstance(ax_reto3, Axes)
            assert ax_reto3.get_xlabel() != ""
            assert ax_reto3.get_ylabel() != ""
            ```
            """,
        ],
        namespace=globals(),
    )

    if sbp_by_age_group is not None:
        sbp_by_age_group
    if fig_reto3 is not None:
        fig_reto3
    _test_content.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 9) Cierre conceptual

    En esta sesión trabajaste el núcleo del enfoque imperativo con Matplotlib:

    - creación explícita de figura y ejes,
    - uso de `plot`, `hist`, `bar` y `scatter`,
    - incorporación manual de títulos, ejes, leyendas y cuadrícula,
    - organización de más de un gráfico mediante subplots,
    - y articulación entre resumen tabular y visualización.

    Este dominio es fundamental porque permite entender la lógica de construcción gráfica antes de pasar a librerías de mayor abstracción.
    """)
    return


if __name__ == "__main__":
    app.run()
