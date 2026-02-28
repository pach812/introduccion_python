import marimo

__generated_with = "0.20.2"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
# Semana 2 · Lección 4  
## Pandas como librería de estructura tabular

**Objetivo:** introducir *Series* y *DataFrame* como estructuras tabulares para análisis de datos en salud: creación, inspección, selección y filtrado usando operaciones básicas (**`loc`**, **`iloc`**, **`describe`**, **`min`**, **`max`**).

---
**Contexto de salud pública (motivación):**  
En análisis clínico/epidemiológico, la mayoría de datos llegan como tablas: filas = pacientes/visitas, columnas = variables (edad, sexo, presión arterial, IMC, biomarcadores). Pandas formaliza ese modelo y lo vuelve programable (selección, filtrado, resumen).

(Referencia conceptual general: material introductorio de “Python for Everybody”.)  [oai_citation:0‡pythonlearn.pdf](sediment://file_00000000652872439532dbc56d350645)
"""
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
## 1) ¿Qué es Pandas en este curso?

Pandas es una librería que ofrece:

- **`Series`**: una columna (1D) con índice.
- **`DataFrame`**: una tabla (2D) con filas y columnas etiquetadas.

En esta lección **NO** vamos a usar métodos avanzados (p. ej., `groupby`, `merge`, `pivot_table`).  
Nos enfocamos en: **crear, inspeccionar, seleccionar, filtrar y resumir**.
"""
    )
    return


@app.cell
def _():
    import pandas as pd

    return (pd,)


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
## 2) Series: una variable clínica como vector etiquetado

Una `Series` es ideal para representar una medición repetida:

- frecuencia cardiaca (bpm)
- glucosa (mg/dL)
- presión sistólica (mmHg)

Además de valores, tiene **índice** (etiquetas de cada observación).
"""
    )
    return


@app.cell
def _(pd):
    heart_rate = pd.Series([72, 88, 64, 91, 77], name="heart_rate_bpm")
    heart_rate
    return (heart_rate,)


@app.cell
def _(heart_rate):
    hr_min = heart_rate.min()
    hr_max = heart_rate.max()
    hr_min, hr_max
    return (hr_max, hr_min)


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
### Selección y filtrado básico en Series

- Comparaciones producen **máscaras booleanas**.
- Puedes filtrar con esa máscara: `serie[mask]`.

Ejemplo clínico: marcar pacientes con frecuencia cardiaca > 90 bpm.
"""
    )
    return


@app.cell
def _(heart_rate):
    tachy_mask = heart_rate > 90
    tachy_mask, heart_rate[tachy_mask]
    return (tachy_mask,)


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
## Mini-reto 1 (Series) — taquicardia

Crea una `Series` llamada `sbp` con presiones sistólicas (mmHg):  
`[118, 135, 142, 126, 160]`

Luego:

1) Calcula `sbp_min` y `sbp_max`.  
2) Filtra valores **≥ 140** en un objeto llamado `high_sbp`.

**Entrega:** variables `sbp`, `sbp_min`, `sbp_max`, `high_sbp`.

### Tip
- Una `Series` se crea con `pd.Series([...], name="...")`.
- Para filtrar: `sbp[sbp >= 140]`.
- `min()` y `max()` funcionan directo sobre la serie.
"""
    )
    return


@app.cell
def _(pd):
    # === TU TURNO (EDITA ESTA CELDA) ===
    # Crea la serie y las variables pedidas.
    sbp = None
    sbp_min = None
    sbp_max = None
    high_sbp = None

    return high_sbp, sbp, sbp_max, sbp_min


@app.cell
def _(high_sbp, sbp, sbp_max, sbp_min):
    # Validaciones (no edites esta celda)
    assert sbp is not None, "Debes definir sbp como una pd.Series."
    assert list(sbp.values) == [118, 135, 142, 126, 160], "Valores de sbp incorrectos."
    assert sbp_min == 118, "sbp_min incorrecto."
    assert sbp_max == 160, "sbp_max incorrecto."
    assert list(high_sbp.values) == [142, 160], "Filtrado high_sbp incorrecto."
    return


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
## 3) DataFrame: tabla clínica mínima

Un `DataFrame` representa el “dataset”:

- filas: pacientes
- columnas: variables

Vamos a construir un ejemplo de cohortes simple con:
- `age`, `sex`
- `sbp` (sistólica)
- `bmi`
"""
    )
    return


@app.cell
def _(pd):
    patients = pd.DataFrame(
        {
            "patient_id": [101, 102, 103, 104, 105],
            "age": [34, 58, 45, 67, 29],
            "sex": ["F", "M", "F", "M", "F"],
            "sbp": [118, 141, 132, 155, 110],
            "bmi": [22.4, 29.1, 31.8, 27.5, 24.0],
        }
    )
    patients
    return (patients,)


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
### Inspección rápida (diagnóstico estructural)

- `shape`: (filas, columnas)
- `columns`: nombres de variables
- `dtypes`: tipos inferidos
- `head()`: primeras filas
"""
    )
    return


@app.cell
def _(patients):
    patients.shape, patients.columns.tolist(), patients.dtypes
    return


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
## 4) Selección: `loc` vs `iloc`

- **`loc`**: selección por **etiquetas** (nombres de fila/columna).
- **`iloc`**: selección por **posiciones** (índices 0,1,2,...).

En salud: “dame columnas `age` y `sbp`” o “dame las primeras 3 filas”.
"""
    )
    return


@app.cell
def _(patients):
    # Selección de columnas por etiqueta
    patients.loc[:, ["age", "sbp"]]
    return


