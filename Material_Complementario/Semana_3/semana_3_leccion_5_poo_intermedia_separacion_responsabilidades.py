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
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import seaborn as sns
    from matplotlib.axes import Axes
    from matplotlib.figure import Figure

    from setup import TipContent, TestContent, find_data_file

    sns.set_theme(style="whitegrid")


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Semana 3 · Lección 5
    ## POO intermedia y separación de responsabilidades

    **Propósito de la sesión:** aprender a organizar un análisis en una clase simple separando con claridad tres responsabilidades:

    - preparar datos,
    - calcular un resumen,
    - visualizar el resultado.

    Esta lección cambia de foco respecto a las anteriores.

    En las lecciones 2, 3 y 4 trabajaste principalmente la **representación de información**.
    Aquí el problema central no es elegir un gráfico, sino diseñar mejor el código que produce ese gráfico.

    La pregunta guía será:

    > **¿Cómo organizar un análisis para que limpiar, resumir y visualizar no queden mezclados en el mismo bloque?**

    La idea más importante de la sesión es esta:

    > una clase analítica intermedia no debe mezclar todo en un solo método.

    En vez de eso, construiremos una arquitectura mínima y legible basada en tres etapas:

    **clean → compute → visualize**
    """)
    return


@app.cell
def _():
    data_path = find_data_file("public/dataset_clase_semana2_small.csv")
    cohort_raw = pd.read_csv(data_path)

    cohort_raw.head()
    return (cohort_raw,)


@app.cell(hide_code=True)
def _(cohort_raw):
    mo.md(f"""
    ## Dataset de trabajo

    Seguiremos trabajando con el mismo dataset clínico de las lecciones anteriores.

    El dataset contiene:

    - **{cohort_raw.shape[0]} registros**
    - **{cohort_raw.shape[1]} variables**

    Cada fila representa un individuo con variables demográficas, factores de riesgo y mediciones clínicas.

    En esta sesión nos concentraremos solo en las variables necesarias para las preguntas de clase y de práctica:

    - `ID`
    - `age`
    - `sex`
    - `Diabetes`
    - `hypertension`
    - `high_cholesterol`
    - `sbp_mmHg`
    - `glucose_mg_dL`
    - `ldl_mg_dL`

    Esta reducción es deliberada.

    En diseño de clases, elegir solo las columnas que una pregunta necesita ayuda a:

    - hacer explícita la unidad de análisis,
    - reducir ruido,
    - y clarificar la responsabilidad de cada método.
    """)
    return


@app.cell
def _(cohort_raw):
    selected_columns = [
        "ID",
        "age",
        "sex",
        "Diabetes",
        "hypertension",
        "high_cholesterol",
        "sbp_mmHg",
        "glucose_mg_dL",
        "ldl_mg_dL",
    ]

    cohort_raw[selected_columns].head(8)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 1) Problema de diseño: mezclar todo en un mismo bloque

    Un análisis suele involucrar varias fases:

    - seleccionar variables,
    - renombrar columnas,
    - estandarizar etiquetas,
    - derivar indicadores,
    - resumir por grupos,
    - construir un gráfico.

    El problema aparece cuando todas esas tareas se mezclan en una sola función o en un solo método.

    Eso genera código que:

    - cuesta leer,
    - cuesta depurar,
    - cuesta modificar,
    - y cuesta reutilizar.

    Síntoma clásico:

    > si quieres cambiar una sola parte del análisis, tienes que volver a entrar a un bloque enorme donde todo está acoplado.
    """)
    return


