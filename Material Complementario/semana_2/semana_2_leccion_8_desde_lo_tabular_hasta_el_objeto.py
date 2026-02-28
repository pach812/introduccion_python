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
# Semana 2 · Lección 8  
## Desde lo tabular hasta el objeto

**Idea central:** un *DataFrame* es una estructura tabular potente, pero a medida que el análisis crece,
necesitamos **encapsular** operaciones y reglas del dominio en **clases** para ganar:

- **Cohesión:** todo lo que “pertenece” al dataset vive en un lugar.
- **Reutilización:** métodos repetibles, sin copiar/pegar.
- **Control de calidad:** validaciones (assert) y contratos mínimos.

**Contexto de salud pública:** trabajaremos con una cohorte sintética de pacientes y consultas
(edad, sexo, peso, talla, presión arterial, HbA1c).
"""
    )
    return


@app.cell
def _():
    mo.md(
        r"""
## 1) Mentalidad tabular vs mentalidad orientada a objetos

### Mentalidad tabular (estilo hoja de cálculo)
- Pensamos en “columnas” y “filas”.
- Operaciones típicas: filtrar, seleccionar, agrupar, resumir.
- Ventaja: rapidez para exploración.

### Mentalidad orientada a objetos
- Pensamos en **entidades** y **responsabilidades**.
- Una clase agrupa:
  - datos (atributos)
  - operaciones (métodos)
  - reglas (validaciones)

**Traducción práctica:**
- DataFrame: *la tabla*  
- Clase: *la tabla + las reglas + los cálculos repetibles*  
"""
    )
    return


@app.cell
def _():
    import numpy as np
    import pandas as pd

    return np, pd


@app.cell
def _(np, pd):
    mo.md(
        r"""
## 2) Dataset sintético (cohorte)

Crearemos dos tablas:

1. `patients`: una fila por paciente.
2. `visits`: múltiples filas por paciente (consultas), con variables clínicas.

Esto simula un caso típico de EHR/registro clínico donde se hacen resúmenes por paciente
o por subgrupos.
"""
    )

    rng = np.random.default_rng(42)

    n_patients = 80
    patient_id = np.arange(1001, 1001 + n_patients)

    patients = pd.DataFrame(
        {
            "patient_id": patient_id,
            "sex": rng.choice(["female", "male"], size=n_patients, replace=True),
            "age": rng.integers(18, 90, size=n_patients),
        }
    )

    # 1–5 visitas por paciente
    visits_per_patient = rng.integers(1, 6, size=n_patients)
    visit_rows = []
    for pid, k in zip(patient_id, visits_per_patient):
        for j in range(k):
            weight_kg = rng.normal(74, 14)
            height_m = rng.normal(1.69, 0.09)
            sbp = rng.normal(124, 16)  # systolic BP
            hba1c = rng.normal(5.7, 0.6)  # %
            visit_rows.append(
                {
                    "patient_id": int(pid),
                    "visit_number": int(j + 1),
                    "weight_kg": float(max(35, weight_kg)),
                    "height_m": float(max(1.40, height_m)),
                    "sbp": float(max(80, sbp)),
                    "hba1c": float(max(4.2, hba1c)),
                }
            )

    visits = pd.DataFrame(visit_rows)

    mo.md(
        f"""
**Vista rápida:**  
- `patients`: {patients.shape[0]} filas × {patients.shape[1]} columnas  
- `visits`: {visits.shape[0]} filas × {visits.shape[1]} columnas
"""
    )

    return patients, visits


@app.cell
def _(patients, visits):
    mo.md(
        r"""
## 3) Operaciones tabulares típicas (pandas)

### Pregunta epidemiológica
> ¿Cuál es el IMC promedio por sexo y grupo etario, usando la **última visita** de cada paciente?

