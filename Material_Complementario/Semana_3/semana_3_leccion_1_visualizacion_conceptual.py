# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "altair==6.0.0",
#     "matplotlib==3.10.8",
#     "numpy==2.4.2",
#     "pandas==3.0.1",
#     "pytest==9.0.2",
#     "requests==2.32.5",
#     "seaborn==0.13.2",
# ]
# ///

import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")

with app.setup(hide_code=True):
    import altair as alt
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import seaborn as sns
    from setup import TipContent, TestContent, find_data_file

    plt.rcParams["figure.figsize"] = (10, 6)
    plt.rcParams["axes.spines.top"] = False
    plt.rcParams["axes.spines.right"] = False
    plt.rcParams["axes.titleweight"] = "bold"
    plt.rcParams["axes.titlesize"] = 13
    plt.rcParams["axes.labelsize"] = 11
    plt.rcParams["xtick.labelsize"] = 10
    plt.rcParams["ytick.labelsize"] = 10


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Semana 3 · Lección 1
    ## Principios fundamentales de visualización de datos clínicos

    Esta sesión introduce la visualización de datos como una herramienta de análisis, razonamiento y comunicación.

    El objetivo principal no es aprender una secuencia mecánica de instrucciones para producir gráficos, sino comprender qué decisiones hacen que una visualización sea adecuada, interpretable y persuasiva en un contexto académico o clínico.

    En términos analíticos, una visualización debe cumplir tres funciones:

    - permitir una lectura inicial de los datos,
    - facilitar la identificación de patrones relevantes,
    - y comunicar una idea con claridad a otra persona.

    A lo largo de esta sesión se trabajará con un mismo subconjunto de datos para mostrar que la calidad de una visualización no depende únicamente de la librería utilizada, sino del criterio con el que se seleccionan variables, escalas, colores, títulos, etiquetas y énfasis visual.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Propósito formativo de la sesión

    Al finalizar esta lección, el estudiante debería poder:

    - distinguir entre una visualización exploratoria y una visualización explicativa,
    - reconocer debilidades frecuentes en un gráfico,
    - justificar qué elementos deben mantenerse y cuáles deben eliminarse,
    - comprender cómo el color, el contraste y la jerarquía visual orientan la atención,
    - y corregir una visualización deficiente hasta convertirla en una representación clara y analíticamente útil.

    No partiremos de un gráfico ideal. Partiremos de un gráfico deficiente, lo evaluaremos críticamente y lo iremos ajustando paso a paso hasta llegar a una versión más adecuada.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Dataset de trabajo

    Durante esta unidad se utilizará un subconjunto de la encuesta SABE (Salud, Bienestar y Envejecimiento).

    Cada fila representa un individuo y el dataset contiene variables demográficas y clínicas que permiten formular preguntas exploratorias de interés en salud.

    En esta sesión se utilizarán principalmente las siguientes variables:

    - `age`: edad en años,
    - `sex`: sexo reportado,
    - `sbp_mmHg`: presión arterial sistólica,
    - `glucose_mg_dL`: glucosa,
    - `ldl_mg_dL`: colesterol LDL.

    El objetivo no será agotar el análisis del dataset, sino utilizarlo como base estable para discutir principios generales de visualización que posteriormente podrán transferirse a otros contextos.
    """)
    return


@app.cell
def _():
    data_path = find_data_file("public/dataset_clase_semana2_small.csv")
    df = pd.read_csv(data_path)

    expected_cols = {"age", "sex", "sbp_mmHg", "glucose_mg_dL", "ldl_mg_dL"}
    assert expected_cols.issubset(df.columns)
    assert not df.empty

    df.head()
    return data_path, df


@app.cell(hide_code=True)
def _(data_path):
    mo.md(rf"""
    ## Confirmación de carga

    El dataset utilizado en esta sesión se ha cargado correctamente desde:

    ```{data_path}```

    La verificación de la ruta de trabajo es un paso necesario en cualquier flujo reproducible de análisis, especialmente cuando el trabajo se realiza en entornos de notebooks o laboratorios virtuales.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Pregunta guía de la sesión

    Utilizaremos una pregunta concreta para organizar la discusión:

    **¿Cómo se relacionan los niveles de glucosa y colesterol LDL en esta muestra?**

    Esta pregunta es adecuada para una sesión introductoria porque obliga a pensar simultáneamente en:

    - el tipo de variables involucradas,
    - el tipo de gráfico que permite representarlas,
    - y la diferencia entre mostrar datos y comunicar una observación.

    Dado que se trata de dos variables numéricas medidas a nivel individual, una representación razonable de partida será un gráfico de dispersión.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## ¿Qué hacer antes de evaluar un gráfico?

    Antes de mirar un gráfico concreto, conviene establecer qué criterios usaremos para juzgarlo.

    Una visualización académicamente adecuada debería permitir responder, al menos, estas preguntas:

    1. ¿Queda claro qué variables se están representando?
    2. ¿Se entiende qué tipo de relación o patrón se quiere examinar?
    3. ¿La mirada del lector se dirige hacia lo importante?
    4. ¿Existen elementos que distraen sin aportar información?
    5. ¿El gráfico comunica solo datos, o también una idea?

    Estos criterios se utilizarán a lo largo de toda la sesión para analizar ejemplos progresivos.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Primera etapa: una visualización técnicamente válida pero conceptualmente débil

    A continuación se presenta un gráfico que, en términos técnicos, puede ejecutarse sin problema.

    Sin embargo, el hecho de que un gráfico sea técnicamente válido no implica que sea una visualización adecuada.

    - ¿Nos parece adecuada?
    - ¿Comunica algo relevante?
    """)
    return


@app.cell
def _(df):
    fig_mala, ax_mala = plt.subplots()

    ax_mala.scatter(
        df["glucose_mg_dL"],
        df["ldl_mg_dL"],
        color="limegreen",
        alpha=1.0,
    )

    ax_mala.set_title("Gráfico")
    ax_mala.set_xlabel("X")
    ax_mala.set_ylabel("Y")
    ax_mala.grid(True, alpha=0.8)

    mo.ui.matplotlib(fig_mala.gca())
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Diagnóstico inicial de la visualización deficiente

    Este gráfico presenta varias debilidades simultáneas:
    1. no identifica con precisión las variables representadas. Las etiquetas genéricas en los ejes obligan al lector a inferir el contenido del gráfico.

    2. el título no formula ninguna pregunta ni transmite una observación. La visualización existe, pero no comunica.

    3. el uso del color no tiene función analítica. El verde intenso atrae la atención, pero no diferencia grupos ni destaca una observación relevante.

    5. la cuadrícula es innecesariamente prominente. Compite visualmente con los datos y aumenta la carga cognitiva.

    El resultado es un gráfico **que muestra puntos**, pero **no orienta la interpretación**.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Primer principio: claridad semántica

    La primera obligación de una visualización es nombrar correctamente lo que representa.

    Una visualización puede ser visualmente atractiva y, aun así, fracasar si no permite responder con rapidez:

    - qué variable está en el eje horizontal,
    - qué variable está en el eje vertical,
    - y cuál es el asunto central del gráfico.

    Por esta razón, el primer ajuste no debe ser estético. Debe ser semántico.

    Antes de mejorar colores, estilos o énfasis, es necesario asegurar que el gráfico pueda leerse correctamente.
    """)
    return


