import marimo

__generated_with = "0.20.2"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
# Semana 2 — Lección 6: Encapsulación de procesamiento en clases (Pandas + POO)

**Idea central:** cuando un flujo de limpieza y resumen empieza a crecer (muchas transformaciones encadenadas), conviene **encapsular** ese flujo dentro de una **clase** para:

- mantener un **estado** (el DataFrame y parámetros),
- garantizar **invariantes** (validaciones de esquema y rangos),
- exponer una interfaz clara (métodos como `clean()`, `add_features()`, `summarize()`),
- reducir duplicación y errores al reusar el flujo.

**Contexto de salud pública:** trabajaremos con un dataset sintético de consultas ambulatorias y medidas antropométricas (edad, sexo, peso, talla), y construiremos un pipeline encapsulado para:
1) validar y limpiar,
2) derivar IMC,
3) resumir por sexo y grupo etario,
4) preparar una tabla tipo “prevalencia” usando `pivot_table`.
"""
    )


@app.cell
def _():
    import numpy as np
    import pandas as pd

    return np, pd


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
## 1) Dataset sintético: consultas ambulatorias y antropometría

Características del dataset:

- `patient_id`: identificador del paciente
- `sex`: "female" / "male"
- `age`: edad en años
- `weight_kg`, `height_m`: medidas para IMC
- `visit_type`: tipo de consulta (e.g., "checkup", "follow_up")
- `sbp`: presión sistólica (mmHg), ejemplo clínico simple

> Nota: incluimos algunos valores “problemáticos” para practicar limpieza (strings numéricos, valores faltantes, alturas sospechosas).
"""
    )


@app.cell
def _(np, pd):
    df_raw = pd.DataFrame(
        {
            "patient_id": [101, 102, 103, 104, 105, 106, 107, 108],
            "sex": [
                "female",
                "male",
                "female",
                "male",
                "female",
                "male",
                "female",
                "male",
            ],
            "age": [34, 52, 29, 67, 45, 38, 73, 60],
            "weight_kg": ["68.0", 85.5, 54.2, "92.1", None, 77.0, 61.3, 110.0],
            "height_m": [1.65, "1.78", 1.58, 1.72, 1.60, None, 1.55, 1.90],
            "visit_type": [
                "checkup",
                "follow_up",
                "checkup",
                "follow_up",
                "checkup",
                "checkup",
                "follow_up",
                "follow_up",
            ],
            "sbp": [118, 132, 110, 145, 128, 121, 150, 138],
        }
    )
    df_raw


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
## 2) Encapsulación: una clase que “posee” el DataFrame y el flujo

Vamos a diseñar una clase `CohortProcessor` con:

- **Estado**:
  - `df`: DataFrame de trabajo
  - configuración de columnas (para evitar “strings mágicos” repetidos)

- **Métodos**:
  - `validate_schema()`: verifica columnas requeridas
  - `coerce_types()`: convierte a tipos numéricos donde aplique
  - `drop_invalid_anthropometrics()`: elimina filas imposibles o insuficientes para IMC
  - `add_bmi()`: crea columna IMC
  - `add_age_group()`: deriva grupo etario (categoría)
  - `summarize_by_sex_age()`: resumen con `groupby` + `agg`
  - `prevalence_table_visit_type()`: tabla con `pivot_table`

