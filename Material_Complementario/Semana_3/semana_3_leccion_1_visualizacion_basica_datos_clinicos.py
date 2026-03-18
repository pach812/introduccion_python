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
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from pathlib import Path
    from setup import TipContent, TestContent

    plt.rcParams["figure.figsize"] = (8, 4.5)
    plt.rcParams["axes.spines.top"] = False
    plt.rcParams["axes.spines.right"] = False
    plt.rcParams["axes.titleweight"] = "bold"
    plt.rcParams["axes.titlesize"] = 13
    plt.rcParams["axes.labelsize"] = 11

    def find_data_file(filename: str) -> Path:
        """Locate a data file in common execution directories."""
        candidates = [
            Path.cwd() / filename,
            Path(__file__).resolve().parent / filename,
            Path("/mnt/data") / filename,
        ]
        for path in candidates:
            if path.exists():
                return path
        raise FileNotFoundError(f"No se encontró el archivo: {filename}")


@app.cell
def _():
    mo.md(r"""
    # Semana 3 · Lección 1
    ## Conceptos básicos de visualización de datos clínicos

    **Propósito de la sesión:** introducir la visualización como herramienta para explorar y comunicar patrones en datos de salud usando **Matplotlib**.

    ### Preguntas centrales de la clase

    1. ¿Cómo elegir un gráfico según la pregunta analítica?
    2. ¿Qué diferencia hay entre mostrar datos y comunicar una observación?
    3. ¿Cómo construir gráficos básicos controlando títulos, ejes y etiquetas?

    ### Ruta de trabajo

    **dataset clínico → pregunta visual → gráfico adecuado → interpretación inicial**

    Durante esta sesión trabajaremos únicamente con tres familias de gráficos:

    - **histograma** para distribuciones,
    - **boxplot** para comparación entre grupos,
    - **scatter plot** para relación entre variables numéricas.
    """)
    return


@app.cell
def _():
    mo.md(r"""
    ## 1) Dataset de trabajo

    Usaremos un subset de la Encuesta sobre Salud, Bienestar y Envejecimiento (SABE), con variables demográficas, factores de riesgo y mediciones básicas, algunas de ellas sintéticas.

    Cada fila representa una persona. Entre las variables disponibles se encuentran:

    - `age`: edad en años
    - `sex`: sexo reportado
    - `Diabetes`: antecedente de diabetes
    - `sbp_mmHg`: presión arterial sistólica
    - `glucose_mg_dL`: glucosa
    - `ldl_mg_dL`: colesterol LDL
    - varias variables categóricas sobre estilo de vida y condiciones funcionales

    ### Objetivo analítico de la sesión

    Responder preguntas visuales introductorias como:

    - ¿cómo se distribuye una medición clínica?
    - ¿cambia la distribución entre grupos?
    - ¿dos variables numéricas parecen moverse juntas o separadas?
    """)
    return


@app.cell
def _():
    data_path = find_data_file("public/dataset_clase_semana2_small.csv")
    df = pd.read_csv(data_path)

    assert not df.empty
    assert {"age", "sex", "sbp_mmHg", "glucose_mg_dL", "ldl_mg_dL"}.issubset(df.columns)

    df.head()
    return data_path, df


@app.cell
def _(data_path):
    mo.md(rf"""
    Siempre es importante verificar desde donde se están cargando los datos, especialmente en entornos de notebooks donde la ubicación de los archivos puede variar. En este caso, el dataset se encuentra en 

    ```{data_path}```.

    Esto confirma que estamos trabajando con la fuente de datos correcta para esta sesión.
    """)
    return


@app.cell
def _():
    mo.md(r"""
    Siempre es adecuado hacer un acercamiento a nuestros datos antes de graficarlos, para entender su estructura, tipos de variables y posibles valores faltantes. Esto nos prepara para elegir el gráfico adecuado y evitar errores comunes al visualizar datos clínicos.

    Una forma de hacerlo es mediante metodos como `df.info()`, `df.describe()`, y verificando la cantidad de valores faltantes por columna. Esto nos da una visión general de qué tipo de datos tenemos y cómo están distribuidos, lo cual es crucial para elegir el gráfico correcto y para interpretar correctamente los patrones que observemos en la visualización.
    """)
    return