@app.cell
def _(df):
    fig_semantica, ax_semantica = plt.subplots()

    ax_semantica.scatter(
        df["glucose_mg_dL"],
        df["ldl_mg_dL"],
        color="limegreen",
        alpha=1.0,
    )

    ax_semantica.set_title("Relación entre glucosa y colesterol LDL")
    ax_semantica.set_xlabel("Glucosa (mg/dL)")
    ax_semantica.set_ylabel("Colesterol LDL (mg/dL)")
    ax_semantica.grid(True, alpha=0.8)

    fig_semantica
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Qué mejoró y qué sigue siendo problemático

    El gráfico ya es semánticamente mejor que el anterior.

    Ahora el lector sabe con claridad qué variables están representadas y en qué unidades.

    Sin embargo, continúan presentes varios problemas:

    - todos los puntos compiten por la misma atención,
    - no hay jerarquía visual,
    - la cuadrícula sigue dominando innecesariamente el fondo,
    - y el título describe el contenido, pero no sugiere aún una lectura analítica.

    Esta distinción es importante: un gráfico puede estar correctamente etiquetado y aun así comunicar mal.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Segundo principio: eliminar elementos que no añaden información

    Una visualización no mejora por acumulación de componentes.

    En la mayoría de los casos, mejora cuando se eliminan elementos que no contribuyen a la lectura del patrón principal.

    Entre los elementos que con frecuencia conviene revisar o reducir se encuentran:

    - cuadrículas demasiado marcadas,
    - colores innecesariamente intensos,
    - bordes superfluos,
    - leyendas evitables,
    - títulos genéricos o redundantes.

    Esta etapa suele describirse como reducción del ruido visual.

    El propósito no es embellecer el gráfico, sino facilitar que el lector concentre su atención en los datos.
    """)
    return


@app.cell
def _(df):
    fig_limpia, ax_limpia = plt.subplots()

    ax_limpia.scatter(
        df["glucose_mg_dL"],
        df["ldl_mg_dL"],
        color="0.55",
        alpha=0.45,
    )

    ax_limpia.set_title("Relación entre glucosa y colesterol LDL")
    ax_limpia.set_xlabel("Glucosa (mg/dL)")
    ax_limpia.set_ylabel("Colesterol LDL (mg/dL)")
    ax_limpia.grid(False)

    fig_limpia
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Lectura crítica de la versión más limpia

    Esta versión es más sobria.

    La eliminación de la cuadrícula dominante y la reducción de la intensidad del color hacen que el fondo visual deje de competir con los datos.

    No obstante, todavía persiste una limitación importante: ***el gráfico es descriptivo, pero no explicativo***.

    Muestra la nube de puntos, pero no deja claro cuál es la observación que debería captar el lector.

    En otras palabras, hemos reducido ruido, pero todavía no hemos construido jerarquía visual.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Tercer principio: jerarquía visual

    Una buena visualización no presenta todos los elementos con el mismo peso.

    Si todo tiene la misma prominencia, nada destaca.

    La jerarquía visual permite responder implícitamente a esta pregunta:

    **¿Qué debe mirar primero el lector?**

    Esto puede lograrse mediante:

    - contraste,
    - color,
    - tamaño,
    - posición,
    - o anotaciones selectivas.

    La función de estas decisiones no es decorar, sino dirigir la percepción.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Construcción de un énfasis analítico

    Supongamos que el interés exploratorio de esta sesión no es toda la nube de puntos por igual, sino un subconjunto clínicamente más llamativo.

    Por ejemplo, individuos con glucosa claramente elevada.

    En ese caso, una estrategia razonable consiste en:

    - mantener el conjunto completo como contexto,
    - y destacar visualmente el subconjunto de interés.

    De este modo, el gráfico deja de ser un mero contenedor de puntos y empieza a orientar la interpretación.
    """)
    return