Pasos tabulares (sin clases):
1) Calcular IMC en `visits`  
2) Seleccionar la última visita de cada paciente  
3) Unir (`merge`) con `patients`  
4) Crear grupos etarios  
5) Resumir por `sex` y grupo etario
"""
    )
    return


@app.cell
def _(pd, patients, visits):
    # 1) IMC por visita
    visits_with_bmi = visits.copy()
    visits_with_bmi["bmi"] = visits_with_bmi["weight_kg"] / (
        visits_with_bmi["height_m"] ** 2
    )

    # 2) Última visita por paciente
    last_visit = (
        visits_with_bmi.sort_values(["patient_id", "visit_number"])
        .groupby("patient_id", as_index=False)
        .tail(1)
        .reset_index(drop=True)
    )

    # 3) Merge con tabla de pacientes
    cohort = patients.merge(last_visit, on="patient_id", how="inner")

    # 4) Grupos etarios (cortes simples)
    bins = [18, 40, 60, 90]
    labels = ["18-39", "40-59", "60-89"]
    cohort["age_group"] = pd.cut(cohort["age"], bins=bins, labels=labels, right=False)

    # 5) Resumen
    summary_tabular = (
        cohort.groupby(["sex", "age_group"], dropna=False)
        .agg(
            n_patients=("patient_id", "nunique"),
            bmi_mean=("bmi", "mean"),
            sbp_mean=("sbp", "mean"),
            hba1c_mean=("hba1c", "mean"),
        )
        .reset_index()
        .sort_values(["sex", "age_group"])
    )

    summary_tabular
    return bins, cohort, labels, last_visit, summary_tabular, visits_with_bmi


@app.cell
def _():
    mo.md(
        r"""
## 4) ¿Qué problema aparece cuando esto crece?

El enfoque tabular es excelente, pero en un proyecto real aparecen fricciones:

- Se repite el mismo bloque de *merge + filtros + groupby* en muchos scripts.
- Reglas del dominio quedan dispersas:
  - rangos válidos
  - columnas obligatorias
  - convenciones de nombres
- “Pequeños cambios” rompen todo:
  - cambia un nombre de columna
  - cambian cortes etarios
  - se agrega una nueva métrica

**Solución del curso (hasta ahora):** encapsular en clases y diseñar un procesador mínimo tipo
`DatasetProcessor` (lo visto en lecciones 6 y 7).
"""
    )
    return


@app.cell
def _():
    mo.md(
        r"""
## 5) Primer paso: un contrato mínimo para una tabla clínica

Vamos a crear una clase que represente *una tabla con reglas*.

### Principios (prácticos)
- La clase recibe un `DataFrame` y valida lo mínimo.
- Los métodos:
  - **no** dependen de variables externas “mágicas”.
  - retornan objetos explícitos (DataFrame o diccionario).
- Las decisiones del dominio (p. ej. cortes etarios) quedan en un lugar controlado.
"""
    )
    return


@app.cell
def _(pd):
    from dataclasses import dataclass
    from typing import Dict, List, Optional

    return Dict, List, Optional, dataclass


@app.cell
def _(Dict, List, Optional, dataclass, pd):
    @dataclass
    class ClinicalCohort:
        """
        Minimal object wrapper around patient + visit tables.

        Attributes
        ----------
        patients:
            One row per patient.
        visits:
            One row per visit. Multiple visits per patient.
        """

        patients: pd.DataFrame
        visits: pd.DataFrame

        def validate(self) -> None:
            """Validate minimal schema and basic value constraints."""
            required_patients = {"patient_id", "sex", "age"}
            required_visits = {
                "patient_id",
                "visit_number",
                "weight_kg",
                "height_m",
                "sbp",
                "hba1c",
            }

            missing_pat = required_patients - set(self.patients.columns)
            missing_vis = required_visits - set(self.visits.columns)

            assert len(missing_pat) == 0, (
                f"patients missing columns: {sorted(missing_pat)}"
            )
            assert len(missing_vis) == 0, (
                f"visits missing columns: {sorted(missing_vis)}"
            )

            # Basic constraints (domain-agnostic, but clinically sensible)
            assert (self.patients["age"] >= 0).all(), "age must be non-negative"
            assert (self.visits["height_m"] > 0).all(), "height_m must be > 0"
            assert (self.visits["weight_kg"] > 0).all(), "weight_kg must be > 0"

        def with_bmi(self) -> pd.DataFrame:
            """Return visits with an additional bmi column."""
            df = self.visits.copy()
            df["bmi"] = df["weight_kg"] / (df["height_m"] ** 2)
            return df

        def last_visit(self) -> pd.DataFrame:
            """Return the last visit record for each patient."""
            df = self.with_bmi()
            out = (
                df.sort_values(["patient_id", "visit_number"])
                .groupby("patient_id", as_index=False)
                .tail(1)
                .reset_index(drop=True)
            )
            return out

        def build_cohort(self) -> pd.DataFrame:
            """Merge patients with last visit to create a one-row-per-patient cohort table."""
            return self.patients.merge(self.last_visit(), on="patient_id", how="inner")

        def add_age_group(
            self, df: pd.DataFrame, bins: List[int], labels: List[str]
        ) -> pd.DataFrame:
            """Return a copy with age_group derived from age using pd.cut."""
            out = df.copy()
            out["age_group"] = pd.cut(out["age"], bins=bins, labels=labels, right=False)
            return out

        def summarize(self, bins: List[int], labels: List[str]) -> pd.DataFrame:
            """Compute cohort summary by sex and age_group."""
            cohort = self.build_cohort()
            cohort = self.add_age_group(cohort, bins=bins, labels=labels)

            out = (
                cohort.groupby(["sex", "age_group"], dropna=False)
                .agg(
                    n_patients=("patient_id", "nunique"),
                    bmi_mean=("bmi", "mean"),
                    sbp_mean=("sbp", "mean"),
                    hba1c_mean=("hba1c", "mean"),
                )
                .reset_index()
                .sort_values(["sex", "age_group"])
            )
            return out

    return ClinicalCohort


@app.cell
def _(ClinicalCohort, bins, labels, patients, visits):
    mo.md(
        r"""
