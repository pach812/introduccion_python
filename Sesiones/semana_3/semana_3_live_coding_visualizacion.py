# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "altair==6.0.0",
#     "matplotlib==3.10.8",
#     "numpy==2.4.2",
#     "pandas==3.0.1",
#     "seaborn==0.13.2",
# ]
# ///

import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")

with app.setup(hide_code=True):
    import altair as alt
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import seaborn as sns

    sns.set_theme(style="whitegrid")
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
    # Semana 3 · Live Coding
    ## Visualización, storytelling y gramáticas gráficas

    Los temas de hoy son:
    1. técnicas para visualización y storytelling con datos,
    2. gráficas con Matplotlib,
    3. gráficas con Seaborn,
    4. gráficas con Altair.
    """)
    return


@app.cell
def _():
    rng = np.random.default_rng(2026)
    n = 20_000

    age = rng.integers(18, 85, size=n)
    sex = rng.choice(["Masculino", "Femenino"], size=n, p=[0.47, 0.53])
    education_grouped = rng.choice(
        ["Primaria", "Secundaria", "Tecnico", "Universidad"],
        size=n,
        p=[0.18, 0.34, 0.22, 0.26],
    )
    bmi_category = rng.choice(
        ["Normal", "Sobrepeso", "Obesidad I", "Obesidad II"],
        size=n,
        p=[0.30, 0.36, 0.23, 0.11],
    )

    sbp = (
        96
        + 0.62 * age
        + np.where(sex == "Masculino", 4.5, 0)
        + np.where(bmi_category == "Sobrepeso", 5, 0)
        + np.where(bmi_category == "Obesidad I", 9, 0)
        + np.where(bmi_category == "Obesidad II", 14, 0)
        + rng.normal(0, 9, size=n)
    )

    glucose = (
        74
        + 0.45 * age
        + np.where(bmi_category == "Sobrepeso", 8, 0)
        + np.where(bmi_category == "Obesidad I", 18, 0)
        + np.where(bmi_category == "Obesidad II", 28, 0)
        + rng.normal(0, 14, size=n)
    )

    ldl = (
        92
        + 0.32 * age
        + np.where(education_grouped == "Primaria", 12, 0)
        + np.where(education_grouped == "Universidad", -6, 0)
        + rng.normal(0, 18, size=n)
    )

    dataset = pd.DataFrame(
        {
            "patient_id": np.arange(1, n + 1),
            "age": age,
            "sex": sex,
            "education_grouped": education_grouped,
            "bmi_category": bmi_category,
            "sbp_mmHg": np.round(sbp, 1),
            "glucose_mg_dL": np.round(glucose, 1),
            "ldl_mg_dL": np.round(ldl, 1),
        }
    )

    dataset["hypertension"] = np.where(dataset["sbp_mmHg"] >= 140, "Si", "No")
    dataset["Diabetes"] = np.where(dataset["glucose_mg_dL"] >= 126, "Si", "No")
    dataset["high_cholesterol"] = np.where(dataset["ldl_mg_dL"] >= 160, "Si", "No")

    age_groups = pd.cut(
        dataset["age"],
        bins=[18, 35, 50, 65, 85],
        labels=["18-34", "35-49", "50-64", "65+"],
        right=False,
    )
    dataset["age_group"] = age_groups.astype(str)

    dataset
    return (dataset,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Dataset de trabajo

    Usaremos un dataset clínico sintético con variables continuas y categóricas.

    Variables principales:

    - `age`
    - `sex`
    - `sbp_mmHg`
    - `glucose_mg_dL`
    - `ldl_mg_dL`
    - `bmi_category`
    - `education_grouped`
    - `hypertension`
    - `Diabetes`
    - `high_cholesterol`

    La idea no es memorizar funciones aisladas, sino ver cómo cambia la lectura según la librería y según el diseño.
    """)
    return