**Regla didáctica:** cada método hace una sola cosa bien, y el flujo completo se compone encadenando métodos.
"""
    )


@app.cell
def _(np, pd):
    class CohortProcessor:
        """
        Minimal cohort processor for a health dataset.
        Encapsulates: validation, cleaning, feature engineering, and summarization.
        """

        def __init__(
            self,
            df: pd.DataFrame,
            patient_id_col: str = "patient_id",
            sex_col: str = "sex",
            age_col: str = "age",
            weight_col: str = "weight_kg",
            height_col: str = "height_m",
            visit_type_col: str = "visit_type",
            sbp_col: str = "sbp",
        ):
            self.patient_id_col = patient_id_col
            self.sex_col = sex_col
            self.age_col = age_col
            self.weight_col = weight_col
            self.height_col = height_col
            self.visit_type_col = visit_type_col
            self.sbp_col = sbp_col

            # Work on a copy to avoid mutating the original DataFrame by accident
            self.df = df.copy()

        def validate_schema(self) -> "CohortProcessor":
            required = {
                self.patient_id_col,
                self.sex_col,
                self.age_col,
                self.weight_col,
                self.height_col,
                self.visit_type_col,
                self.sbp_col,
            }
            missing = required - set(self.df.columns)
            assert len(missing) == 0, f"Missing required columns: {sorted(missing)}"
            return self

        def coerce_types(self) -> "CohortProcessor":
            # Coerce numeric columns; invalid parses become NaN
            self.df[self.age_col] = pd.to_numeric(
                self.df[self.age_col], errors="coerce"
            )
            self.df[self.weight_col] = pd.to_numeric(
                self.df[self.weight_col], errors="coerce"
            )
            self.df[self.height_col] = pd.to_numeric(
                self.df[self.height_col], errors="coerce"
            )
            self.df[self.sbp_col] = pd.to_numeric(
                self.df[self.sbp_col], errors="coerce"
            )

            # Normalize sex values (defensive)
            self.df[self.sex_col] = (
                self.df[self.sex_col].astype(str).str.strip().str.lower()
            )
            return self

        def drop_invalid_anthropometrics(
            self,
            min_height_m: float = 1.2,
            max_height_m: float = 2.2,
            min_weight_kg: float = 30.0,
            max_weight_kg: float = 250.0,
        ) -> "CohortProcessor":
            # Keep rows with non-missing and plausible height/weight
            mask = self.df[self.height_col].between(
                min_height_m, max_height_m, inclusive="both"
            ) & self.df[self.weight_col].between(
                min_weight_kg, max_weight_kg, inclusive="both"
            )
            self.df = self.df.loc[mask].reset_index(drop=True)
            return self

        def add_bmi(self, bmi_col: str = "bmi") -> "CohortProcessor":
            self.df[bmi_col] = self.df[self.weight_col] / (
                self.df[self.height_col] ** 2
            )
            return self

        def add_age_group(
            self,
            bins=None,
            labels=None,
            age_group_col: str = "age_group",
        ) -> "CohortProcessor":
            if bins is None:
                bins = [0, 18, 35, 50, 65, 200]
            if labels is None:
                labels = ["0-17", "18-34", "35-49", "50-64", "65+"]

            self.df[age_group_col] = pd.cut(
                self.df[self.age_col],
                bins=bins,
                labels=labels,
                right=False,
                include_lowest=True,
            )
            return self

        def summarize_by_sex_age(
            self,
            bmi_col: str = "bmi",
            age_group_col: str = "age_group",
        ) -> pd.DataFrame:
            # Grouped descriptive summary
            out = (
                self.df.groupby([self.sex_col, age_group_col], dropna=False)
                .agg(
                    n_patients=(self.patient_id_col, "nunique"),
                    mean_bmi=(bmi_col, "mean"),
                    mean_sbp=(self.sbp_col, "mean"),
                )
                .reset_index()
            )
            return out

        def prevalence_table_visit_type(
            self,
            age_group_col: str = "age_group",
        ) -> pd.DataFrame:
            # "Prevalence-like" distribution of visit_type by sex and age_group
            tab = pd.pivot_table(
                self.df,
                index=[self.sex_col, age_group_col],
                columns=self.visit_type_col,
                values=self.patient_id_col,
                aggfunc="nunique",
                fill_value=0,
            ).reset_index()
            return tab

    CohortProcessor


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
## 3) Ejecutar el flujo encapsulado (pipeline mínimo)

Estrategia:

1) Validar esquema
2) Coaccionar tipos
3) Eliminar filas sin antropometría válida
4) Calcular IMC
5) Crear grupo etario
6) Producir salidas: resumen y tabla tipo pivot
"""
    )


@app.cell
def _(CohortProcessor, df_raw):
    processor = (
        CohortProcessor(df_raw)
        .validate_schema()
        .coerce_types()
        .drop_invalid_anthropometrics()
        .add_bmi()
        .add_age_group()
    )

    df_clean = processor.df
    df_clean


@app.cell
def _(processor):
    summary = processor.summarize_by_sex_age()
    summary


@app.cell
def _(processor):
    prevalence_like = processor.prevalence_table_visit_type()
    prevalence_like


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
---

## Mini-reto 1 (guiado): validación de rango de IMC dentro de la clase

**Objetivo:** agregar un método `assert_bmi_plausible()` a la clase para asegurar que los IMC calculados estén en un rango razonable (por ejemplo, 10 a 80).

- Si hay valores fuera de rango, el método debe lanzar un `AssertionError`.
- No debe modificar el DataFrame; solo validar.

**Restricción:** usa únicamente conceptos ya vistos (POO + pandas).
"""
    )


@app.cell(hide_code=True)
def _(mo):
    tip_content = mo.md(
        r"""
### Tip (sin dar la respuesta)

- Calcula el IMC **ya existente** (columna `bmi`) y crea una máscara con `between(...)`.
- Si quieres contar cuántos fallan, usa `(~mask).sum()`.
- La condición del `assert` típicamente verifica que **todos** cumplan (por ejemplo, con `mask.all()`).
"""
    )
    return tip_content


@app.cell
def _(CohortProcessor, df_raw):
    # === TU TURNO (EDITA ESTA CELDA) ===
    # Implementa el método en la clase y luego úsalo aquí.

    # 1) Crea el processor como antes
    processor_mr1 = (
        CohortProcessor(df_raw)
        .validate_schema()
        .coerce_types()
        .drop_invalid_anthropometrics()
        .add_bmi()
        .add_age_group()
    )

    # 2) Llama al método que vas a crear:
    # TODO: processor_mr1.assert_bmi_plausible(bmi_col="bmi", min_bmi=..., max_bmi=...)

    # 3) Deja un assert simple para verificar que tu método existe
    assert hasattr(processor_mr1, "assert_bmi_plausible"), (
        "Define assert_bmi_plausible() en la clase."
    )
    processor_mr1.df


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
---

## 4) Encapsulación y “contratos” (invariantes)

En análisis de salud pública, errores silenciosos son particularmente costosos:

- edades fuera de rango,
- sexo con categorías inconsistentes,
- medidas antropométricas imposibles,
- sesgos por filtrado accidental.

**Patrón recomendado:** usar métodos de validación como “contratos” del pipeline:
- `validate_schema()` asegura estructura mínima
- `coerce_types()` define interpretación numérica
- `assert_*()` garantiza invariantes clave (rangos plausibles, categorías esperadas)

Esto hace que el pipeline sea más **confiable** y fácil de depurar.
"""
    )


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
---