### Probemos la clase

La diferencia clave es que ahora el “flujo” está empaquetado en métodos que:

- se pueden reutilizar,
- tienen un contrato mínimo (`validate`),
- y producen outputs explícitos.
"""
    )

    cohort_obj = ClinicalCohort(patients=patients, visits=visits)
    cohort_obj.validate()

    summary_object = cohort_obj.summarize(bins=bins, labels=labels)
    summary_object
    return cohort_obj, summary_object


@app.cell
def _(summary_object, summary_tabular):
    mo.md(
        r"""
### Consistencia: tabular vs objeto

La salida debe ser equivalente (mismas columnas y número de filas).
"""
    )

    assert set(summary_object.columns) == set(summary_tabular.columns)
    assert summary_object.shape[0] == summary_tabular.shape[0]
    return


# -----------------------------------------------------------------------------
# Mini-reto 1
# -----------------------------------------------------------------------------


@app.cell
def _():
    mo.md(
        r"""
## Mini-reto 1 (guiado): normalizar nombres de columnas en una tabla clínica

En proyectos reales, los datasets llegan con columnas tipo:

- `"Patient ID"`, `"Age (years)"`, `"HbA1c%"`, `"Systolic BP"`

Tu tarea es completar una función que convierta nombres a un formato estándar:

- minúsculas
- espacios → `_`
- eliminar paréntesis y `%`
- eliminar dobles `_`

**Objetivo:** que la misma clase pueda reutilizarse con datasets “desordenados”.

"""
    )
    return


@app.cell
def _(pd):
    # === TU TURNO (EDITA ESTA CELDA) ===
    def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
        """
        Return a copy of df with standardized column names.

        Rules (apply in order):
        1) Lowercase
        2) Replace spaces with underscores
        3) Remove characters: '(', ')', '%'
        4) Replace repeated underscores with a single underscore
        5) Strip leading/trailing underscores
        """
        out = df.copy()

        # TODO: implement the rules above using out.columns
        # Hint: work with a list of strings and then assign back.
        return out

    return normalize_columns


@app.cell(hide_code=True)
def _(normalize_columns, pd):
    # Hidden checks (do not modify)
    toy = pd.DataFrame(
        {"Patient ID": [1], "Age (years)": [35], "HbA1c%": [5.8], "Systolic  BP": [120]}
    )
    norm = normalize_columns(toy)
    assert "patient_id" in norm.columns
    assert "age_years" in norm.columns
    assert "hba1c" in norm.columns
    assert "systolic_bp" in norm.columns
    return


@app.cell
def _():
    mo.md(
        r"""
