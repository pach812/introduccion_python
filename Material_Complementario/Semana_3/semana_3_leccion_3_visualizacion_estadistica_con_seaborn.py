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

__generated_with = "0.20.4"
app = marimo.App(width="medium")

with app.setup(hide_code=True):
    import marimo as mo
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    from matplotlib.axes import Axes
    from matplotlib.figure import Figure

    from setup import TipContent, TestContent, find_data_file


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Semana 3 · Lección 3
    ## Visualización estadística con Seaborn

    **Propósito de la sesión:** aprender a construir visualizaciones estadísticas declarativas con Seaborn para comparar grupos, explorar distribuciones y representar relaciones entre variables con menor fricción que en Matplotlib puro.

    En la lección anterior trabajaste el enfoque imperativo de Matplotlib:

    - crear `Figure` y `Axes`,
    - dibujar manualmente,
    - agregar líneas, texto y anotaciones,
    - controlar el gráfico paso a paso.

    En esta lección cambiaremos de nivel de abstracción:

    > pasamos de **decir cómo dibujar** a **declarar qué relación queremos mostrar**.

    Seaborn no reemplaza el razonamiento analítico.

    Lo que hace es facilitar tareas como:

    - comparar distribuciones entre grupos,
    - codificar categorías con color,
    - agregar capas estadísticas,
    - construir paneles múltiples de forma consistente.

    Idea central:

    > **menos código no significa menos pensamiento; significa que el esfuerzo puede concentrarse más en la pregunta analítica que en la mecánica del dibujo.**
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
    assert set(numeric_cols).issubset(df.columns)

    df.head()
    return categorical_cols, df, numeric_cols


@app.cell(hide_code=True)
def _(df):
    mo.md(f"""
    ## Dataset de trabajo

    Utilizaremos el mismo dataset clínico de las lecciones anteriores para mantener continuidad conceptual y comparabilidad entre estrategias de visualización.

    El dataset contiene **{df.shape[0]} registros** y **{df.shape[1]} variables**.

    Cada fila representa un individuo y contiene variables demográficas, factores de riesgo y mediciones clínicas.

    Variables que usaremos con más frecuencia en esta sesión:

    - `age`
    - `sbp_mmHg`
    - `glucose_mg_dL`
    - `ldl_mg_dL`
    - `sex`
    - `hypertension`
    - `Diabetes`
    - `bmi_category`

    En esta lección no cambia el dominio del problema.

    Lo que cambia es la forma de representar preguntas como:

    - ¿cómo se distribuye una variable dentro de cada grupo?
    - ¿cómo se comparan dos categorías?
    - ¿cómo cambia una relación al introducir una tercera variable?
    - ¿cuándo conviene usar varios paneles en lugar de una sola figura?
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
    ## 1) Cambio conceptual: de instrucciones a relaciones

    En Matplotlib trabajabas de esta forma:

    ```python
    fig, ax = plt.subplots()
    ax.scatter(...)
    ax.set_title(...)
    ax.set_xlabel(...)
    ```

    Allí la lógica principal era:

    - crear el eje,
    - elegir la geometría,
    - y construir manualmente el gráfico.

    En Seaborn, el patrón suele ser:

    ```python
    sns.<grafica>(data=df, x="variable_1", y="variable_2")
    ```

    Aquí la lógica cambia:

    - das un dataset,
    - declaras qué variable va en cada dimensión,
    - y Seaborn genera una representación coherente por defecto.

    Esto es útil porque desplaza la atención desde el detalle mecánico hacia la pregunta analítica.

    Idea clave:

    > **Seaborn es especialmente útil cuando quieres expresar una relación entre variables de forma rápida, consistente y estadísticamente informativa.**
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 2) Primer ejemplo: scatterplot declarativo

    Empezaremos con una relación sencilla entre dos variables numéricas:

    - presión arterial sistólica (`sbp_mmHg`)
    - glucosa (`glucose_mg_dL`)

    La pregunta analítica es:

    > ¿existe algún patrón conjunto visible entre ambas variables?

    Aquí Seaborn se apoya en Matplotlib, pero nos permite construir el gráfico con una sintaxis más centrada en datos y variables.
    """)
    return


