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
# Semana 2 · Lección 7  
## Diseño de un procesador de dataset (DatasetProcessor)

**Idea central:** pasar de “hacer pasos sueltos en celdas” a **un objeto** que encapsula un flujo mínimo de procesamiento y produce **outputs estructurados**.

En esta sesión construiremos una clase `DatasetProcessor` que:
1. **recibe** un `DataFrame` (tabular),
2. ejecuta **validaciones** mínimas,
3. aplica **limpieza** reproducible,
4. calcula **métricas** con `groupby/agg`,
5. retorna resultados como **diccionarios** + `DataFrame` resumen.

**Contexto aplicado:** datos sintéticos de salud pública (tamizaje cardiometabólico en atención primaria).
"""
    )
    return


@app.cell
def _():
    import numpy as np
    import pandas as pd

    return np, pd


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
## 1) Dataset sintético: tamizaje cardiometabólico

Vamos a simular un dataset con variables típicas:
- `patient_id`: identificador
- `age`: edad (años)
- `sex`: sexo biológico (female/male)
- `bmi`: índice de masa corporal
- `sbp`: presión sistólica (mmHg)
- `smoker`: fumador actual (0/1)
- `hba1c`: hemoglobina glicosilada (%)

Este dataset NO representa pacientes reales. Su objetivo es didáctico.
"""
    )
    return


@app.cell
def _(np, pd):
    rng = np.random.default_rng(20260228)

    n = 600
    df_raw = pd.DataFrame(
        {
            "patient_id": np.arange(1, n + 1),
            "age": rng.integers(18, 90, size=n),
            "sex": rng.choice(["female", "male"], size=n, p=[0.55, 0.45]),
            "bmi": np.round(rng.normal(loc=27.5, scale=5.2, size=n), 1),
            "sbp": np.round(rng.normal(loc=128, scale=18, size=n), 0),
            "smoker": rng.choice([0, 1], size=n, p=[0.78, 0.22]),
            "hba1c": np.round(rng.normal(loc=5.6, scale=0.7, size=n), 1),
        }
    )

    # Introducimos algunos problemas comunes de calidad (missing y outliers)
    df_raw.loc[rng.choice(n, size=18, replace=False), "bmi"] = np.nan
    df_raw.loc[rng.choice(n, size=10, replace=False), "sbp"] = np.nan
    df_raw.loc[rng.choice(n, size=6, replace=False), "hba1c"] = np.nan

    # Outliers intencionales
    df_raw.loc[rng.choice(n, size=3, replace=False), "bmi"] = [6.0, 65.0, 80.0]
    df_raw.loc[rng.choice(n, size=3, replace=False), "sbp"] = [60.0, 240.0, 260.0]
    df_raw.loc[rng.choice(n, size=3, replace=False), "hba1c"] = [3.2, 14.5, 18.0]

    df_raw.head()
    return df_raw, n, rng


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
## 2) ¿Qué significa “procesar un dataset” en términos formales?

En análisis de datos, **procesar** significa aplicar una secuencia ordenada de transformaciones
y verificaciones para obtener una tabla más:
- **coherente** (tipos, rangos, categorías),
- **robusta** (manejo mínimo de valores faltantes),
- **reutilizable** (mismas reglas, mismos resultados),
- **auditable** (reglas explícitas).

En vez de ejecutar 12 pasos manuales en un notebook, los encapsulamos como **métodos**
dentro de un objeto. Esto reduce:
- duplicación,
- errores por “cambiar una celda y olvidar otra”,
- resultados difíciles de reproducir.
"""
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
## 3) Contrato mínimo de un `DatasetProcessor`

Un procesador bien diseñado define un **contrato** (qué entra y qué sale).

### Inputs (entrada)
- Un `pd.DataFrame` (tabular)
- Reglas de validación (columnas requeridas, rangos)
- Parámetros de limpieza (winsorización, filtros, imputación simple)

### Outputs (salida)
- `data_clean`: `DataFrame` limpio (mismo “granulado” del original)
- `metrics`: `dict` con métricas (p. ej. prevalencias por grupos)
- `summary_table`: `DataFrame` pequeño con agregados

En esta lección evitamos visualización o pipelines complejos; nos quedamos con:
**validar → limpiar → resumir**.
"""
    )
    return


# -----------------------------------------------------------------------------
# Mini-reto 1
# -----------------------------------------------------------------------------


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
## Mini-reto 1 (guiado): reglas de validación

Implementa una función `validate_schema(df)` que:
1. verifique que existan las columnas requeridas,
2. verifique que `age` sea numérica y esté en [0, 120],
3. verifique que `sex` solo contenga {"female", "male"} (ignorando NA).

