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

    **Propósito de la sesión:** aprender a construir visualizaciones paso a paso, entendiendo cómo cada decisión modifica lo que un gráfico comunica.

    En la lección anterior trabajaste el **por qué visualizar** y cómo una visualización puede comunicar bien o generar ruido.

    En esta lección avanzamos un nivel:

    > pasar de **leer gráficos** a **construirlos explícitamente**.

    El foco no es hacer gráficos “bonitos”.
    El foco es **controlar la representación** para que el mensaje sea claro.

    Trabajaremos con una idea central:

    > un gráfico no aparece automáticamente: se construye mediante decisiones explícitas.

    Esta lógica es especialmente importante en análisis de datos en salud, donde una visualización puede influir en la interpretación de una distribución, una diferencia entre grupos o una posible asociación.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 1) Marco conceptual — construir vs. obtener un gráfico

    En muchos entornos un gráfico puede generarse automáticamente a partir de una tabla.

    Eso es útil, pero también puede ocultar algo importante:

    > **cada gráfico es el resultado de una serie de decisiones.**

    En el enfoque imperativo de Matplotlib esas decisiones quedan más visibles.

    La lógica general es:

    1. crear el espacio donde se dibuja (figura y ejes),
    2. decidir qué variable va en cada eje ,
    3. elegir el tipo de representación (geometría o gráfico a usar),
    4. añadir contexto (título, unidades, etiquetas),
    5. ajustar lo necesario para facilitar la lectura.

    Esto nos lleva a una idea clave:

    > **visualizar no es solo dibujar datos; es codificar información para que otra persona la interprete.**
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
    ## 2) Dataset de trabajo

    Utilizaremos un subset de la Encuesta sobre Salud, Bienestar y Envejecimiento (SABE) con **{df.shape[0]} registros** y **{df.shape[1]} variables**.

    Cada fila representa un individuo y contiene variables demográficas, factores de riesgo y mediciones clínicas.

    En esta sesión nos concentraremos en variables útiles para visualización básica con Matplotlib:

    - `age`
    - `sbp_mmHg`
    - `glucose_mg_dL`
    - `ldl_mg_dL`
    - `sex`
    - `hypertension`
    - `Diabetes`
    - `bmi_category`

    El objetivo no es graficar por graficar.

    El objetivo es **elegir una representación coherente con la pregunta analítica**.
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
    ## 3) Anatomía mínima de un gráfico en Matplotlib

    El patrón base que repetiremos es:

    ```python
    fig, ax = plt.subplots()
    ax.plot(...)
    ax.set_title(...)
    ax.set_xlabel(...)
    ax.set_ylabel(...)
    ```

    - `fig` representa la figura completa.
    - `ax` representa el área específica donde se dibuja el gráfico.

    En términos prácticos, casi todo lo importante sucede en `ax`.

    Esto permite trabajar con más control y entender mejor la construcción del gráfico.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 4) Modelo mental de Matplotlib: Figure, Axes y artistas

    Para avanzar con mayor control conviene pensar Matplotlib como una jerarquía de objetos.

    ### Figure

    La `Figure` es el contenedor completo del gráfico.

    Puede verse como la página o el lienzo total sobre el que vivirán uno o varios gráficos.

    ### Axes

    Cada `Axes` es una zona concreta de dibujo dentro de la figura.

    Aquí suelen definirse:

    - líneas,
    - barras,
    - histogramas,
    - texto,
    - anotaciones,
    - límites,
    - ticks,
    - leyendas.

    ### Artistas

    En Matplotlib, los elementos visibles del gráfico se llaman artistas (**artists**).

    Ejemplos:

    - una línea,
    - un texto,
    - una barra,
    - una leyenda,
    - un título.

    Idea clave:

    > cada vez que agregas algo visual al gráfico, estás agregando un artista.

    ### Subplots y facets

    Cuando una figura contiene varios `Axes`, hablamos de una cuadrícula de subplots.

    En esta lección usaremos la palabra **facets** de forma introductoria para describir comparaciones distribuidas en varios paneles pequeños, cada uno con la misma lógica gráfica aplicada a un subgrupo distinto.
    """)
    return


@app.cell
def _(df):
    # Agrupación y resumen
    # - groupby("age"): agrupa por edad
    # - mean_sbp: calcula la media de presión sistólica (sbp_mmHg)
    # - sort_values: asegura orden ascendente en el eje X
    sbp_by_age = (
        df.groupby("age", as_index=False)
        .agg(mean_sbp=("sbp_mmHg", "mean"))
        .sort_values("age")
    )

    # Crear figura y eje
    fig_line, ax_line = plt.subplots(figsize=(8, 4.5))

    # Línea
    # - X: edad
    # - Y: presión sistólica media
    # - marker="o": muestra cada punto observado
    # - linewidth: grosor de la línea
    # - label: texto para la leyenda
    ax_line.plot(
        sbp_by_age["age"],
        sbp_by_age["mean_sbp"],
        marker="o",
        linewidth=1.8,
        label="PAS media por edad",
    )

    # Título y etiquetas
    ax_line.set_title("Presión arterial sistólica media por edad")
    ax_line.set_xlabel("Edad (años)")
    ax_line.set_ylabel("PAS media (mmHg)")

    # Elementos de apoyo visual
    # - legend(): identifica la serie
    # - grid(): facilita la lectura de valores
    ax_line.legend()
    ax_line.grid(True, alpha=0.3)

    # Ajuste de layout
    fig_line.tight_layout()

    # Mostrar figura
    fig_line
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 5) Lectura del ejemplo – qué decisiones se tomaron

    Este gráfico se construyó paso a paso:

    1. se resumieron los datos,
    2. se creó una figura y un eje,
    3. se agregó una línea,
    4. se nombraron ejes y título,
    5. se añadió una leyenda,
    6. se mejoró la legibilidad con cuadrícula suave.

    Idea clave:

    > **cada elemento del gráfico debe tener una razón.**

    Si no aporta a la interpretación, probablemente sobra.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 6) Histograma – entender la distribución

    Antes de comparar grupos o estudiar relaciones, una pregunta muy frecuente es:

    > ¿cómo se distribuye una variable?

    El histograma permite observar:

    - dónde se concentran los valores,
    - si hay asimetría,
    - si existen posibles valores extremos,
    - si la variable parece tener uno o varios picos.

    En salud, esto es especialmente útil para variables como:

    - glucosa,
    - presión arterial,
    - colesterol,
    - edad.
    """)
    return