@app.cell
def _(df):
    # Crear figura y eje
    fig_scatter_base, ax_scatter_base = plt.subplots(figsize=(7, 4.5))

    # Scatter plot con seaborn
    # - data: DataFrame de origen
    # - x: variable en eje X (PAS)
    # - y: variable en eje Y (glucosa)
    # - ax: eje donde se dibuja
    sns.scatterplot(
        data=df,
        x="sbp_mmHg",
        y="glucose_mg_dL",
        ax=ax_scatter_base,
    )

    # Título y etiquetas
    ax_scatter_base.set_title("Relación entre PAS y glucosa")
    ax_scatter_base.set_xlabel("PAS (mmHg)")
    ax_scatter_base.set_ylabel("Glucosa (mg/dL)")

    # Ajuste de layout
    fig_scatter_base.tight_layout()

    # Mostrar figura
    fig_scatter_base
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 3) Codificación estética: `hue`, `style` y `size`

    Una de las ventajas más importantes de Seaborn es que permite agregar dimensiones adicionales del dataset usando codificaciones visuales.

    Algunas de las más frecuentes son:

    - `hue`: cambia color según una variable,
    - `style`: cambia forma o estilo,
    - `size`: cambia tamaño.

    En esta sesión nos centraremos sobre todo en `hue`, porque es una de las formas más útiles de introducir una variable categórica adicional sin tener que construir varios gráficos manualmente.

    Ejemplo:

    ```python
    sns.scatterplot(
        data=df,
        x="sbp_mmHg",
        y="glucose_mg_dL",
        hue="Diabetes"
    )
    ```

    Esto permite responder una pregunta distinta:

    > ¿la relación entre PAS y glucosa se distribuye igual según estado de diabetes?
    """)
    return


@app.cell
def _(df):
    # Crear figura y eje
    fig_scatter_hue, ax_scatter_hue = plt.subplots(figsize=(7, 4.5))

    # Scatter plot con agrupación por color (hue)
    # - x / y: variables numéricas
    # - hue: separa puntos por categoría (estado de diabetes)
    # - alpha: transparencia para manejar solapamiento
    sns.scatterplot(
        data=df,
        x="sbp_mmHg",
        y="glucose_mg_dL",
        hue="Diabetes",
        alpha=0.75,
        ax=ax_scatter_hue,
    )

    # Título y etiquetas
    ax_scatter_hue.set_title("Relación entre PAS y glucosa según diabetes")
    ax_scatter_hue.set_xlabel("PAS (mmHg)")
    ax_scatter_hue.set_ylabel("Glucosa (mg/dL)")

    # Ajuste de layout
    fig_scatter_hue.tight_layout()

    # Mostrar figura
    fig_scatter_hue
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 4) Distribuciones con Seaborn: `histplot`

    En Matplotlib ya trabajaste histogramas.

    En Seaborn, `histplot` mantiene esa idea pero añade una sintaxis más integrada con dataframes y la posibilidad de combinar capas estadísticas con más facilidad.

    Ejemplo básico:

    ```python
    sns.histplot(data=df, x="glucose_mg_dL")
    ```

    Y si quieres acompañarlo con una curva suavizada:

    ```python
    sns.histplot(data=df, x="glucose_mg_dL", kde=True)
    ```

    Esto no cambia la pregunta de fondo.

    Sigue siendo:

    > ¿cómo se distribuye una variable?

    Pero la representación puede ser más compacta y expresiva.
    """)
    return