Debe retornar `None` si todo está bien y lanzar `AssertionError` si algo falla.

**Pista:** usa `set(required).issubset(df.columns)` y `df["col"].dropna().isin(...).all()`.
"""
    )
    return


@app.cell
def _(pd):
    def validate_schema(df: pd.DataFrame) -> None:
        """
        Validate minimal schema constraints for a health screening dataset.

        Parameters
        ----------
        df:
            Input dataframe.

        Returns
        -------
        None

        Raises
        ------
        AssertionError
            If any schema constraint fails.
        """
        required_cols = {"patient_id", "age", "sex", "bmi", "sbp", "smoker", "hba1c"}
        assert required_cols.issubset(set(df.columns)), (
            f"Missing required columns: {sorted(required_cols - set(df.columns))}"
        )

        # Age constraints
        assert pd.api.types.is_numeric_dtype(df["age"]), "Column 'age' must be numeric."
        age_ok = df["age"].dropna().between(0, 120).all()
        assert age_ok, "Column 'age' must be within [0, 120]."

        # Sex constraints
        sex_ok = df["sex"].dropna().isin({"female", "male"}).all()
        assert sex_ok, "Column 'sex' must be 'female' or 'male'."

        return None

    # Smoke-test: should pass for our synthetic data
    validate_schema(df_raw)
    return validate_schema


@app.cell(hide_code=True)
def _():
    tip = mo.md(
        r"""
### Tip (Mini-reto 1)

Si una condición depende de NA, **elimínalos primero** con `.dropna()` para que la validación
evalúe únicamente valores observados.

Para validar rangos numéricos:
- `.between(min, max)` produce un vector booleano.
- Luego usa `.all()` para exigir que todos cumplan.

Evita “arreglar” datos dentro de la validación: **valida primero, transforma después**.
"""
    )
    return tip


# -----------------------------------------------------------------------------
# 4) Diseño de limpieza: decisiones explícitas
# -----------------------------------------------------------------------------


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
## 4) Limpieza mínima (sin anticipar temas futuros)

En datos de salud, un patrón realista es:
- **outliers**: valores fuera de plausibilidad clínica (p. ej. BMI=80)
- **missingness**: mediciones ausentes
- **tipos**: enteros vs floats

Definimos reglas explícitas:

### Reglas de plausibilidad (simplificadas)
- BMI plausible: [12, 60]
- SBP plausible: [70, 220]
- HbA1c plausible: [3.5, 15]

### Manejo de outliers
- Convertir valores fuera de rango a `NaN` (y tratarlos como faltantes)

### Manejo de faltantes (simple, y suficiente para la lección)
- Imputación por mediana para variables numéricas: BMI, SBP, HbA1c
"""
    )
    return


@app.cell
def _(pd):
    def clean_screening_data(df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean a cardiometabolic screening dataset using simple plausibility rules.

        Steps
        -----
        1) Copy dataframe.
        2) Coerce numeric columns.
        3) Replace implausible values with NaN.
        4) Impute numeric missing values with the median.

        Returns
        -------
        pd.DataFrame
            Cleaned dataset.
        """
        df_clean = df.copy()

        # Coerce numeric columns (robust against accidental strings)
        numeric_cols = ["age", "bmi", "sbp", "smoker", "hba1c"]
        for col in numeric_cols:
            df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")

        # Plausibility masks -> set to NaN
        df_clean.loc[~df_clean["bmi"].between(12, 60), "bmi"] = pd.NA
        df_clean.loc[~df_clean["sbp"].between(70, 220), "sbp"] = pd.NA
        df_clean.loc[~df_clean["hba1c"].between(3.5, 15), "hba1c"] = pd.NA

        # Simple imputation: median
        for col in ["bmi", "sbp", "hba1c"]:
            med = df_clean[col].median(skipna=True)
            df_clean[col] = df_clean[col].fillna(med)

        # Post-conditions (asserts as "internal contract")
        assert df_clean[["bmi", "sbp", "hba1c"]].isna().sum().sum() == 0
        assert df_clean["bmi"].between(12, 60).all()
        assert df_clean["sbp"].between(70, 220).all()
        assert df_clean["hba1c"].between(3.5, 15).all()

        return df_clean

    df_clean = clean_screening_data(df_raw)
    df_clean.head()
    return clean_screening_data, df_clean


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
## 5) Métricas estructuradas: de tabla → diccionario

Cuando construimos procesadores, conviene que las métricas tengan **forma estable**.

Ejemplos útiles para salud pública:
- prevalencia de **hipertensión probable** por sexo
- prevalencia de **alto riesgo cardiometabólico** por grupo etario

Definimos umbrales (simplificados):
- Hipertensión probable: SBP ≥ 140
- Alto riesgo: (BMI ≥ 30) o (HbA1c ≥ 6.5) o (SBP ≥ 140)

**Nota:** Estos umbrales son didácticos, no guías clínicas completas.
"""
    )
    return


