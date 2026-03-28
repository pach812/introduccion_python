# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "pandas",
#     "matplotlib",
# ]
# ///

import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")

with app.setup:
    import marimo as mo
    import pandas as pd

    from setup import find_data_file


@app.cell(hide_code=True)
def _():
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


@app.cell
def _():
    dataset = 2
    pregunta_elegida = "SM-P0"
    return


@app.cell(hide_code=True)
def _():
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
    ruta = "./datasets/Salud_mental_kaggle_live.csv"
    ruta_archivo = find_data_file(ruta)

    df = pd.read_csv(ruta_archivo)
    df
    return (df,)


@app.cell(hide_code=True)
def _():
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
    RP_01 = df.shape
    return


@app.cell
def _(df):
    df.info()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 3) Valores faltantes

    El siguiente paso es cuantificar faltantes por variable.

    En el taller, este conteo debe hacerse sobre la base original. Solo después de esta revisión se eliminan las filas con cualquier dato faltante.
    """)
    return


@app.cell
def _(df):
    RP_02 = (
        df.isna()
        .sum()
        .rename_axis("Variable")
        .reset_index(name="n_faltantes")
        .sort_values("n_faltantes", ascending=False)
        .reset_index(drop=True)
    )

    RP_02
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 4) Limpiar filas incompletas

    Para homogeneizar el proceso, desde este punto trabajaremos solo con datos completos.

    Aquí eliminamos toda fila que tenga al menos un valor faltante en cualquier columna.
    """)
    return


@app.cell
def _(df):
    df_final = df.dropna().copy()

    print(f"dataset original tenia {df.shape[0]}, columnas despues de retirar faltantes {df_final.shape[0]}")
    return (df_final,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 5) Resumir el desenlace

    El desenlace principal es `nivel_agotamiento`.

    Como es una variable categórica, una forma natural de resumirla es mediante frecuencias absolutas y relativas.
    """)
    return


@app.cell
def _(df_final):
    RP_03 = df_final["nivel_agotamiento"].value_counts(normalize=True).mul(100)
    RP_03
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 6) Resumir la variable clave

    La variable clave es `promedio_acumulado`.

    Como es numérica, conviene revisar un resumen descriptivo básico antes de categorizarla.
    """)
    return


@app.cell
def _(df_final):
    RP_04 = df_final["promedio_acumulado"].describe().round(3)
    RP_04
    return


@app.cell(hide_code=True)
def _():
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
def _(df_final):
    # pd.cut() <- particion rapida
    bins = [0, 6, 8, 11]
    etiquetas = ["Bajo", "Medio", "Alto"]

    df_analisis = df_final.assign(
        cat_promedio_acumulado = pd.cut(
           df_final["promedio_acumulado"],
            bins=bins,
            labels=etiquetas,
            right=False
        )
    )

    df_analisis["cat_promedio_acumulado"].value_counts()

    # df.apply()

    def categorizar_promedio(val):
        if val < 6:
            return "Bajo"
        elif val < 8:
            return "Medio"
        else:
            return "Alto"

    df_analisis["cat_func_promedio"] = df_analisis["promedio_acumulado"].apply(categorizar_promedio)
    df_analisis["cat_promedio_acumulado"].value_counts(),df_analisis["cat_func_promedio"].value_counts()
    return (df_analisis,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 8) Tabla de conteos por grupo y desenlace

    Ahora cruzamos la variable derivada con el desenlace.

    Esta tabla es útil porque muestra el volumen de estudiantes en cada combinación de categorías.
    """)
    return


@app.cell
def _(df_analisis):
    RP_05 = df_analisis.groupby(by = ["cat_promedio_acumulado","nivel_agotamiento"]).size()\
        .reset_index(name="n")
        # .sort_values("cat_promedio_acumulado", ascending=False)
        # .reset_index(drop=True)
    RP_05
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 9) Proporción de agotamiento alto por grupo

    Para priorizar grupos, es útil pasar de conteos a proporciones.

    Aquí construiremos una bandera binaria que indique si el estudiante presenta **agotamiento alto**.
    Luego calcularemos su proporción dentro de cada categoría de rendimiento.
    """)
    return


@app.cell
def _(df_analisis):
    RP_06 = df_analisis["cat_promedio_acumulado"].value_counts(normalize=True).mul(100)

    df_analisis["PA_alto"] = df_analisis["cat_promedio_acumulado"]== 'Alto'

    df_analisis['PA_alto'].sum()
    # tabla_proporcion = df_analisis.groupby(by="cat_promedio_acumulado")\
    #     .agg(
    #         n_estudiantes = ("id_estudiante","count"),
    #         proporcion_alto = ("PA_alto",'sum')
    #     )

    # tabla_proporcion
    return


@app.cell(hide_code=True)
def _():
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
def _(df_analisis):
    RP_07 = pd.pivot_table(
        df_analisis,
        index="cat_promedio_acumulado",
        columns="nivel_agotamiento",
        values="id_estudiante",
        aggfunc="count"
    )

    RP_07
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 11) Ranking de grupos

    Ordenamos los grupos de mayor a menor según la proporción de agotamiento alto.

    Esto permite identificar rápidamente qué categorías de rendimiento presentan mayor carga del desenlace prioritario.
    """)
    return


@app.cell
def _(df_analisis):
    df_analisis2 = df_analisis.assign(
        alto_agotamiento = (df_analisis["nivel_agotamiento"] == "Alto").astype(int)
    )

    tabla_prop2 = df_analisis2.groupby(by="cat_promedio_acumulado").agg(
        n_estudiantes = ("id_estudiante","count"),
        proporcion_agotamiento_alto = ("alto_agotamiento","mean")
    )

    ranking_table = (
        tabla_prop2.sort_values("proporcion_agotamiento_alto", ascending = False).reset_index()
    )

    ranking_table["rank"] = ranking_table.index +1
    RP_08 = ranking_table
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 12) Visualización del patrón principal

    Para la clase conviene usar un gráfico simple y muy legible.

    Aquí mostraremos la proporción de agotamiento alto por categoría de rendimiento académico.
    """)
    return


@app.cell
def _():
    import seaborn as sns


    return (sns,)


@app.cell
def _(df_analisis, sns):
    g = sns.catplot(data = df_analisis, x = "nivel_agotamiento", y = "promedio_acumulado", kind="box")

    g.ax.set_title("distribucion del promedio acumulado por \ncategorias de nivel de agotamiento")

    RP_09 = g
    RP_09
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 13) Conclusión descriptiva

    Una buena conclusión en este contexto debe:

    - recuperar la pregunta,
    - nombrar el grupo con mayor carga del desenlace,
    - y resumir el patrón observado sin exagerarlo.
    """)
    return


@app.cell
def _():
    RP_10 = "Conclusion!"
    return


if __name__ == "__main__":
    app.run()
