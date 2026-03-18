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
    import seaborn as sns
    import matplotlib.pyplot as plt
    from pathlib import Path

    sns.set_theme(style="whitegrid")
    pd.options.display.max_columns = 50
    pd.options.display.float_format = "{:.2f}".format

    def locate_dataset() -> Path:
        candidates = [
            Path(__file__).with_name("dataset_clase_semana2_small.csv"),
            Path("dataset_clase_semana2_small.csv"),
            Path("/mnt/data/dataset_clase_semana2_small.csv"),
        ]
        for path in candidates:
            if path.exists():
                return path
        raise FileNotFoundError(
            "No se encontró dataset_clase_semana2_small.csv en una ruta accesible."
        )

    def render_tips(items: list[str]):
        blocks = []
        for idx, item in enumerate(items, start=1):
            blocks.append(
                mo.md(
                    rf"""
**Tip {idx}.** {item}
"""
                )
            )
        return mo.accordion({"Tips": mo.vstack(blocks)})

    def note(text: str):
        return mo.callout(mo.md(text), kind="info")


@app.cell(hide_code=True)
def _():
    mo.md(r"""
# Semana 3 · Lección 3 · Visualización estadística con seaborn

## Propósito de la sesión

En esta lección trabajaremos la **visualización estadística con seaborn** como una capa de abstracción que se integra naturalmente con `pandas`.

La idea no es dibujar gráficos “bonitos” por sí mismos, sino usar gráficos para responder preguntas analíticas sobre datos de salud.

### Preguntas que guían la sesión

- ¿Cómo cambia una variable numérica entre grupos clínicos?
- ¿Cómo exploramos una relación entre dos medidas continuas?
- ¿Cómo resumimos correlaciones entre variables numéricas?
- ¿Qué aporta seaborn por encima de matplotlib cuando ya tenemos un `DataFrame`?

### Librerías de la sesión

- `pandas` para manipulación tabular
- `matplotlib` como base de dibujo
- `seaborn` para visualización estadística de alto nivel

### Regla metodológica

Antes de elegir un gráfico, define primero:

1. la **pregunta analítica**,
2. el **tipo de variables** involucradas,
3. y la **comparación** que realmente quieres mostrar.
""")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
## 1) Dataset de trabajo

Usaremos el dataset adjunto de la semana 2, que contiene variables sociodemográficas, clínicas y funcionales de una cohorte sintética en salud.

Cada fila representa una persona. Esto es importante porque las visualizaciones que construyamos deben interpretarse a nivel individual agregado por subgrupos.

Nos concentraremos en cuatro tipos de variables:

- **numéricas:** `age`, `sbp_mmHg`, `glucose_mg_dL`, `ldl_mg_dL`
- **categóricas clínicas:** `hypertension`, `Diabetes`, `bmi_category`
- **categóricas sociodemográficas:** `sex`, `education_grouped`
- **categóricas derivadas:** `sbp_cat`, `glucose_cat`, `ldl_cat`
""")
    return


@app.cell
def _():
    data_path = locate_dataset()
    df = pd.read_csv(data_path)

    expected_columns = {
        "ID",
        "age",
        "sex",
        "Diabetes",
        "hypertension",
        "bmi_category",
        "sbp_mmHg",
        "glucose_mg_dL",
        "ldl_mg_dL",
    }
    assert expected_columns.issubset(df.columns)
    df.head()
    return data_path, df


@app.cell
def _(df):
    df_info = pd.DataFrame(
        {
            "column": df.columns,
            "dtype": df.dtypes.astype(str).values,
            "missing": df.isna().sum().values,
            "n_unique": df.nunique(dropna=False).values,
        }
    )
    df_info
    return (df_info,)


@app.cell(hide_code=True)
def _(data_path, df):
    mo.vstack(
        [
            note(
                rf"""
**Ruta detectada del dataset:** `{data_path}`

**Dimensión del dataset:** {df.shape[0]} filas × {df.shape[1]} columnas.
"""
            ),
            mo.md(r"""
Observa que ya no estamos en una fase de carga o limpieza intensa: esa parte del curso ya fue cubierta.