@app.cell
def _(pd):
    def compute_metrics(df: pd.DataFrame) -> dict:
        """
        Compute basic group metrics for a screening dataset.

        Returns
        -------
        dict
            A dictionary with:
            - "n_rows"
            - "hypertension_prev_by_sex" (dict)
            - "high_risk_prev_by_age_group" (dict)
        """
        out = {}
        out["n_rows"] = int(df.shape[0])

        ht = (df["sbp"] >= 140).astype(int)
        ht_by_sex = (
            df.assign(ht=ht)
            .groupby("sex", dropna=False)["ht"]
            .mean()
            .sort_index()
            .to_dict()
        )
        out["hypertension_prev_by_sex"] = {k: float(v) for k, v in ht_by_sex.items()}

        # Age group: 18–39, 40–59, 60+
        age_group = pd.cut(
            df["age"],
            bins=[17, 39, 59, 120],
            labels=["18-39", "40-59", "60+"],
            include_lowest=True,
        )
        high_risk = (
            (df["bmi"] >= 30) | (df["hba1c"] >= 6.5) | (df["sbp"] >= 140)
        ).astype(int)

        risk_by_age = (
            df.assign(age_group=age_group, high_risk=high_risk)
            .groupby("age_group", dropna=False)["high_risk"]
            .mean()
            .to_dict()
        )
        out["high_risk_prev_by_age_group"] = {
            k: float(v) for k, v in risk_by_age.items()
        }

        return out

    metrics = compute_metrics(df_clean)
    metrics
    return compute_metrics, metrics


# -----------------------------------------------------------------------------
# Mini-reto 2
# -----------------------------------------------------------------------------


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
## Mini-reto 2 (guiado): tabla resumen con `groupby` + `agg`

Implementa `build_summary_table(df)` para producir un `DataFrame` con:
- índice: `sex`
- columnas: `n` (conteo), `mean_bmi`, `mean_sbp`, `mean_hba1c`, `smoker_prev`

Detalles:
- `smoker_prev` debe ser el promedio de `smoker` (0/1).
- Nombres de columnas exactamente como arriba.

**Pista:** usa `.agg()` con un diccionario de agregaciones.
"""
    )
    return


@app.cell
def _(pd):
    def build_summary_table(df: pd.DataFrame) -> pd.DataFrame:
        """
        Build a compact summary table by sex.

        Returns
        -------
        pd.DataFrame
            Columns: n, mean_bmi, mean_sbp, mean_hba1c, smoker_prev
        """
        summary = (
            df.groupby("sex", dropna=False)
            .agg(
                n=("patient_id", "count"),
                mean_bmi=("bmi", "mean"),
                mean_sbp=("sbp", "mean"),
                mean_hba1c=("hba1c", "mean"),
                smoker_prev=("smoker", "mean"),
            )
            .reset_index()
        )

        # Ensure contract: required columns exist
        expected = {"sex", "n", "mean_bmi", "mean_sbp", "mean_hba1c", "smoker_prev"}
        assert expected.issubset(set(summary.columns))
        return summary

    summary_table = build_summary_table(df_clean)
    summary_table
    return build_summary_table, summary_table


@app.cell(hide_code=True)
def _():
    tip = mo.md(
        r"""
### Tip (Mini-reto 2)

Cuando uses `.agg()` con nombres amigables:
- la forma recomendada es `nuevo_nombre=("columna", "funcion")`.
- esto te evita renombrar después.

Para prevalencias binarias:
- si `smoker` está codificada como 0/1, el **promedio** ya es la proporción.
"""
    )
    return tip


# -----------------------------------------------------------------------------
# 6) La clase DatasetProcessor: encapsulación mínima
# -----------------------------------------------------------------------------


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
## 6) Implementación de `DatasetProcessor`

Ahora convertimos el flujo (validar → limpiar → métricas → resumen) en un objeto.

Regla de diseño: cada método hace **una sola cosa**:
- `validate()`: contrato de entrada
- `clean()`: reglas de limpieza
- `compute_metrics()`: diccionario estable
- `summary()`: tabla agregada
- `run()`: orquestación (ejecuta en orden y guarda resultados)

Esto sigue la idea de “secuencialidad con control” que ya hemos usado en scripts,
pero ahora empaquetada para reutilizarla en nuevos datasets.
"""
    )
    return