@app.cell
def _(df):
    # Crear figura y eje
    fig_hist, ax_hist = plt.subplots(figsize=(7, 4.5))

    # Histograma
    # - Datos: glucosa sin valores faltantes
    # - bins: número de intervalos (resolución de la distribución)
    # - edgecolor: mejora la separación visual entre barras
    ax_hist.hist(
        df["glucose_mg_dL"].dropna(),
        bins=18,
        edgecolor="black",
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
    ## 7) Líneas de referencia: verticales y horizontales

    Muchas veces no basta con mostrar los datos.

    También conviene marcar un valor importante para ayudar a interpretar el gráfico.

    Ejemplos frecuentes:

    - un punto de corte,
    - una media o mediana,
    - un umbral clínico,
    - un valor objetivo.

    ### Línea vertical

    Se usa cuando quieres marcar un valor del eje x.

    ```python
    ax.axvline(x=126, color="red", linestyle="--", linewidth=2)
    ```

    ### Línea horizontal

    Se usa cuando quieres marcar un valor del eje y.

    ```python
    ax.axhline(y=140, color="darkorange", linestyle=":", linewidth=2)
    ```

    Idea clave:

    > una línea de referencia no agrega datos nuevos, pero sí agrega contexto interpretativo.
    """)
    return


@app.cell
def _(df):
    # Crear figura y eje
    fig_ref, ax_ref = plt.subplots(figsize=(7.5, 4.5))

    # Histograma
    # - Datos: glucosa sin valores faltantes
    # - bins: número de intervalos
    # - edgecolor: mejora la separación visual
    ax_ref.hist(
        df["glucose_mg_dL"].dropna(),
        bins=18,
        edgecolor="black"
    )

    # Línea vertical de referencia (umbral clínico)
    # - x=126: valor de glucosa
    # - linestyle="--": estilo punteado
    ax_ref.axvline(
        x=126,
        color="red",
        linestyle="--",
        linewidth=2,
        label="Umbral clínico: 126 mg/dL"
    )

    # Línea horizontal de referencia (conteo)
    # - y=100: frecuencia de referencia
    # - útil para ilustrar niveles altos de conteo
    ax_ref.axhline(
        y=100,
        color="blue",
        linestyle=":",
        linewidth=2,
        label="Conteo = 100"
    )

    # Título y etiquetas
    ax_ref.set_title("Distribución de glucosa con líneas de referencia")
    ax_ref.set_xlabel("Glucosa (mg/dL)")
    ax_ref.set_ylabel("Frecuencia")

    # Leyenda para interpretar líneas
    ax_ref.legend()

    # Ajuste de layout
    fig_ref.tight_layout()

    # Mostrar figura
    fig_ref
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 8) Texto dentro del gráfico

    Un gráfico puede necesitar texto adicional para aclarar qué significa una marca o llamar la atención sobre una región importante.

    Para eso se usa `ax.text(...)`.

    Patrón básico:

    ```python
    ax.text(x, y, "Texto")
    ```

    Aquí:

    - `x` controla la posición horizontal,
    - `y` controla la posición vertical,
    - el tercer argumento es el texto visible.

    Idea importante:

    > el texto debe aclarar, no repetir lo obvio.
    """)
    return


