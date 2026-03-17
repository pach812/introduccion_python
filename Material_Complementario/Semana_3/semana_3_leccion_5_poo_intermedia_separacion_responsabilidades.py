# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "pandas",
#     "numpy",
#     "matplotlib",
#     "seaborn",
# ]
# ///

import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


with app.setup(hide_code=True):
    import re
    from pathlib import Path

    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import seaborn as sns

    sns.set_theme(style="whitegrid")

    class _PanelContent:
        def __init__(self, items_raw, header):
            self.items_raw = items_raw
            self.header = header

        def _parse_item(self, raw_text):
            text = raw_text.strip()
            match = re.match(r"<([^>]+)>\s*(.*)", text, flags=re.DOTALL)
            if match:
                title = match.group(1).strip()
                body = match.group(2).strip()
            else:
                title = "Sección"
                body = text
            return title, body

        def render(self):
            blocks = []
            for item in self.items_raw:
                title, body = self._parse_item(item)
                blocks.append(
                    f"""
<details>
<summary><strong>{title}</strong></summary>

{body}

</details>
"""
                )

            return mo.md(
                f"### {self.header}\n\n" + "\n".join(blocks)
            )


    class TipContent(_PanelContent):
        def __init__(self, items_raw):
            super().__init__(items_raw=items_raw, header="Tips")


    class TestContent(_PanelContent):
        def __init__(self, items_raw):
            super().__init__(items_raw=items_raw, header="Test")


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
# Semana 3 · Lección 5 · POO intermedia y separación de responsabilidades

## Propósito de la sesión

Diseñar una clase analítica simple para datos de salud separando responsabilidades en tres métodos:

- `clean_data()`
- `compute_profile()`
- `visualize_profile()`

## Pregunta guía

Queremos responder una pregunta sencilla pero realista:

> **¿Cómo cambia el perfil cardiometabólico entre subgrupos definidos por sexo y diabetes?**

Trabajaremos con un dataset tabular de salud ya conocido, pero ahora el foco no estará solo en pandas o en gráficos por separado, sino en **cómo organizar el análisis dentro de una clase** para que el flujo sea más claro, reusable y mantenible.

## Idea central de la lección

Una clase analítica intermedia no debe mezclar todo en un solo método.

La meta es dividir el trabajo así:

1. **clean**  
   preparar y estandarizar la tabla;

2. **compute**  
   calcular resúmenes o métricas;

3. **visualize**  
   construir una visualización a partir de un resultado ya resumido.