@app.cell
def _(dataset):
    dataset.head(10)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Sección 1
    ## Técnicas para visualización y storytelling con los datos

    Esta sección recoge lo trabajado en visualización conceptual:

    - diferencia entre **mostrar datos** y **comunicar una observación**,
    - limpieza visual,
    - jerarquía,
    - énfasis,
    - y uso del título como mensaje.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Modelo general: Visualización y Storytelling

    Antes de hablar de librerías, hay que entender algo clave:

    > **una gráfica no es el objetivo, es un medio para comunicar una idea**
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Dos tipos de análisis

    ### Exploratorio

    - buscas patrones
    - pruebas hipótesis
    - generas muchas gráficas
    - no hay una narrativa clara todavía

    ### Explicativo

    - ya sabes qué quieres mostrar
    - reduces el ruido
    - construyes una historia
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Error más común

    > mostrar todo lo que analizaste

    Esto es incorrecto.

    El objetivo es:

    > **mostrar solo lo que responde la pregunta**
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Estructura de una buena visualización

    Toda gráfica debe responder:

    1. ¿Qué quiero que vean?
    2. ¿Qué quiero que entiendan?
    3. ¿Qué quiero que hagan?
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Principios clave

    - simplicidad > complejidad
    - claridad > estética
    - foco > cantidad
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Traducción a código

    El código no empieza con:

    "voy a hacer un plot"

    Empieza con:

    - definir pregunta
    - seleccionar variables
    - decidir tipo de gráfico
    - luego codificar
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Antes de elegir una librería

    Primero debe estar clara la pregunta.

    Tres preguntas distintas suelen requerir estructuras distintas:

    1. **Comparación** → ¿qué grupo tiene más o menos?
    2. **Distribución** → ¿cómo se concentran los valores?
    3. **Relación** → ¿cambian juntas dos variables?

    La librería importa, pero la lógica analítica importa más.
    """)
    return


@app.cell
def _(dataset):
    fig_poor, ax_poor = plt.subplots(figsize=(9, 5))

    ax_poor.scatter(
        dataset["age"],
        dataset["glucose_mg_dL"],
        color="red",
        s=70,
        edgecolor="black",
        alpha=0.9,
        label="Patients",
    )
    ax_poor.grid(True, linewidth=1.2)
    ax_poor.set_title("Age and glucose")
    ax_poor.set_xlabel("x")
    ax_poor.set_ylabel("y")
    ax_poor.legend()

    fig_poor
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Qué hace débil a un gráfico técnicamente válido

    El gráfico anterior se puede ejecutar, pero comunica mal.

    Problemas frecuentes:

    - etiquetas semánticamente pobres,
    - color fuerte sin propósito analítico,
    - leyenda innecesaria,
    - cuadrícula con demasiado protagonismo,
    - título descriptivo pero no interpretativo.

    Es un ejemplo útil de **gráfico correcto pero poco útil**.
    """)
    return