@app.cell
def _(df):
    # Crear figura y eje
    fig_text, ax_text = plt.subplots(figsize=(7.5, 4.5))

    # Histograma
    # - Datos: glucosa sin valores faltantes
    # - bins: número de intervalos
    # - edgecolor: mejora la lectura de las barras
    ax_text.hist(
        df["glucose_mg_dL"].dropna(),
        bins=18,
        edgecolor="black"
    )

    # Línea vertical de referencia
    # - x=126: umbral de interés
    # - linestyle="--": estilo punteado
    ax_text.axvline(
        x=126,
        color="red",
        linestyle="--",
        linewidth=2
    )

    # Texto anotado
    # - (x, y): posición del texto en coordenadas del gráfico
    # - etiqueta: valor de referencia
    ax_text.text(
        128,   # ligeramente a la derecha de la línea
        20,    # altura en el eje Y
        "126 mg/dL",
        fontsize=9,
    )

    # Título y etiquetas
    ax_text.set_title("Distribución de glucosa con texto explicativo")
    ax_text.set_xlabel("Glucosa (mg/dL)")
    ax_text.set_ylabel("Frecuencia")

    # Ajuste de layout
    fig_text.tight_layout()

    # Mostrar figura
    fig_text
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 9) Anotaciones: texto con flecha

    Cuando quieres conectar explícitamente un texto con un punto, una barra o una línea, `ax.annotate(...)` suele ser mejor que `ax.text(...)`.

    Patrón general:

    ```python
    ax.annotate(
        "texto",
        xy=(x_objetivo, y_objetivo),
        xytext=(x_texto, y_texto),
        arrowprops={"arrowstyle": "->"},
    )
    ```

    Esto permite:

    - elegir el punto que quieres señalar,
    - ubicar el texto en otra posición,
    - y conectar ambos con una flecha.

    Idea clave:

    > `text` coloca texto; `annotate` coloca una explicación conectada a algo específico.
    """)
    return


@app.cell
def _(df):
    # Cálculo del histograma (sin graficar)
    # - np.histogram: devuelve conteos por bin y los límites de cada bin
    # - bins=18: número de intervalos
    glucose_counts, glucose_bins = np.histogram(
        df["glucose_mg_dL"].dropna(),
        bins=18
    )

    # Identificar el bin con mayor frecuencia
    # - argmax(): índice del bin con mayor conteo
    max_bin_idx = glucose_counts.argmax()

    # Coordenadas del pico
    # - x_peak: punto medio del bin con mayor frecuencia
    # - y_peak: valor máximo de conteo
    x_peak = (glucose_bins[max_bin_idx] + glucose_bins[max_bin_idx + 1]) / 2
    y_peak = glucose_counts[max_bin_idx]

    # Crear figura y eje
    fig_annot, ax_annot = plt.subplots(figsize=(7.5, 4.5))

    # Histograma
    # - mismos datos y bins para consistencia con el cálculo previo
    ax_annot.hist(
        df["glucose_mg_dL"].dropna(),
        bins=18,
        edgecolor="black"
    )

    # Anotación
    # - xy: punto de interés (máxima concentración)
    # - xytext: posición del texto (desplazada para visibilidad)
    # - arrowprops: dibuja flecha hacia el punto
    ax_annot.annotate(
        "Zona de mayor concentración",
        xy=(x_peak, y_peak),
        xytext=(x_peak + 20, y_peak + 2),
        arrowprops={"arrowstyle": "->", "color": "red"},
        fontsize=9,
        color="darkgreen",
    )

    # Título y etiquetas
    ax_annot.set_title("Distribución de glucosa con anotación")
    ax_annot.set_xlabel("Glucosa (mg/dL)")
    ax_annot.set_ylabel("Frecuencia")

    # Ajuste de layout
    fig_annot.tight_layout()

    # Mostrar figura
    fig_annot
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 10) Otras utilidades prácticas al construir gráficos

    A medida que el gráfico se vuelve más informativo, suele ser necesario ajustar componentes adicionales del `Axes`.

    ### Límites

    ```python
    ax.set_xlim(60, 220)
    ax.set_ylim(0, 35)
    ```

    ### Ticks y etiquetas

    ```python
    ax.set_xticks([70, 100, 126, 150, 180, 210])
    ax.set_xticklabels(["70", "100", "126", "150", "180", "210"])
    ```

    ### Leyendas

    ```python
    ax.plot(x, y1, label="Serie 1")
    ax.plot(x, y2, label="Serie 2")
    ax.legend()
    ```

    ### Transparencia

    ```python
    ax.scatter(x, y, alpha=0.5)
    ```

    ### Rotación de etiquetas

    ```python
    ax.tick_params(axis="x", rotation=30)
    ```

    Idea clave:

    > la construcción del gráfico no termina cuando se dibuja la geometría; termina cuando otra persona puede interpretarlo con claridad.
    """)
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
            <Idea base>
            Un histograma representa una sola variable numérica.
            """,
            r"""
            <Construcción>
            Usa `plt.subplots()` y luego `ax.hist(...)`.
            """,
            r"""
            <Semántica>
            No olvides título y etiquetas.
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
    ## 11) Gráfico de barras – comparación entre grupos o variables categóricas

    Cuando la pregunta cambia a:

    > ¿cómo se comparan categorías?

    el histograma deja de ser adecuado.

    El gráfico de barras es útil para:

    - comparar magnitudes,
    - identificar diferencias entre grupos,
    - comunicar resultados de manera directa.

    Ejemplos típicos:

    - número de personas por categoría de IMC,
    - recuentos por sexo,
    - frecuencia por diagnóstico.
    """)
    return


@app.cell
def _(df):
    # Conteo por categoría
    # - value_counts: cuenta frecuencia de cada categoría (incluye NA)
    # - rename_axis: nombra la columna de categorías
    # - reset_index: convierte a DataFrame con columna "n"
    bmi_counts = (
        df["bmi_category"]
        .value_counts(dropna=False)
        .rename_axis("bmi_category")
        .reset_index(name="n")
    )

    # Crear figura y eje
    fig_bar, ax_bar = plt.subplots(figsize=(8, 4.5))

    # Gráfico de barras
    # - X: categorías de IMC
    # - Y: número de personas
    ax_bar.bar(
        bmi_counts["bmi_category"],
        bmi_counts["n"]
    )

    # Título y etiquetas
    ax_bar.set_title("Número de personas por categoría de IMC")
    ax_bar.set_xlabel("Categoría de IMC")
    ax_bar.set_ylabel("Número de personas")

    # Ajuste de etiquetas en eje X
    # - rotation: mejora legibilidad si hay muchas categorías
    ax_bar.tick_params(axis="x", rotation=30)

    # Ajuste de layout
    fig_bar.tight_layout()

    # Mostrar figura
    fig_bar
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 12) Scatter plot — relación entre dos variables

    Cuando la pregunta es:

    > ¿existe una relación entre dos variables cuantitativas?

    el gráfico de dispersión suele ser una buena opción.

    Permite observar:

    - si hay asociación visual,
    - cuánta dispersión existe,
    - si aparecen agrupamientos,
    - si hay valores atípicos.

    Importante:

    > un scatter plot es exploratorio; no demuestra causalidad.
    """)
    return