Aquí partimos de un `DataFrame` listo para explorar y nos enfocamos en la relación entre:

- el tipo de variable,
- la pregunta analítica,
- y el gráfico más informativo.
"""),
        ]
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
## 2) Seaborn como interfaz estadística sobre `DataFrame`

Mientras `matplotlib` nos obliga a controlar explícitamente muchos componentes del gráfico, seaborn trabaja mejor cuando ya tenemos un `DataFrame` y podemos decirle directamente:

- qué columna va al eje `x`,
- qué columna va al eje `y`,
- y qué variable define los grupos.

Esto permite pasar más rápido de la tabla a una visualización con intención analítica.

En esta sesión trabajaremos cuatro gráficos centrales:

1. `boxplot` para comparar distribuciones por grupo,
2. `regplot` para evaluar asociación entre variables numéricas,
3. `violinplot` para inspeccionar forma y densidad de una distribución,
4. `heatmap` para resumir correlaciones en forma matricial.
""")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
## 3) `boxplot`: comparar distribuciones entre grupos clínicos

Un `boxplot` resume una distribución usando una lógica compacta:

- mediana,
- cuartiles,
- dispersión,
- y posibles valores extremos.

Es útil cuando queremos responder preguntas del tipo:

> ¿La presión arterial sistólica parece distinta entre personas con y sin hipertensión?

Aquí la lógica de variables es:

- variable categórica en `x`: `hypertension`
- variable numérica en `y`: `sbp_mmHg`
""")
    return


@app.cell
def _(df):
    hypertension_order = ["No", "Yes"]
    boxplot_input = df[["hypertension", "sbp_mmHg"]].dropna().copy()

    fig_box, ax_box = plt.subplots(figsize=(8, 4.5))
    sns.boxplot(
        data=boxplot_input,
        x="hypertension",
        y="sbp_mmHg",
        order=hypertension_order,
        ax=ax_box,
    )
    ax_box.set_title("Presión arterial sistólica según antecedente de hipertensión")
    ax_box.set_xlabel("Hipertensión reportada")
    ax_box.set_ylabel("PAS (mmHg)")
    fig_box
    return boxplot_input, fig_box, hypertension_order


@app.cell
def _(boxplot_input):
    sbp_summary_by_hypertension = (
        boxplot_input.groupby("hypertension", as_index=False)
        .agg(
            n_people=("sbp_mmHg", "count"),
            mean_sbp=("sbp_mmHg", "mean"),
            median_sbp=("sbp_mmHg", "median"),
        )
        .sort_values("hypertension")
    )
    sbp_summary_by_hypertension
    return (sbp_summary_by_hypertension,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
### Interpretación conceptual

Este gráfico no muestra solamente promedios. También deja ver:

- si la distribución está desplazada hacia arriba o hacia abajo,
- si un grupo presenta mayor variabilidad,
- y si existen valores muy altos o muy bajos que merecen atención.

En salud, esto es especialmente útil porque dos grupos pueden tener medias parecidas pero distribuciones muy distintas.
""")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
## Mini-reto 1 — Resumen para un `boxplot` clínico

Construye una tabla llamada `mini1_summary` que resuma `sbp_mmHg` por `sex`.

La tabla debe tener exactamente estas columnas:

- `sex`
- `n_people`
- `mean_sbp`
- `median_sbp`

Además, ordénala alfabéticamente por `sex`.