@app.cell
def _(cohort_raw):
    # Definición de función que realiza todo le trabajo sin separar responsabilidades
    # - recibe un DataFrame crudo
    # - devuelve una tabla resumen
    def analyze_everything(raw_df: pd.DataFrame) -> pd.DataFrame:

        # Selección de variables
        # - conserva solo columnas relevantes para el análisis
        # - copy(): evita modificar el DataFrame original
        df = raw_df[
            [
                "ID",
                "age",
                "sex",
                "Diabetes",
                "hypertension",
                "high_cholesterol",
                "sbp_mmHg",
                "ldl_mg_dL",
            ]
        ].copy()

        # Estandarización de texto
        # - convierte valores de Diabetes a minúsculas
        # - útil cuando hay etiquetas como "Yes" y "yes"
        df["Diabetes"] = df["Diabetes"].str.lower()

        # Creación de indicadores booleanos
        # - eq("Yes"): True si la condición se cumple
        # - estos indicadores facilitan el cálculo de proporciones
        df["has_hypertension"] = df["hypertension"].eq("Yes")
        df["has_high_cholesterol"] = df["high_cholesterol"].eq("Yes")

        # Construcción de tabla resumen
        # - groupby: agrupa por sexo y diabetes
        # - agg: calcula conteos, medias y proporciones
        summary = (
            df.groupby(["sex", "Diabetes"], as_index=False)
            .agg(
                n_people=("ID", "count"),
                mean_age=("age", "mean"),
                mean_sbp=("sbp_mmHg", "mean"),
                mean_ldl=("ldl_mg_dL", "mean"),
                prop_hypertension=("has_hypertension", "mean"),
                prop_high_cholesterol=("has_high_cholesterol", "mean"),
            )

            # Orden y formato final
            .sort_values(["sex", "Diabetes"])
            .round(2)
        )

        # Salida de la función
        return summary

    # Ejecutar función sobre el dataset de cohorte
    overloaded_summary = analyze_everything(cohort_raw)

    # Mostrar resultado
    overloaded_summary
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    El resultado anterior puede ser correcto, pero la arquitectura sigue siendo débil:

    - no existe una fase explícita para inspeccionar la tabla limpia,
    - no existe una fase explícita para reutilizar el resumen,
    - y no queda claro dónde modificar el flujo si la pregunta analítica cambia.

    Por eso ahora construiremos una clase con responsabilidades separadas.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 2) Arquitectura objetivo de la clase

    La clase tendrá tres atributos principales:

    - `raw_df`: tabla original,
    - `cleaned_df`: tabla preparada,
    - `summary_df`: tabla resumida.

    Y tres métodos principales:

    - `clean_data()`
    - `compute_profile()`
    - `visualize_profile()`

    La lógica del flujo será:

    **raw_df → clean_data() → cleaned_df → compute_profile() → summary_df → visualize_profile() → gráfico**

    Idea clave:

    > cada método debe tener una responsabilidad principal y reconocible.
    """)
    return


@app.class_definition
# Definición de la clase
# - organiza el análisis en pasos: limpiar, resumir y visualizar
# - permite guardar resultados intermedios como atributos del objeto
class CohortProfileAnalyzer:

    # Método inicial
    # - recibe el DataFrame original
    # - crea espacios para guardar datos limpios y resumen
    def __init__(self, raw_df: pd.DataFrame):
        self.raw_df = raw_df.copy()
        self.cleaned_df = None
        self.summary_df = None

    # Limpieza y preparación de datos
    def clean_data(self) -> pd.DataFrame:
        # Selección de variables
        # - conserva solo columnas útiles para esta pregunta analítica
        df = self.raw_df[
            [
                "ID",
                "age",
                "sex",
                "Diabetes",
                "hypertension",
                "high_cholesterol",
                "sbp_mmHg",
                "glucose_mg_dL",
                "ldl_mg_dL",
            ]
        ].copy()

        # Renombrar columnas
        # - usa nombres más cortos y consistentes para el análisis
        df = df.rename(
            columns={
                "ID": "person_id",
                "Diabetes": "diabetes",
                "sbp_mmHg": "sbp",
                "glucose_mg_dL": "glucose",
                "ldl_mg_dL": "ldl",
            }
        )

        # Estandarización y creación de indicadores
        # - strip(): elimina espacios extra
        # - title() / lower(): uniforma etiquetas
        # - eq("Yes"): crea variables booleanas
        df["sex"] = df["sex"].str.strip().str.title()
        df["diabetes"] = df["diabetes"].str.strip().str.lower()
        df["has_hypertension"] = df["hypertension"].eq("Yes")
        df["has_high_cholesterol"] = df["high_cholesterol"].eq("Yes")

        # Guardar datos limpios en el objeto
        self.cleaned_df = df
        return self.cleaned_df

    # Cálculo del perfil resumido
    def compute_profile(self) -> pd.DataFrame:
        # Si no hay datos limpios, los prepara primero
        if self.cleaned_df is None:
            self.clean_data()

        # Tabla resumen
        # - groupby: agrupa por sexo y diabetes
        # - agg: calcula conteos, medias y proporciones
        summary = (
            self.cleaned_df.groupby(["sex", "diabetes"], as_index=False)
            .agg(
                n_people=("person_id", "count"),
                mean_age=("age", "mean"),
                mean_sbp=("sbp", "mean"),
                mean_glucose=("glucose", "mean"),
                mean_ldl=("ldl", "mean"),
                prop_hypertension=("has_hypertension", "mean"),
                prop_high_cholesterol=("has_high_cholesterol", "mean"),
            )
            .sort_values(["sex", "diabetes"])
            .round(2)
        )

        # Guardar resumen en el objeto
        self.summary_df = summary
        return self.summary_df

    # Visualización del perfil
    def visualize_profile(self):
        # Si no existe el resumen, lo calcula antes de graficar
        if self.summary_df is None:
            self.compute_profile()

        # Copia del resumen para visualización
        plot_df = self.summary_df.copy()

        # Crear figura y eje
        fig, ax = plt.subplots(figsize=(7, 4.5))

        # Gráfico de barras
        # - x: estado de diabetes
        # - y: proporción de hipertensión
        # - hue: separación por sexo
        sns.barplot(
            data=plot_df,
            x="diabetes",
            y="prop_hypertension",
            hue="sex",
            ax=ax,
        )

        # Título y etiquetas
        ax.set_title("Proporción de hipertensión por sexo y diabetes")
        ax.set_xlabel("Diabetes")
        ax.set_ylabel("Proporción")

        # Escala y leyenda
        # - ylim(0, 1): adecuado para proporciones
        ax.set_ylim(0, 1)
        ax.legend(title="Sexo")

        # Ajuste de layout
        fig.tight_layout()

        # Devuelve el eje para seguir personalizando si se necesita
        return ax


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 3) Lectura de la separación de responsabilidades

    ### `clean_data()`

    Se encarga de:

    - seleccionar variables,
    - renombrar columnas,
    - estandarizar etiquetas,
    - crear indicadores derivados simples.

    ### `compute_profile()`

    Se encarga de:

    - agrupar,
    - calcular conteos,
    - calcular medias,
    - calcular proporciones.

    ### `visualize_profile()`

    Se encarga de:

    - tomar una tabla resumen ya lista,
    - elegir una visualización adecuada,
    - definir ejes, etiquetas y rango.

    La regla operativa es muy simple:

    > **limpiar no es resumir, resumir no es graficar, y graficar no es volver a limpiar.**
    """)
    return


