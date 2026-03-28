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
    import marimo as mo
    import numpy as np
    import pandas as pd

    # Graficas
    import matplotlib.pyplot as plt
    import seaborn as sns
    import altair as alt

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


@app.cell(hide_code=True)
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
    # iniciar la fig y los ejes:

    figura_pobre, eje_pobre = plt.subplots(figsize=(9, 5))

    eje_pobre.scatter(
        dataset["age"],
        dataset["glucose_mg_dL"],
        color="red",
        s=30,
        alpha=0.25,
        # edgecolor="black",
        label="Pacientes",
    )

    eje_pobre.grid(True, linewidth=0.2)
    eje_pobre.legend()

    eje_pobre.set_xlabel("edad")
    eje_pobre.set_ylabel("Glucosa Serica (mg/dL)")

    eje_pobre.set_title("Disbucion de glucosa con edad")
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
    # iniciar la fig y los ejes:

    figura_buena, eje_bueno = plt.subplots(figsize=(9, 5))

    dataset_alta_glucosa = dataset.query("glucose_mg_dL >= 120")
    dataset_normal_glucosa = dataset.query("glucose_mg_dL < 120")


    eje_bueno.scatter(
        dataset_alta_glucosa["age"],
        dataset_alta_glucosa["glucose_mg_dL"],
        color="red",
        s=30,
        alpha=0.25,
        # edgecolor="black",
        label="Pacientes con glucosa alterada",
    )

    eje_bueno.scatter(
        dataset_normal_glucosa["age"],
        dataset_normal_glucosa["glucose_mg_dL"],
        color="grey",
        s=30,
        alpha=0.25,
        # edgecolor="black",
        label="Pacientes con glucosa normal",
    )

    eje_bueno.axhline(120, color="blue", linestyle="--")

    eje_bueno.grid(True, linewidth=0.2)
    eje_bueno.legend()

    eje_bueno.set_xlabel("Edad (Años)")
    eje_bueno.set_ylabel("Glucosa Sérica (mg/dL)")

    eje_bueno.set_title(
        "Valores altos de glucosa se distribuyen \ncon mayor frecuencia en adultos mayores"
    )
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
    # Cálculo de proporción de hipertensión por grupo de edad
    # - assign: crea indicador booleano de hipertensión
    # - eq("Si"): True si el paciente tiene hipertensión
    hipertension_por_edad = (
        dataset.assign(tiene_hipertension=dataset["hypertension"].eq("Si"))
        # Agrupación por grupo de edad
        # - mean sobre booleanos → proporción
        .groupby("age_group", as_index=False)
        .agg(prop_hipertension=("tiene_hipertension", "mean"))
    )

    # Conversión a porcentaje
    # - facilita interpretación clínica
    hipertension_por_edad["prop_hipertension_pct"] = (
        hipertension_por_edad["prop_hipertension"] * 100
    ).round(1)

    # Resultado final
    hipertension_por_edad
    return (hipertension_por_edad,)


@app.cell
def _(hipertension_por_edad):
    # Crear figura y eje
    figura_barras_historia, eje_barras_historia = plt.subplots(figsize=(8, 5))

    # Gráfico de barras
    # - X: grupos de edad
    # - Y: porcentaje de hipertensión
    # - color: gradiente para sugerir progresión
    barras = eje_barras_historia.bar(
        hipertension_por_edad["age_group"],
        hipertension_por_edad["prop_hipertension_pct"],
        color=["#cbd5e1", "#94a3b8", "#64748b", "#0f172a"],
    )

    # Título y etiquetas
    # - ahora comunican un mensaje interpretativo
    eje_barras_historia.set_title("La hipertensión aumenta con la edad")
    eje_barras_historia.set_xlabel("Grupo de edad")
    eje_barras_historia.set_ylabel("Hipertensión (%)")

    # Escala y grid
    # - ylim(0, 100): coherente con porcentaje
    # - grid en eje Y: facilita comparación vertical
    eje_barras_historia.set_ylim(0, 100)
    eje_barras_historia.grid(axis="y", alpha=0.20)

    # Etiquetas sobre cada barra
    # - muestra valor exacto para reforzar lectura
    for barra in barras:
        altura = barra.get_height()
        eje_barras_historia.text(
            barra.get_x() + barra.get_width() / 2,
            altura + 2,
            f"{altura:.1f}%",
            ha="center",
            va="bottom",
            fontsize=10,
        )

    # Mostrar figura
    figura_barras_historia
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
def _(figura_linea):
    figura_linea
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
    # Cálculo de PAS media por edad
    # - groupby("age"): agrupa por cada edad individual
    # - mean: calcula el promedio de presión sistólica
    # - sort_values: asegura orden correcto para análisis/visualización
    pas_media_por_edad = (
        dataset.groupby("age", as_index=False)
        .agg(pas_media_mmHg=("sbp_mmHg", "mean"))
        .sort_values("age")
    )

    # Resultado final
    pas_media_por_edad
    return (pas_media_por_edad,)