@app.cell
def _(pd, validate_schema, clean_screening_data, compute_metrics, build_summary_table):
    class DatasetProcessor:
        """
        Minimal dataset processor for a health screening dataset.

        The processor implements a simple pipeline:
        validate -> clean -> compute metrics -> build summary table.

        Attributes
        ----------
        data_raw:
            Original dataframe (as provided).
        data_clean:
            Cleaned dataframe (after `clean` or `run`).
        metrics:
            Dictionary of computed metrics (after `compute` or `run`).
        summary_table:
            Summary table (after `summary` or `run`).
        """

        def __init__(self, data_raw: pd.DataFrame):
            self.data_raw = data_raw.copy()
            self.data_clean: pd.DataFrame | None = None
            self.metrics: dict | None = None
            self.summary_table: pd.DataFrame | None = None

        def validate(self) -> None:
            validate_schema(self.data_raw)

        def clean(self) -> pd.DataFrame:
            self.data_clean = clean_screening_data(self.data_raw)
            return self.data_clean

        def compute(self) -> dict:
            assert self.data_clean is not None, "Run clean() before compute()."
            self.metrics = compute_metrics(self.data_clean)
            return self.metrics

        def summary(self) -> pd.DataFrame:
            assert self.data_clean is not None, "Run clean() before summary()."
            self.summary_table = build_summary_table(self.data_clean)
            return self.summary_table

        def run(self) -> dict:
            """
            Execute the full pipeline and return a structured output.
            """
            self.validate()
            self.clean()
            self.compute()
            self.summary()

            return {
                "data_clean": self.data_clean,
                "metrics": self.metrics,
                "summary_table": self.summary_table,
            }

    processor = DatasetProcessor(df_raw)
    outputs = processor.run()
    outputs["metrics"]
    return DatasetProcessor, outputs, processor


# -----------------------------------------------------------------------------
# Mini-reto 3 (final)
# -----------------------------------------------------------------------------


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
## Mini-reto 3 (final): extender el procesador sin romper el contrato

Agrega al `DatasetProcessor` un método `filter_adults(min_age=18)` que:
1. filtre `data_raw` dejando `age >= min_age`,
2. retorne el `DataFrame` filtrado,
3. NO ejecute limpieza ni métricas automáticamente.

Luego:
- crea un procesador,
- llama `filter_adults(min_age=40)`,
- ejecuta `run()` y verifica con `assert` que todas las edades sean >= 40.

**Pista:** recuerda que `run()` usa `self.data_raw` como entrada; por tanto,
si quieres que el filtro afecte el pipeline, debes actualizar `self.data_raw`.
"""
    )
    return


@app.cell
def _(DatasetProcessor, df_raw):
    class DatasetProcessorV2(DatasetProcessor):
        def filter_adults(self, min_age: int = 18):
            """
            Filter raw data by a minimum age threshold.

            Parameters
            ----------
            min_age:
                Minimum age to keep.

            Returns
            -------
            pd.DataFrame
                Filtered dataframe.
            """
            df_filt = self.data_raw[self.data_raw["age"] >= min_age].copy()
            self.data_raw = df_filt
            return df_filt

    proc2 = DatasetProcessorV2(df_raw)
    _df40 = proc2.filter_adults(min_age=40)
    out2 = proc2.run()

    assert out2["data_clean"]["age"].min() >= 40
    out2["summary_table"]
    return DatasetProcessorV2, out2, proc2


@app.cell(hide_code=True)
def _():
    tip = mo.md(
        r"""
### Tip (Mini-reto 3)

Piensa en “estado interno” del objeto:
- `self.data_raw` es la fuente del pipeline.
- si filtras pero NO reasignas `self.data_raw`, el pipeline seguirá usando la tabla original.

Diseño intencional: `filter_adults()` **no** ejecuta `run()` por sí misma,
porque eso mezcla responsabilidades (filtrar vs orquestar todo).
"""
    )
    return tip


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
## Cierre: checklist conceptual

Al final, una clase como `DatasetProcessor` sirve para:

- **Definir contrato** de entrada/salida
- **Reducir errores** por pasos manuales dispersos
- **Estandarizar métricas** para comparar cohortes o cortes poblacionales
- **Facilitar reuse** (misma lógica en múltiples datasets)

En la siguiente sesión (sin anticiparla aquí), esta estructura será la base
para diseños más robustos, pero lo esencial ya está: un procesador **coherente**.
"""
    )
    return


if __name__ == "__main__":
    app.run()