## Mini-reto 2 (guiado): estandarizar categorías de sexo

**Objetivo:** crear un método `standardize_sex()` que:

- convierta a minúsculas,
- reemplace valores comunes (por ejemplo "f", "female", "m", "male") a solo `"female"` / `"male"`,
- y luego valide que el conjunto final esté dentro de `{"female", "male"}`.

**Pista:** puedes usar `replace({...})` y luego un `assert` con `isin(...)`.

> Nota: el dataset actual ya viene limpio, pero el método debe quedar robusto para datos reales.
"""
    )


@app.cell(hide_code=True)
def _(mo):
    tip_content = mo.md(
        r"""
### Tip (sin dar la respuesta)

- Normaliza primero: `astype(str)`, `str.strip()`, `str.lower()`.
- `replace` acepta un diccionario de mapeo.
- La validación típica revisa: `df[col].isin(allowed).all()`.
"""
    )
    return tip_content


@app.cell
def _(CohortProcessor, df_raw):
    # === TU TURNO (EDITA ESTA CELDA) ===
    # Implementa standardize_sex() en la clase y úsalo aquí.

    processor_mr2 = (
        CohortProcessor(df_raw)
        .validate_schema()
        .coerce_types()
        # TODO: .standardize_sex(allowed={"female","male"})
        .drop_invalid_anthropometrics()
        .add_bmi()
        .add_age_group()
    )

    assert hasattr(processor_mr2, "standardize_sex"), (
        "Define standardize_sex() en la clase."
    )
    processor_mr2.df[[processor_mr2.patient_id_col, processor_mr2.sex_col]].head()


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
---

## 5) Salidas formales: “métricas” y tablas listas para reporte

Con `groupby + agg` obtuvimos un resumen *tidy* por sexo y grupo etario.
Con `pivot_table` generamos una tabla *wide* útil para reportes.

La encapsulación permite que:
- el DataFrame limpio sea un **producto intermedio** (`processor.df`)
- los outputs sean **productos finales** (métodos que retornan DataFrames)

Esto es clave para análisis reproducibles.
"""
    )


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
---

## Mini-reto 3 (final, guiado): crear un método `run_basic_report()`

**Objetivo:** dentro de la clase, implementar un método que:

1) ejecute el pipeline mínimo (validar → tipos → filtros → IMC → grupo etario),
2) retorne un **diccionario** con:
   - `"clean_df"`: DataFrame limpio
   - `"summary"`: resumen por sexo y grupo etario
   - `"prevalence_like"`: pivot por tipo de consulta

**Restricción:** no uses librerías nuevas; solo pandas/POO.

> Este mini-reto integra lo visto: encapsulación + salidas estructuradas usando dict.
"""
    )


@app.cell(hide_code=True)
def _(mo):
    tip_content = mo.md(
        r"""
### Tip (sin dar la respuesta)

- Un método puede “orquestar” otros métodos de la misma clase.
- Para no duplicar lógica, llama internamente:
  - `self.validate_schema()`, `self.coerce_types()`, etc.
- Construye el dict con claves fijas y valores que ya tienes disponibles:
  - `self.df` y outputs de tus métodos de resumen.
"""
    )
    return tip_content


@app.cell
def _(CohortProcessor, df_raw):
    # === TU TURNO (EDITA ESTA CELDA) ===
    # Implementa run_basic_report() en la clase y úsalo aquí.

    processor_mr3 = CohortProcessor(df_raw)

    # TODO: report = processor_mr3.run_basic_report()

    assert hasattr(processor_mr3, "run_basic_report"), (
        "Define run_basic_report() en la clase."
    )
    # Cuando lo implementes, deberías poder inspeccionar:
    # report["clean_df"], report["summary"], report["prevalence_like"]


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
## Cierre: qué debes poder explicar al final

- Por qué una clase es útil para encapsular un flujo de pandas (estado + métodos).
- Cómo se diseñan métodos con responsabilidades claras.
- Cómo `groupby/agg` y `pivot_table` se integran como “outputs formales”.
- Cómo las validaciones (`assert`) funcionan como contratos del pipeline.

[Diagrama conceptual: clase como “contenedor” del DataFrame + métodos (clean → features → summary)]
"""
    )


if __name__ == "__main__":
    app.run()