@app.cell
def _(df):
    valores_altos_glucosa = df[df["glucose_mg_dL"] >= 120].copy()

    fig_enfasis, ax_enfasis = plt.subplots()

    ax_enfasis.scatter(
        df["glucose_mg_dL"],
        df["ldl_mg_dL"],
        color="lightgrey",
        alpha=0.35,
        label="Resto de observaciones",
    )

    ax_enfasis.scatter(
        valores_altos_glucosa["glucose_mg_dL"],
        valores_altos_glucosa["ldl_mg_dL"],
        color="crimson",
        alpha=0.8,
        label="Glucosa elevada",
    )

    ax_enfasis.set_title("Relación entre glucosa y LDL con énfasis en glucosa elevada")
    ax_enfasis.set_xlabel("Glucosa (mg/dL)")
    ax_enfasis.set_ylabel("Colesterol LDL (mg/dL)")
    ax_enfasis.legend(frameon=False)
    ax_enfasis.grid(False)

    fig_enfasis
    return (valores_altos_glucosa,)


@app.cell(hide_code=True)
def _(valores_altos_glucosa):
    mo.md(rf"""
    ## Qué aporta esta versión

    Ahora la visualización establece una diferencia entre contexto y foco.

    El conjunto completo de observaciones sigue presente, lo que evita perder referencia global.

    Sin embargo, el subconjunto con glucosa elevada queda visualmente destacado.

    Este ajuste produce dos efectos importantes:

    - la lectura se vuelve más rápida,
    - y el gráfico comienza a sugerir una observación analítica.

    En esta muestra, el número de observaciones destacadas es **{len(valores_altos_glucosa)}**.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Cuarto principio: una visualización debe comunicar una idea

    Existe una diferencia importante entre un gráfico que muestra información y un gráfico que transmite un mensaje.

    Un gráfico meramente exploratorio puede ser suficiente para quien lo construye.

    Pero cuando la visualización está dirigida a otra persona, debe ayudar a responder la pregunta:

    > **¿Qué es lo que debería retener el lector después de observar este gráfico?**

    En este punto, el título deja de ser solo un rótulo y empieza a cumplir una función narrativa.
    """)
    return