@app.cell
def _(df):
    # Crear figura y eje
    fig_hist_kde, ax_hist_kde = plt.subplots(figsize=(7, 4.5))

    # Histograma + densidad (KDE)
    # - x: variable numérica
    # - bins: número de intervalos del histograma
    # - kde=True: añade curva de densidad suavizada
    # - ax: eje donde se dibuja
    sns.histplot(
        data=df,
        x="glucose_mg_dL",
        kde=True,
        bins=18,
        ax=ax_hist_kde,
    )

    # Título y etiquetas
    ax_hist_kde.set_title("Distribución de glucosa (histograma + densidad)")
    ax_hist_kde.set_xlabel("Glucosa (mg/dL)")
    ax_hist_kde.set_ylabel("Frecuencia")

    # Ajuste de layout
    fig_hist_kde.tight_layout()

    # Mostrar figura
    fig_hist_kde
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 5) Comparar distribuciones entre grupos: `hue` en histogramas

    Un paso natural después de mirar una distribución total es preguntarse:

    > ¿se distribuye igual esta variable en todos los grupos?

    Aquí `hue` vuelve a ser útil.

    Ejemplo:

    ```python
    sns.histplot(
        data=df,
        x="glucose_mg_dL",
        hue="sex"
    )
    ```

    Esto puede superponer distribuciones o separarlas, según cómo se configure el gráfico.

    Interpretación importante:

    - un solo panel facilita comparación rápida,
    - pero demasiada superposición puede dificultar la lectura.

    Más adelante resolveremos esto con facets.
    """)
    return


@app.cell
def _(df):
    # Crear figura y eje
    fig_hist_hue, ax_hist_hue = plt.subplots(figsize=(7.5, 4.5))

    # Histograma con separación por grupo (hue)
    # - x: variable numérica
    # - hue: divide por categorías (sexo)
    # - bins: número de intervalos
    # - alpha: transparencia para comparar distribuciones
    # - element="step": contornos en lugar de barras sólidas
    # - stat="count": muestra frecuencias absolutas
    # - common_norm=False: evita normalización conjunta entre grupos
    sns.histplot(
        data=df,
        x="glucose_mg_dL",
        hue="sex",
        bins=15,
        alpha=0.5,
        element="step",
        stat="count",
        common_norm=False,
        ax=ax_hist_hue,
    )

    # Título y etiquetas
    ax_hist_hue.set_title("Distribución de glucosa según sexo")
    ax_hist_hue.set_xlabel("Glucosa (mg/dL)")
    ax_hist_hue.set_ylabel("Frecuencia")

    # Ajuste de layout
    fig_hist_hue.tight_layout()

    # Mostrar figura
    fig_hist_hue
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 6) Comparación entre grupos: `boxplot`

    Cuando quieres comparar distribuciones entre categorías y no solo observar la forma general, el `boxplot` es muy útil.

    Ejemplo:

    ```python
    sns.boxplot(data=df, x="sex", y="glucose_mg_dL")
    ```

    Esto permite resumir por grupo:

    - mediana,
    - dispersión central,
    - rango intercuartílico,
    - posibles valores atípicos.

    La pregunta analítica aquí es distinta del histograma.

    Ya no es solo:

    > ¿cómo se distribuye?

    sino también:

    > ¿cómo cambia esa distribución entre grupos?
    """)
    return