@app.cell
def _(pas_media_por_edad):
    # Crear figura y eje
    figura_linea, eje_linea = plt.subplots(figsize=(10, 5))

    # Gráfico de línea
    # - X: edad
    # - Y: presión sistólica media
    # - marker: muestra cada punto observado
    # - markersize: tamaño discreto para no saturar
    # - linewidth: grosor de la línea
    # - color: tono sobrio para buena legibilidad
    eje_linea.plot(
        pas_media_por_edad["age"],
        pas_media_por_edad["pas_media_mmHg"],
        marker="o",
        markersize=3.5,
        linewidth=1.8,
        color="tab:blue",
    )

    # Título y etiquetas
    # - comunican tendencia clara
    eje_linea.set_title("La presión sistólica media aumenta con la edad")
    eje_linea.set_xlabel("Edad (años)")
    eje_linea.set_ylabel("PAS media (mmHg)")

    # Grid suave
    # - facilita lectura sin dominar la gráfica
    eje_linea.grid(alpha=0.20)

    # Mostrar figura
    figura_linea
    return (figura_linea,)


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
    figura_histograma, eje_histograma = plt.subplots(figsize=(9, 5))

    eje_histograma.hist(dataset["glucose_mg_dL"], bins=20, alpha=0.7)

    eje_histograma.axvline(120, color="green", linestyle=":", linewidth=3.5)

    eje_histograma.set_title(
        "Distribución de glucosa con línea de referencia clínica"
    )
    eje_histograma.set_xlabel("Glucosa (mg/dL)")
    eje_histograma.set_ylabel("Frecuencia")

    eje_histograma.grid(alpha=0.15)

    conteos_hist, bins_hist = np.histogram(
        dataset["glucose_mg_dL"].dropna(), bins=18
    )
    indice_pico = conteos_hist.argmax()

    x_pico = (bins_hist[indice_pico] + bins_hist[indice_pico + 1]) / 2
    y_pico = conteos_hist[indice_pico]

    eje_histograma.annotate(
        "Mayor concentración",
        xy=(x_pico, y_pico),
        xytext=(x_pico + 15, y_pico - 12),
        arrowprops={"arrowstyle": "->", "lw": 1.3},
        fontsize=10,
    )

    figura_histograma
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