@app.cell
def _(df, valores_altos_glucosa):
    fig_mensaje, ax_mensaje = plt.subplots()

    ax_mensaje.scatter(
        df["glucose_mg_dL"],
        df["ldl_mg_dL"],
        color="lightgrey",
        alpha=0.30,
    )

    ax_mensaje.scatter(
        valores_altos_glucosa["glucose_mg_dL"],
        valores_altos_glucosa["ldl_mg_dL"],
        color="crimson",
        alpha=0.85,
    )

    ax_mensaje.set_title(
        "Las observaciones con glucosa elevada concentran\n parte de los valores anormales LDL"
    )
    ax_mensaje.set_xlabel("Glucosa (mg/dL)")
    ax_mensaje.set_ylabel("Colesterol LDL (mg/dL)")
    ax_mensaje.grid(False)

    fig_mensaje
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## De un gráfico correcto a un gráfico útil

    La diferencia entre la versión anterior y esta no está en el tipo de gráfico.

    Sigue siendo un gráfico de dispersión.

    La diferencia se encuentra en la intención comunicativa.

    El gráfico ya no se limita a identificar dos variables. Ahora propone una lectura.

    En términos pedagógicos, esta es una distinción central:

    - un gráfico correcto puede limitarse a representar,
    - un gráfico útil debe también orientar la interpretación.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Demostración comparativa con otra librería: Seaborn

    Las decisiones conceptuales que se han discutido hasta este punto no dependen exclusivamente de Matplotlib.

    A continuación se presenta una visualización similar utilizando Seaborn.

    La finalidad no es enseñar sintaxis detallada, sino mostrar que los principios de claridad, reducción de ruido y énfasis visual pueden sostenerse también cuando se emplea una librería con mayor nivel de abstracción.
    """)
    return


@app.cell
def _(df):
    datos_sex_plot = df[["sex", "sbp_mmHg"]].dropna().copy()

    fig_seaborn, ax_seaborn = plt.subplots()

    sns.boxplot(
        data=datos_sex_plot,
        x="sex",
        y="sbp_mmHg",
        ax=ax_seaborn,
        width=0.55,
    )

    ax_seaborn.set_title("Distribución de presión arterial sistólica según sexo")
    ax_seaborn.set_xlabel("Sexo")
    ax_seaborn.set_ylabel("Presión arterial sistólica (mmHg)")
    ax_seaborn.grid(False)

    fig_seaborn
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Qué enseña este segundo ejemplo

    Este gráfico no responde a la pregunta sobre relación entre glucosa y LDL.

    Responde a otra pregunta:

    **¿Cómo cambia la distribución de la presión arterial sistólica entre grupos?**

    Esto permite introducir una idea adicional:

    el criterio principal para elegir un gráfico no es la librería, sino la estructura de la pregunta analítica.

    Si la pregunta cambia, también debe cambiar la representación.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Demostración comparativa con una tercera librería: Altair

    A continuación se presenta una visualización con Altair.

    El propósito de este ejemplo es mostrar que una misma intención analítica puede expresarse con una lógica distinta de construcción gráfica.

    Altair permite un enfoque declarativo y resulta especialmente útil cuando se desea una estructura más compacta o interacción.

    > Fijate como puedes inspeccionar los datos al pasar el cursor sobre los puntos.
    """)
    return