@app.cell
def _(cohort_raw):
    analyzer_demo = CohortProfileAnalyzer(cohort_raw)
    clean_demo = analyzer_demo.clean_data()
    summary_demo = analyzer_demo.compute_profile()

    clean_demo.head(6), summary_demo
    return (analyzer_demo,)


@app.cell
def _(analyzer_demo):
    ax_demo = analyzer_demo.visualize_profile()
    ax_demo
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 4) ¿Por qué esta separación mejora el código?

    Esta arquitectura mejora el análisis porque:

    - permite inspeccionar cada fase por separado,
    - facilita pruebas más estables,
    - hace más fácil cambiar una parte sin romper las demás,
    - permite reutilizar la tabla resumen en otro gráfico,
    - y reduce duplicación de trabajo.

    En otras palabras:

    > la separación de responsabilidades mejora la cohesión y reduce acoplamiento innecesario.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 5) Mini-reto 1 — Fase de limpieza

    > ¿Cómo cambia el perfil metabólico por grupo de edad y sexo?

    Tu tarea es preparar los datos para poder responder esa pregunta.

    Debes editar `clean_data()` en `StudentRiskStratifier` para que la tabla resultante:

    - contenga solo las variables necesarias,
    - tenga nombres consistentes,
    - tenga categorías limpias,
    - incluya una variable de edad agrupada,
    - incluya indicadores binarios clínicamente útiles.

    Requisitos mínimos:

    1. Seleccionar columnas relevantes.
    2. Renombrar `ID`, `Diabetes`, `glucose_mg_dL`, `ldl_mg_dL`.
    3. Estandarizar `sex` y `diabetes`.
    4. Crear `age_group` con:
       - `60-69`
       - `70-79`
       - `80+`
    5. Crear:
       - `has_diabetes`
       - `has_high_cholesterol`
    6. Guardar en `self.cleaned_df`.
    7. Retornar el resultado.

    Restricción:

    No agregues, no resumas, no visualices.
    """)
    return


@app.class_definition
class StudentRiskStratifier:
    def __init__(self, raw_df: pd.DataFrame):
        self.raw_df = raw_df.copy()
        self.cleaned_df = None
        self.summary_df = None

    def clean_data(self) -> pd.DataFrame:
        # === TU TURNO (EDITA ESTE MÉTODO) ===
        self.cleaned_df = None
        return self.cleaned_df

    def compute_profile(self) -> pd.DataFrame:
        # === TU TURNO (EDITA ESTE MÉTODO EN EL MINI-RETO 2) ===
        self.summary_df = None
        return self.summary_df

    def visualize_profile(self):
        # === TU TURNO (EDITA ESTE MÉTODO EN EL MINI-RETO 3) ===
        return None


@app.cell(hide_code=True)
def _():
    _tip_content = TipContent(
        items_raw=[
            r"""
    <Idea principal>
    La limpieza debe dejar lista la tabla para una agrupación posterior por `age_group` y `sex`.
    """,
            r"""
    <Variable derivada nueva>
    Aquí necesitas convertir una edad continua en bandas etarias. `pd.cut(...)` puede ayudarte.
    """,
            r"""
    <Indicadores>
    Si más adelante quieres calcular proporciones, conviene dejar listas columnas booleanas como `has_diabetes` y `has_high_cholesterol`.
    """,
            r"""
    <solucion>
    ```python
    def clean_data(self) -> pd.DataFrame:
    df = self.raw_df[
        [
            "ID",
            "age",
            "sex",
            "Diabetes",
            "high_cholesterol",
            "glucose_mg_dL",
            "ldl_mg_dL",
        ]
    ].copy()

    df = df.rename(
        columns={
            "ID": "person_id",
            "Diabetes": "diabetes",
            "glucose_mg_dL": "glucose",
            "ldl_mg_dL": "ldl",
        }
    )

    df["sex"] = df["sex"].str.strip().str.title()
    df["diabetes"] = df["diabetes"].str.strip().str.lower()

    df["age_group"] = pd.cut(
        df["age"],
        bins=[40, 55, 70, np.inf],
        right=False,
        labels=["40-54", "55-69", "70+"],
    ).astype(str)

    df["has_diabetes"] = df["diabetes"].eq("yes")
    df["has_high_cholesterol"] = df["high_cholesterol"].eq("Yes")

    self.cleaned_df = df
    return self.cleaned_df
    ```
    """,
        ]
    )
    _tip_content.render()
    return


@app.cell(hide_code=True)
def _():
    _test_content = TestContent(
        items_raw=[
            r"""
    <Salida esperada>
    ```python
    student = StudentRiskStratifier(cohort_raw)
    cleaned = student.clean_data()

    assert cleaned is not None
    assert isinstance(cleaned, pd.DataFrame)
    print("La salida tiene estructura tabular.")
    ```
    """,
            r"""
    <Columnas mínimas>
    ```python
    expected_columns = {
    "person_id",
    "age",
    "sex",
    "diabetes",
    "high_cholesterol",
    "glucose",
    "ldl",
    "age_group",
    "has_diabetes",
    "has_high_cholesterol",
    }
    assert expected_columns.issubset(set(cleaned.columns))
    print("Columnas correctas.")
    ```
    """,
            r"""
    <Bandas etarias esperadas>
    ```python
    assert set(cleaned["age_group"].unique()).issubset({"60-69", "70-79", "80+"})
    print("Grupos de edad válidos.")
    ```
    """,
        ],
        namespace=globals(),
    )
    _test_content.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 6) Segunda fase — Construcción del perfil

    Ahora ya no trabajas con individuos, sino con grupos.

    El perfil debe construirse por:

    - `age_group`
    - `sex`

    Y debe describir cada subgrupo mediante métricas resumen.

    Piensa:

    - ¿qué significa “perfil metabólico” en términos agregados?
    - ¿qué métricas lo capturan mejor?

    Regla:

    No redefinas variables que ya debieron existir desde la limpieza.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto 2 — compute_profile()

    Debes editar `compute_profile()` en `StudentRiskStratifier`.

    Tu función debe producir una tabla donde cada fila represente un subgrupo.

    Requisitos:

    1. Usar `self.cleaned_df`.
    2. Si no existe, llamar a `self.clean_data()`.
    3. Agrupar por:
       - `age_group`
       - `sex`
    4. Calcular:
       - `n_people`
       - `mean_glucose`
       - `mean_ldl`
       - `prop_diabetes`
       - `prop_high_cholesterol`
    5. Ordenar por `age_group` y `sex`.
    6. Redondear a dos decimales.
    7. Guardar en `self.summary_df`.
    8. Retornar el resultado.

    Antes de agregar algo al código, pregunta:
    > Esto ¿pertenece a la limpieza o al resumen?
    > si pertenece a la limpieza, debe colocarse en el método `clean_data()`
    > Si pertenece al resumen, ¿qué método es el adecuado para esa tarea?
    """)
    return