"""
    )
    return


@app.cell
def _(Path, pd):
    base_path = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
    csv_path = base_path / "dataset_clase_semana2_small.csv"

    cohort_raw = pd.read_csv(csv_path)

    cohort_raw.head(8)
    return cohort_raw, csv_path


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
## 1) Dataset y variables de trabajo

Usaremos una cohorte sintética con variables sociodemográficas, clínicas y funcionales.

Para esta sesión nos concentraremos en un subconjunto pequeño de variables:

- `ID`
- `age`
- `sex`
- `Diabetes`
- `hypertension`
- `high_cholesterol`
- `sbp_mmHg`
- `glucose_mg_dL`
- `ldl_mg_dL`

### Decisión didáctica

Reducir columnas no es “perder información”.

En diseño analítico, elegir menos variables al inicio ayuda a:

- clarificar la unidad de análisis,
- reducir ruido innecesario,
- y hacer más explícita la responsabilidad de cada método.
"""
    )
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

    cohort_raw[selected_columns].head(10)
    return (selected_columns,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
## 2) El problema de mezclar todo en un solo bloque

Cuando un análisis:

- selecciona columnas,
- recodifica variables,
- agrupa,
- calcula métricas,
- y además grafica,

todo dentro de una sola función o método, el resultado suele ser difícil de leer y difícil de modificar.

### Síntoma clásico

Si necesitas cambiar una etiqueta, una métrica o un gráfico, debes volver a entrar a un bloque enorme de código donde todo está mezclado.

### Alternativa

Separar responsabilidades:

- **`clean_data()`** no debe graficar;
- **`compute_profile()`** no debe limpiar de nuevo;
- **`visualize_profile()`** no debe rehacer el resumen desde cero.

Esta separación mejora la cohesión del código.
"""
    )
    return


@app.cell
def _(cohort_raw, pd):
    def analyze_everything(raw_df: pd.DataFrame) -> pd.DataFrame:
        # This example is intentionally overloaded for teaching purposes.
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

        df["Diabetes"] = df["Diabetes"].str.lower()
        df["has_hypertension"] = df["hypertension"].eq("Yes")
        df["has_high_cholesterol"] = df["high_cholesterol"].eq("Yes")

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
            .sort_values(["sex", "Diabetes"])
        )

        return summary.round(2)

    overloaded_summary = analyze_everything(cohort_raw)
    overloaded_summary
    return overloaded_summary,


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
El resultado anterior puede funcionar, pero la arquitectura sigue siendo pobre:

- si quieres inspeccionar solo la tabla limpia, no tienes un método específico;
- si quieres reutilizar el resumen en otro gráfico, el flujo no está claramente separado;
- si quieres depurar errores, no es fácil saber en qué fase del proceso ocurrió el problema.

Por eso ahora construiremos una clase con tres responsabilidades explícitas.
"""
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
## 3) Estructura objetivo de la clase

[Diagrama conceptual del flujo de una clase analítica con tres pasos: datos crudos → clean_data() → cleaned_df → compute_profile() → summary_df → visualize_profile() → gráfico]

La clase trabajará con tres atributos importantes:

- `raw_df`: tabla original;
- `cleaned_df`: tabla preparada;
- `summary_df`: tabla resumida.

Y con tres métodos principales:

- `clean_data()`
- `compute_profile()`
- `visualize_profile()`
"""
    )
    return


@app.cell
def _(pd, plt, sns):
    class CohortProfileAnalyzer:
        def __init__(self, raw_df: pd.DataFrame):
            self.raw_df = raw_df.copy()
            self.cleaned_df = None
            self.summary_df = None

        def clean_data(self) -> pd.DataFrame:
            # Select only the variables needed for this analytical question.
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

            # Standardize labels and derive boolean indicators.
            df = df.rename(
                columns={
                    "ID": "person_id",
                    "Diabetes": "diabetes",
                    "sbp_mmHg": "sbp",
                    "glucose_mg_dL": "glucose",
                    "ldl_mg_dL": "ldl",
                }
            )

            df["sex"] = df["sex"].str.strip().str.title()
            df["diabetes"] = df["diabetes"].str.strip().str.lower()
            df["has_hypertension"] = df["hypertension"].eq("Yes")
            df["has_high_cholesterol"] = df["high_cholesterol"].eq("Yes")

            self.cleaned_df = df
            return self.cleaned_df

        def compute_profile(self) -> pd.DataFrame:
            if self.cleaned_df is None:
                self.clean_data()

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

            self.summary_df = summary
            return self.summary_df

        def visualize_profile(self):
            if self.summary_df is None:
                self.compute_profile()

            plot_df = self.summary_df.copy()

            fig, ax = plt.subplots(figsize=(7, 4.5))
            sns.barplot(
                data=plot_df,
                x="diabetes",
                y="prop_hypertension",
                hue="sex",
                ax=ax,
            )

            ax.set_title("Proporción de hipertensión por sexo y diabetes")
            ax.set_xlabel("Diabetes")
            ax.set_ylabel("Proporción")
            ax.set_ylim(0, 1)
            ax.legend(title="Sexo")
            fig.tight_layout()
            return ax
    return (CohortProfileAnalyzer,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
## 4) Observa la separación de responsabilidades

### `clean_data()`
Su tarea es preparar la tabla:

- seleccionar columnas,
- renombrar variables,
- estandarizar etiquetas,
- derivar indicadores simples.

### `compute_profile()`
Su tarea es resumir:

- agrupar,
- calcular conteos,
- calcular medias,
- calcular proporciones.

### `visualize_profile()`
Su tarea es mostrar el resultado:

- usa la tabla resumen,
- decide ejes y etiquetas,
- construye el gráfico.

La idea más importante es esta:

> cada método debe tener una responsabilidad principal y reconocible.
"""
    )
    return


@app.cell
def _(CohortProfileAnalyzer, cohort_raw):
    analyzer_demo = CohortProfileAnalyzer(cohort_raw)
    clean_demo = analyzer_demo.clean_data()
    summary_demo = analyzer_demo.compute_profile()

    clean_demo.head(8), summary_demo
    return analyzer_demo, clean_demo, summary_demo