@app.cell
def _(df):
    datos_altair = df[["age", "glucose_mg_dL", "sex"]].dropna().copy()

    grafico_altair = (
        alt.Chart(datos_altair)
        .mark_circle(opacity=0.45)
        .encode(
            x=alt.X("age:Q", title="Edad (años)"),
            y=alt.Y("glucose_mg_dL:Q", title="Glucosa (mg/dL)"),
            color=alt.Color("sex:N", title="Sexo"),
            tooltip=["age", "glucose_mg_dL", "sex"],
        )
        .properties(
            title="Edad y glucosa con diferenciación por sexo",
            width=560,
            height=360,
        )
    )

    grafico_altair
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Lección transversal de los tres ejemplos

    Hasta ahora, se han utilizado tres librerías distintas:

    - [Matplotlib](https://matplotlib.org/stable/gallery/index.html),
    - [Seaborn](https://seaborn.pydata.org/examples/index.html),
    - [Altair](https://altair-viz.github.io/gallery/index.html#example-gallery).

    Sin embargo, la enseñanza principal no es el número de librerias usadas, o sus propiedades.

    La conclusión más importante es que una visualización adecuada requiere siempre las mismas decisiones conceptuales:

    - definir la pregunta,
    - elegir la estructura gráfica pertinente,
    - reducir el ruido visual,
    - construir jerarquía,
    - y comunicar un mensaje interpretable.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Criterios para evaluar críticamente un gráfico

    Antes de aceptar una visualización como adecuada, conviene revisar sistemáticamente los siguientes puntos:

    1. ¿Las variables están correctamente identificadas?
    2. ¿Las unidades son claras?
    3. ¿El tipo de gráfico corresponde a la pregunta analítica?
    4. ¿Hay elementos visuales que distraen sin aportar información?
    5. ¿Existe un foco interpretativo claro?
    6. ¿El gráfico comunica una observación o solo muestra datos?

    Esta lista puede utilizarse como guía de autoevaluación y como criterio para revisar trabajos ajenos.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Ejercicio final

    Un compañero del equipo ha generado la siguiente visualización para explorar la relación entre **edad** y **niveles de glucosa en sangre**. Sin embargo, como supervisor, consideras que la gráfica no comunica adecuadamente el mensaje y requiere mejoras sustanciales.

    Tu rol es revisar y ajustar esta visualización desde una perspectiva crítica y fundamentada.

    **Pregunta a responder:**

    - ¿Cuáles son las principales debilidades de esta gráfica en términos de claridad, interpretación y diseño?
    - ¿Cómo la rediseñarías para comunicar de forma más efectiva la relación entre edad y glucosa?

    Este ejercicio no busca creatividad gráfica libre.
    Busca aplicar de forma explícita los principios de visualización trabajados en la sesión.
    """)
    return


@app.cell
def _(df):
    fig_ejercicio, ax_ejercicio = plt.subplots()

    ax_ejercicio.scatter(
        df["age"],
        df["glucose_mg_dL"],
        color="orange",
        alpha=1.0,
    )

    ax_ejercicio.set_title("Gráfico")
    ax_ejercicio.set_xlabel("Eje X")
    ax_ejercicio.set_ylabel("Eje Y")
    ax_ejercicio.grid(True, alpha=0.9)

    fig_ejercicio
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Tarea del estudiante

    Corrige la visualización anterior para que comunique de forma más clara la relación entre **edad** y **glucosa en sangre**.

    Tu versión corregida debe cumplir con lo siguiente:

    - identificar claramente ambas variables,
    - presentar un diseño visual más limpio y legible,
    - incluir un mensaje principal explícito,
    - y resultar adecuada para comunicar una observación a otra persona.

    Imagina que esta versión será mostrada a un colega que no vio el proceso de construcción de la gráfica, por lo que debe poder interpretarla con facilidad.

    Variables de salida requeridas:

    - `datos_corregidos_plot`
    - `fig_grafico_corregido`
    - `ax_grafico_corregido`
    - `mensaje_principal`

    La variable `mensaje_principal` debe contener un texto breve que resuma la idea central que la visualización corregida intenta comunicar.
    """)
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    datos_corregidos_plot = None
    fig_grafico_corregido = None
    ax_grafico_corregido = None
    mensaje_principal = None
    return


@app.cell(hide_code=True)
def _():
    tip_content_final = TipContent(
        items_raw=[
            r"""
    <Revisión conceptual>
    Antes de modificar el gráfico, identifica explícitamente sus debilidades.

    En esta actividad, al menos deberías corregir:
    - etiquetas de ejes,
    - título,
    - ruido visual,
    - y claridad del mensaje.
    """,
            r"""
    <Preparación mínima de datos>
    Puedes empezar creando una tabla pequeña solo con las dos variables que vas a utilizar y eliminando valores faltantes.

    Esa tabla te ayudará a mantener el control sobre el contenido del gráfico.
    """,
            r"""
    <Jerarquía visual>
    No es obligatorio introducir grupos complejos, pero sí es importante que la versión corregida refleje una intención visual más clara que la del gráfico original.
    """,
            r"""
    <solucion>
    ```python
    datos_corregidos_plot = df[["age", "glucose_mg_dL"]].dropna()

    fig_grafico_corregido, ax_grafico_corregido = plt.subplots()
    ax_grafico_corregido.scatter(
        datos_corregidos_plot["age"],
        datos_corregidos_plot["glucose_mg_dL"],
        color="0.45",
        alpha=0.45,
    )
    ax_grafico_corregido.set_title(
        "La glucosa muestra alta dispersión a lo largo del rango de edad observado"
    )
    ax_grafico_corregido.set_xlabel("Edad (años)")
    ax_grafico_corregido.set_ylabel("Glucosa (mg/dL)")
    ax_grafico_corregido.grid(False)

    mensaje_principal = (
        "La visualización corregida busca mostrar la distribución conjunta de edad y "
        "glucosa con mayor claridad, reduciendo ruido visual y definiendo un mensaje explícito."
    )
    ```
    """,
        ]
    )

    tip_content_final.render()
    return


@app.cell(hide_code=True)
def _():
    test_content_final = TestContent(
        items_raw=[
            r"""
    <Existencia de variables>
    ``python
    assert datos_corregidos_plot is not None, "Debes definir `datos_corregidos_plot`."
    assert fig_grafico_corregido is not None, "Debes definir `fig_grafico_corregido`."
    assert ax_grafico_corregido is not None, "Debes definir `ax_grafico_corregido`."
    assert mensaje_principal is not None, "Debes definir `mensaje_principal`."
    print("Variables definidas correctamente.")
    ``
    """,
            r"""
    <Tipo de objeto>
    ``python
    from matplotlib.figure import Figure
    from matplotlib.axes import Axes

    assert isinstance(datos_corregidos_plot, pd.DataFrame), (
        "`datos_corregidos_plot` debe ser un DataFrame."
    )
    assert isinstance(fig_grafico_corregido, Figure), (
        "`fig_grafico_corregido` debe ser una figura de Matplotlib."
    )
    assert isinstance(ax_grafico_corregido, Axes), (
        "`ax_grafico_corregido` debe ser un eje de Matplotlib."
    )
    assert isinstance(mensaje_principal, str), (
        "`mensaje_principal` debe ser una cadena de texto."
    )
    print("Tipos correctos.")
    ``
    """,
            r"""
    <Estructura mínima del gráfico>
    ``python
    assert ax_grafico_corregido.get_title() != "", "El gráfico corregido debe tener título."
    assert ax_grafico_corregido.get_xlabel() != "", "El eje x debe tener etiqueta."
    assert ax_grafico_corregido.get_ylabel() != "", "El eje y debe tener etiqueta."
    print("Etiquetas mínimas presentes.")
    ``
    """,
            r"""
    <Preparación de datos>
    ``python
    assert datos_corregidos_plot.shape[1] == 2, (
        "`datos_corregidos_plot` debe contener dos columnas."
    )
    assert datos_corregidos_plot.notna().all().all(), (
        "`datos_corregidos_plot` no debería contener faltantes."
    )
    print("Datos preparados correctamente.")
    ``
    """,
        ],
        namespace=globals(),
    )

    test_content_final.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Cierre conceptual

    La calidad de una visualización no depende primordialmente de la sofisticación del código.

    Depende de la claridad con la que se responde a estas preguntas:

    - ¿qué se quiere mostrar?,
    - ¿qué debe ver primero el lector?,
    - ¿qué elementos pueden eliminarse?,
    - ¿qué idea debería quedar después de observar el gráfico?

    Una visualización adecuada en contextos clínicos y académicos no es simplemente correcta en términos técnicos.

    Es una representación que organiza la percepción para favorecer una interpretación precisa.
    """)
    return


if __name__ == "__main__":
    app.run()