@app.cell
def _(df):
    # Preparación de datos
    # - Selección de variables relevantes
    # - dropna(): elimina filas con valores faltantes
    # - copy(): evita modificar el DataFrame original
    df_scatter = df[["sbp_mmHg", "glucose_mg_dL", "Diabetes"]].dropna().copy()

    # Estandarización de etiquetas
    # - Unifica valores inconsistentes ("Yes", "yes", etc.)
    diabetes_map = {
        "Yes": "Diabetes",
        "No": "No diabetes",
        "yes": "Diabetes",
        "no": "No diabetes",
    }

    # Nueva columna para visualización
    # - map(): aplica el diccionario
    # - fillna(): conserva valores no mapeados
    df_scatter["Diabetes_plot"] = df_scatter["Diabetes"].map(diabetes_map).fillna(
        df_scatter["Diabetes"]
    )

    # Crear figura y eje
    fig_scatter, ax_scatter = plt.subplots(figsize=(7, 4.5))

    # Scatter plot por grupo
    # - groupby(): separa por estado de diabetes
    # - alpha: controla transparencia (mejor para solapamientos)
    # - label: permite crear leyenda automática
    for _label, _subset in df_scatter.groupby("Diabetes_plot"):
        ax_scatter.scatter(
            _subset["sbp_mmHg"],        # X: presión sistólica
            _subset["glucose_mg_dL"],   # Y: glucosa
            alpha=0.6,
            label=_label,
        )

    # Título y etiquetas
    ax_scatter.set_title("Presión arterial y glucosa según estado de diabetes")
    ax_scatter.set_xlabel("PAS (mmHg)")
    ax_scatter.set_ylabel("Glucosa (mg/dL)")

    # Elementos de apoyo visual
    # - legend(): identifica grupos
    # - grid(): facilita lectura de patrones
    ax_scatter.legend()
    ax_scatter.grid(True, alpha=0.2)

    # Ajuste de layout
    fig_scatter.tight_layout()

    # Mostrar figura
    fig_scatter
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto 2 — Barras de hipertensión por sexo

    Construye un gráfico de barras que compare el **número de personas con hipertensión** entre categorías de `sex`.

    Sugerencia analítica: primero resume la tabla y luego grafica el resultado.

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
            ax_reto2.bar(
                hypertension_by_sex["sex"],
                hypertension_by_sex["n_hypertension"],
            )
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
    ## 13) Facets y comparación en múltiples paneles

    A veces una sola visualización mezcla demasiadas cosas.

    En esos casos, dividir la comparación en varios paneles puede ser mejor.

    Esto se implementa creando varios `Axes` dentro de una misma figura.

    Patrón general:

    ```python
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    ```

    También puedes compartir escalas entre paneles:

    ```python
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharex=True, sharey=True)
    ```

    Esto ayuda a:

    - separar grupos,
    - reducir superposición,
    - mantener la misma estructura visual,
    - comparar patrones con menos ruido.
    """)
    return


@app.cell
def _(df):
    # Crear figura con múltiples subplots (facetas)
    # - 1 fila, 2 columnas
    # - sharex/sharey: mismos ejes para facilitar comparación
    fig_facets, axes_facets = plt.subplots(
        1, 2,
        figsize=(10, 4),
        sharex=True,
        sharey=True
    )

    # Selección de categorías
    # - dropna(): elimina valores faltantes
    # - astype(str): asegura consistencia de tipo
    # - unique + sorted: obtiene categorías ordenadas
    # - [:2]: limita a dos grupos para visualizar
    sex_values = sorted(
        df["sex"].dropna().astype(str).unique().tolist()
    )[:2]

    # Iteración por facetas
    # - zip(): asigna cada eje a una categoría
    for ax, sex_value in zip(axes_facets, sex_values):
    
        # Subconjunto de datos por categoría
        # - loc: filtra por sexo
        # - dropna(): elimina valores faltantes
        subset = df.loc[
            df["sex"] == sex_value,
            "glucose_mg_dL"
        ].dropna()
    
        # Histograma por grupo
        # - mismos bins para comparabilidad
        ax.hist(
            subset,
            bins=15,
            edgecolor="black"
        )
    
        # Título y etiquetas
        ax.set_title(f"Glucosa en {sex_value}")
        ax.set_xlabel("Glucosa (mg/dL)")
        ax.set_ylabel("Frecuencia")

    # Ajuste de layout
    fig_facets.tight_layout()

    # Mostrar figura
    fig_facets
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 14) Subplots: comparación coordinada

    Cuando dos gráficos comparten propósito analítico, puede ser útil colocarlos dentro de la misma figura.

    Esto permite mantener una narrativa comparativa bajo una estructura común.
    """)
    return