@app.cell
def _(df):
    # Crear figura y eje
    fig_box, ax_box = plt.subplots(figsize=(7, 4.5))

    # Boxplot por grupo
    # - x: variable categórica (sexo)
    # - y: variable numérica (glucosa)
    # - resume: mediana, cuartiles y posibles outliers
    sns.boxplot(
        data=df,
        x="sex",
        y="glucose_mg_dL",
        ax=ax_box,
    )

    # Título y etiquetas
    ax_box.set_title("Glucosa por sexo")
    ax_box.set_xlabel("Sexo")
    ax_box.set_ylabel("Glucosa (mg/dL)")

    # Ajuste de layout
    fig_box.tight_layout()

    # Mostrar figura
    fig_box
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 7) Combinar resumen y observaciones: `boxplot` + `stripplot`

    Un boxplot resume bien, pero también puede ocultar cuántos datos hay y cómo se concentran exactamente las observaciones.

    Una estrategia útil es combinar:

    - una capa de resumen (`boxplot`),
    - y una capa de puntos individuales (`stripplot`).

    Esto ayuda a no perder completamente la granularidad del dataset.

    Idea clave:

    > **combinar capas puede mejorar mucho la interpretación cuando cada capa cumple una función distinta.**
    """)
    return


@app.cell
def _(df):
    # Crear figura y eje
    fig_box_strip, ax_box_strip = plt.subplots(figsize=(7, 4.5))

    # Boxplot (resumen estadístico)
    # - muestra mediana, cuartiles y outliers por grupo
    sns.boxplot(
        data=df,
        x="sex",
        y="glucose_mg_dL",
        ax=ax_box_strip,
    )

    # Stripplot (datos individuales)
    # - superpone cada observación
    # - alpha: reduce saturación visual
    # - color: uniforme para no competir con el boxplot
    sns.stripplot(
        data=df,
        x="sex",
        y="glucose_mg_dL",
        alpha=0.35,
        color="black",
        ax=ax_box_strip,
    )

    # Título y etiquetas
    ax_box_strip.set_title("Glucosa por sexo con puntos individuales")
    ax_box_strip.set_xlabel("Sexo")
    ax_box_strip.set_ylabel("Glucosa (mg/dL)")

    # Ajuste de layout
    fig_box_strip.tight_layout()

    # Mostrar figura
    fig_box_strip
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 8) Estimación estadística visual: `barplot`

    En Matplotlib, un gráfico de barras suele construirse a partir de una tabla ya resumida.

    En Seaborn, `barplot` puede calcular internamente una agregación, normalmente la media, y mostrarla por grupo.

    Ejemplo:

    ```python
    sns.barplot(data=df, x="sex", y="sbp_mmHg")
    ```

    Esto responde una pregunta como:

    > ¿cuál es la PAS media por sexo?

    Importante:

    - aquí la barra no representa conteos,
    - representa una estimación resumen.

    Por eso conviene usar este tipo de gráfico con conciencia de qué estadístico se está mostrando.
    """)
    return


@app.cell
def _(df):
    # Crear figura y eje
    fig_bar_mean, ax_bar_mean = plt.subplots(figsize=(7, 4.5))

    # Barplot con estimador
    # - x: variable categórica (sexo)
    # - y: variable numérica (PAS)
    # - estimator="mean": calcula la media por grupo
    #   Otros estimadores comunes:
    #   - "median": robusto a outliers
    #   - "sum": total acumulado
    #   - "min" / "max": valores extremos
    #   - np.std: variabilidad (desviación estándar)
    #   - np.var: varianza
    #   - np.percentile (con wrapper): percentiles específicos (ej. p75)
    # - errorbar="ci": intervalo de confianza (por defecto 95%)
    sns.barplot(
        data=df,
        x="sex",
        y="sbp_mmHg",
        estimator="mean",
        errorbar="ci",
        ax=ax_bar_mean,
    )

    # Título y etiquetas
    ax_bar_mean.set_title("PAS media por sexo")
    ax_bar_mean.set_xlabel("Sexo")
    ax_bar_mean.set_ylabel("PAS media estimada (mmHg)")

    # Ajuste de layout
    fig_bar_mean.tight_layout()

    # Mostrar figura
    fig_bar_mean
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 9) Relación con tendencia: `regplot`

    Cuando quieres ver no solo los puntos, sino también una tendencia general, Seaborn ofrece `regplot`.

    Ejemplo:

    ```python
    sns.regplot(data=df, x="age", y="sbp_mmHg")
    ```

    Esto agrega una línea de ajuste y una banda de incertidumbre.

    Interpretación cuidadosa:

    - el gráfico sugiere tendencia,
    - no demuestra causalidad,
    - y no reemplaza un análisis formal.

    Pero como herramienta exploratoria, es muy útil para comunicar dirección general de asociación.
    """)
    return


@app.cell
def _(df):
    # Crear figura y eje
    fig_reg, ax_reg = plt.subplots(figsize=(7, 4.5))

    # Regresión lineal + scatter
    # - x / y: variables numéricas
    # - scatter_kws: personaliza puntos (alpha reduce solapamiento)
    # - line_kws: personaliza la línea de regresión
    # - ajusta automáticamente un modelo lineal (OLS)
    sns.regplot(
        data=df,
        x="age",
        y="sbp_mmHg",
        scatter_kws={"alpha": 0.45},
        line_kws={"linewidth": 2},
        ax=ax_reg,
    )

    # Título y etiquetas
    ax_reg.set_title("Tendencia entre edad y PAS")
    ax_reg.set_xlabel("Edad (años)")
    ax_reg.set_ylabel("PAS (mmHg)")

    # Ajuste de layout
    fig_reg.tight_layout()

    # Mostrar figura
    fig_reg
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 10) Facets con Seaborn

    En la lección 2 trabajaste paneles múltiples con `plt.subplots(...)`.

    Seaborn permite automatizar esa lógica para ciertas tareas usando funciones de nivel figura, como `displot`, `catplot` o `relplot`.

    Ejemplo:

    ```python
    sns.displot(data=df, x="glucose_mg_dL", col="sex")
    ```

    Esto crea un panel por grupo.

    Ventajas:

    - evita superposición excesiva,
    - mantiene una estructura visual consistente,
    - facilita comparación directa.

    Idea clave:

    > **cuando una sola figura empieza a mezclar demasiadas capas, separar en facets suele mejorar la lectura.**
    """)
    return