### Tip (Mini-reto 1)

- Convierte `df.columns` a una lista de strings.
- Aplica transformaciones con operaciones de string.
- Para “dobles guiones bajos”, una estrategia es reemplazar `__` repetidamente.
- Al final, reasigna `out.columns = new_cols`.

*(No intentes resolver todo en una sola línea: primero corre una transformación, imprime el resultado,
y luego añade la siguiente.)*
"""
    )
    return


# -----------------------------------------------------------------------------
# Mini-reto 2
# -----------------------------------------------------------------------------


@app.cell
def _():
    mo.md(
        r"""
## 6) Del DataFrame al método: reglas clínicas como código

Ahora agregaremos una **regla de clasificación**.

### Caso de salud pública
Clasificar IMC en categorías (OMS simplificada):
- `< 18.5` bajo peso
- `18.5–24.9` normal
- `25.0–29.9` sobrepeso
- `>= 30.0` obesidad

Vamos a añadir un método que, dado un DataFrame con `bmi`, retorne una nueva columna
`bmi_class`.
"""
    )
    return


@app.cell
def _(ClinicalCohort, pd):
    # === TU TURNO (EDITA ESTA CELDA) ===
    def add_bmi_class(df: pd.DataFrame) -> pd.DataFrame:
        """
        Return a copy of df with a bmi_class column based on bmi.
        """
        out = df.copy()

        # TODO: implement categorical classification using if/elif/else inside a helper,
        # or use pandas operations that you already know.
        # Constraint: assume bmi exists and is numeric.
        return out

    # Attach as a method-like helper for the lesson (keeps class unchanged)
    ClinicalCohort.add_bmi_class = staticmethod(add_bmi_class)
    return add_bmi_class


@app.cell(hide_code=True)
def _(ClinicalCohort, cohort_obj, pd):
    # Hidden checks (do not modify)
    df = cohort_obj.last_visit()
    df2 = ClinicalCohort.add_bmi_class(df)
    assert "bmi_class" in df2.columns
    # Must not introduce missing values if bmi is present
    assert df2["bmi_class"].isna().sum() == 0
    return


@app.cell
def _():
    mo.md(
        r"""
### Tip (Mini-reto 2)

- Primero define claramente los cortes del IMC.
- Evita comparar strings con números: asegúrate de usar `bmi` como numérico.
- Si usas una función auxiliar, recuerda que ya conoces `if/elif/else` y funciones (Semana 1).
- Si usas pandas, piensa en “máscaras booleanas” por rangos.
"""
    )
    return


# -----------------------------------------------------------------------------
# Construcción tipo DatasetProcessor (lo visto en lección 7)
# -----------------------------------------------------------------------------


@app.cell
def _():
    mo.md(
        r"""
## 7) Del objeto a un procesador mínimo (DatasetProcessor)

Un patrón útil (ya visto) es separar el flujo en pasos:

- `clean()`  → normaliza/valida (esquema, nombres, rangos)
- `compute()` → crea variables derivadas (IMC, categorías, etc.)
- `summarize()` → métricas agregadas
- `run()` → orquesta lo anterior y devuelve un output estructurado