@app.cell(hide_code=True)
def _(dataset):
    # Definir colores por grupo
    # - mapea categorías de diabetes a colores consistentes
    colores_diabetes = {"No": "#94a3b8", "Si": "#dc2626"}

    # Crear figura y eje
    figura_dispersion, eje_dispersion = plt.subplots(figsize=(9, 5))

    # Scatter por grupo
    # - groupby: separa por estado de diabetes
    # - color: refuerza diferenciación visual
    # - alpha: ayuda a manejar solapamiento
    for estado_diabetes, subconjunto in dataset.groupby("Diabetes"):
        eje_dispersion.scatter(
            subconjunto["age"],  # X: edad
            subconjunto["sbp_mmHg"],  # Y: presión sistólica
            label=estado_diabetes,
            color=colores_diabetes[estado_diabetes],
            alpha=0.75,
            s=36,
        )

    # Título y etiquetas
    # - comunican una hipótesis/lectura del gráfico
    eje_dispersion.set_title(
        "Pacientes con diabetes tienden a concentrarse en valores altos de PAS"
    )
    eje_dispersion.set_xlabel("Edad (años)")
    eje_dispersion.set_ylabel("PAS (mmHg)")

    # Leyenda y grid
    eje_dispersion.legend(title="Diabetes")
    eje_dispersion.grid(alpha=0.18)

    # Identificar valor máximo de PAS
    # - nlargest(1): fila con mayor presión sistólica
    punto_max_pas = dataset.nlargest(1, "sbp_mmHg").iloc[0]

    # Anotación del punto extremo
    # - resalta observación relevante en el dataset
    eje_dispersion.annotate(
        "Mayor PAS en la cohorte",
        xy=(punto_max_pas["age"], punto_max_pas["sbp_mmHg"]),
        xytext=(punto_max_pas["age"] - 22, punto_max_pas["sbp_mmHg"] + 10),
        arrowprops={"arrowstyle": "->", "lw": 1.3},
        fontsize=10,
    )

    # Mostrar figura
    figura_dispersion
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
def _(ejes_subplots):
    ejes_subplots
    return