La idea de este reto es reforzar que una buena visualización estadística casi siempre parte de entender primero la estructura tabular que la respalda.
""")
    return


@app.cell
def _(df):
    # === TU TURNO (EDITA ESTA CELDA) ===
    mini1_summary = None
    return (mini1_summary,)


@app.cell(hide_code=True)
def _():
    render_tips(
        [
            "La variable de agrupación es `sex` y la variable numérica a resumir es `sbp_mmHg`.",
            "Usa `groupby(..., as_index=False)` junto con `agg(...)` para construir varias métricas en una sola tabla.",
            "La función `count` sobre `sbp_mmHg` te permite obtener el número de personas con dato disponible en cada grupo.",
            "Si quieres verificar tu lógica antes del test, compara tu tabla con la idea: una fila por sexo y tres métricas numéricas de resumen.",
        ]
    )
    return


@app.cell(hide_code=True)
def _(mini1_summary):
    mo.stop(
        mini1_summary is None,
        mo.callout(
            mo.md("Aún no has definido `mini1_summary`. Completa la celda del ejercicio y vuelve a ejecutar."),
            kind="warn",
        ),
    )

    assert isinstance(mini1_summary, pd.DataFrame), "`mini1_summary` debe ser un DataFrame."
    assert list(mini1_summary.columns) == [
        "sex",
        "n_people",
        "mean_sbp",
        "median_sbp",
    ], "Las columnas no coinciden con lo solicitado."
    assert mini1_summary["sex"].isin(["Female", "Male"]).all(), "Los valores de `sex` no son los esperados."
    assert mini1_summary["n_people"].sum() == df["sbp_mmHg"].notna().sum(), "El total de personas resumidas no coincide."

    mo.callout(mo.md("Tests de Mini-reto 1 superados correctamente."), kind="success")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
## 4) `regplot`: relación entre dos variables numéricas

Cuando la pregunta analítica involucra dos variables continuas, un gráfico de dispersión es una primera estrategia razonable.

Seaborn ofrece `regplot`, que combina:

- nube de puntos,
- y una línea de tendencia lineal.

Pregunta guía:

> ¿Tiende a aumentar la presión arterial sistólica con la edad?

Variables:

- `x = age`
- `y = sbp_mmHg`
""")
    return


@app.cell
def _(df):
    scatter_input = df[["age", "sbp_mmHg"]].dropna().copy()

    fig_reg, ax_reg = plt.subplots(figsize=(8, 4.8))
    sns.regplot(
        data=scatter_input,
        x="age",
        y="sbp_mmHg",
        scatter_kws={"alpha": 0.35},
        line_kws={"linewidth": 2},
        ax=ax_reg,
    )
    ax_reg.set_title("Edad y presión arterial sistólica")
    ax_reg.set_xlabel("Edad (años)")
    ax_reg.set_ylabel("PAS (mmHg)")
    fig_reg
    return fig_reg, scatter_input


@app.cell(hide_code=True)
def _():
    mo.md(r"""
### ¿Qué leer en un `regplot`?

No debemos interpretar la línea como causalidad. Aquí la función principal es descriptiva:

- identificar si la relación parece positiva o negativa,
- observar si la nube es muy dispersa,
- y detectar si existen patrones no lineales o puntos atípicos.

En un análisis clínico real, este tipo de gráfico suele ser una inspección inicial antes de modelar o ajustar por covariables.
""")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
## Mini-reto 2 — Matriz de correlación para `heatmap`

Antes de construir un `heatmap`, necesitamos una matriz que resuma relaciones entre variables numéricas.

Construye un objeto llamado `mini2_corr` usando exclusivamente estas columnas:

- `age`
- `sbp_mmHg`
- `glucose_mg_dL`
- `ldl_mg_dL`

El resultado debe ser una matriz de correlación cuadrada de 4 × 4.
""")
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    mini2_corr = None
    return (mini2_corr,)


@app.cell(hide_code=True)
def _():
    render_tips(
        [
            "Primero selecciona un subconjunto del DataFrame con las cuatro variables numéricas pedidas.",
            "La función `.corr()` aplicada sobre un DataFrame numérico produce directamente la matriz de correlación.",
            "Recuerda que una matriz de correlación válida debe ser simétrica y tener 1 en la diagonal principal.",
            "No necesitas agrupar ni transformar el dataset: este reto es una relación global entre variables continuas.",
        ]
    )
    return


@app.cell(hide_code=True)
def _(mini2_corr):
    mo.stop(
        mini2_corr is None,
        mo.callout(
            mo.md("Aún no has definido `mini2_corr`. Completa la celda del ejercicio y vuelve a ejecutar."),
            kind="warn",
        ),
    )

    expected = ["age", "sbp_mmHg", "glucose_mg_dL", "ldl_mg_dL"]
    assert isinstance(mini2_corr, pd.DataFrame), "`mini2_corr` debe ser un DataFrame."
    assert list(mini2_corr.index) == expected, "El índice debe respetar el orden solicitado."
    assert list(mini2_corr.columns) == expected, "Las columnas deben respetar el orden solicitado."
    assert mini2_corr.shape == (4, 4), "La matriz debe ser de 4 × 4."
    assert np.allclose(np.diag(mini2_corr), 1.0), "La diagonal de una matriz de correlación debe ser 1."

    mo.callout(mo.md("Tests de Mini-reto 2 superados correctamente."), kind="success")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
## 5) `heatmap`: resumir correlaciones en una matriz visual

Un `heatmap` es útil cuando queremos mostrar varias relaciones al mismo tiempo y ya disponemos de una matriz numérica.

En este caso, cada celda resume la correlación entre dos variables clínicas.

Ventajas:

- sintetiza muchas relaciones en poco espacio,
- facilita identificar asociaciones altas, bajas o cercanas a cero,
- y sirve como exploración rápida antes de un análisis posterior.
""")
    return