@app.cell(hide_code=True)
def _():
    _tip_content = TipContent(
        items_raw=[
            r"""
    <Dependencia correcta>
    Este método debe partir de `self.cleaned_df`, no del dataset crudo.
    """,
            r"""
    <Resumen>
    La tabla final debe ser una fila por combinación entre grupo de edad y sexo.
    """,
            r"""
    <Proporciones>
    El promedio de una variable booleana vuelve a ser útil para representar proporciones.
    """,
            r"""
    <solucion>
    ```python
    def compute_profile(self) -> pd.DataFrame:
    if self.cleaned_df is None:
        self.clean_data()

    summary = (
        self.cleaned_df.groupby(["age_group", "sex"], as_index=False)
        .agg(
            n_people=("person_id", "count"),
            mean_glucose=("glucose", "mean"),
            mean_ldl=("ldl", "mean"),
            prop_diabetes=("has_diabetes", "mean"),
            prop_high_cholesterol=("has_high_cholesterol", "mean"),
        )
        .sort_values(["age_group", "sex"])
        .round(2)
    )

    self.summary_df = summary
    return self.summary_df
    ```
    """,
        ]
    )
    _tip_content.render()
    return


@app.cell(hide_code=True)
def _():
    _test_content = TestContent(
        items_raw=[
            r"""
    <Existencia del resumen>
    ```python
    student = StudentRiskStratifier(cohort_raw)
    student.clean_data()
    summary = student.compute_profile()

    assert summary is not None
    assert isinstance(summary, pd.DataFrame)
    print("Resumen generado.")
    ```
    """,
            r"""
    <Columnas esperadas>
    ```python
    assert list(summary.columns) == [
    "age_group",
    "sex",
    "n_people",
    "mean_glucose",
    "mean_ldl",
    "prop_diabetes",
    "prop_high_cholesterol",
    ]
    print("Columnas correctas.")
    ```
    """,
            r"""
    <Rango de proporciones>
    ```python
    assert summary["prop_diabetes"].between(0, 1).all()
    assert summary["prop_high_cholesterol"].between(0, 1).all()
    print("Proporciones válidas.")
    ```
    """,
        ],
        namespace=globals(),
    )
    _test_content.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 7) Tercera fase — Visualización

    Aquí no transformas datos. Tomas decisiones.

    Debes trabajar únicamente con `self.summary_df`.

    Tu objetivo:

    Convertir una tabla en una comparación visual clara.

    Piensa:

    - ¿qué variable quieres destacar?
    - ¿qué comparación debe ser evidente?
    - ¿qué decisión visual facilita esa lectura?

    Evita:

    - recalcular métricas,
    - reagrupar datos,
    - modificar columnas.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto 3 — visualize_profile()

    Debes editar `visualize_profile()` en `StudentRiskStratifier`.

    Requisitos:

    1. Usar `self.summary_df`.
    2. Si no existe, llamar a `self.compute_profile()`.
    3. Construir un gráfico de barras:
       - eje x: `age_group`
       - eje y: `prop_high_cholesterol`
    4. Diferenciar `sex` con color (`hue`).
    5. Agregar título y etiquetas.
    6. Usar rango en y entre 0 y 1.
    7. Retornar `ax`.

    Pregunta final:

    > ¿Tu gráfico permite comparar rápidamente entre edades y entre sexos sin explicación adicional?
    """)
    return


@app.cell(hide_code=True)
def _():
    _tip_content = TipContent(
        items_raw=[
            r"""
    <Entrada del gráfico>
    La tabla resumen ya contiene la proporción que necesitas graficar.
    """,
            r"""
    <Tipo de gráfico>
    Aquí basta con una comparación de proporciones entre subgrupos; un gráfico de barras agrupadas sigue siendo adecuado.
    """,
            r"""
    <Convención de salida>
    En esta lección usaremos como convención devolver `ax`.
    """,
            r"""
    <solucion>
    ```python
    def visualize_profile(self):
    if self.summary_df is None:
        self.compute_profile()

    plot_df = self.summary_df.copy()

    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    sns.barplot(
        data=plot_df,
        x="age_group",
        y="prop_high_cholesterol",
        hue="sex",
        ax=ax,
    )

    ax.set_title("Proporción de colesterol alto por edad y sexo")
    ax.set_xlabel("Grupo de edad")
    ax.set_ylabel("Proporción")
    ax.set_ylim(0, 1)
    ax.legend(title="Sexo")
    fig.tight_layout()
    return ax
    ```
    """,
        ]
    )
    _tip_content.render()
    return


@app.cell(hide_code=True)
def _():
    _test_content = TestContent(
        items_raw=[
            r"""
    <Tipo de salida>
    ```python
    student = StudentRiskStratifier(cohort_raw)
    student.clean_data()
    student.compute_profile()
    ax = student.visualize_profile()

    assert ax is not None
    assert isinstance(ax, Axes)
    print("El método devuelve un objeto gráfico.")
    ```
    """,
            r"""
    <Etiquetas mínimas>
    ```python
    assert ax.get_title() != ""
    assert ax.get_xlabel() != ""
    assert ax.get_ylabel() != ""
    print("Etiquetas definidas.")
    ```
    """,
            r"""
    <Rango esperado>
    ```python
    ymin, ymax = ax.get_ylim()
    assert ymin <= 0
    assert ymax >= 1
    print("Rango vertical adecuado.")
    ```
    """,
        ],
        namespace=globals(),
    )
    _test_content.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 8) Flujo completo integrado

    A continuación se muestra el flujo completo usando la clase de referencia.

    La secuencia esperada es:

    `raw_df → clean_data() → compute_profile() → visualize_profile()`

    Observa que cada método se apoya en el resultado anterior, pero no reemplaza su responsabilidad.

    Haz lo mismo con tu clase `StudentRiskStratifier` para asegurarte de que el flujo completo funciona sin errores y se parece al de referencia.
    """)
    return


