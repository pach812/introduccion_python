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
# Semana 2 · Lección 5  
## Métodos avanzados de agrupación y resumen en pandas

**Propósito de la sesión.** Aprender a construir resúmenes descriptivos reproducibles a partir de datos clínicos tabulares usando:  
- `groupby` (segmentación)  
- `agg` (múltiples métricas)  
- `merge` (enriquecer tablas con metadatos)  
- `pivot_table` (tablas de contingencia / resúmenes tipo “excel”)

**Regla de oro.** Primero definimos:  
1) *unidad de análisis* (paciente, visita, laboratorio)  
2) *variables de estratificación* (sexo, hospital, diagnóstico)  
3) *métrica* (promedio, mediana, conteo, proporción)

[Esquema conceptual: “Datos → Agrupar → Resumir → Interpretar”]
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
## 1) Dataset de ejemplo (salud pública / clínica)

Usaremos un dataset sintético de **visitas ambulatorias**. Cada fila representa una visita de un paciente:

- `patient_id`: identificador del paciente  
- `visit_id`: identificador de la visita  
- `hospital`: institución  
- `sex`: sexo biológico reportado (categoría)  
- `age`: edad en años (numérica)  
- `condition`: condición principal de la visita (categoría)  
- `sbp`: presión arterial sistólica (mmHg)  
- `ldl`: LDL colesterol (mg/dL)  
- `days_to_next`: días hasta la próxima visita (proxy simple de seguimiento)

**Objetivo analítico.** Construir resúmenes por hospital/sexo/condición para describir carga y severidad.
"""
    )
    return


@app.cell
def _(np, pd):
    rng = np.random.default_rng(20260228)

    n_patients = 180
    visits_per_patient = rng.integers(1, 6, size=n_patients)
    patient_ids = np.arange(1, n_patients + 1)

    hospitals = np.array(["HOSP_A", "HOSP_B", "HOSP_C"])
    conditions = np.array(["HTA", "T2D", "EPOC", "ASMA"])
    sexes = np.array(["female", "male"])

    rows = []
    visit_counter = 1

    for pid, k in zip(patient_ids, visits_per_patient):
        sex = rng.choice(sexes, p=[0.55, 0.45])
        age = int(rng.normal(loc=52, scale=16))
        age = int(np.clip(age, 18, 90))
        hospital = rng.choice(hospitals, p=[0.4, 0.35, 0.25])

        for _i in range(int(k)):
            condition = rng.choice(conditions, p=[0.35, 0.30, 0.20, 0.15])

            # Simplificación: "severidad" se refleja en distribución de SBP/LDL por condición
            base_sbp = {"HTA": 145, "T2D": 135, "EPOC": 128, "ASMA": 124}[condition]
            sbp = float(rng.normal(loc=base_sbp, scale=12))

            base_ldl = {"HTA": 125, "T2D": 135, "EPOC": 120, "ASMA": 118}[condition]
            ldl = float(rng.normal(loc=base_ldl, scale=22))

            # Seguimiento (días a próxima visita) con dispersión amplia
            days_to_next = int(np.clip(rng.gamma(shape=2.2, scale=18), 1, 180))

            rows.append(
                {
                    "patient_id": int(pid),
                    "visit_id": int(visit_counter),
                    "hospital": hospital,
                    "sex": sex,
                    "age": age,
                    "condition": condition,
                    "sbp": round(sbp, 1),
                    "ldl": round(ldl, 1),
                    "days_to_next": int(days_to_next),
                }
            )
            visit_counter += 1

    visits = pd.DataFrame(rows)

    # Validaciones mínimas del dataset
    assert visits["patient_id"].nunique() == n_patients
    assert visits["visit_id"].is_unique
    assert set(visits["sex"].unique()).issubset({"female", "male"})
    assert visits["age"].between(18, 90).all()

    visits.head(10)
    return (
        hospitals,
        patient_ids,
        rows,
        sexes,
        visits,
        visit_counter,
        visits_per_patient,
        rng,
        conditions,
    )


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
## 2) `groupby`: segmentación y métricas simples

`groupby` se interpreta como:  
> “particionar el DataFrame por una o más columnas, y luego aplicar una función resumen por grupo”.

Ejemplos típicos en salud:
- Promedio de PAS (SBP) por sexo.
- Conteo de visitas por hospital.
- Mediana de LDL por condición.
"""
    )
    return


@app.cell
def _(visits):
    visits_by_sex = (
        visits.groupby("sex", as_index=False)
        .agg(
            n_visits=("visit_id", "count"),
            mean_sbp=("sbp", "mean"),
            mean_ldl=("ldl", "mean"),
        )
        .sort_values("sex")
    )

    # Validación: debe haber exactamente 2 filas (female/male)
    assert visits_by_sex.shape[0] == 2

    visits_by_sex
    return (visits_by_sex,)


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
### Mini‑reto 1 (guiado): PAS promedio por hospital

**Tarea.** Construye un resumen con `groupby` que tenga:  
- una fila por `hospital`  
- `n_visits`: número de visitas  
- `mean_sbp`: PAS promedio  
- `min_age` y `max_age`: edad mínima y máxima observada  