@app.cell
def _(dataset):
    # Crear figura con dos subplots
    # - 1 fila, 2 columnas
    # - sharey=False: cada gráfico usa su propia escala
    figura_subplots, ejes_subplots = plt.subplots(
        1, 2, figsize=(12, 4.5), sharey=False
    )

    # ---------------------------
    # Histograma de PAS
    # ---------------------------
    # - bins: número de intervalos
    # - color: tono claro para lectura limpia
    ejes_subplots[0].hist(
        dataset["sbp_mmHg"],
        bins=16,
        color="#60a5fa",
        edgecolor="white",
    )

    # Título y etiquetas
    ejes_subplots[0].set_title("Distribución de PAS")
    ejes_subplots[0].set_xlabel("PAS (mmHg)")
    ejes_subplots[0].set_ylabel("Frecuencia")

    # ---------------------------
    # Orden de categorías educativas
    # ---------------------------
    # - define orden lógico para visualización
    orden_educacion = ["Primaria", "Secundaria", "Tecnico", "Universidad"]

    # Cálculo de LDL medio por nivel educativo
    # - groupby: agrupa por educación
    # - mean: promedio de LDL
    # - Categorical: asegura orden correcto en el eje X
    ldl_por_educacion = (
        dataset.groupby("education_grouped", as_index=False)
        .agg(ldl_medio=("ldl_mg_dL", "mean"))
        .assign(
            education_grouped=lambda d: pd.Categorical(
                d["education_grouped"],
                categories=orden_educacion,
                ordered=True,
            )
        )
        .sort_values("education_grouped")
    )

    # Gráfico de barras
    # - X: niveles educativos ordenados
    # - Y: LDL promedio
    ejes_subplots[1].bar(
        ldl_por_educacion["education_grouped"].astype(str),
        ldl_por_educacion["ldl_medio"],
        color="#334155",
    )

    # Título y etiquetas
    ejes_subplots[1].set_title("LDL medio por nivel educativo")
    ejes_subplots[1].set_xlabel("Nivel educativo")
    ejes_subplots[1].set_ylabel("LDL medio (mg/dL)")

    # Rotación de etiquetas
    # - mejora legibilidad si hay textos largos
    ejes_subplots[1].tick_params(axis="x", rotation=20)

    # Ajuste de layout
    figura_subplots.tight_layout()

    # Mostrar figura
    figura_subplots
    return (ejes_subplots,)


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
    # Crear figura y eje
    figura_hist_sns, eje_hist_sns = plt.subplots(figsize=(9, 5))

    # Histograma con separación por grupo (seaborn)
    # - x: variable numérica (glucosa)
    # - hue: separa por estado de diabetes
    # - bins: número de intervalos
    # - stat="count": frecuencias absolutas
    # - alpha: transparencia para comparar distribuciones
    # - multiple="layer": superpone histogramas
    sns.histplot(
        data=dataset,
        x="glucose_mg_dL",
        hue="Diabetes",
        bins=18,
        stat="count",
        alpha=0.55,
        multiple="layer",
        ax=eje_hist_sns,
    )

    # Título y etiquetas
    # - describen claramente la comparación entre grupos
    eje_hist_sns.set_title("Distribución de glucosa según estado de diabetes")
    eje_hist_sns.set_xlabel("Glucosa (mg/dL)")
    eje_hist_sns.set_ylabel("Frecuencia")

    # Mostrar figura
    figura_hist_sns
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
    # Definir orden de categorías
    # - asegura progresión lógica en el eje X
    orden_imc = ["Normal", "Sobrepeso", "Obesidad I", "Obesidad II"]

    # Crear figura y eje
    figura_boxplot, eje_boxplot = plt.subplots(figsize=(10, 5))

    # Boxplot por categoría de IMC
    # - x: variable categórica ordenada
    # - y: variable numérica (PAS)
    # - order: controla el orden de visualización
    # - color: tono uniforme para facilitar comparación
    sns.boxplot(
        data=dataset,
        x="bmi_category",
        y="sbp_mmHg",
        order=orden_imc,
        color="#93c5fd",
        ax=eje_boxplot,
    )

    # Título y etiquetas
    # - comunican tendencia observada
    eje_boxplot.set_title("La distribución de PAS aumenta con el IMC")
    eje_boxplot.set_xlabel("Categoría de IMC")
    eje_boxplot.set_ylabel("PAS (mmHg)")

    # Mostrar figura
    figura_boxplot
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
    # Crear figura y eje
    figura_regresion, eje_regresion = plt.subplots(figsize=(9, 5))

    # Regresión lineal + scatter (seaborn)
    # - x / y: variables numéricas (edad vs LDL)
    # - scatter_kws: personaliza puntos (alpha y tamaño)
    # - line_kws: personaliza la línea de regresión
    # - ajusta automáticamente un modelo lineal (OLS)
    sns.regplot(
        data=dataset,
        x="age",
        y="ldl_mg_dL",
        scatter_kws={
            "alpha": 0.45,  # reduce solapamiento
            "s": 35,  # tamaño moderado
        },
        line_kws={
            "color": "tab:red",  # destaca la tendencia
            "linewidth": 2,
        },
        ci=95,
        ax=eje_regresion,
    )

    # Título y etiquetas
    # - expresan la tendencia observada
    eje_regresion.set_title("El LDL tiende a aumentar moderadamente con la edad")
    eje_regresion.set_xlabel("Edad (años)")
    eje_regresion.set_ylabel("LDL (mg/dL)")

    # Mostrar figura
    figura_regresion
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
    # Construcción de tabla para heatmap
    # - assign: crea indicador de diabetes (booleano)
    # - groupby: agrupa por IMC y nivel educativo
    # - mean: proporción de diabetes
    # - pivot: reorganiza a formato matricial
    # - reindex: asegura orden lógico en filas y columnas
    tabla_heatmap = (
        dataset
        .assign(tiene_diabetes=dataset["Diabetes"].eq("Si"))
        .groupby(["bmi_category", "education_grouped"], as_index=False)
        .agg(
            prop_diabetes=("tiene_diabetes", "mean")
        )
        .pivot(
            index="bmi_category",
            columns="education_grouped",
            values="prop_diabetes"
        )
        .reindex(index=["Normal", "Sobrepeso", "Obesidad I", "Obesidad II"])
        .reindex(columns=["Primaria", "Secundaria", "Tecnico", "Universidad"])
    )

    # Crear figura y eje
    figura_heatmap, eje_heatmap = plt.subplots(figsize=(8, 5.5))

    # Heatmap con seaborn
    # - *100: convierte proporciones a porcentaje
    # - annot: muestra valores en cada celda
    # - fmt: formato numérico
    # - cmap: escala de color (intensidad = mayor prevalencia)
    # - linewidths: separación visual entre celdas
    sns.heatmap(
        tabla_heatmap * 100,
        annot=True,
        fmt=".1f",
        cmap="Reds",
        linewidths=0.5,
        cbar_kws={"label": "Diabetes (%)"},
        ax=eje_heatmap,
    )

    # Título y etiquetas
    # - describen la matriz comparativa
    eje_heatmap.set_title("Prevalencia de diabetes según IMC y nivel educativo")
    eje_heatmap.set_xlabel("Nivel educativo")
    eje_heatmap.set_ylabel("Categoría de IMC")

    # Mostrar figura
    figura_heatmap
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
    # Cálculo de hipertensión por sexo
    # - assign: crea indicador booleano
    # - eq("Si"): True si hay hipertensión
    hipertension_por_sexo = (
        dataset
        .assign(tiene_hipertension=dataset["hypertension"].eq("Si"))
    
        # Agrupación por sexo
        # - mean sobre booleanos → proporción
        .groupby("sex", as_index=False)
        .agg(
            prop_hipertension=("tiene_hipertension", "mean")
        )
    )

    # Conversión a porcentaje
    # - facilita interpretación
    hipertension_por_sexo["prop_hipertension_pct"] = (
        hipertension_por_sexo["prop_hipertension"] * 100
    ).round(1)

    # Resultado final
    hipertension_por_sexo
    return (hipertension_por_sexo,)