@app.cell
def _(analyzer_demo):
    ax_demo = analyzer_demo.visualize_profile()
    ax_demo
    return (ax_demo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
## Mini-reto 1 — Implementar `clean_data()`

**Objetivo:** construir el primer método de la clase.

Debes editar la clase del estudiante para que `clean_data()`:

1. seleccione solo las columnas necesarias,
2. renombre `ID`, `Diabetes`, `sbp_mmHg`, `glucose_mg_dL` y `ldl_mg_dL`,
3. estandarice `sex` y `diabetes`,
4. cree `has_hypertension` y `has_high_cholesterol`,
5. y guarde el resultado en `self.cleaned_df`.

La meta no es resumir ni graficar todavía.

Aquí solo se prepara la tabla.
"""
    )
    return


@app.cell
def _(pd):
    class StudentCohortAnalyzer:
        def __init__(self, raw_df: pd.DataFrame):
            self.raw_df = raw_df.copy()
            self.cleaned_df = None
            self.summary_df = None

        def clean_data(self) -> pd.DataFrame:
            # === TU TURNO (EDITA ESTE MÉTODO) ===
            # Keep only the variables required for the analysis.
            # Rename columns to simpler analysis-friendly names.
            # Standardize the labels in sex and diabetes.
            # Create the boolean indicators requested in the prompt.
            self.cleaned_df = None
            return self.cleaned_df

        def compute_profile(self) -> pd.DataFrame:
            # === TU TURNO (EDITA ESTE MÉTODO EN EL MINI-RETO 2) ===
            self.summary_df = None
            return self.summary_df

        def visualize_profile(self):
            # === TU TURNO (EDITA ESTE MÉTODO EN EL MINI-RETO 3) ===
            return None
    return (StudentCohortAnalyzer,)


@app.cell(hide_code=True)
def _(TipContent):
    _tip_content = TipContent(
        items_raw=[
            r"""
<Seleccionar antes de transformar>
Comienza creando una copia con solo las columnas necesarias.

Eso hace que el método sea más claro y evita cargar variables que no usarás.
""",
            r"""
<Renombrar para facilitar el análisis>
Busca nombres que hagan más legible la siguiente fase del flujo.

En vez de conservar `sbp_mmHg`, `glucose_mg_dL` o `ldl_mg_dL`, usa nombres cortos pero claros.
""",
            r"""
<Estandarización mínima>
Las etiquetas categóricas deben quedar consistentes antes de agrupar.

Piensa en operaciones como `str.strip()`, `str.lower()` o `str.title()`.
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
            "hypertension",
            "high_cholesterol",
            "sbp_mmHg",
            "glucose_mg_dL",
            "ldl_mg_dL",
        ]
    ].copy()

    df = df.rename(
        columns={
            "ID": "person_id",
            "Diabetes": "diabetes",
            "sbp_mmHg": "sbp",
            "glucose_mg_dL": "glucose",
            "ldl_mg_dL": "ldl",
        }
    )

    df["sex"] = df["sex"].str.strip().str.title()
    df["diabetes"] = df["diabetes"].str.strip().str.lower()
    df["has_hypertension"] = df["hypertension"].eq("Yes")
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
def _(TestContent):
    _test_content = TestContent(
        items_raw=[
            r"""
<Salida esperada>
El método debe devolver un DataFrame y además guardarlo en `self.cleaned_df`.

```python
student = StudentCohortAnalyzer(cohort_raw)
cleaned = student.clean_data()

assert cleaned is not None
assert hasattr(cleaned, "columns")
print("La salida tiene estructura tabular.")
```
""",
            r"""
<Columnas mínimas>
Verifica que existan las columnas derivadas y renombradas.

```python
expected_columns = {
    "person_id",
    "age",
    "sex",
    "diabetes",
    "hypertension",
    "high_cholesterol",
    "sbp",
    "glucose",
    "ldl",
    "has_hypertension",
    "has_high_cholesterol",
}
assert expected_columns.issubset(set(cleaned.columns))
print("Columnas correctas.")
```
""",
            r"""
<Estandarización básica>
La columna `diabetes` debe quedar con etiquetas comparables.

```python
assert set(cleaned["diabetes"].unique()).issubset({"yes", "no"})
print("Etiquetas de diabetes estandarizadas.")
```
""",
        ]
    )

    _test_content.render()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
## 5) Fase `compute`: resumir sin volver a limpiar