@app.cell
def _(cohort_raw):
    final_analyzer = CohortProfileAnalyzer(cohort_raw)
    final_cleaned = final_analyzer.clean_data()
    final_summary = final_analyzer.compute_profile()
    final_ax = final_analyzer.visualize_profile()

    final_cleaned.head(6), final_summary, final_ax
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 9) Lectura final del diseño

    Con esta arquitectura ya podemos responder preguntas concretas sin mezclar fases.

    Por ejemplo:

    - ¿qué subgrupo tiene mayor proporción de hipertensión?
    - ¿qué método habría que modificar si cambia la forma de limpiar etiquetas?
    - ¿qué método habría que modificar si cambia la visualización final?

    La respuesta estructural resume la lección:

    - si cambia la preparación, modificas `clean_data()`;
    - si cambia el resumen, modificas `compute_profile()`;
    - si cambia la comunicación visual, modificas `visualize_profile()`.

    Eso es separación de responsabilidades.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Extensión — Cuando el problema crece

    Ahora imagina que el problema deja de ser simple.

    Empiezan a aparecer nuevas necesidades:

    - múltiples definiciones clínicas (ej. distintos puntos de corte),
    - variables longitudinales,
    - múltiples cohortes,
    - diferentes poblaciones de referencia,
    - pruebas estadisticas automatizadas,
    - análisis reproducibles en distintos datasets.

    Pregunta:

    ¿Tu diseño sigue funcionando o se rompe? De esto va a depender que tan robusto es el esquema inicial y que tanto puede adaptarse a nuevas necesidades sin mezclar responsabilidades o agregar más codigo.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Extensión — Adaptaciones en limpieza

    La fase de limpieza puede volverse más potente sin cambiar su rol.

    Ejemplos:

    - mapear códigos clínicos a categorías (ICD, SNOMED),
    - aplicar múltiples definiciones (ej. diabetes por laboratorio vs diagnóstico),
    - manejar missingness de forma explícita,
    - crear variables derivadas complejas (scores, índices).

    La regla no cambia:

    Todo lo que define *qué significa cada variable* vive aquí.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Extensión — Adaptaciones en el perfil

    El resumen puede escalar en complejidad.

    Ejemplos:

    - estratificar por más dimensiones (edad × sexo × cohorte),
    - incorporar pesos muestrales,
    - calcular intervalos de confianza,
    - comparar grupos (diferencias, ratios),
    - integrar modelos (ej. regresión en lugar de medias simples).
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Extensión — Adaptaciones en visualización

    La visualización también puede evolucionar.

    Ejemplos:

    - múltiples métricas en paneles (faceting),
    - incertidumbre (barras de error),
    - comparaciones longitudinales,
    - dashboards interactivos,
    - diferentes audiencias (clínica vs técnica).

    La función no cambia:

    No produce datos, solo los comunica.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Lectura final

    El diseño no está hecho para este ejercicio.

    Está hecho para escalar.

    Si mañana cambias:

    - la definición de exposición,
    - la estructura del dataset,
    - el tipo de análisis,
    - o la forma de comunicar resultados,

    no reescribes todo.

    Solo modificas una parte.

    Esa es la diferencia entre código que funciona
    y código que se puede usar repetidamente en diferentes investigaciones.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Cierre conceptual

    En una clase analítica intermedia, separar responsabilidades no es un detalle de estilo.

    Es una decisión de diseño que ayuda a:

    - leer mejor el código,
    - detectar errores más rápido,
    - reutilizar resultados,
    - probar cada fase por separado,
    - y modificar una parte del flujo sin romper las demás.

    Idea final:

    una buena clase analítica no intenta hacer todo al mismo tiempo.

    Hace el análisis por etapas claras:

    **limpiar → calcular → visualizar**

    Esa secuencia será la base para arquitecturas más robustas en las siguientes lecciones.
    """)
    return


if __name__ == "__main__":
    app.run()