@app.cell
def _(dataset):
    data_high_glucose = dataset.query("glucose_mg_dL >= 126")
    data_context = dataset.query("glucose_mg_dL < 126")

    fig_story, ax_story = plt.subplots(figsize=(9, 5))

    ax_story.scatter(
        data_context["age"],
        data_context["glucose_mg_dL"],
        color="0.80",
        alpha=0.7,
        s=35,
    )
    ax_story.scatter(
        data_high_glucose["age"],
        data_high_glucose["glucose_mg_dL"],
        color="tab:red",
        alpha=0.9,
        s=40,
    )

    ax_story.axhline(126, color="tab:red", linestyle="--", linewidth=1.5)
    ax_story.set_title("Higher glucose values concentrate more often in older patients")
    ax_story.set_xlabel("Age (years)")
    ax_story.set_ylabel("Glucose (mg/dL)")
    ax_story.grid(alpha=0.20)

    ax_story.annotate(
        "Clinical threshold: 126 mg/dL",
        xy=(72, 126),
        xytext=(52, 168),
        arrowprops={"arrowstyle": "->", "lw": 1.4},
        fontsize=10,
    )

    fig_story
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Qué cambió en la versión mejorada

    Ahora el gráfico ya sugiere una lectura:

    - el conjunto completo queda como **contexto**,
    - el subconjunto relevante queda como **énfasis**,
    - la línea de referencia agrega significado,
    - el título ya comunica una idea,
    - y la anotación guía la atención.

    Aquí aparece la diferencia entre **exploración** y **storytelling**.
    """)
    return


@app.cell
def _(dataset):
    hypertension_by_age = (
        dataset.assign(has_hypertension=dataset["hypertension"].eq("Si"))
        .groupby("age_group", as_index=False)
        .agg(prop_hypertension=("has_hypertension", "mean"))
    )
    hypertension_by_age["prop_hypertension_pct"] = (
        hypertension_by_age["prop_hypertension"] * 100
    ).round(1)

    hypertension_by_age
    return (hypertension_by_age,)


@app.cell
def _(hypertension_by_age):
    fig_bar_story, ax_bar_story = plt.subplots(figsize=(8, 5))

    bars = ax_bar_story.bar(
        hypertension_by_age["age_group"],
        hypertension_by_age["prop_hypertension_pct"],
        color=["#cbd5e1", "#94a3b8", "#64748b", "#0f172a"],
    )

    ax_bar_story.set_title("Hypertension becomes more frequent as age group increases")
    ax_bar_story.set_xlabel("Age group")
    ax_bar_story.set_ylabel("Hypertension (%)")
    ax_bar_story.set_ylim(0, 100)
    ax_bar_story.grid(axis="y", alpha=0.20)

    for bar in bars:
        height = bar.get_height()
        ax_bar_story.text(
            bar.get_x() + bar.get_width() / 2,
            height + 2,
            f"{height:.1f}%",
            ha="center",
            va="bottom",
            fontsize=10,
        )

    fig_bar_story
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Ideas prácticas de storytelling gráfico

    Una versión útil del proceso sería:

    1. definir la pregunta,
    2. elegir la estructura visual correcta,
    3. limpiar ruido,
    4. destacar lo importante,
    5. escribir un título que exprese el mensaje.

    El gráfico no reemplaza la interpretación. La organiza.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Sección 2
    ## Gráficas con Matplotlib

    Aquí retomamos la lógica de construcción imperativa:

    - `Figure`
    - `Axes`
    - geometrías dibujadas paso a paso
    - títulos, ejes, referencias y anotaciones

    Matplotlib es ideal cuando quieres **control fino** sobre cada decisión visual.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Modelo general: Matplotlib

    Matplotlib es la base de toda la visualización en Python.

    ## Idea central

    > **Matplotlib es una librería imperativa**

    Tú le dices exactamente qué hacer, paso a paso.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Modelo general

    Hay tres componentes clave:

    ### 1. Figure

    - el contenedor completo
    - el "canvas"

    ### 2. Axes

    - el área donde se dibuja el gráfico
    - donde viven los datos

    ### 3. Plot

    - la representación visual de los datos
    """)
    return