Una vez que la tabla ya está preparada, la segunda responsabilidad es resumirla.

En esta sesión construiremos un perfil por:

- `sex`
- `diabetes`

y calcularemos:

- tamaño del subgrupo,
- edad media,
- PAS media,
- glucosa media,
- LDL medio,
- proporción con hipertensión,
- proporción con colesterol alto.

Observa que aquí ya no deberíamos volver a recodificar etiquetas ni renombrar columnas.

Eso pertenece a la fase `clean`.
"""
    )
    return


@app.cell
def _(summary_demo):
    summary_demo
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
## Mini-reto 2 — Implementar `compute_profile()`

**Objetivo:** resumir la tabla limpia sin rehacer la limpieza.

Debes editar `compute_profile()` para que:

1. use `self.cleaned_df`,
2. agrupe por `sex` y `diabetes`,
3. calcule las métricas pedidas,
4. ordene el resultado,
5. redondee a dos decimales,
6. y guarde la tabla en `self.summary_df`.

### Pista conceptual

Si `compute_profile()` empieza seleccionando columnas del dataset crudo, entonces está invadiendo la responsabilidad de `clean_data()`.
"""
    )
    return


@app.cell(hide_code=True)
def _(TipContent):
    _tip_content = TipContent(
        items_raw=[
            r"""
<Dependencia entre métodos>
Este método debe depender de una tabla ya limpia.

Si `self.cleaned_df` aún no existe, puedes llamar internamente a `self.clean_data()`.
""",
            r"""
<Agrupación>
El resumen no es por paciente individual sino por subgrupos definidos por dos variables categóricas.

Revisa con cuidado cuáles son esas dos columnas.
""",
            r"""
<Proporciones>
Recuerda que el promedio de una columna booleana puede interpretarse como proporción.

Eso te permite calcular prevalencias simples sin construir fórmulas más largas.
""",
            r"""
<solucion>

```python
def compute_profile(self) -> pd.DataFrame:
    if self.cleaned_df is None:
        self.clean_data()

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

    self.summary_df = summary
    return self.summary_df
```
""",
        ]
    )

    _tip_content.render()
    return


@app.cell(hide_code=True)
def _(TestContent):
    _test_content = TestContent(
        items_raw=[
            r"""
<Existencia del resumen>
El método debe devolver un DataFrame resumen.

```python
student = StudentCohortAnalyzer(cohort_raw)
student.clean_data()
summary = student.compute_profile()

assert summary is not None
assert hasattr(summary, "shape")
print("Resumen generado.")
```
""",
            r"""
<Columnas esperadas>
Revisa que el resultado tenga las métricas pedidas.

```python
assert list(summary.columns) == [
    "sex",
    "diabetes",
    "n_people",
    "mean_age",
    "mean_sbp",
    "mean_glucose",
    "mean_ldl",
    "prop_hypertension",
    "prop_high_cholesterol",
]
print("Columnas correctas.")
```
""",
            r"""
<Rango de proporciones>
Las proporciones deben quedar entre 0 y 1.

```python
assert summary["prop_hypertension"].between(0, 1).all()
assert summary["prop_high_cholesterol"].between(0, 1).all()
print("Proporciones válidas.")
```
""",
        ]
    )

    _test_content.render()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
## 6) Fase `visualize`: usar el resumen, no rehacerlo

Ahora entramos a la tercera responsabilidad.

La visualización debe partir de `self.summary_df`.

Eso significa que el método gráfico debería concentrarse en:

- elegir el tipo de gráfico,
- definir ejes,
- etiquetar bien,
- controlar el rango,
- y mejorar la legibilidad.

No debería volver a agrupar ni recalcular métricas desde la tabla original.

### Relación con lecciones previas

Aquí se integran contenidos vistos en visualización:

- selección de un gráfico adecuado,
- reducción de clutter,
- etiquetas claras,
- y atención al mensaje principal.
"""
    )
    return


@app.cell
def _(ax_demo):
    ax_demo
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
## Mini-reto 3 — Implementar `visualize_profile()`

**Objetivo:** construir el gráfico final del flujo de la clase.

Debes editar `visualize_profile()` para que:

1. use `self.summary_df`,
2. construya un gráfico de barras con `diabetes` en el eje x,
3. use `prop_hypertension` en el eje y,
4. diferencie `sex` mediante color,
5. defina título, etiquetas y rango vertical entre 0 y 1,
6. y devuelva el objeto `ax`.

Este es el mini-reto final de la sesión y reúne:

- diseño de clase,
- resumen tabular,
- y visualización analítica.
"""
    )
    return