Esto transforma un notebook “lineal” en un componente reutilizable.
"""
    )
    return


@app.cell
def _(Dict, List, Optional, dataclass, pd):
    @dataclass
    class CohortProcessor:
        """
        Minimal dataset processor.

        Notes
        -----
        This class is intentionally small and explicit:
        - Uses only pandas/numpy + Python fundamentals already covered.
        - Returns a structured dictionary output.
        """

        patients: pd.DataFrame
        visits: pd.DataFrame
        bins: List[int]
        labels: List[str]

        cohort_: Optional[pd.DataFrame] = None
        summary_: Optional[pd.DataFrame] = None

        def clean(self) -> None:
            """Validate and build the one-row-per-patient cohort table."""
            cohort = ClinicalCohort(self.patients, self.visits)
            cohort.validate()
            self.cohort_ = cohort.build_cohort()

            assert self.cohort_ is not None and self.cohort_.shape[0] > 0

        def compute(self) -> None:
            """Add derived variables needed for analysis."""
            assert self.cohort_ is not None, "Run clean() first."

            df = self.cohort_.copy()

            df["age_group"] = pd.cut(
                df["age"], bins=self.bins, labels=self.labels, right=False
            )

            # BMI class via helper from mini-reto 2
            df = ClinicalCohort.add_bmi_class(df)

            self.cohort_ = df

        def summarize(self) -> None:
            """Create a group summary table."""
            assert self.cohort_ is not None, "Run compute() first."

            df = self.cohort_
            self.summary_ = (
                df.groupby(["sex", "age_group", "bmi_class"], dropna=False)
                .agg(
                    n_patients=("patient_id", "nunique"),
                    bmi_mean=("bmi", "mean"),
                    sbp_mean=("sbp", "mean"),
                    hba1c_mean=("hba1c", "mean"),
                )
                .reset_index()
                .sort_values(["sex", "age_group", "bmi_class"])
            )

        def run(self) -> Dict[str, object]:
            """Run the full processing pipeline and return structured outputs."""
            self.clean()
            self.compute()
            self.summarize()

            assert self.cohort_ is not None
            assert self.summary_ is not None

            return {
                "cohort": self.cohort_,
                "summary": self.summary_,
                "n_patients": int(self.cohort_["patient_id"].nunique()),
                "n_visits": int(self.visits.shape[0]),
            }

    return CohortProcessor


@app.cell
def _(CohortProcessor, bins, labels, patients, visits):
    processor = CohortProcessor(
        patients=patients, visits=visits, bins=bins, labels=labels
    )
    output = processor.run()
    output["summary"].head(10)
    return output, processor


# -----------------------------------------------------------------------------
# Mini-reto 3 (final)
# -----------------------------------------------------------------------------


@app.cell
def _():
    mo.md(
        r"""
## Mini-reto 3 (final, guiado): output estructurado para auditoría mínima

En salud pública, no basta con un DataFrame final: necesitamos trazabilidad.

Tu tarea es completar una función que, a partir de `output` (diccionario del procesador),
construya un **resumen estructurado** con:

- `n_patients`
- `n_visits`
- `columns_cohort` (lista de columnas del cohort final)
- `groups_in_summary` (lista de tuplas únicas de `sex` y `age_group` presentes en el summary)

**Restricción:** usa únicamente conceptos ya vistos (diccionarios, listas, tuplas, pandas básico).
"""
    )
    return


@app.cell
def _(pd):
    # === TU TURNO (EDITA ESTA CELDA) ===
    def build_audit_report(output: dict) -> dict:
        """
        Build a lightweight audit report from a processor output.

        Parameters
        ----------
        output:
            Dictionary with keys: cohort, summary, n_patients, n_visits.

        Returns
        -------
        dict
            A dictionary with audit-friendly fields.
        """
        # TODO: implement the report
        report = {}
        return report

    return build_audit_report


@app.cell(hide_code=True)
def _(build_audit_report, output):
    # Hidden checks (do not modify)
    rep = build_audit_report(output)
    assert set(
        ["n_patients", "n_visits", "columns_cohort", "groups_in_summary"]
    ).issubset(rep.keys())
    assert isinstance(rep["columns_cohort"], list)
    assert isinstance(rep["groups_in_summary"], list)
    return


@app.cell
def _():
    mo.md(
        r"""
### Tip (Mini-reto 3)

- `output["cohort"]` y `output["summary"]` son DataFrames.
- Para columnas: `list(df.columns)`.
- Para tuplas únicas: selecciona las columnas, elimina duplicados y convierte a una lista de tuplas.
  *(Pista: `itertuples(index=False, name=None)` produce tuplas fila por fila.)*
"""
    )
    return


@app.cell
def _():
    mo.md(
        r"""
## Cierre: ¿qué cambió en tu forma de pensar?

- Antes: “tengo una tabla y hago operaciones”.
- Ahora: “tengo una **entidad** (cohorte) y un **procesador** (pipeline) con contratos”.

Esto prepara el terreno para construir sistemas analíticos que:
- sean reutilizables,
- auditablemente consistentes,
- y menos frágiles que un único notebook lineal.
"""
    )
    return


if __name__ == "__main__":
    app.run()