@app.cell
def _(fig_line):
    fig_line
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Flujo típico

    1. crear figura
    2. crear ejes
    3. dibujar datos
    4. personalizar
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Ejemplo conceptual

    ```python
    fig, ax = plt.subplots()

    ax.plot(x, y)

    ax.set_title(...)
    ax.set_xlabel(...)
    ax.set_ylabel(...)
    ```
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Características clave

    - control total
    - muy flexible
    - más código
    - menos automatización
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Cuándo usarlo

    - cuando necesitas control fino
    - cuando quieres entender cómo funciona la gráfica
    - cuando otras librerías no son suficientes

    ## Riesgo

    > puedes crear gráficos muy malos si no sabes lo que haces, porque nada está automatizado
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Modelo mental de Matplotlib

    En Matplotlib conviene pensar en tres niveles:

    - **Figure**: el contenedor general,
    - **Axes**: la zona concreta donde dibujas,
    - **artists**: líneas, textos, barras, leyendas y anotaciones.

    No estás pidiendo un gráfico terminado.
    Estás **construyéndolo** explícitamente.
    """)
    return


@app.cell
def _(dataset):
    mean_sbp_by_age = (
        dataset.groupby("age", as_index=False)
        .agg(mean_sbp_mmHg=("sbp_mmHg", "mean"))
        .sort_values("age")
    )

    mean_sbp_by_age
    return (mean_sbp_by_age,)


@app.cell
def _(mean_sbp_by_age):
    fig_line, ax_line = plt.subplots(figsize=(10, 5))

    ax_line.plot(
        mean_sbp_by_age["age"],
        mean_sbp_by_age["mean_sbp_mmHg"],
        marker="o",
        markersize=3.5,
        linewidth=1.8,
        color="tab:blue",
    )

    ax_line.set_title("Mean systolic blood pressure increases with age")
    ax_line.set_xlabel("Age (years)")
    ax_line.set_ylabel("Mean SBP (mmHg)")
    ax_line.grid(alpha=0.20)

    fig_line
    return (fig_line,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Primer ejemplo Matplotlib

    Este patrón es útil cuando quieres mostrar una **evolución resumida**.

    Ideas para comentar en clase:

    - por qué la edad se ordena explícitamente,
    - qué aporta el marcador además de la línea,
    - por qué el eje y debe describir la métrica y no solo la variable.
    """)
    return


@app.cell
def _(dataset):
    fig_hist, ax_hist = plt.subplots(figsize=(9, 5))

    ax_hist.hist(
        dataset["glucose_mg_dL"].dropna(),
        bins=18,
        color="steelblue",
        edgecolor="white",
        alpha=0.9,
    )
    ax_hist.axvline(126, color="tab:red", linestyle="--", linewidth=2)
    ax_hist.set_title("Glucose distribution with diagnostic reference line")
    ax_hist.set_xlabel("Glucose (mg/dL)")
    ax_hist.set_ylabel("Frequency")
    ax_hist.grid(alpha=0.15)

    hist_counts, hist_bins = np.histogram(dataset["glucose_mg_dL"].dropna(), bins=18)
    peak_idx = hist_counts.argmax()
    x_peak = (hist_bins[peak_idx] + hist_bins[peak_idx + 1]) / 2
    y_peak = hist_counts[peak_idx]

    ax_hist.annotate(
        "Highest concentration",
        xy=(x_peak, y_peak),
        xytext=(x_peak + 15, y_peak + 12),
        arrowprops={"arrowstyle": "->", "lw": 1.3},
        fontsize=10,
    )

    fig_hist
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Histograma con referencia y anotación

    Este ejemplo junta tres ideas importantes de la lección de Matplotlib:

    - distribución,
    - línea de referencia,
    - anotación dirigida.

    Es un muy buen ejemplo de cómo pasar de una geometría simple a un gráfico más explicativo sin cambiar de librería.
    """)
    return


@app.cell
def _(dataset):
    diabetes_colors = {"No": "#94a3b8", "Si": "#dc2626"}

    fig_scatter, ax_scatter = plt.subplots(figsize=(9, 5))

    for diabetes_status, subset in dataset.groupby("Diabetes"):
        ax_scatter.scatter(
            subset["age"],
            subset["sbp_mmHg"],
            label=diabetes_status,
            color=diabetes_colors[diabetes_status],
            alpha=0.75,
            s=36,
        )

    ax_scatter.set_title("Patients with diabetes tend to accumulate at higher SBP values")
    ax_scatter.set_xlabel("Age (years)")
    ax_scatter.set_ylabel("SBP (mmHg)")
    ax_scatter.legend(title="Diabetes")
    ax_scatter.grid(alpha=0.18)

    top_sbp = dataset.nlargest(1, "sbp_mmHg").iloc[0]
    ax_scatter.annotate(
        "Highest SBP in the cohort",
        xy=(top_sbp["age"], top_sbp["sbp_mmHg"]),
        xytext=(top_sbp["age"] - 22, top_sbp["sbp_mmHg"] + 10),
        arrowprops={"arrowstyle": "->", "lw": 1.3},
        fontsize=10,
    )

    fig_scatter
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Scatter plot imperativo

    Este gráfico es útil para explicar:

    - relación entre dos variables continuas,
    - uso del color para grupos,
    - leyenda como apoyo,
    - anotaciones puntuales sobre observaciones extremas.

    Aquí se ve bien por qué Matplotlib es flexible para composiciones más personalizadas.
    """)
    return


