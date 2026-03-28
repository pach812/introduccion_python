# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "pandas",
#     "matplotlib",
# ]
# ///

import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")

with app.setup(hide_code=True):
    import marimo as mo
    import pandas as pd
    import matplotlib.pyplot as plt
    from pathlib import Path


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Live coding · Salud mental
    ## Nivel de agotamiento según categorías de rendimiento académico

    **Propósito de la sesión:** mostrar, paso a paso, cómo construir una historia descriptiva reproducible a partir de una pregunta maestra sencilla.

    **Pregunta de trabajo:**

    > ¿Cómo se comporta el nivel de agotamiento según las categorías de rendimiento académico?

    **Variables importantes:** `promedio_acumulado`, `nivel_agotamiento`

    **Ruta de trabajo en clase:**

    1. cargar la base,
    2. revisar tamaño y columnas,
    3. cuantificar faltantes,
    4. resumir el desenlace,
    5. resumir la variable clave,
    6. construir una variable derivada,
    7. crear tablas de conteos y proporciones,
    8. reorganizar en pivote,
    9. priorizar grupos,
    10. visualizar y concluir.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1) Cargar la base

    Usaremos la estructura esperada del taller:

    ```
    data/
    └── datasets/
        └── Salud_mental_kaggle.csv
    ```

    La celda siguiente intenta primero esa ruta relativa. Si no la encuentra, usa una ruta alternativa local para facilitar la demostración.
    """)
    return


@app.cell
def _():
    candidate_paths = [
        Path("./datasets/Salud_mental_kaggle.csv"),
        Path("/mnt/data/Salud_mental_kaggle.csv"),
    ]

    dataset_path = None
    for path in candidate_paths:
        if path.exists():
            dataset_path = path
            break

    if dataset_path is None:
        raise FileNotFoundError(
            "No se encontró 'Salud_mental_kaggle.csv' en las rutas esperadas."
        )

    df = pd.read_csv(dataset_path)
    df.head()
    return dataset_path, df


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2) Inspección inicial

    Antes de transformar datos, conviene responder dos preguntas básicas:

    - ¿cuál es el tamaño de la base?
    - ¿qué columnas tengo disponibles?

    Esto ayuda a verificar que estamos trabajando con el archivo correcto y a reconocer las variables útiles para la pregunta.
    """)
    return


@app.cell
def _(df):
    shape_info = pd.DataFrame(
        {
            "n_filas": [df.shape[0]],
            "n_columnas": [df.shape[1]],
        }
    )
    shape_info
    return (shape_info,)


@app.cell
def _(df):
    columns_table = pd.DataFrame({"columna": df.columns})
    columns_table
    return (columns_table,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3) Valores faltantes

    El siguiente paso es cuantificar faltantes por variable.

    En el taller, este conteo debe hacerse sobre la base original. Solo después de esta revisión se eliminan las filas con cualquier dato faltante.
    """)
    return


@app.cell
def _(df):
    missing_table = (
        df.isna()
        .sum()
        .rename_axis("variable")
        .reset_index(name="n_missing")
        .sort_values(["n_missing", "variable"], ascending=[False, True])
        .reset_index(drop=True)
    )
    missing_table
    return (missing_table,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4) Limpiar filas incompletas

    Para homogeneizar el proceso, desde este punto trabajaremos solo con datos completos.

    Aquí eliminamos toda fila que tenga al menos un valor faltante en cualquier columna.
    """)
    return


@app.cell
def _(df):
    df_complete = df.dropna().copy()
    cleaning_summary = pd.DataFrame(
        {
            "filas_originales": [df.shape[0]],
            "filas_completas": [df_complete.shape[0]],
            "filas_eliminadas": [df.shape[0] - df_complete.shape[0]],
        }
    )
    cleaning_summary
    return cleaning_summary, df_complete


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5) Resumir el desenlace

    El desenlace principal es `nivel_agotamiento`.

    Como es una variable categórica, una forma natural de resumirla es mediante frecuencias absolutas y relativas.
    """)
    return


@app.cell
def _(df_complete):
    burnout_counts = (
        df_complete["nivel_agotamiento"]
        .value_counts(dropna=False)
        .rename_axis("nivel_agotamiento")
        .reset_index(name="n")
    )
    burnout_counts["proporcion"] = burnout_counts["n"] / burnout_counts["n"].sum()
    burnout_counts
    return (burnout_counts,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6) Resumir la variable clave

    La variable clave es `promedio_acumulado`.

    Como es numérica, conviene revisar un resumen descriptivo básico antes de categorizarla.
    """)
    return


@app.cell
def _(df_complete):
    gpa_summary = df_complete[["promedio_acumulado"]].describe().round(2)
    gpa_summary
    return (gpa_summary,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7) Construir la variable derivada

    Para responder la pregunta, vamos a convertir el promedio acumulado en una variable categórica interpretable.

    En esta sesión usaremos la siguiente regla:

    - **Bajo**: promedio menor que 6.0
    - **Medio**: promedio entre 6.0 y menor que 8.0
    - **Alto**: promedio mayor o igual que 8.0

    Esta decisión didáctica permite comparar grupos con claridad y reproducibilidad.
    """)
    return


@app.cell
def _(df_complete):
    bins = [float("-inf"), 6.0, 8.0, float("inf")]
    labels = ["Bajo", "Medio", "Alto"]

    df_analysis = df_complete.assign(
        categoria_rendimiento=pd.cut(
            df_complete["promedio_acumulado"],
            bins=bins,
            labels=labels,
            right=False,
        )
    )

    category_counts = (
        df_analysis["categoria_rendimiento"]
        .value_counts(dropna=False)
        .rename_axis("categoria_rendimiento")
        .reset_index(name="n")
    )
    category_counts
    return category_counts, df_analysis


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8) Tabla de conteos por grupo y desenlace

    Ahora cruzamos la variable derivada con el desenlace.

    Esta tabla es útil porque muestra el volumen de estudiantes en cada combinación de categorías.
    """)
    return