@app.cell
def _(df):
    # Crear figura con múltiples subplots
    # - 1 fila, 2 columnas
    # - cada eje mostrará una variable distinta
    fig_grid, axes_grid = plt.subplots(1, 2, figsize=(11, 4))

    # Histograma 1: Presión arterial sistólica (PAS)
    # - dropna(): elimina valores faltantes
    # - bins: número de intervalos
    axes_grid[0].hist(
        df["sbp_mmHg"].dropna(),
        bins=18,
        edgecolor="black"
    )
    axes_grid[0].set_title("Distribución de PAS")
    axes_grid[0].set_xlabel("PAS (mmHg)")
    axes_grid[0].set_ylabel("Frecuencia")

    # Histograma 2: LDL
    # - misma configuración para comparabilidad visual
    axes_grid[1].hist(
        df["ldl_mg_dL"].dropna(),
        bins=18,
        edgecolor="black",
        color="darkorange"
    )
    axes_grid[1].set_title("Distribución de LDL")
    axes_grid[1].set_xlabel("LDL (mg/dL)")
    axes_grid[1].set_ylabel("Frecuencia")

    # Ajuste de layout
    fig_grid.tight_layout()

    # Mostrar figura
    fig_grid
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
            Usa `ax.plot(...)` con marcador y agrega etiquetas claras.
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
    ## Mini-reto 4 — Línea de referencia y texto

    Construye un histograma de `ldl_mg_dL` y agrega:

    1. una línea vertical en `130`,
    2. un texto breve que indique qué representa esa línea.

    **Variables esperadas:**

    - `fig_reto4`
    - `ax_reto4`
    """)
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    fig_reto4, ax_reto4 = None, None
    return (fig_reto4,)


@app.cell(hide_code=True)
def _():
    _tip_content = TipContent(
        items_raw=[
            r"""
            <Idea gráfica>
            Primero construye el histograma y después agrega la línea y el texto.
            """,
            r"""
            <Línea>
            La línea vertical se agrega con `ax.axvline(...)`.
            """,
            r"""
            <Texto>
            El texto se agrega con `ax.text(...)` en una posición `(x, y)` elegida por ti.
            """,
            r"""
            <solucion>
            ```python
            fig_reto4, ax_reto4 = plt.subplots(figsize=(7.5, 4.5))
            ax_reto4.hist(df["ldl_mg_dL"].dropna(), bins=18, edgecolor="black")
            ax_reto4.axvline(x=130, color="red", linestyle="--", linewidth=2)
            ax_reto4.text(132, 18, "Referencia: 130 mg/dL", fontsize=9)
            ax_reto4.set_title("Distribución de LDL con línea de referencia")
            ax_reto4.set_xlabel("LDL (mg/dL)")
            ax_reto4.set_ylabel("Frecuencia")
            fig_reto4.tight_layout()
            ```
            """,
        ]
    )
    _tip_content.render()
    return


@app.cell(hide_code=True)
def _(fig_reto4):
    _test_content = TestContent(
        items_raw=[
            r"""
            <Existencia>
            ```python
            assert fig_reto4 is not None and ax_reto4 is not None
            ```
            """,
            r"""
            <Tipos>
            ```python
            assert isinstance(fig_reto4, Figure)
            assert isinstance(ax_reto4, Axes)
            ```
            """,
            r"""
            <Elementos mínimos>
            ```python
            assert len(ax_reto4.lines) >= 1
            assert len(ax_reto4.texts) >= 1
            ```
            """,
        ],
        namespace=globals(),
    )

    if fig_reto4 is not None:
        fig_reto4
    _test_content.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto 5 — Facets por grupo

    Construye una figura con **dos paneles** que compare la distribución de `sbp_mmHg` según `sex`.

    Requisitos:

    1. usar `plt.subplots(1, 2, ...)`,
    2. compartir escala en x e y,
    3. dibujar un histograma por panel,
    4. titular cada panel según el grupo.

    **Variables esperadas:**

    - `fig_reto5`
    - `axes_reto5`
    """)
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    fig_reto5, axes_reto5 = None, None
    return (fig_reto5,)