@app.cell
def _(dataset):
    fig_subplots, axes_subplots = plt.subplots(1, 2, figsize=(12, 4.5), sharey=False)

    axes_subplots[0].hist(
        dataset["sbp_mmHg"],
        bins=16,
        color="#60a5fa",
        edgecolor="white",
    )
    axes_subplots[0].set_title("SBP distribution")
    axes_subplots[0].set_xlabel("SBP (mmHg)")
    axes_subplots[0].set_ylabel("Frequency")

    education_order = ["Primaria", "Secundaria", "Tecnico", "Universidad"]
    ldl_by_education = (
        dataset.groupby("education_grouped", as_index=False)
        .agg(mean_ldl=("ldl_mg_dL", "mean"))
        .assign(
            education_grouped=lambda d: pd.Categorical(
                d["education_grouped"],
                categories=education_order,
                ordered=True,
            )
        )
        .sort_values("education_grouped")
    )

    axes_subplots[1].bar(
        ldl_by_education["education_grouped"].astype(str),
        ldl_by_education["mean_ldl"],
        color="#334155",
    )
    axes_subplots[1].set_title("Mean LDL by education level")
    axes_subplots[1].set_xlabel("Education")
    axes_subplots[1].set_ylabel("Mean LDL (mg/dL)")
    axes_subplots[1].tick_params(axis="x", rotation=20)

    fig_subplots.tight_layout()
    fig_subplots
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Subplots

    Los subplots son útiles cuando quieres comparar estructuras distintas dentro de una misma figura.

    Puntos importantes para explicar:

    - cómo `plt.subplots()` devuelve figura y ejes,
    - cómo se indexan los ejes,
    - cuándo conviene usar un panel múltiple y cuándo conviene separar gráficos.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Sección 3
    ## Gráficas con Seaborn

    Seaborn abstrae muchas decisiones estadísticas comunes.

    En vez de construir todo manualmente, declaras relaciones frecuentes:

    - distribuciones,
    - comparación entre grupos,
    - relaciones bivariadas,
    - matrices resumidas.

    Es especialmente útil en **EDA** y en visualización estadística rápida.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Qué aporta Seaborn sobre Matplotlib

    Seaborn sigue usando Matplotlib por debajo, pero ofrece:

    - defaults visuales más consistentes,
    - funciones centradas en patrones estadísticos,
    - menos código mecánico para estructuras frecuentes.

    La pregunta cambia de “¿cómo dibujo esto?” a “¿qué relación quiero mostrar?”.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Modelo mental

    Tú especificas:

    - dataset
    - variables
    - tipo de relación

    Seaborn decide:

    - cómo representarlo
    - cómo estilizarlo
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Ejemplo conceptual

    ```python
    sns.scatterplot(
        data=df,
        x="age",
        y="glucose",
        hue="sex"
    )
    ```
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Qué hace Seaborn automáticamente

    - colores
    - leyendas
    - escalas
    - agrupaciones
    - agregaciones (en algunos casos)
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Tipos de relaciones comunes

    - distribución (histplot, kdeplot)
    - relación (scatterplot, lineplot)
    - comparación (boxplot, violinplot)
    - agregación (barplot)
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Ventajas

    - menos código
    - mejor estética por defecto
    - pensado para análisis

    ---

    ## Limitaciones

    - menos control fino que matplotlib
    - puede ser difícil personalizar casos complejos

    ---

    ## Cuándo usarlo

    - análisis exploratorio
    - relaciones estadísticas
    - visualización rápida y clara
    """)
    return


@app.cell
def _(dataset):
    fig_sns_hist, ax_sns_hist = plt.subplots(figsize=(9, 5))

    sns.histplot(
        data=dataset,
        x="glucose_mg_dL",
        hue="Diabetes",
        bins=18,
        stat="count",
        alpha=0.55,
        multiple="layer",
        ax=ax_sns_hist,
    )

    ax_sns_hist.set_title("Glucose distribution separated by diabetes status")
    ax_sns_hist.set_xlabel("Glucose (mg/dL)")
    ax_sns_hist.set_ylabel("Count")

    fig_sns_hist
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Histplot con hue

    Este ejemplo permite explicar:

    - distribución total vs. distribución por grupos,
    - cuándo un `hue` aporta lectura y cuándo la complica,
    - cómo Seaborn resuelve con poco código una tarea que en Matplotlib requeriría más manejo manual.
    """)
    return