@app.cell
def _(df):
    df.info()
    return


@app.cell
def _():
    mo.md(r"""
    Otra forma es crear nuestro propio resumen, usando las herramientas que aprendimos la semana pasada.
    """)
    return


@app.cell
def _(df):
    numeric_columns = df.select_dtypes(include="number").columns.tolist()
    categorical_columns = df.select_dtypes(exclude="number").columns.tolist()

    dataset_overview = pd.DataFrame(
        {
            "n_rows": [df.shape[0]],
            "n_columns": [df.shape[1]],
            "numeric_variables": [len(numeric_columns)],
            "categorical_variables": [len(categorical_columns)],
        }
    )

    dataset_overview
    return


@app.cell
def _():
    mo.md(r"""
    ## 2) Antes de graficar: formular la pregunta visual

    Un gráfico no se elige por costumbre, sino por la **pregunta** que queremos responder.

    ### Mapa mínimo de decisión

    - **Si la pregunta es sobre distribución** de una variable numérica → usar **histograma**.
    - **Si la pregunta es sobre comparación entre grupos** para una variable numérica → usar **boxplot**.
    - **Si la pregunta es sobre relación entre dos variables numéricas** → usar **scatter plot**.

    En esta etapa inicial conviene evitar el exceso de elementos decorativos. Lo más importante es que el gráfico permita:

    1. identificar el patrón principal,
    2. leer los ejes con claridad,
    3. sostener una interpretación breve y concreta.
    """)
    return


@app.cell
def _():
    mo.md(r"""
    ## 3) Histograma: visualizar distribuciones

    El **histograma** agrupa una variable numérica en intervalos y cuenta cuántas observaciones caen dentro de cada uno.

    En salud, esto es útil para observar si una medición:

    - se concentra en un rango,
    - está muy dispersa,
    - tiene colas,
    - o muestra posibles valores extremos.

    La pregunta que responderemos primero es:

    **¿Cómo se distribuye la edad en este dataset?**
    """)
    return


@app.cell
def _(df):
    age_values = df["age"].dropna()
    age_mean = age_values.mean()

    # Ejemplo de histograma de edad con línea de la media

    # primero preparamos la figura y el eje
    fig_age_hist, ax_age_hist = plt.subplots()

    # luego graficamos el histograma, 
    ax_age_hist.hist(age_values, bins=12, edgecolor="black")

    # añadimos la línea de la media y 
    ax_age_hist.axvline(age_mean,
                        linestyle="--",
                        linewidth=2,
                        color = "red")

    # finalmente configuramos títulos y etiquetas.
    ax_age_hist.set_title("Distribución de la edad")
    ax_age_hist.set_xlabel("Edad (años)")
    ax_age_hist.set_ylabel("Frecuencia")
    ax_age_hist.grid(axis="y", alpha=0.25)

    fig_age_hist
    return (age_mean,)


@app.cell
def _(age_mean):
    mo.md(rf"""
    ### Lectura inicial del gráfico

    La línea punteada marca la media de edad del dataset, aproximadamente **{age_mean:.1f} años**.

    Observa cómo un gráfico muy simple ya permite responder preguntas descriptivas básicas:

    - en qué rango se concentra la mayor parte de la muestra,
    - si la distribución parece simétrica o no,
    - y si existen edades poco frecuentes en los extremos.

    En esta fase no buscamos una inferencia formal. Buscamos una **lectura visual ordenada** que prepare el análisis posterior.
    """)
    return


@app.cell
def _():
    mo.md(r"""
    ## Ejercicio guiado 1

    Ahora traslademos la misma lógica a otra variable clínica.

    Pregunta guiada:

    **¿Cómo se distribuye el colesterol LDL (`ldl_mg_dL`) en la muestra?**

    Antes de programar, conviene decidir:

    - qué variable va en el eje *x*,
    - qué representa el eje *y*,
    - cuántos intervalos usarás,
    - y qué títulos y etiquetas necesita el gráfico para ser interpretable por otra persona.
    """)
    return