@app.cell
def _(hipertension_por_sexo):
    # Gráfico de barras con Altair
    # - Chart: usa el DataFrame resumido
    # - mark_bar: representación en barras
    grafico_barras_altair = (
        alt.Chart(hipertension_por_sexo)
        .mark_bar()
    
        # Codificación de variables
        .encode(
            # Eje X (categórico)
            x=alt.X("sex:N", title="Sexo"),
        
            # Eje Y (cuantitativo)
            # - escala fija 0–100 para interpretación como porcentaje
            y=alt.Y(
                "prop_hipertension_pct:Q",
                title="Hipertensión (%)",
                scale=alt.Scale(domain=[0, 100]),
            ),
        
            # Color por grupo
            # - refuerza diferenciación visual sin mostrar leyenda redundante
            color=alt.Color("sex:N", legend=None),
        
            # Tooltips interactivos
            # - muestran valor exacto al pasar el cursor
            tooltip=[
                alt.Tooltip("sex:N", title="Sexo"),
                alt.Tooltip(
                    "prop_hipertension_pct:Q",
                    title="Hipertensión (%)"
                ),
            ],
        )
    
        # Propiedades del gráfico
        .properties(
            title="Proporción de hipertensión por sexo",
            width=450,
            height=320,
        )
    )

    # Mostrar gráfico
    grafico_barras_altair
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
    # Cálculo de PAS media por grupo de edad
    # - groupby: agrupa por categorías de edad
    # - mean: promedio de presión sistólica
    pas_media_por_grupo_edad = (
        dataset
        .groupby("age_group", as_index=False)
        .agg(
            pas_media_mmHg=("sbp_mmHg", "mean")
        )
    
        # Redondeo
        # - mejora legibilidad para presentación
        .assign(
            pas_media_mmHg=lambda d: d["pas_media_mmHg"].round(1)
        )
    )

    # Resultado final
    pas_media_por_grupo_edad
    return (pas_media_por_grupo_edad,)


@app.cell
def _(pas_media_por_grupo_edad):
    # Gráfico de línea con Altair
    # - mark_line(point=True): línea + puntos por grupo
    grafico_linea_altair = (
        alt.Chart(pas_media_por_grupo_edad)
        .mark_line(point=True)
    
        # Codificación de variables
        .encode(
            # Eje X (categórico ordenado)
            # - sort: define progresión lógica de edad
            x=alt.X(
                "age_group:N",
                sort=["18-34", "35-49", "50-64", "65+"],
                title="Grupo de edad",
            ),
        
            # Eje Y (cuantitativo)
            # - PAS media
            y=alt.Y(
                "pas_media_mmHg:Q",
                title="PAS media (mmHg)"
            ),
        
            # Tooltips interactivos
            tooltip=[
                alt.Tooltip("age_group:N", title="Grupo de edad"),
                alt.Tooltip(
                    "pas_media_mmHg:Q",
                    title="PAS media"
                ),
            ],
        )
    
        # Propiedades del gráfico
        .properties(
            title="PAS media por grupo de edad",
            width=500,
            height=320
        )
    )

    # Mostrar gráfico
    grafico_linea_altair
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
    return


@app.cell
def _():
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
def _():
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