@app.cell
def _(dataset):
    bmi_order = ["Normal", "Sobrepeso", "Obesidad I", "Obesidad II"]

    fig_box, ax_box = plt.subplots(figsize=(10, 5))

    sns.boxplot(
        data=dataset,
        x="bmi_category",
        y="sbp_mmHg",
        order=bmi_order,
        color="#93c5fd",
        ax=ax_box,
    )

    ax_box.set_title("SBP distribution shifts upward across BMI categories")
    ax_box.set_xlabel("BMI category")
    ax_box.set_ylabel("SBP (mmHg)")

    fig_box
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Boxplot para comparación entre grupos

    El boxplot es una buena estructura para hablar de:

    - mediana,
    - dispersión,
    - rango intercuartílico,
    - y posibles valores atípicos.

    Pedagógicamente también sirve para insistir en que no toda comparación entre grupos debe resolverse con barras.
    """)
    return


@app.cell
def _(dataset):
    fig_reg, ax_reg = plt.subplots(figsize=(9, 5))

    sns.regplot(
        data=dataset,
        x="age",
        y="ldl_mg_dL",
        scatter_kws={"alpha": 0.45, "s": 35},
        line_kws={"color": "tab:red", "linewidth": 2},
        ax=ax_reg,
    )

    ax_reg.set_title("LDL tends to increase moderately with age")
    ax_reg.set_xlabel("Age (years)")
    ax_reg.set_ylabel("LDL (mg/dL)")

    fig_reg
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Regplot

    `regplot` es útil para introducir una idea clave:

    - un scatter muestra puntos,
    - una línea suaviza la lectura de la tendencia.

    No reemplaza un modelo, pero sí ayuda a visualizar la dirección general de la relación.
    """)
    return