@app.cell
def _():
    mo.md(r"""
    ## Mini-reto 1 — Histograma de LDL

    Construye un histograma para `ldl_mg_dL` usando Matplotlib.

    ### Variables de salida requeridas

    Debes crear exactamente estas variables:

    - `ldl_values`
    - `fig_hist_ldl`
    - `ax_hist_ldl`

    ### Requisitos mínimos

    - usar la columna `ldl_mg_dL`,
    - incluir título,
    - incluir etiqueta del eje *x*,
    - incluir etiqueta del eje *y*.
    """)
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    # Create the requested histogram and keep the required variable names.
    ldl_values = None
    fig_hist_ldl = None
    ax_hist_ldl = None
    return


@app.cell
def _():
    _tip_content = TipContent(
        items_raw=[
            r"""
    <Variable correcta>
    Trabaja con la columna numérica `ldl_mg_dL` y elimina valores faltantes si lo consideras necesario.
    """,
            r"""
    <Secuencia mínima>
    La secuencia más estable es:

    ```python
    fig_hist_ldl, ax_hist_ldl = plt.subplots()
    ax_hist_ldl.hist(...)
    ```
    """,
            r"""
    <Lectura del gráfico>
    El título debe decir qué variable estás mostrando y los ejes deben permitir interpretar la escala sin ambigüedad.
    """,
            r"""
    <solucion>
    ```python
    ldl_values = df["ldl_mg_dL"].dropna()
    fig_hist_ldl, ax_hist_ldl = plt.subplots()
    ax_hist_ldl.hist(ldl_values, bins=12, edgecolor="black")
    ax_hist_ldl.set_title("Distribución de LDL")
    ax_hist_ldl.set_xlabel("LDL (mg/dL)")
    ax_hist_ldl.set_ylabel("Frecuencia")
    ax_hist_ldl.grid(axis="y", alpha=0.25)
    fig_hist_ldl
    ```
    """,
        ]
    )

    _tip_content.render()
    return


@app.cell
def _():
    _test_content = TestContent(
        items_raw=[
            r"""
    <Existencia de variables>
    ```python
    assert ldl_values is not None, "Debes definir `ldl_values`."
    assert fig_hist_ldl is not None, "Debes definir `fig_hist_ldl`."
    assert ax_hist_ldl is not None, "Debes definir `ax_hist_ldl`."
    print("Variables definidas correctamente.")
    ```
    """,
            r"""
    <Tipo de objeto>
    ```python
    from matplotlib.axes import Axes
    from matplotlib.figure import Figure

    assert isinstance(fig_hist_ldl, Figure), "`fig_hist_ldl` debe ser una figura de Matplotlib."
    assert isinstance(ax_hist_ldl, Axes), "`ax_hist_ldl` debe ser un eje de Matplotlib."
    print("Objetos de Matplotlib correctos.")
    ```
    """,
            r"""
    <Etiquetas mínimas>
    ```python
    assert ax_hist_ldl.get_title() != "", "El gráfico debe tener título."
    assert ax_hist_ldl.get_xlabel() != "", "El eje x debe tener etiqueta."
    assert ax_hist_ldl.get_ylabel() != "", "El eje y debe tener etiqueta."
    print("Etiquetas básicas presentes.")
    ```
    """,
            r"""
    <Consistencia de datos>
    ```python
    assert len(ldl_values) == df["ldl_mg_dL"].notna().sum(), (
    "`ldl_values` debe corresponder a los valores no faltantes de `ldl_mg_dL`."
    )
    print("Datos utilizados correctamente.")
    ```
    """,
        ]
    )

    _test_content.render()
    return


@app.cell
def _():
    mo.md(r"""
    ## 4) Boxplot: comparar distribuciones entre grupos

    El **boxplot** resume una variable numérica mediante:

    - mediana,
    - rango intercuartílico,
    - y valores alejados del centro.

    Es especialmente útil cuando queremos comparar una misma medición entre dos o más grupos.

    Pregunta de esta sección:

    **¿Cómo cambia la presión arterial sistólica (`sbp_mmHg`) entre mujeres y hombres en este dataset?**
    """)
    return