Entrega un DataFrame llamado `summary_hospital`.

**Restricción.** No uses bucles; usa `groupby` + `agg`.
"""
    )
    return


@app.cell
def _(mo):
    tip_content = mo.md(
        r"""
### Tip

- Piensa en `groupby("hospital", as_index=False)` para que `hospital` quede como columna.
- Con `agg` puedes definir varias salidas:  
  `n_visits=("visit_id", "count")`, `mean_sbp=("sbp", "mean")`, `min_age=("age","min")`, `max_age=("age","max")`.
- Si quieres un orden estable, agrega `.sort_values("hospital")` al final.
"""
    )
    return (tip_content,)


@app.cell
def _(visits):
    # === TU TURNO (EDITA ESTA CELDA) ===
    # Construye `summary_hospital` según el mini-reto 1.

    summary_hospital = None

    # --- Validaciones (no editar) ---
    assert summary_hospital is not None, (
        "Debes asignar un DataFrame a `summary_hospital`."
    )
    assert list(summary_hospital.columns) == [
        "hospital",
        "n_visits",
        "mean_sbp",
        "min_age",
        "max_age",
    ], "Columnas esperadas: hospital, n_visits, mean_sbp, min_age, max_age."
    assert summary_hospital["hospital"].nunique() == summary_hospital.shape[0]
    assert summary_hospital["n_visits"].sum() == visits.shape[0]
    return (summary_hospital,)


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
## 3) `agg`: múltiples métricas por grupo (forma “tabla de reporte”)

En práctica clínica o epidemiología descriptiva, un reporte suele incluir:
- tamaño muestral (`count`)
- tendencia central (`mean`, `median`)
- dispersión (`std`, `min`, `max`)
- *métricas ad hoc* (por ejemplo, proporción de “alto riesgo”)

`agg` permite declarar explícitamente qué métrica se calcula sobre qué columna.
"""
    )
    return


@app.cell
def _(pd, visits):
    def prop_high_sbp(s: pd.Series) -> float:
        # Proporción de visitas con PAS ≥ 140 mmHg (umbral clínico simplificado)
        return float((s >= 140).mean())

    report_condition_sex = (
        visits.groupby(["condition", "sex"], as_index=False)
        .agg(
            n_visits=("visit_id", "count"),
            mean_age=("age", "mean"),
            median_sbp=("sbp", "median"),
            prop_high_sbp=("sbp", prop_high_sbp),
            mean_ldl=("ldl", "mean"),
        )
        .sort_values(["condition", "sex"])
    )

    assert set(report_condition_sex.columns) == {
        "condition",
        "sex",
        "n_visits",
        "mean_age",
        "median_sbp",
        "prop_high_sbp",
        "mean_ldl",
    }

    report_condition_sex.head(12)
    return prop_high_sbp, report_condition_sex


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
## 4) `pivot_table`: resúmenes “tipo Excel” con dos ejes

`pivot_table` es útil cuando quieres:
- filas = una dimensión (p. ej., hospital)
- columnas = otra dimensión (p. ej., condición)
- valores = una métrica (conteo o promedio)

En salud pública, esto aparece como:
- tabla de “casos por hospital y diagnóstico”
- promedio de biomarcadores por subgrupo

**Nota.** `pivot_table` usa `aggfunc` por defecto `mean`.
"""
    )
    return


@app.cell
def _(pd, visits):
    pivot_counts = pd.pivot_table(
        visits,
        index="hospital",
        columns="condition",
        values="visit_id",
        aggfunc="count",
        fill_value=0,
        margins=True,
        margins_name="TOTAL",
    )

    # Validación: debe tener fila TOTAL y columna TOTAL
    assert "TOTAL" in pivot_counts.index
    assert "TOTAL" in pivot_counts.columns

    pivot_counts
    return (pivot_counts,)


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
### Mini‑reto 2 (guiado): tabla de PAS promedio por hospital y sexo

**Tarea.** Construye una tabla con `pivot_table` que tenga:
- `index="hospital"`
- `columns="sex"`
- valores: promedio de `sbp`
- redondea a 1 decimal

Guárdala en `pivot_sbp`.

**Interpretación esperada.** Cada celda debe representar *promedio de PAS* en ese subgrupo (hospital × sexo).
"""
    )
    return


@app.cell
def _(mo):
    tip_content = mo.md(
        r"""
### Tip

- `pd.pivot_table(..., values="sbp", aggfunc="mean")` te da promedios.
- Después puedes usar `.round(1)` para redondear.
- Si quieres evitar `NaN` (por ejemplo, subgrupos sin visitas), usa `fill_value=...` con cuidado:  
  para promedios, suele ser mejor **dejar NaN** para no inventar datos.
"""
    )
    return (tip_content,)