@app.cell
def _(df):
    corr_vars = ["age", "sbp_mmHg", "glucose_mg_dL", "ldl_mg_dL"]
    corr_matrix = df[corr_vars].corr()

    fig_heat, ax_heat = plt.subplots(figsize=(6.5, 5.5))
    sns.heatmap(
        corr_matrix,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        vmin=-1,
        vmax=1,
        ax=ax_heat,
    )
    ax_heat.set_title("Correlaciones entre variables clínicas numéricas")
    fig_heat
    return corr_matrix, corr_vars, fig_heat


@app.cell(hide_code=True)
def _():
    mo.md(r"""
### Lectura analítica de un `heatmap`

La intensidad del color no reemplaza la lectura del número. Debemos usar ambos componentes:

- el color ayuda a localizar patrones rápidamente,
- el valor anotado permite interpretar la magnitud con precisión.

Recuerda además que correlación no implica causalidad. Aquí el objetivo es explorar co-variación, no establecer mecanismos causales.
""")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
## 6) `violinplot`: distribución + densidad

El `violinplot` combina una lógica similar al `boxplot` con una representación de densidad.

Es especialmente útil cuando queremos comparar la forma de la distribución entre grupos y no solo sus cuantiles.

Pregunta guía:

> ¿Cómo se distribuye la glucosa según la categoría de IMC?

Variables:

- `x = bmi_category`
- `y = glucose_mg_dL`

Para que la lectura sea clínicamente más clara, ordenaremos las categorías de IMC desde menor a mayor nivel de exceso de peso.
""")
    return


@app.cell
def _(df):
    bmi_order = [
        "Underweight (<18.5)",
        "Normal (18.6-25)",
        "Overweight (25-29.9)",
        "Obese (30-39.9)",
        "Severe Obesity (40+)",
    ]

    violin_input = df[["bmi_category", "glucose_mg_dL"]].dropna().copy()
    violin_input = violin_input[violin_input["bmi_category"].isin(bmi_order)]

    fig_violin, ax_violin = plt.subplots(figsize=(10, 5.2))
    sns.violinplot(
        data=violin_input,
        x="bmi_category",
        y="glucose_mg_dL",
        order=bmi_order,
        cut=0,
        inner="quartile",
        ax=ax_violin,
    )
    ax_violin.set_title("Distribución de glucosa según categoría de IMC")
    ax_violin.set_xlabel("Categoría de IMC")
    ax_violin.set_ylabel("Glucosa (mg/dL)")
    ax_violin.tick_params(axis="x", rotation=20)
    fig_violin
    return bmi_order, fig_violin, violin_input


@app.cell(hide_code=True)
def _():
    mo.md(r"""
### Comparación entre `boxplot` y `violinplot`

Ambos gráficos sirven para comparar distribuciones entre grupos.

- `boxplot`: más compacto y muy útil para reportes rápidos.
- `violinplot`: más expresivo cuando interesa la forma de la distribución.

En términos docentes, conviene recordar esta regla:

> si la pregunta central es sobre **mediana y dispersión**, un `boxplot` suele bastar;
> si la pregunta central es también sobre **forma y concentración**, el `violinplot` aporta más información.
""")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
## Mini-reto 3 — Resumen final para una visualización clínica por IMC

Construye una tabla llamada `mini3_summary` que resuma el perfil cardiometabólico por `bmi_category`.

Debe contener exactamente estas columnas:

- `bmi_category`
- `n_people`
- `mean_glucose`
- `mean_sbp`
- `prop_diabetes`

Reglas:

- `prop_diabetes` debe calcularse como proporción de personas con `Diabetes == "Yes"`.
- Ordena el resultado **de mayor a menor** según `mean_glucose`.

Este mini-reto final integra los contenidos ya vistos en el curso:

- selección de columnas,
- creación de una variable booleana derivada,
- `groupby` + `agg`,
- y preparación de una tabla lista para visualización con seaborn.
""")
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    mini3_summary = None
    return (mini3_summary,)


@app.cell(hide_code=True)
def _():
    render_tips(
        [
            "Puedes crear una columna booleana derivada con `assign(diabetes_flag=...)` y luego agrupar.",
            "El promedio de una columna booleana en pandas se interpreta como proporción cuando `True` representa el evento de interés.",
            "Asegúrate de que el conteo use una columna que no tenga valores faltantes estructurales, por ejemplo `ID`.",
            "El orden final debe priorizar las categorías con mayor `mean_glucose`, porque esa es la lógica analítica pedida.",
        ]
    )
    return


@app.cell(hide_code=True)
def _(df, mini3_summary):
    mo.stop(
        mini3_summary is None,
        mo.callout(
            mo.md("Aún no has definido `mini3_summary`. Completa la celda del ejercicio y vuelve a ejecutar."),
            kind="warn",
        ),
    )

    assert isinstance(mini3_summary, pd.DataFrame), "`mini3_summary` debe ser un DataFrame."
    assert list(mini3_summary.columns) == [
        "bmi_category",
        "n_people",
        "mean_glucose",
        "mean_sbp",
        "prop_diabetes",
    ], "Las columnas no coinciden con lo solicitado."
    assert mini3_summary["prop_diabetes"].between(0, 1).all(), "`prop_diabetes` debe estar entre 0 y 1."
    assert mini3_summary["n_people"].sum() == df["bmi_category"].notna().sum(), "La suma de `n_people` no coincide con el total esperado."
    assert mini3_summary["mean_glucose"].is_monotonic_decreasing, "La tabla debe quedar ordenada de mayor a menor `mean_glucose`."

    mo.callout(mo.md("Tests de Mini-reto 3 superados correctamente."), kind="success")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
## 7) Buenas prácticas mínimas al usar seaborn en análisis de salud

1. **Nombrar claramente ejes y título**
   Evita dejar etiquetas genéricas o nombres crudos si dificultan la lectura.

2. **No sobredibujar variables innecesarias**
   Un gráfico responde mejor cuando está alineado con una sola pregunta analítica.

3. **Ordenar categorías cuando el orden importa**
   IMC, categorías clínicas o niveles educativos suelen requerir un orden deliberado.

4. **Separar descripción de inferencia**
   Un gráfico descriptivo muestra patrones; no demuestra causalidad por sí mismo.

5. **Usar la tabla como respaldo de la figura**
   Muchas veces conviene mirar primero el resumen tabular y luego visualizar.
""")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
## Cierre conceptual

En esta lección, seaborn apareció como una extensión natural del trabajo tabular ya realizado con `pandas`.

La secuencia analítica que conviene conservar es:

**pregunta → tipo de variable → tabla base → gráfico → interpretación**

### Idea central de la sesión

La visualización estadística no reemplaza el análisis tabular, sino que lo hace más legible.

### Herramientas que ya dominas al terminar esta lección

- `sns.boxplot()` para comparar distribuciones por grupo,
- `sns.regplot()` para explorar asociación entre variables numéricas,
- `sns.heatmap()` para resumir matrices de correlación,
- `sns.violinplot()` para inspeccionar forma y densidad de distribuciones.

El siguiente paso natural en el curso será pensar cada vez más en la visualización no solo como exploración, sino también como comunicación deliberada de hallazgos.
""")
    return


if __name__ == "__main__":
    app.run()