@app.cell
def _(df):
    # Lipiamos las variables de valores faltantes
    sbp_female = df.loc[df["sex"] == "Female", "sbp_mmHg"].dropna()
    sbp_male = df.loc[df["sex"] == "Male", "sbp_mmHg"].dropna()

    # Construimos el boxplot comparando la presión arterial sistólica entre mujeres y hombres
    # Creacion de la figura y el eje
    fig_box_sbp, ax_box_sbp = plt.subplots()

    # Graficamos el boxplot con las dos series de datos y etiquetas
    ax_box_sbp.boxplot([sbp_female, sbp_male], tick_labels=["Mujeres", "Hombres"])

    # Configuramos títulos y etiquetas
    ax_box_sbp.set_title("Presión arterial sistólica por sexo")
    ax_box_sbp.set_xlabel("Sexo")
    ax_box_sbp.set_ylabel("PAS (mmHg)")
    ax_box_sbp.grid(axis="y", alpha=0.25)

    fig_box_sbp
    return


@app.cell
def _(df):
    sbp_by_sex = (
        df.groupby("sex", as_index=False)
        .agg(
            n=("sbp_mmHg", "count"),
            median_sbp=("sbp_mmHg", "median"),
            q1_sbp=("sbp_mmHg", lambda s: s.quantile(0.25)),
            q3_sbp=("sbp_mmHg", lambda s: s.quantile(0.75)),
        )
        .sort_values("sex")
    )

    sbp_by_sex
    return


@app.cell
def _():
    mo.md(r"""
    ### Lectura inicial del boxplot

    Cuando observes un boxplot en una etapa introductoria, prioriza tres preguntas:

    1. ¿Las medianas parecen similares o distintas?
    2. ¿Un grupo muestra más dispersión que otro?
    3. ¿Se observan puntos extremos o colas más largas?

    La idea no es sobreinterpretar. La idea es aprender a traducir la forma del gráfico en una descripción breve y clínicamente razonable.
    """)
    return


@app.cell
def _():
    mo.md(r"""
    ## 5) Scatter plot: relación entre dos variables numéricas

    El **scatter plot** coloca una variable numérica en el eje *x* y otra en el eje *y*.

    Cada punto representa una observación individual.

    Este gráfico sirve para examinar visualmente si dos variables parecen:

    - aumentar juntas,
    - disminuir juntas,
    - o no mostrar un patrón claro.

    Pregunta de esta sección:

    **¿Cómo se ven conjuntamente glucosa y LDL en la muestra?**
    """)
    return


@app.cell
def _(df):
    fig_scatter_glucose_ldl, ax_scatter_glucose_ldl = plt.subplots()
    ax_scatter_glucose_ldl.scatter(df["glucose_mg_dL"], df["ldl_mg_dL"], alpha=0.45)
    ax_scatter_glucose_ldl.set_title("Glucosa y LDL en observaciones individuales")
    ax_scatter_glucose_ldl.set_xlabel("Glucosa (mg/dL)")
    ax_scatter_glucose_ldl.set_ylabel("LDL (mg/dL)")
    ax_scatter_glucose_ldl.grid(alpha=0.2)

    fig_scatter_glucose_ldl
    return


@app.cell
def _():
    mo.md(r"""
    ### Observación importante

    En un scatter plot básico todavía no estamos cuantificando asociación con métricas formales.

    Lo que buscamos aquí es una lectura visual inicial:

    - si la nube de puntos parece dispersa o concentrada,
    - si hay observaciones aisladas,
    - y si aparece alguna dirección general aparente.

    Esto es suficiente para una primera sesión de visualización clínica.
    """)
    return


@app.cell
def _():
    mo.md(r"""
    ## Mini-reto final — Scatter plot de edad y glucosa

    Construye un scatter plot que responda a la siguiente pregunta:

    **¿Cómo se distribuyen conjuntamente la edad y la glucosa en este dataset?**

    ### Variables de salida requeridas

    Debes crear exactamente estas variables:

    - `scatter_data_age_glucose`
    - `fig_scatter_age_glucose`
    - `ax_scatter_age_glucose`

    ### Requisitos mínimos

    - usar las columnas `age` y `glucose_mg_dL`,
    - incluir título,
    - incluir etiqueta del eje *x*,
    - incluir etiqueta del eje *y*.
    """)
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    # Build the requested scatter plot and keep the required variable names.
    scatter_data_age_glucose = None
    fig_scatter_age_glucose = None
    ax_scatter_age_glucose = None
    return