@app.cell(hide_code=True)
def _():
    _tip_content = TipContent(
        items_raw=[
            r"""
            <Estructura>
            Crea una figura con dos ejes usando `plt.subplots(1, 2, ...)`.
            """,
            r"""
            <Comparación>
            Usa `sharex=True` y `sharey=True` para mantener la misma escala.
            """,
            r"""
            <Subconjuntos>
            En cada eje, filtra `df` por una categoría de `sex` y dibuja el histograma.
            """,
            r"""
            <solucion>
            ```python
            fig_reto5, axes_reto5 = plt.subplots(
                1,
                2,
                figsize=(10, 4),
                sharex=True,
                sharey=True,
            )

            sex_values = sorted(df["sex"].dropna().astype(str).unique().tolist())[:2]

            for ax, sex_value in zip(axes_reto5, sex_values):
                subset = df.loc[df["sex"] == sex_value, "sbp_mmHg"].dropna()
                ax.hist(subset, bins=15, edgecolor="black")
                ax.set_title(f"PAS en {sex_value}")
                ax.set_xlabel("PAS (mmHg)")
                ax.set_ylabel("Frecuencia")

            fig_reto5.tight_layout()
            ```
            """,
        ]
    )
    _tip_content.render()
    return


@app.cell(hide_code=True)
def _(fig_reto5):
    _test_content = TestContent(
        items_raw=[
            r"""
            <Existencia>
            ```python
            assert fig_reto5 is not None and axes_reto5 is not None
            ```
            """,
            r"""
            <Figura y cantidad de ejes>
            ```python
            assert isinstance(fig_reto5, Figure)
            assert len(axes_reto5) == 2
            ```
            """,
            r"""
            <Títulos>
            ```python
            assert all(ax.get_title() != "" for ax in axes_reto5)
            ```
            """,
        ],
        namespace=globals(),
    )

    if fig_reto5 is not None:
        fig_reto5
    _test_content.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 15) Buenas prácticas mínimas en visualización imperativa

    En este punto ya puedes extraer algunas reglas operativas:

    - elegir el tipo de gráfico según la pregunta,
    - no usar elementos decorativos innecesarios,
    - titular con precisión,
    - nombrar unidades cuando existan,
    - usar líneas o anotaciones solo cuando aporten interpretación,
    - mantener consistencia visual entre paneles comparables.

    Idea clave:

    > construir un gráfico es solo una parte del trabajo; hacer que otra persona lo interprete correctamente es la parte más importante.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 16) Cierre conceptual

    En esta sesión trabajaste el núcleo del enfoque imperativo con Matplotlib:

    - creación explícita de `Figure` y `Axes`,
    - uso de `plot`, `hist`, `bar` y `scatter`,
    - incorporación manual de títulos, etiquetas, leyendas y cuadrícula,
    - líneas verticales y horizontales de referencia,
    - texto y anotaciones dentro del gráfico,
    - organización de múltiples paneles con subplots,
    - y una primera intuición sobre artistas y facets.

    Este dominio es importante porque te permite entender que una visualización es una construcción deliberada y no un producto automático de la librería.

    > puedes complementar y explorar otros diseños disponibles en la [galeria de Matplotlib](https://matplotlib.org/stable/gallery/index.html) para ampliar tu repertorio visual.
    """)
    return


if __name__ == "__main__":
    app.run()