@app.cell
def _(df_analysis):
    counts_table = (
        df_analysis.groupby(["categoria_rendimiento", "nivel_agotamiento"], observed=False)
        .size()
        .reset_index(name="n")
        .sort_values(["categoria_rendimiento", "nivel_agotamiento"])
        .reset_index(drop=True)
    )
    counts_table
    return (counts_table,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 9) Proporción de agotamiento alto por grupo

    Para priorizar grupos, es útil pasar de conteos a proporciones.

    Aquí construiremos una bandera binaria que indique si el estudiante presenta **agotamiento alto**.
    Luego calcularemos su proporción dentro de cada categoría de rendimiento.
    """)
    return


@app.cell
def _(df_analysis):
    df_analysis_2 = df_analysis.assign(
        agotamiento_alto=(df_analysis["nivel_agotamiento"] == "Alto").astype(int)
    )

    proportion_table = (
        df_analysis_2.groupby("categoria_rendimiento", observed=False, as_index=False)
        .agg(
            n_estudiantes=("id_estudiante", "count"),
            proporcion_agotamiento_alto=("agotamiento_alto", "mean"),
        )
        .sort_values("categoria_rendimiento")
        .reset_index(drop=True)
    )
    proportion_table
    return df_analysis_2, proportion_table


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 10) Tabla pivote

    La tabla pivote reorganiza los conteos para que la comparación entre grupos sea más legible.

    En este caso:

    - filas = categoría de rendimiento
    - columnas = nivel de agotamiento
    - celdas = número de estudiantes
    """)
    return


@app.cell
def _(df_analysis):
    pivot_table = pd.pivot_table(
        df_analysis,
        index="categoria_rendimiento",
        columns="nivel_agotamiento",
        values="id_estudiante",
        aggfunc="count",
        fill_value=0,
    )
    pivot_table
    return (pivot_table,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 11) Ranking de grupos

    Ordenamos los grupos de mayor a menor según la proporción de agotamiento alto.

    Esto permite identificar rápidamente qué categorías de rendimiento presentan mayor carga del desenlace prioritario.
    """)
    return


@app.cell
def _(proportion_table):
    ranking_table = (
        proportion_table.sort_values(
            "proporcion_agotamiento_alto", ascending=False
        ).reset_index(drop=True)
    )
    ranking_table["rank"] = ranking_table.index + 1
    ranking_table = ranking_table[
        [
            "rank",
            "categoria_rendimiento",
            "n_estudiantes",
            "proporcion_agotamiento_alto",
        ]
    ]
    ranking_table
    return (ranking_table,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 12) Visualización del patrón principal

    Para la clase conviene usar un gráfico simple y muy legible.

    Aquí mostraremos la proporción de agotamiento alto por categoría de rendimiento académico.
    """)
    return


@app.cell
def _(proportion_table):
    plot_df = proportion_table.copy()
    plot_df["proporcion_agotamiento_alto"] = (
        plot_df["proporcion_agotamiento_alto"] * 100
    )

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.bar(
        plot_df["categoria_rendimiento"].astype(str),
        plot_df["proporcion_agotamiento_alto"],
    )
    ax.set_title("Agotamiento alto según categoría de rendimiento")
    ax.set_xlabel("Categoría de rendimiento académico")
    ax.set_ylabel("Porcentaje con agotamiento alto")
    ax.set_ylim(0, max(plot_df["proporcion_agotamiento_alto"].max() + 5, 10))

    for x, y in zip(
        plot_df["categoria_rendimiento"].astype(str),
        plot_df["proporcion_agotamiento_alto"],
    ):
        ax.text(x, y + 0.8, f"{y:.1f}%", ha="center")

    fig.tight_layout()
    fig
    return fig, plot_df


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 13) Conclusión descriptiva

    Una buena conclusión en este contexto debe:

    - recuperar la pregunta,
    - nombrar el grupo con mayor carga del desenlace,
    - y resumir el patrón observado sin exagerarlo.
    """)
    return


@app.cell
def _(ranking_table):
    top_group = ranking_table.iloc[0]
    bottom_group = ranking_table.iloc[-1]

    conclusion = (
        f"En esta muestra, la categoría de rendimiento '{top_group['categoria_rendimiento']}' "
        f"presentó la mayor proporción de agotamiento alto "
        f"({top_group['proporcion_agotamiento_alto'] * 100:.1f}%), mientras que "
        f"la categoría '{bottom_group['categoria_rendimiento']}' mostró la menor "
        f"({bottom_group['proporcion_agotamiento_alto'] * 100:.1f}%)."
    )

    mo.callout(conclusion, kind="success")
    return (conclusion,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 14) Extensión opcional para discusión en clase

    Si quieres profundizar el procedimiento, una extensión natural es estratificar por género.

    Por ejemplo, puedes rehacer:

    - la tabla de conteos,
    - la tabla de proporciones,
    - la tabla pivote,
    - o la visualización,

    usando una estructura del tipo:

    `categoria_rendimiento × genero`

    Esto permite mostrar cómo una segunda dimensión puede enriquecer la historia descriptiva.
    """)
    return


if __name__ == "__main__":
    app.run()
