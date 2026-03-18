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
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    import altair as alt
    from pathlib import Path

    pd.options.display.max_columns = 50
    pd.options.display.max_rows = 20
    pd.options.display.float_format = "{:.2f}".format

    class TipContent:
        def __init__(self, items_raw):
            self.items_raw = items_raw

        def render(self):
            items = []
            for idx, raw in enumerate(self.items_raw, start=1):
                text = raw.strip()
                if "<solucion>" in text:
                    title = f"Tip {idx} · solución sugerida"
                    body = text.replace("<solucion>", "").strip()
                else:
                    title = f"Tip {idx}"
                    body = text
                items.append({title: mo.md(body)})
            return mo.accordion(items)

    class TestContent:
        def __init__(self, items_raw, namespace=None):
            self.items_raw = items_raw
            self.namespace = namespace if namespace is not None else {}

        def render(self):
            outputs = []
            for idx, raw in enumerate(self.items_raw, start=1):
                block = raw.strip()
                title = block.splitlines()[0].strip() if block else f"Test {idx}"
                code = ""
                if "```python" in block:
                    code = block.split("```python", 1)[1].split("```", 1)[0].strip()
                result = "No se encontró bloque de prueba."
                if code:
                    try:
                        exec(code, self.namespace, self.namespace)
                        result = "✅ Prueba superada"
                    except Exception as exc:
                        result = f"❌ {type(exc).__name__}: {exc}"
                outputs.append({f"Test {idx} · {title}": mo.md(result)})
            return mo.accordion(outputs)

    def dataset_path():
        here = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
        candidates = [
            here / "dataset_clase_semana2_small.csv",
            Path.cwd() / "dataset_clase_semana2_small.csv",
            Path("/mnt/data/dataset_clase_semana2_small.csv"),
        ]
        for candidate in candidates:
            if candidate.exists():
                return candidate
        raise FileNotFoundError(
            "No se encontró `dataset_clase_semana2_small.csv` en una ruta esperada."
        )


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
# Semana 3 · Lección 7
## Construcción de `MLPreAnalysis` e integración completa de análisis modular

En esta sesión construiremos una clase llamada `MLPreAnalysis` que integra en un mismo objeto tres responsabilidades analíticas:

1. **`clean()`** para preparar el dataset.
2. **`compute()`** para producir métricas estructuradas.
3. **`visualize()`** para generar visualizaciones reproducibles.

El objetivo no es introducir aprendizaje automático todavía, sino **diseñar una pre-etapa analítica organizada** que deje los datos listos para exploración y modelado posterior.

Trabajaremos con un dataset de salud pública que contiene variables demográficas, clínicas y funcionales en una cohorte de personas mayores.
"""
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
## 1) Cargar y reconocer el dataset

Antes de construir una clase, conviene entender qué tipo de información deberá administrar.

En este dataset cada fila representa una persona y las columnas combinan:

- características demográficas,
- factores sociales,
- indicadores clínicos,
- y variables categorizadas ya preparadas.

En términos de diseño, nuestra futura clase deberá poder:

- recibir un `DataFrame`,
- guardar una copia interna,
- transformar variables cuando sea necesario,
- producir salidas estructuradas,
- y devolver gráficos listos para comunicar hallazgos.
"""
    )
    return


@app.cell
def _():
    data_path = dataset_path()
    df_raw = pd.read_csv(data_path)

    df_raw.head()
    return data_path, df_raw


@app.cell
def _(df_raw):
    dataset_overview = pd.DataFrame(
        {
            "n_filas": [df_raw.shape[0]],
            "n_columnas": [df_raw.shape[1]],
            "columnas": [", ".join(df_raw.columns.tolist())],
        }
    )

    dataset_overview
    return (dataset_overview,)


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
## 2) De lo tabular al objeto analítico

Hasta ahora hemos trabajado con operaciones sueltas sobre `DataFrame`.  
Ahora cambiaremos de perspectiva: en lugar de pensar solo en pasos aislados, construiremos un **objeto analítico cohesivo**.

La clase `MLPreAnalysis` tendrá atributos para almacenar:

- el dataset original,
- una versión limpia,
- un diccionario de métricas,
- y una lista de gráficos.

Esta organización tiene varias ventajas:

- evita repetir código,
- hace explícita la secuencia del análisis,
- y facilita reutilizar el mismo diseño con otros datasets.
"""
    )
    return


@app.cell
def _():
    class MLPreAnalysis:
        def __init__(self, df: pd.DataFrame):
            self.raw_df = df.copy()
            self.cleaned_df = None
            self.metrics = {}
            self.figures = []

        def clean(self) -> pd.DataFrame:
            df = self.raw_df.copy()

            # Estandarización mínima de texto
            df["sex"] = df["sex"].str.lower().str.strip()
            df["ethnicity"] = df["ethnicity"].str.strip()
            df["residence_area"] = df["residence_area"].str.strip()

            # Conversión explícita de variables numéricas
            numeric_cols = ["age", "sbp_mmHg", "glucose_mg_dL", "ldl_mg_dL"]
            for col in numeric_cols:
                df[col] = pd.to_numeric(df[col], errors="coerce")

            # Derivación de una banda etaria útil para análisis posteriores
            df["age_group"] = pd.cut(
                df["age"],
                bins=[59, 69, 79, 120],
                labels=["60-69", "70-79", "80+"],
            )

            # Bandera clínica simple para una fase pre-analítica
            df["high_cardiometabolic_risk"] = (
                (df["sbp_mmHg"] >= 140) | (df["ldl_mg_dL"] >= 160)
            )

            self.cleaned_df = df
            return self.cleaned_df

        def compute(self) -> dict:
            if self.cleaned_df is None:
                raise ValueError("Primero debes ejecutar `clean()`.")

            df = self.cleaned_df

            n_rows = int(df.shape[0])
            n_columns = int(df.shape[1])

            age_summary = {
                "mean_age": round(float(df["age"].mean()), 2),
                "min_age": int(df["age"].min()),
                "max_age": int(df["age"].max()),
            }

            diabetes_by_sex = (
                df.groupby("sex", as_index=False)
                .agg(
                    n=("ID", "count"),
                    prop_diabetes=("Diabetes", "mean"),
                    mean_sbp=("sbp_mmHg", "mean"),
                )
                .sort_values("sex")
            )

            risk_by_age_group = (
                df.groupby("age_group", as_index=False, observed=False)
                .agg(
                    n=("ID", "count"),
                    prop_high_risk=("high_cardiometabolic_risk", "mean"),
                )
                .sort_values("age_group")
            )

            self.metrics = {
                "dimensions": {"n_rows": n_rows, "n_columns": n_columns},
                "age_summary": age_summary,
                "diabetes_by_sex": diabetes_by_sex,
                "risk_by_age_group": risk_by_age_group,
            }
            return self.metrics

        def visualize(self) -> list:
            if self.cleaned_df is None:
                raise ValueError("Primero debes ejecutar `clean()`.")

            df = self.cleaned_df
            figs = []

            fig1, ax1 = plt.subplots(figsize=(7, 4))
            sns.histplot(data=df, x="age", bins=15, ax=ax1)
            ax1.set_title("Distribución de edad")
            ax1.set_xlabel("Edad")
            ax1.set_ylabel("Frecuencia")
            fig1.tight_layout()
            figs.append(fig1)

            fig2, ax2 = plt.subplots(figsize=(7, 4))
            sns.boxplot(data=df, x="sex", y="sbp_mmHg", ax=ax2)
            ax2.set_title("Presión sistólica por sexo")
            ax2.set_xlabel("Sexo")
            ax2.set_ylabel("PAS (mmHg)")
            fig2.tight_layout()
            figs.append(fig2)

            chart_data = (
                df.groupby("age_group", observed=False, as_index=False)
                .agg(prop_diabetes=("Diabetes", "mean"))
                .sort_values("age_group")
            )

            chart = (
                alt.Chart(chart_data)
                .mark_bar()
                .encode(
                    x=alt.X("age_group:N", title="Grupo de edad"),
                    y=alt.Y("prop_diabetes:Q", title="Proporción con diabetes"),
                    tooltip=["age_group", alt.Tooltip("prop_diabetes", format=".2f")],
                )
                .properties(
                    title="Proporción de diabetes por grupo de edad",
                    width=500,
                    height=280,
                )
            )
            figs.append(chart)

            self.figures = figs
            return self.figures

        def run_all(self) -> dict:
            self.clean()
            self.compute()
            self.visualize()

            return {
                "cleaned_df": self.cleaned_df,
                "metrics": self.metrics,
                "figures": self.figures,
            }

    MLPreAnalysis
    return (MLPreAnalysis,)


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
## 3) Interpretación del diseño de la clase

Observa la lógica de responsabilidades:

- `clean()` modifica estructura y crea variables derivadas.
- `compute()` produce objetos formales que resumen el dataset.
- `visualize()` devuelve una lista de objetos gráficos.
- `run_all()` integra el flujo completo en una sola llamada.

Este patrón retoma contenidos previos del curso:

- `pandas` para transformación tabular,
- POO para encapsular comportamiento,
- y visualización con `matplotlib`, `seaborn` y `altair`.

La idea central es que el objeto no solo **guarda datos**, sino que también **organiza el razonamiento analítico**.
"""
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
## Mini-reto 1 — Crear el objeto y ejecutar la limpieza

En este primer reto debes construir una instancia de `MLPreAnalysis` a partir de `df_raw` y ejecutar el método `clean()`.

Guarda los resultados en dos variables con nombres fijos:

- `analysis_1`
- `clean_df`

Este reto verifica que puedas pasar de un `DataFrame` aislado a un objeto con estado interno.
"""
    )
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    # TODO: crear el objeto y ejecutar la limpieza
    analysis_1 = None
    clean_df = None
    return analysis_1, clean_df


@app.cell(hide_code=True)
def _():
    _tip_content = TipContent(
        items_raw=[
            r"""
Primero necesitas instanciar la clase usando el dataset original.

Después debes llamar el método que devuelve la versión limpia del dataset.
""",
            r"""
La instancia debe guardarse en `analysis_1`.

El `DataFrame` limpio debe guardarse en `clean_df`.
""",
            r"""
<solucion>

```python
analysis_1 = MLPreAnalysis(df_raw)
clean_df = analysis_1.clean()
```
""",
        ]
    )

    _tip_content.render()
    return


@app.cell(hide_code=True)
def _(analysis_1, clean_df):
    _test_content = TestContent(
        items_raw=[
            r"""
Instancia creada

```python
assert analysis_1 is not None, "Debes definir `analysis_1`."
assert hasattr(analysis_1, "clean"), "`analysis_1` debe ser una instancia de la clase."
```
""",
            r"""
DataFrame limpio disponible

```python
assert clean_df is not None, "Debes definir `clean_df`."
assert hasattr(clean_df, "columns"), "`clean_df` debe comportarse como un DataFrame."
```
""",
            r"""
Variables derivadas presentes

```python
assert "age_group" in clean_df.columns, "Falta la columna `age_group`."
assert "high_cardiometabolic_risk" in clean_df.columns, (
    "Falta la columna `high_cardiometabolic_risk`."
)
```
""",
        ],
        namespace=globals(),
    )

    clean_df.head()
    _test_content.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
## 4) Métricas estructuradas como salida formal

En la lección anterior se introdujo la idea de que un análisis reproducible no debería dejar sus resultados dispersos.

Aquí `compute()` devuelve un diccionario con cuatro componentes:

- dimensiones del dataset,
- resumen etario,
- una tabla por sexo,
- una tabla por grupo de edad.

Este diseño tiene una ventaja importante:  
**permite distinguir entre el proceso analítico y sus salidas formales**.
"""
    )
    return


@app.cell
def _(MLPreAnalysis, df_raw):
    analysis_demo = MLPreAnalysis(df_raw)
    analysis_demo.clean()
    demo_metrics = analysis_demo.compute()

    demo_metrics["dimensions"], demo_metrics["age_summary"]
    return analysis_demo, demo_metrics


@app.cell
def _(demo_metrics):
    demo_metrics["diabetes_by_sex"]
    return


@app.cell
def _(demo_metrics):
    demo_metrics["risk_by_age_group"]
    return


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
## Mini-reto 2 — Calcular y guardar métricas centrales

Ahora debes construir una nueva instancia, ejecutar limpieza y luego calcular las métricas estructuradas.

Usa estos nombres fijos:

- `analysis_2`
- `metrics_summary`

Este reto evalúa si puedes recuperar resultados formales desde la clase y reconocer que el producto de `compute()` es un diccionario analítico.
"""
    )
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    # TODO: crear el objeto, limpiar y calcular métricas
    analysis_2 = None
    metrics_summary = None
    return analysis_2, metrics_summary


@app.cell(hide_code=True)
def _():
    _tip_content = TipContent(
        items_raw=[
            r"""
Debes repetir la lógica de creación del objeto.

Después de limpiar, llama al método que produce el diccionario de métricas.
""",
            r"""
Recuerda que `compute()` requiere que `clean()` ya haya sido ejecutado.
""",
            r"""
<solucion>

```python
analysis_2 = MLPreAnalysis(df_raw)
analysis_2.clean()
metrics_summary = analysis_2.compute()
```
""",
        ]
    )

    _tip_content.render()
    return


@app.cell(hide_code=True)
def _(metrics_summary):
    _test_content = TestContent(
        items_raw=[
            r"""
Diccionario definido

```python
assert metrics_summary is not None, "Debes definir `metrics_summary`."
assert isinstance(metrics_summary, dict), "`metrics_summary` debe ser un diccionario."
```
""",
            r"""
Claves principales presentes

```python
expected_keys = {"dimensions", "age_summary", "diabetes_by_sex", "risk_by_age_group"}
assert expected_keys.issubset(metrics_summary.keys()), (
    "Faltan claves principales en `metrics_summary`."
)
```
""",
            r"""
Estructura de dimensiones válida