@app.cell
def _():
    _tip_content = TipContent(
        items_raw=[
            r"""
    <Preparación de datos>
    Puedes crear primero una tabla pequeña con las dos columnas necesarias y luego eliminar filas faltantes.

    ```python
    scatter_data_age_glucose = df[["age", "glucose_mg_dL"]].dropna()
    ```
    """,
            r"""
    <Construcción del gráfico>
    Después de preparar los datos, utiliza `scatter()` indicando explícitamente el eje *x* y el eje *y*.
    """,
            r"""
    <Interpretación>
    Este gráfico no resume grupos: muestra observaciones individuales. Por eso las etiquetas deben dejar claro qué variable aparece en cada eje.
    """,
            r"""
    <solucion>
    ```python
    scatter_data_age_glucose = df[["age", "glucose_mg_dL"]].dropna()
    fig_scatter_age_glucose, ax_scatter_age_glucose = plt.subplots()
    ax_scatter_age_glucose.scatter(
    scatter_data_age_glucose["age"],
    scatter_data_age_glucose["glucose_mg_dL"],
    alpha=0.45,
    )
    ax_scatter_age_glucose.set_title("Edad y glucosa")
    ax_scatter_age_glucose.set_xlabel("Edad (años)")
    ax_scatter_age_glucose.set_ylabel("Glucosa (mg/dL)")
    ax_scatter_age_glucose.grid(alpha=0.2)
    fig_scatter_age_glucose
    ```
    """,
        ]
    )

    _tip_content.render()
    return


@app.cell
def _():
    _test_content = TestContent(
        items_raw=[
            r"""
    <Existencia de variables>
    ```python
    assert scatter_data_age_glucose is not None, "Debes definir `scatter_data_age_glucose`."
    assert fig_scatter_age_glucose is not None, "Debes definir `fig_scatter_age_glucose`."
    assert ax_scatter_age_glucose is not None, "Debes definir `ax_scatter_age_glucose`."
    print("Variables definidas correctamente.")
    ```
    """,
            r"""
    <Tipo de objeto>
    ```python
    from matplotlib.axes import Axes
    from matplotlib.figure import Figure

    assert isinstance(fig_scatter_age_glucose, Figure), (
    "`fig_scatter_age_glucose` debe ser una figura de Matplotlib."
    )
    assert isinstance(ax_scatter_age_glucose, Axes), (
    "`ax_scatter_age_glucose` debe ser un eje de Matplotlib."
    )
    print("Objetos de Matplotlib correctos.")
    ```
    """,
            r"""
    <Estructura de datos>
    ```python
    assert list(scatter_data_age_glucose.columns) == ["age", "glucose_mg_dL"], (
    "La tabla intermedia debe contener las columnas `age` y `glucose_mg_dL`."
    )
    assert scatter_data_age_glucose.shape[0] == df[["age", "glucose_mg_dL"]].dropna().shape[0], (
    "El número de filas debe coincidir con los casos no faltantes en ambas variables."
    )
    print("Datos preparados correctamente.")
    ```
    """,
            r"""
    <Etiquetas mínimas>
    ```python
    assert ax_scatter_age_glucose.get_title() != "", "El gráfico debe tener título."
    assert ax_scatter_age_glucose.get_xlabel() != "", "El eje x debe tener etiqueta."
    assert ax_scatter_age_glucose.get_ylabel() != "", "El eje y debe tener etiqueta."
    print("Etiquetas básicas presentes.")
    ```
    """,
        ]
    )

    _test_content.render()
    return


@app.cell
def _():
    mo.md(r"""
    ## 6) Cierre de la sesión

    En esta lección construiste un primer repertorio de visualización clínica con Matplotlib.

    ### Ideas que deben quedar firmes

    - **histograma** → distribución de una variable numérica,
    - **boxplot** → comparación de una variable numérica entre grupos,
    - **scatter plot** → relación visual entre dos variables numéricas.

    ### Regla práctica para seguir avanzando

    Antes de programar cualquier gráfico, formula una pregunta concreta:

    - **distribución**,
    - **comparación**,
    - o **relación**.

    Después elige el gráfico que mejor responda esa pregunta y añade solamente los elementos necesarios para que otra persona pueda leerlo con claridad.
    """)
    return


if __name__ == "__main__":
    app.run()