@app.cell(hide_code=True)
def _(TipContent):
    _tip_content = TipContent(
        items_raw=[
            r"""
<Entrada del gráfico>
No necesitas volver a calcular la proporción de hipertensión.

Ese valor ya existe en la tabla resumen.
""",
            r"""
<Elección del gráfico>
Aquí quieres comparar una proporción entre categorías y subgrupos.

Un gráfico de barras agrupadas es suficiente y más claro que alternativas más complejas.
""",
            r"""
<Legibilidad>
No olvides definir título, etiquetas de ejes y límite vertical.

Eso hace que la figura sea más interpretables y comparable entre ejecuciones.
""",
            r"""
<solucion>

```python
def visualize_profile(self):
    if self.summary_df is None:
        self.compute_profile()

    plot_df = self.summary_df.copy()

    fig, ax = plt.subplots(figsize=(7, 4.5))
    sns.barplot(
        data=plot_df,
        x="diabetes",
        y="prop_hypertension",
        hue="sex",
        ax=ax,
    )

    ax.set_title("Proporción de hipertensión por sexo y diabetes")
    ax.set_xlabel("Diabetes")
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
def _(TestContent):
    _test_content = TestContent(
        items_raw=[
            r"""
<Tipo de salida>
La convención usada en esta sesión es devolver `ax`.

```python
student = StudentCohortAnalyzer(cohort_raw)
student.clean_data()
student.compute_profile()
ax = student.visualize_profile()

assert ax is not None
print("El método devuelve un objeto gráfico.")
```
""",
            r"""
<Etiquetas mínimas>
El gráfico debe tener información textual básica.

```python
assert ax.get_title() != ""
assert ax.get_xlabel() != ""
assert ax.get_ylabel() != ""
print("Etiquetas definidas.")
```
""",
            r"""
<Rango esperado>
La proporción debe representarse en escala 0 a 1.

```python
ymin, ymax = ax.get_ylim()
assert ymin <= 0
assert ymax >= 1
print("Rango vertical adecuado.")
```
""",
        ]
    )

    _test_content.render()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
## 7) Ejecución integrada del flujo completo

A continuación se muestra el flujo completo usando la clase de referencia.

La secuencia esperada es:

`raw_df → clean_data() → compute_profile() → visualize_profile()`

Observa que cada método se apoya en el resultado anterior, pero no reemplaza su responsabilidad.
"""
    )
    return


@app.cell
def _(CohortProfileAnalyzer, cohort_raw):
    final_analyzer = CohortProfileAnalyzer(cohort_raw)
    final_cleaned = final_analyzer.clean_data()
    final_summary = final_analyzer.compute_profile()
    final_ax = final_analyzer.visualize_profile()

    final_cleaned.head(6), final_summary, final_ax
    return final_analyzer, final_ax, final_cleaned, final_summary


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
## 8) Lectura analítica del ejemplo

Con esta arquitectura ya podemos responder preguntas concretas sin mezclar fases.

Por ejemplo:

- ¿qué subgrupo tiene mayor proporción de hipertensión?
- ¿la diabetes se asocia con una carga cardiometabólica mayor en ambos sexos?
- ¿qué parte del flujo habría que modificar si ahora quisiéramos otro gráfico?

La respuesta a la última pregunta es justamente la enseñanza estructural de la sesión:

- si cambia la preparación, modificas `clean_data()`;
- si cambia el resumen, modificas `compute_profile()`;
- si cambia la comunicación visual, modificas `visualize_profile()`.

Eso es separación de responsabilidades.
"""
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
## Cierre conceptual

En una clase analítica intermedia, separar responsabilidades no es un detalle estético.

Es una decisión de diseño que ayuda a:

- leer mejor el código,
- detectar errores más rápido,
- reutilizar resultados,
- y modificar una parte del flujo sin romper las demás.

### Idea final

Una buena clase analítica no hace “todo al tiempo”.

Hace el análisis por etapas claras:

**limpiar → calcular → visualizar**

Esa secuencia será la base para las siguientes arquitecturas analíticas del curso.
"""
    )
    return


if __name__ == "__main__":
    app.run()