@app.cell
def _(df):
    # FacetGrid con distribuciones
    # - displot: figura de alto nivel (crea su propia figura)
    # - x: variable numérica
    # - col: crea una faceta por categoría (sexo)
    # - bins: número de intervalos
    # - height: altura de cada panel
    # - aspect: relación ancho/alto
    g_facet = sns.displot(
        data=df,
        x="glucose_mg_dL",
        col="sex",
        bins=15,
        height=4,
        aspect=1,
    )

    # Título general
    # - fig.suptitle: título para toda la figura (no solo un eje)
    # - y: ajusta posición vertical para evitar solapamiento
    g_facet.fig.suptitle(
        "Distribución de glucosa por sexo",
        y=1.03
    )

    # Mostrar figura
    g_facet
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 11) Cuándo conviene Seaborn y cuándo conviene Matplotlib

    En este punto conviene explicitar la relación entre ambas librerías.

    ### Seaborn conviene cuando:

    - quieres mapear variables de un dataframe rápidamente,
    - necesitas comparaciones estadísticas frecuentes,
    - quieres consistencia visual por defecto,
    - quieres trabajar con agrupaciones y facets sin construir cada elemento desde cero.

    ### Matplotlib conviene cuando:

    - necesitas control muy fino,
    - quieres agregar artistas personalizados,
    - quieres construir una figura con detalles muy específicos,
    - necesitas mezclar múltiples componentes con control local exacto.

    En la práctica, muchas veces se usan juntas:

    - Seaborn para la geometría estadística principal,
    - Matplotlib para ajustes finos del `Axes`.

    Esa combinación es justamente la que iremos fortaleciendo.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto 1 — Scatter con `hue`

    Construye un gráfico de dispersión entre:

    - `age`
    - `sbp_mmHg`

    y agrega una diferenciación por `sex` usando `hue`.

    Además:

    - agrega un título,
    - nombra ambos ejes.

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
            <Relación base>
            La función principal aquí es `sns.scatterplot(...)`.
            """,
            r"""
            <Codificación adicional>
            Usa `hue="sex"` para distinguir categorías.
            """,
            r"""
            <Integración con Matplotlib>
            Crea primero `fig_reto1, ax_reto1 = plt.subplots(...)` y luego pasa `ax=ax_reto1`.
            """,
            r"""
            <solucion>
            ```python
            fig_reto1, ax_reto1 = plt.subplots(figsize=(7, 4.5))
            sns.scatterplot(
                data=df,
                x="age",
                y="sbp_mmHg",
                hue="sex",
                ax=ax_reto1,
            )
            ax_reto1.set_title("Relación entre edad y PAS según sexo")
            ax_reto1.set_xlabel("Edad (años)")
            ax_reto1.set_ylabel("PAS (mmHg)")
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
            <Existencia>
            ```python
            assert fig_reto1 is not None and ax_reto1 is not None
            ```
            """,
            r"""
            <Tipos>
            ```python
            assert isinstance(fig_reto1, Figure)
            assert isinstance(ax_reto1, Axes)
            ```
            """,
            r"""
            <Etiquetas mínimas>
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
    ## Mini-reto 2 — Histograma con `kde`

    Construye una visualización de la distribución de `ldl_mg_dL` usando `sns.histplot(...)`.

    Requisitos:

    - incluir la curva de densidad (`kde=True`),
    - agregar título,
    - nombrar ejes.

    **Variables esperadas:**

    - `fig_reto2`
    - `ax_reto2`
    """)
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    fig_reto2, ax_reto2 = None, None
    return (fig_reto2,)


@app.cell(hide_code=True)
def _():
    _tip_content = TipContent(
        items_raw=[
            r"""
            <Función principal>
            Usa `sns.histplot(...)`.
            """,
            r"""
            <Distribución suavizada>
            Agrega `kde=True`.
            """,
            r"""
            <Integración>
            Puedes construir la figura con `plt.subplots(...)` y pasar el eje con `ax=...`.
            """,
            r"""
            <solucion>
            ```python
            fig_reto2, ax_reto2 = plt.subplots(figsize=(7, 4.5))
            sns.histplot(
                data=df,
                x="ldl_mg_dL",
                kde=True,
                bins=18,
                ax=ax_reto2,
            )
            ax_reto2.set_title("Distribución de LDL")
            ax_reto2.set_xlabel("LDL (mg/dL)")
            ax_reto2.set_ylabel("Frecuencia")
            fig_reto2.tight_layout()
            ```
            """,
        ]
    )
    _tip_content.render()
    return


@app.cell(hide_code=True)
def _(fig_reto2):
    _test_content = TestContent(
        items_raw=[
            r"""
            <Existencia>
            ```python
            assert fig_reto2 is not None and ax_reto2 is not None
            ```
            """,
            r"""
            <Tipos>
            ```python
            assert isinstance(fig_reto2, Figure)
            assert isinstance(ax_reto2, Axes)
            ```
            """,
            r"""
            <Etiquetas mínimas>
            ```python
            assert ax_reto2.get_title() != ""
            assert ax_reto2.get_xlabel() != ""
            assert ax_reto2.get_ylabel() != ""
            ```
            """,
        ],
        namespace=globals(),
    )

    if fig_reto2 is not None:
        fig_reto2
    _test_content.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto 3 — Boxplot para comparación entre grupos

    Construye un `boxplot` que compare `glucose_mg_dL` entre categorías de `bmi_category`.

    Requisitos:

    - usar `sns.boxplot(...)`,
    - rotar etiquetas del eje x para mejorar lectura,
    - agregar título y nombres de ejes.

    **Variables esperadas:**

    - `fig_reto3`
    - `ax_reto3`
    """)
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    fig_reto3, ax_reto3 = None, None
    return (fig_reto3,)


@app.cell(hide_code=True)
def _():
    _tip_content = TipContent(
        items_raw=[
            r"""
            <Comparación>
            La variable categórica va en `x` y la numérica en `y`.
            """,
            r"""
            <Función>
            Usa `sns.boxplot(data=df, x=..., y=...)`.
            """,
            r"""
            <Legibilidad>
            Puedes rotar etiquetas con `ax_reto3.tick_params(axis="x", rotation=30)`.
            """,
            r"""
            <solucion>
            ```python
            fig_reto3, ax_reto3 = plt.subplots(figsize=(8, 4.5))
            sns.boxplot(
                data=df,
                x="bmi_category",
                y="glucose_mg_dL",
                ax=ax_reto3,
            )
            ax_reto3.set_title("Glucosa por categoría de IMC")
            ax_reto3.set_xlabel("Categoría de IMC")
            ax_reto3.set_ylabel("Glucosa (mg/dL)")
            ax_reto3.tick_params(axis="x", rotation=30)
            fig_reto3.tight_layout()
            ```
            """,
        ]
    )
    _tip_content.render()
    return


@app.cell(hide_code=True)
def _(fig_reto3):
    _test_content = TestContent(
        items_raw=[
            r"""
            <Existencia>
            ```python
            assert fig_reto3 is not None and ax_reto3 is not None
            ```
            """,
            r"""
            <Tipos>
            ```python
            assert isinstance(fig_reto3, Figure)
            assert isinstance(ax_reto3, Axes)
            ```
            """,
            r"""
            <Etiquetas mínimas>
            ```python
            assert ax_reto3.get_title() != ""
            assert ax_reto3.get_xlabel() != ""
            assert ax_reto3.get_ylabel() != ""
            ```
            """,
        ],
        namespace=globals(),
    )

    if fig_reto3 is not None:
        fig_reto3
    _test_content.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto final — Facets para comparación estructurada

    Construye una visualización con facets que compare la distribución de `sbp_mmHg` según `sex`.

    Requisitos:

    - usar `sns.displot(...)`,
    - crear un panel por categoría de `sex`,
    - añadir un título global a la figura.

    **Variable esperada:**

    - `g_reto_final`

    En este caso la salida esperada no es una `Figure` estándar de Matplotlib sino un objeto de Seaborn del tipo `FacetGrid`.
    """)
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    g_reto_final = None
    return (g_reto_final,)


@app.cell(hide_code=True)
def _():
    _tip_content = TipContent(
        items_raw=[
            r"""
            <Función de nivel figura>
            Usa `sns.displot(...)`, no `plt.subplots(...)`.
            """,
            r"""
            <Facets>
            La clave está en `col="sex"`.
            """,
            r"""
            <Título global>
            Después de crear el objeto, puedes usar `g_reto_final.fig.suptitle(...)`.
            """,
            r"""
            <solucion>
            ```python
            g_reto_final = sns.displot(
                data=df,
                x="sbp_mmHg",
                col="sex",
                bins=15,
                height=4,
                aspect=1,
            )
            g_reto_final.fig.suptitle("Distribución de PAS por sexo", y=1.03)
            ```
            """,
        ]
    )
    _tip_content.render()
    return


@app.cell(hide_code=True)
def _(g_reto_final):
    _test_content = TestContent(
        items_raw=[
            r"""
            <Existencia>
            ```python
            assert g_reto_final is not None
            ```
            """,
            r"""
            <Atributo esperado>
            ```python
            assert hasattr(g_reto_final, "fig")
            ```
            """,
            r"""
            <Figura asociada>
            ```python
            assert isinstance(g_reto_final.fig, Figure)
            ```
            """,
        ],
        namespace=globals(),
    )

    if g_reto_final is not None:
        g_reto_final
    _test_content.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 12) Cierre conceptual

    En esta lección aprendiste a usar Seaborn como una capa declarativa sobre Matplotlib para representar relaciones estadísticas con mayor rapidez y consistencia.

    Trabajaste:

    - `scatterplot` para relaciones entre variables,
    - `hue` para introducir una categoría adicional,
    - `histplot` para distribuciones,
    - `boxplot` para comparación entre grupos,
    - `barplot` para estimaciones resumen,
    - `regplot` para tendencia visual,
    - y `displot` para facets.

    La progresión respecto a la lección anterior es importante:

    - en Matplotlib aprendiste **cómo construir**,
    - en Seaborn empiezas a decidir **qué estructura relacional conviene declarar**.

    Idea final:

    > **Seaborn reduce fricción técnica, pero el criterio sobre qué mostrar, por qué mostrarlo y cómo interpretarlo sigue dependiendo del analista.**

    > Si quieres tener más opciones o inspiración, explora la [galería de Seaborn](https://seaborn.pydata.org/examples/index.html) y prueba a replicar algunos de los gráficos usando tu propio dataset o el que hemos trabajado en esta sesión.
    """)
    return


if __name__ == "__main__":
    app.run()