@app.cell
def _(dataset):
    heatmap_table = (
        dataset.assign(has_diabetes=dataset["Diabetes"].eq("Si"))
        .groupby(["bmi_category", "education_grouped"], as_index=False)
        .agg(prop_diabetes=("has_diabetes", "mean"))
        .pivot(index="bmi_category", columns="education_grouped", values="prop_diabetes")
        .reindex(index=["Normal", "Sobrepeso", "Obesidad I", "Obesidad II"])
        .reindex(columns=["Primaria", "Secundaria", "Tecnico", "Universidad"])
    )

    fig_heat_sns, ax_heat_sns = plt.subplots(figsize=(8, 5.5))

    sns.heatmap(
        heatmap_table * 100,
        annot=True,
        fmt=".1f",
        cmap="Reds",
        linewidths=0.5,
        cbar_kws={"label": "Diabetes (%)"},
        ax=ax_heat_sns,
    )

    ax_heat_sns.set_title("Diabetes prevalence matrix by BMI and education")
    ax_heat_sns.set_xlabel("Education level")
    ax_heat_sns.set_ylabel("BMI category")

    fig_heat_sns
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Heatmap en Seaborn

    Este ejemplo sirve para explicar cuándo una tabla matricial deja de ser legible y conviene convertirla en color.

    La idea no es decorar.
    La idea es facilitar la comparación de múltiples combinaciones de grupos.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Sección 4
    ## Gráficas con Altair

    > Altair trabaja con una gramática declarativa.

    En vez de construir el gráfico paso a paso, especificas:

    - datos,
    - marca,
    - encodings,
    - propiedades.

    Es una muy buena librería para enseñar estructura visual e interactividad ligera.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    > Altair es completamente diferente a Matplotlib y Seaborn.

    No escribes "cómo dibujar".

    Defines una gramática de visualización.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Modelo mental de Altair

    Piensa en cuatro bloques:

    1. `Chart(data)`
    2. `mark_*()`
    3. `encode(...)`
    4. `properties(...)`

    No describes cómo dibujar cada elemento.
    Describes **qué mapeo visual debe existir**.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Ejemplo conceptual

    ```python
    alt.Chart(df)
        .mark_point()
            .encode(
                x="age",
                y="glucose",
                color="sex"
            )
    ```
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Componentes clave

    ### 1. Data

    el dataset

    ### 2. Mark

    tipo de gráfico:
    - point
    - line
    - bar

    ### 3. Encoding

    cómo se mapean variables:
    - x
    - y
    - color
    - size
    - shape

    ### 4. Properties

    - título
    - dimensiones
    - interactividad
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Ventajas

    - muy expresivo
    - muy limpio
    - fácil de combinar
    - excelente para dashboards

    ---

    ## Diferencia fundamental

    Matplotlib:
    → dibuja

    Seaborn:
    → resume relaciones

    Altair:
    → **describe la visualización**
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Cuándo usarlo

    - visualizaciones interactivas
    - dashboards
    ## Riesgo

    > requiere cambiar la forma de pensar y adaptarse a una gramática diferente a la de Matplotlib y Seaborn
    """)
    return


@app.cell
def _(dataset):
    hypertension_by_sex = (
        dataset.assign(has_hypertension=dataset["hypertension"].eq("Si"))
        .groupby("sex", as_index=False)
        .agg(prop_hypertension=("has_hypertension", "mean"))
    )
    hypertension_by_sex["prop_hypertension_pct"] = (
        hypertension_by_sex["prop_hypertension"] * 100
    ).round(1)

    hypertension_by_sex
    return (hypertension_by_sex,)


@app.cell
def _(hypertension_by_sex):
    chart_alt_bar = (
        alt.Chart(hypertension_by_sex)
        .mark_bar()
        .encode(
            x=alt.X("sex:N", title="Sex"),
            y=alt.Y(
                "prop_hypertension_pct:Q",
                title="Hypertension (%)",
                scale=alt.Scale(domain=[0, 100]),
            ),
            color=alt.Color("sex:N", legend=None),
            tooltip=[
                alt.Tooltip("sex:N", title="Sex"),
                alt.Tooltip("prop_hypertension_pct:Q", title="Hypertension (%)"),
            ],
        )
        .properties(
            title="Hypertension proportion by sex",
            width=450,
            height=320,
        )
    )

    chart_alt_bar
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Barras declarativas

    Este ejemplo deja muy visible la estructura:

    - variable nominal en x,
    - variable cuantitativa en y,
    - color para reforzar grupo,
    - tooltip para detalle.

    Es muy útil para explicar la diferencia entre sintaxis imperativa y sintaxis declarativa.
    """)
    return


@app.cell
def _(dataset):
    sbp_by_age_group = (
        dataset.groupby("age_group", as_index=False)
        .agg(mean_sbp_mmHg=("sbp_mmHg", "mean"))
        .assign(mean_sbp_mmHg=lambda d: d["mean_sbp_mmHg"].round(1))
    )

    sbp_by_age_group
    return (sbp_by_age_group,)