```python
assert metrics_summary["dimensions"]["n_rows"] > 0, "El número de filas debe ser positivo."
assert metrics_summary["dimensions"]["n_columns"] > 0, "El número de columnas debe ser positivo."
```
""",
        ],
        namespace=globals(),
    )

    metrics_summary
    _test_content.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
## 5) Visualización como parte de la clase

Una decisión de diseño importante en esta lección es que la visualización no aparece como un bloque aislado fuera de la clase.

En cambio, `visualize()` forma parte del objeto y devuelve una lista llamada `figures`.

Esto expresa una idea de arquitectura:

- las visualizaciones son **salidas del sistema analítico**,
- no adornos añadidos al final.

En esta implementación se generan tres objetos:

1. un histograma con `matplotlib`/`seaborn`,
2. un boxplot con `matplotlib`/`seaborn`,
3. un gráfico de barras con `altair`.
"""
    )
    return


@app.cell
def _(analysis_demo):
    demo_figures = analysis_demo.visualize()

    len(demo_figures)
    return (demo_figures,)


@app.cell
def _(demo_figures):
    demo_figures[0]
    return


@app.cell
def _(demo_figures):
    demo_figures[1]
    return


@app.cell
def _(demo_figures):
    demo_figures[2]
    return


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
## 6) Integración completa del flujo

El propósito final de `MLPreAnalysis` es permitir una llamada compacta que mantenga el orden lógico del análisis.

Por eso `run_all()` reúne en un único punto:

- limpieza,
- cálculo de métricas,
- producción de visualizaciones.

El resultado final es un diccionario con tres componentes:

- `cleaned_df`
- `metrics`
- `figures`

Esta es una forma mínima pero potente de integración modular.
"""
    )
    return


@app.cell
def _(MLPreAnalysis, df_raw):
    analysis_full_demo = MLPreAnalysis(df_raw)
    full_demo_outputs = analysis_full_demo.run_all()

    full_demo_outputs.keys()
    return analysis_full_demo, full_demo_outputs


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
## Mini-reto 3 — Ejecutar el flujo completo con `run_all()`

Este mini-reto final integra toda la sesión.

Debes:

1. crear una instancia final,
2. ejecutar el flujo completo,
3. guardar los resultados en variables con nombre fijo.

Usa exactamente estos nombres:

- `analysis_final`
- `final_outputs`

Este reto está alineado con todos los temas ya vistos: `pandas`, visualización, POO intermedia y outputs estructurados.
"""
    )
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    # TODO: ejecutar el flujo analítico completo
    analysis_final = None
    final_outputs = None
    return analysis_final, final_outputs


@app.cell(hide_code=True)
def _():
    _tip_content = TipContent(
        items_raw=[
            r"""
Debes volver a crear una instancia usando `df_raw`.

Luego puedes ejecutar una sola llamada que encapsula todo el flujo.
""",
            r"""
El resultado final debe ser un diccionario con tres componentes principales.
""",
            r"""
<solucion>

```python
analysis_final = MLPreAnalysis(df_raw)
final_outputs = analysis_final.run_all()
```
""",
        ]
    )

    _tip_content.render()
    return


@app.cell(hide_code=True)
def _(final_outputs):
    _test_content = TestContent(
        items_raw=[
            r"""
Objeto de salida definido

```python
assert final_outputs is not None, "Debes definir `final_outputs`."
assert isinstance(final_outputs, dict), "`final_outputs` debe ser un diccionario."
```
""",
            r"""
Claves esperadas presentes

```python
expected_keys = {"cleaned_df", "metrics", "figures"}
assert expected_keys.issubset(final_outputs.keys()), (
    "Las claves esperadas son `cleaned_df`, `metrics` y `figures`."
)
```
""",
            r"""
Lista de figuras válida

```python
assert isinstance(final_outputs["figures"], list), "`figures` debe ser una lista."
assert len(final_outputs["figures"]) == 3, "Se esperaban exactamente 3 objetos gráficos."
```
""",
            r"""
Métricas consistentes

```python
assert final_outputs["metrics"]["dimensions"]["n_rows"] == final_outputs["cleaned_df"].shape[0], (
    "El número de filas en métricas debe coincidir con el DataFrame limpio."
)
```
""",
        ],
        namespace=globals(),
    )

    final_outputs
    _test_content.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
## Cierre conceptual

La clase `MLPreAnalysis` no pretende ser una solución definitiva ni un framework complejo.

Su valor pedagógico está en mostrar cómo integrar, en una misma arquitectura mínima, todo lo que has trabajado hasta ahora:

- manipulación tabular con `pandas`,
- clases con responsabilidades diferenciadas,
- métricas estructuradas en diccionarios y tablas,
- y visualizaciones como objetos formales del análisis.

La transición importante de esta lección es la siguiente:

**de hacer análisis por fragmentos**  
**a diseñar un sistema analítico pequeño, coherente y reutilizable**.

Ese cambio de perspectiva será fundamental para construir, más adelante, flujos analíticos más completos.
"""
    )
    return


if __name__ == "__main__":
    app.run()