@app.cell
def _(patients):
    # Selección por posición: filas 0..2 y columnas 0..2
    patients.iloc[0:3, 0:3]
    return


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
## 5) Filtrado de filas (criterios clínicos)

El filtrado típico combina condiciones booleanas:

- hipertensión por cribado (ejemplo simple): `sbp >= 140`
- obesidad: `bmi >= 30`
- edad: `age >= 60`

**Importante:** usa paréntesis con operadores `&` (AND) y `|` (OR).
"""
    )
    return


@app.cell
def _(patients):
    high_risk = patients[(patients["sbp"] >= 140) & (patients["age"] >= 60)]
    high_risk
    return (high_risk,)


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
## 6) Resúmenes: `describe`, `min`, `max`

Para variables numéricas:

- `describe()` entrega estadísticos descriptivos
- `min()` / `max()` extraen extremos

Esto es el “primer vistazo” estándar antes de modelar.
"""
    )
    return


@app.cell
def _(patients):
    patients[["age", "sbp", "bmi"]].describe()
    return


@app.cell
def _(patients):
    patients["bmi"].min(), patients["bmi"].max()
    return


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
## Mini-reto 2 (DataFrame) — selección con `loc` e `iloc`

Usando el DataFrame `patients`:

1) Crea `demo` con columnas `patient_id`, `sex`, `age` (en ese orden).  
2) Crea `first_two_rows` con las **primeras 2 filas** y **primeras 3 columnas** usando `iloc`.

**Entrega:** variables `demo`, `first_two_rows`.

### Tip
- `loc` selecciona por nombres: `patients.loc[:, [...]]`
- `iloc` selecciona por posiciones: `patients.iloc[filas, columnas]`
- Recuerda que “primeras 2 filas” en Python suele ser `0:2`.
"""
    )
    return


@app.cell
def _(patients):
    # === TU TURNO (EDITA ESTA CELDA) ===
    demo = None
    first_two_rows = None

    return demo, first_two_rows


@app.cell
def _(demo, first_two_rows, patients):
    # Validaciones (no edites esta celda)
    assert demo is not None, "Debes definir demo."
    assert list(demo.columns) == ["patient_id", "sex", "age"], (
        "Columnas de demo incorrectas."
    )
    assert demo.shape == (patients.shape[0], 3), "Dimensión de demo incorrecta."

    assert first_two_rows is not None, "Debes definir first_two_rows."
    assert first_two_rows.shape == (2, 3), "Dimensión de first_two_rows incorrecta."
    assert first_two_rows.iloc[0, 0] == patients.iloc[0, 0], (
        "Contenido de first_two_rows no coincide."
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
## 7) Transformaciones simples: crear columnas

Un patrón básico en Pandas es derivar nuevas variables:

- IMC, razón cintura-cadera, score de riesgo simple, etc.

En un DataFrame, crear una columna nueva es asignar:

`df["new_col"] = ...`

Vamos a crear una variable categórica de obesidad (sí/no) basada en IMC.
"""
    )
    return


@app.cell
def _(patients):
    patients2 = patients.copy()
    patients2["obesity"] = patients2["bmi"] >= 30
    patients2
    return (patients2,)


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
## Mini-reto 3 (final) — tamizaje básico con IMC y PA

Con `patients2`:

1) Crea `screened` filtrando pacientes con:
   - `obesity == True` **o**
   - `sbp >= 140`

2) Crea `summary` con `describe()` **solo** para columnas numéricas `age`, `sbp`, `bmi`
   del DataFrame filtrado.

**Entrega:** variables `screened`, `summary`.

### Tip
- OR en Pandas: `(cond1) | (cond2)` (con paréntesis).
- Para `describe()` de columnas específicas: `df[["col1","col2"]].describe()`.
- Si dudas, imprime `screened.shape` para verificar cuántas filas quedaron.
"""
    )
    return


@app.cell
def _(patients2):
    # === TU TURNO (EDITA ESTA CELDA) ===
    screened = None
    summary = None

    return screened, summary


@app.cell
def _(screened, summary):
    # Validaciones (no edites esta celda)
    assert screened is not None, "Debes definir screened."
    assert summary is not None, "Debes definir summary."
    assert all(c in screened.columns for c in ["age", "sbp", "bmi", "obesity"]), (
        "Faltan columnas esperadas."
    )
    # Deben quedar al menos los casos con bmi>=30 (id 103) o sbp>=140 (id 102 y 104)
    kept_ids = set(screened["patient_id"].tolist())
    assert {102, 103, 104}.issubset(kept_ids), (
        "Tu filtro no está reteniendo todos los casos esperados."
    )
    # summary debe ser un DataFrame de describe()
    assert hasattr(summary, "loc"), "summary debe ser un objeto tipo DataFrame."
    for idx in ["count", "mean", "std", "min", "25%", "50%", "75%", "max"]:
        assert idx in summary.index, "summary no parece venir de describe()."
    return


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
# Cierre

En esta lección aprendiste a:

- Representar una medición clínica como `Series`.
- Representar un dataset clínico como `DataFrame`.
- Inspeccionar estructura (`shape`, `dtypes`) y explorar (`describe`, `min`, `max`).
- Seleccionar con `loc` e `iloc`.
- Filtrar con condiciones booleanas.
- Crear variables derivadas como columnas nuevas.

La siguiente fase natural (pero aún no aquí) es aprender a **resumir por grupos** y **combinar tablas**.
"""
    )
    return


if __name__ == "__main__":
    app.run()