@app.cell
def _(visits):
    import pandas as pd

    # === TU TURNO (EDITA ESTA CELDA) ===
    # Construye `pivot_sbp` según el mini-reto 2.

    pivot_sbp = None

    # --- Validaciones (no editar) ---
    assert pivot_sbp is not None, "Debes asignar una tabla a `pivot_sbp`."
    assert list(pivot_sbp.index.name for _ in [0])[0] == "hospital", (
        "El índice debe ser hospital."
    )
    assert set(pivot_sbp.columns).issubset({"female", "male"}), (
        "Columnas esperadas: female/male (o subset)."
    )
    return pd, pivot_sbp


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
## 5) `merge`: enriquecer una tabla con metadatos

En análisis de servicios de salud, es común tener:
- tabla de eventos/visitas
- tabla de metadatos de instituciones (región, nivel de complejidad, etc.)

`merge` permite unir ambas por una llave (p. ej., `hospital`) para luego resumir por los atributos nuevos.
"""
    )
    return


@app.cell
def _(pd):
    hospitals_meta = pd.DataFrame(
        {
            "hospital": ["HOSP_A", "HOSP_B", "HOSP_C"],
            "region": ["Urbana", "Urbana", "Rural"],
            "level": ["Alta complejidad", "Media complejidad", "Baja complejidad"],
        }
    )

    assert hospitals_meta["hospital"].is_unique
    hospitals_meta
    return (hospitals_meta,)


@app.cell
def _(pd, visits, hospitals_meta):
    visits_enriched = visits.merge(hospitals_meta, on="hospital", how="left")

    # Validaciones
    assert visits_enriched.shape[0] == visits.shape[0]
    assert visits_enriched["region"].isna().sum() == 0

    visits_enriched.head(10)
    return (visits_enriched,)


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
## 6) Caso aplicado: “tasa de seguimiento temprano” por región

Definimos un indicador simple (didáctico):  
- *seguimiento temprano* = próxima visita dentro de 30 días (`days_to_next <= 30`)

Luego estimamos la **proporción** de seguimiento temprano por región y condición.
"""
    )
    return


@app.cell
def _(pd, visits_enriched):
    visits_flags = visits_enriched.assign(
        early_follow_up=lambda d: d["days_to_next"] <= 30
    )

    followup_by_region_condition = (
        visits_flags.groupby(["region", "condition"], as_index=False)
        .agg(
            n_visits=("visit_id", "count"),
            prop_early_follow_up=("early_follow_up", "mean"),
        )
        .sort_values(["region", "condition"])
    )

    # Validaciones
    assert followup_by_region_condition["prop_early_follow_up"].between(0, 1).all()

    followup_by_region_condition
    return followup_by_region_condition, visits_flags


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
### Mini‑reto 3 (final, guiado): riesgo alto por región con `merge` + `groupby`

**Contexto.** Ya tienes `visits_enriched` (visitas + metadatos de hospital).  
Define “alto riesgo cardiometabólico” como:  
- `sbp >= 140` **o** `ldl >= 160`

**Tarea.** Construye un DataFrame `risk_by_region` con:
- una fila por `region`
- `n_visits`: conteo de visitas
- `prop_high_risk`: proporción de alto riesgo (entre 0 y 1)
- `mean_age`: edad promedio

**Reglas.**
- Usa `assign` para crear la columna booleana `high_risk`.
- Usa `groupby` + `agg` para el resumen.
- Ordena por `prop_high_risk` descendente para priorizar regiones con mayor carga.

Este mini‑reto integra toda la sesión: **enriquecer (merge) → derivar indicador → agrupar → resumir**.
"""
    )
    return


@app.cell
def _(mo):
    tip_content = mo.md(
        r"""
### Tip

- Para la columna booleana, combina condiciones con `|` y paréntesis:  
  `(d["sbp"] >= 140) | (d["ldl"] >= 160)`
- En `agg`, para proporciones de booleanos, `mean` funciona porque `True=1` y `False=0`.
- Asegúrate de mantener el resultado como DataFrame y de incluir `region` como columna (no como índice).
"""
    )
    return (tip_content,)


@app.cell
def _(visits_enriched):
    # === TU TURNO (EDITA ESTA CELDA) ===
    # Construye `risk_by_region` según el mini-reto 3.

    risk_by_region = None

    # --- Validaciones (no editar) ---
    assert risk_by_region is not None, "Debes asignar un DataFrame a `risk_by_region`."
    assert list(risk_by_region.columns) == [
        "region",
        "n_visits",
        "prop_high_risk",
        "mean_age",
    ], "Columnas esperadas: region, n_visits, prop_high_risk, mean_age."
    assert risk_by_region["prop_high_risk"].between(0, 1).all()
    assert risk_by_region["n_visits"].sum() == visits_enriched.shape[0]
    return (risk_by_region,)


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
## Cierre conceptual

En análisis tabular en salud, estas operaciones forman el “núcleo” de un reporte descriptivo:

- `groupby` define *estratos* (subpoblaciones).
- `agg` define *métricas* por estrato.
- `pivot_table` define *matrices* para comparar dimensiones.
- `merge` permite integrar *contexto* (metadatos) antes de resumir.

En la siguiente sesión, este estilo de resumen se vuelve una pieza de arquitectura:  
**tablas limpias + resúmenes estandarizados = outputs reproducibles**.
"""
    )
    return


if __name__ == "__main__":
    app.run()