@app.cell
def _(sbp_by_age_group):
    chart_alt_line = (
        alt.Chart(sbp_by_age_group)
        .mark_line(point=True)
        .encode(
            x=alt.X(
                "age_group:N",
                sort=["18-34", "35-49", "50-64", "65+"],
                title="Age group",
            ),
            y=alt.Y("mean_sbp_mmHg:Q", title="Mean SBP (mmHg)"),
            tooltip=[
                alt.Tooltip("age_group:N", title="Age group"),
                alt.Tooltip("mean_sbp_mmHg:Q", title="Mean SBP"),
            ],
        )
        .properties(title="Mean SBP by age group", width=500, height=320)
    )

    chart_alt_line
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Línea declarativa

    Aquí conviene remarcar una idea docente importante:

    El orden lógico del eje x no siempre aparece automáticamente.
    En variables categóricas ordenadas, conviene declarar el orden explícitamente.
    """)
    return


@app.cell
def _(dataset):
    alt_heat_table = (
        dataset.groupby(["bmi_category", "Diabetes"], as_index=False)
        .agg(mean_ldl_mg_dL=("ldl_mg_dL", "mean"))
        .assign(mean_ldl_mg_dL=lambda d: d["mean_ldl_mg_dL"].round(1))
    )

    alt_heat_table
    return (alt_heat_table,)


@app.cell
def _(alt_heat_table):
    base_alt_heat = alt.Chart(alt_heat_table).encode(
        x=alt.X("Diabetes:N", title="Diabetes"),
        y=alt.Y(
            "bmi_category:N",
            title="BMI category",
            sort=["Normal", "Sobrepeso", "Obesidad I", "Obesidad II"],
        ),
    )

    rect_alt_heat = base_alt_heat.mark_rect().encode(
        color=alt.Color("mean_ldl_mg_dL:Q", title="Mean LDL (mg/dL)")
    )

    text_alt_heat = base_alt_heat.mark_text(fontSize=12).encode(
        text=alt.Text("mean_ldl_mg_dL:Q", format=".1f"),
        color=alt.condition(
            alt.datum.mean_ldl_mg_dL >= 130,
            alt.value("white"),
            alt.value("black"),
        ),
    )

    chart_alt_heatmap = (rect_alt_heat + text_alt_heat).properties(
        title="Mean LDL by BMI category and diabetes status",
        width=340,
        height=220,
    )

    chart_alt_heatmap
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Heatmap con capas

    Altair es muy expresivo cuando quieres superponer capas:

    - una capa para la geometría base,
    - otra capa para texto,
    - y una regla clara para el contraste del texto.

    Esto ayuda a explicar composición y jerarquía dentro de una gramática declarativa.
    """)
    return


@app.cell
def _(dataset):
    chart_alt_facet = (
        alt.Chart(dataset)
        .mark_bar()
        .encode(
            x=alt.X("sbp_mmHg:Q", bin=alt.Bin(maxbins=16), title="SBP (binned)"),
            y=alt.Y("count():Q", title="Count"),
            tooltip=[alt.Tooltip("count():Q", title="Count")],
        )
        .properties(width=220, height=160)
        .facet(column=alt.Column("sex:N", title="Sex"))
        .resolve_scale(y="independent")
    )

    chart_alt_facet
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Facets

    Los facets son especialmente útiles cuando:

    - un solo gráfico empieza a mezclar demasiadas cosas,
    - quieres comparar el mismo patrón en subgrupos,
    - quieres mantener la misma estructura visual en todos los paneles.

    En docencia, ayudan mucho a discutir comparación controlada.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Cierre de la sesión

    Resumen conceptual de la semana:

    ### 1. Storytelling y criterios visuales
    - un gráfico no debe solo mostrar datos,
    - debe orientar una lectura.

    ### 2. Matplotlib
    - conviene cuando necesitas control fino y construcción manual.

    ### 3. Seaborn
    - conviene cuando quieres explorar relaciones estadísticas frecuentes con menos fricción.

    ### 4. Altair
    - conviene cuando quieres expresar la lógica visual de manera declarativa y con interactividad ligera.

    La idea más importante de la semana no es memorizar sintaxis.

    La idea es aprender a decidir:

    - qué estructura usar,
    - qué reducir,
    - qué destacar,
    - y qué mensaje debería quedar después de mirar el gráfico.
    """)
    return


if __name__ == "__main__":
    app.run()
