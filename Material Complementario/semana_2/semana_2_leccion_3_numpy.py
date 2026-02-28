# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "numpy==2.4.2",
# ]
# ///

import marimo

__generated_with = "0.20.2"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Semana 2 · Lección 3 — NumPy: arrays y vectorización

    **Objetivo conceptual:** pasar de *colecciones Python* (listas) a *arrays NumPy* para expresar operaciones numéricas **por lotes** (batch) sin escribir ciclos explícitos, manteniendo el código más claro y reproducible en tareas de salud pública.

    En esta lección trabajaremos con:
    - `ndarray` (arreglos) y sus propiedades (`shape`, `dtype`)
    - creación de arrays (`np.array`, `np.arange`, `np.linspace`)
    - operaciones element-wise y **vectorización**
    - indexación y slicing (1D y 2D)
    - máscaras booleanas y selección
    - agregaciones básicas (`mean`, `sum`, `min`, `max`)
    """)
    return


@app.cell
def _():
    import numpy as np


    return (np,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1) ¿Por qué NumPy en analítica de salud?

    En analítica clínica o epidemiológica, lo típico es operar sobre **vectores**:
    - pesos, tallas, IMC, presión arterial, colesterol, edad…
    - miles/millones de observaciones

    Con listas, muchas transformaciones requieren ciclos (`for`) y acumuladores.
    Con NumPy, expresamos el cálculo como **una sola operación sobre todo el vector**.

    **Idea clave:** *vectorización* = reemplazar ciclos explícitos por expresiones sobre arrays.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2) `ndarray`: el objeto central

    Un `ndarray` es un contenedor homogéneo (idealmente numérico):
    - `dtype`: tipo de dato (ej., `int64`, `float64`)
    - `shape`: forma (dimensiones)
    - operaciones aritméticas element-wise

    En salud, esto facilita:
    - calcular IMC para una cohorte
    - estandarizar biomarcadores (z-score)
    - seleccionar subgrupos con reglas clínicas (máscaras)
    """)
    return


@app.cell
def _(np):
    # Datos clínicos sintéticos (pequeños, pero representativos)
    # Peso (kg) y talla (m) de 8 pacientes
    peso_kg = np.array([72.0, 85.5, 60.2, 95.0, 68.0, 77.3, 110.4, 49.8])
    talla_m = np.array([1.75, 1.80, 1.62, 1.70, 1.68, 1.72, 1.78, 1.55])

    # Presión arterial sistólica (mmHg)
    pas_mmHg = np.array([118, 135, 110, 142, 128, 125, 160, 105])

    peso_kg, talla_m, pas_mmHg
    return pas_mmHg, peso_kg, talla_m


@app.cell
def _(peso_kg, talla_m):
    # Propiedades básicas del array
    peso_info = (peso_kg.shape, peso_kg.dtype)
    talla_info = (talla_m.shape, talla_m.dtype)
    peso_info, talla_info
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Operación vectorizada: IMC

    \[
    IMC = \frac{\text{peso (kg)}}{\text{talla (m)}^2}
    \]

    En NumPy, `talla_m ** 2` eleva al cuadrado **cada elemento**.
    """)
    return


@app.cell
def _(np, peso_kg, talla_m):
    imc = peso_kg / (talla_m**2)
    imc_2_dec = np.round(imc, 2)
    imc_2_dec
    return imc, imc_2_dec


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3) Indexación y slicing (1D)

    - `arr[i]` selecciona el elemento i
    - `arr[a:b]` selecciona un rango (incluye a, excluye b)

    En salud: seleccionar pacientes 0–2 para inspección rápida, o un “batch” de revisión.
    """)
    return


@app.cell
def _(imc_2_dec):
    primer_paciente = imc_2_dec[0]
    primeros_tres = imc_2_dec[:3]
    primer_paciente, primeros_tres
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4) Máscaras booleanas: selección por criterio clínico

    Una máscara booleana es un array de `True/False` del mismo tamaño:
    - `imc >= 30` produce una máscara
    - `imc[imc >= 30]` filtra los valores

    En salud pública: identificar obesidad, hipertensión probable, etc.
    """)
    return


@app.cell
def _(imc, np, pas_mmHg):
    def _():
        obesidad = imc >= 30
        probable_hta = pas_mmHg >= 140

        imc_obesidad = np.round(imc[obesidad], 2)
        pas_probable_hta = pas_mmHg[probable_hta]
        return obesidad, probable_hta, imc_obesidad, pas_probable_hta


    _()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5) Agregaciones básicas (resumen rápido)

    NumPy permite calcular estadísticas descriptivas inmediatas:
    - `mean()`, `min()`, `max()`, `sum()`

    Esto conecta con análisis descriptivo de cohortes (sin necesidad de tablas todavía).
    """)
    return


@app.cell
def _(imc, pas_mmHg):
    resumen = {
        "imc_mean": float(imc.mean()),
        "imc_min": float(imc.min()),
        "imc_max": float(imc.max()),
        "pas_mean": float(pas_mmHg.mean()),
        "pas_min": int(pas_mmHg.min()),
        "pas_max": int(pas_mmHg.max()),
    }
    resumen
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    # Mini-reto 1 — Cohorte (IMC vectorizado)

    **Dominio:** clínica / salud pública

    Tienes una cohorte de pacientes con `peso_kg_r1` y `talla_m_r1`.

    **Tarea:** calcula `imc_r1` como array NumPy (sin ciclos) y redondea a 1 decimal en `imc_r1_1d`.

    **Restricción didáctica:** usa solo lo visto (arrays y operaciones vectorizadas).
    """)
    return


@app.cell
def _(np):
    # Datos (no cambiar)
    peso_kg_r1 = np.array([50.0, 64.2, 72.0, 80.0, 92.5])
    talla_m_r1 = np.array([1.55, 1.68, 1.75, 1.80, 1.70])

    # === TU TURNO (EDITA ESTA CELDA) ===
    # TODO: calcula IMC vectorizado (np.array ya está)
    imc_r1 = None

    # TODO: redondea a 1 decimal
    imc_r1_1d = None

    print("IMC (1 decimal):", imc_r1_1d)
    return imc_r1, imc_r1_1d, peso_kg_r1, talla_m_r1


@app.cell(hide_code=True)
def _(mo):
    _tip = mo.md(
        r"""
    - La fórmula es: `peso / (talla ** 2)`
    - Si `peso` y `talla` son arrays, la operación se aplica elemento a elemento.
    - Para redondear: `np.round(arr, 1)`
    """
    )
    mo.accordion({"### Tip": _tip})
    return


@app.cell(hide_code=True)
def _(imc_r1, imc_r1_1d, mo, np, peso_kg_r1, talla_m_r1):
    def _():
        # Validación oculta (sin mostrar solución)
        imc_ref = peso_kg_r1 / (talla_m_r1**2)
        imc_ref_1d = np.round(imc_ref, 1)

        assert isinstance(imc_r1, np.ndarray)
        assert isinstance(imc_r1_1d, np.ndarray)
        assert imc_r1.shape == peso_kg_r1.shape
        assert np.allclose(imc_r1, imc_ref, rtol=0, atol=1e-12)
        assert np.allclose(imc_r1_1d, imc_ref_1d, rtol=0, atol=1e-12)
        return mo.md("✅ Mini-reto 1 superado.")


    _()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6) Estandarización (z-score) sin ciclos

    En cohortes, es frecuente estandarizar biomarcadores:

    \[
    z = \frac{x - \mu}{\sigma}
    \]

    En NumPy:
    - `x.mean()` y `x.std()` producen escalares
    - `x - x.mean()` produce un array
    - todo se aplica vectorizado
    """)
    return


@app.cell
def _(np):
    # Biomarcador (p. ej. proteína inflamatoria) en unidades arbitrarias
    biomarcador = np.array([2.1, 2.4, 1.9, 3.2, 2.8, 2.0, 3.6, 1.7])
    mu = biomarcador.mean()
    sigma = biomarcador.std()

    z = (biomarcador - mu) / sigma
    np.round(z, 2)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    # Mini-reto 2 — Laboratorio (z-score + umbral)

    **Dominio:** laboratorio / epidemiología

    Usa `biomarcador_r2` y calcula:

    1) `z_r2`: z-score vectorizado
    2) `alto_riesgo_r2`: máscara booleana para `z_r2 >= 1.0`
    3) `n_alto_riesgo_r2`: cuántos pacientes cumplen el criterio (entero)

    **Nota:** no uses ciclos.
    """)
    return


@app.cell
def _(np):
    # Datos (no cambiar)
    biomarcador_r2 = np.array([10.0, 9.5, 12.2, 11.1, 8.9, 9.8, 13.0, 10.4])

    # === TU TURNO (EDITA ESTA CELDA) ===
    # TODO: media y desviación estándar
    mu_r2 = None
    sigma_r2 = None

    # TODO: z-score vectorizado
    z_r2 = None

    # TODO: máscara alto riesgo
    alto_riesgo_r2 = None

    # TODO: conteo de alto riesgo (int)
    n_alto_riesgo_r2 = None

    print("z:", z_r2)
    print("alto_riesgo:", alto_riesgo_r2)
    print("n_alto_riesgo:", n_alto_riesgo_r2)
    return (
        alto_riesgo_r2,
        biomarcador_r2,
        mu_r2,
        n_alto_riesgo_r2,
        sigma_r2,
        z_r2,
    )


@app.cell(hide_code=True)
def _(mo):
    def _():
        tip = mo.md(
            r"""
        - `mu = arr.mean()`
        - `sigma = arr.std()`
        - `z = (arr - mu) / sigma`
        - Una máscara se crea con una comparación: `z >= 1.0`
        - Para contar `True`: `mask.sum()` (en NumPy, `True` cuenta como 1)
        """
        )
        return mo.accordion({"### Tip": tip})


    _()
    return


@app.cell(hide_code=True)
def _(
    alto_riesgo_r2,
    biomarcador_r2,
    mo,
    mu_r2,
    n_alto_riesgo_r2,
    np,
    sigma_r2,
    z_r2,
):
    def _():
        mu_ref = biomarcador_r2.mean()
        sigma_ref = biomarcador_r2.std()
        z_ref = (biomarcador_r2 - mu_ref) / sigma_ref
        mask_ref = z_ref >= 1.0
        n_ref = int(mask_ref.sum())

        assert abs(mu_r2 - mu_ref) < 1e-12
        assert abs(sigma_r2 - sigma_ref) < 1e-12
        assert isinstance(z_r2, np.ndarray) and z_r2.shape == biomarcador_r2.shape
        assert np.allclose(z_r2, z_ref, rtol=0, atol=1e-12)
        assert isinstance(alto_riesgo_r2, np.ndarray) and alto_riesgo_r2.dtype == bool
        assert np.array_equal(alto_riesgo_r2, mask_ref)
        assert int(n_alto_riesgo_r2) == n_ref
        return mo.md("✅ Mini-reto 2 superado.")


    _()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7) Arrays 2D: “paciente × variable”

    Una forma simple de representar un bloque clínico es una matriz:

    - filas = pacientes
    - columnas = variables (ej. PAS, PAD, FC)

    En NumPy:
    - `X.shape` devuelve `(n_filas, n_columnas)`
    - `X[:, j]` selecciona la columna j
    - `X[i, :]` selecciona la fila i
    """)
    return


@app.cell
def _(np):
    # Matriz: columnas = [PAS, PAD, FC]
    X_vitales = np.array(
        [
            [118, 76, 70],
            [135, 85, 78],
            [110, 72, 66],
            [142, 90, 88],
            [128, 82, 74],
            [125, 80, 72],
            [160, 95, 92],
            [105, 68, 60],
        ],
        dtype=float,
    )

    X_vitales.shape, X_vitales.dtype
    return (X_vitales,)


@app.cell
def _(X_vitales, np):
    # Promedio por columna (variable): PAS, PAD, FC
    mean_por_variable = X_vitales.mean(axis=0)
    np.round(mean_por_variable, 2)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8) Composición de criterios con máscaras

    Podemos combinar criterios clínicos con operadores lógicos:
    - `&` (AND) y `|` (OR) para arrays booleanos
    *(no usar `and/or` con arrays)*

    Ejemplo: “probable HTA” si:
    - PAS >= 140 **o** PAD >= 90
    """)
    return


@app.cell
def _(X_vitales):
    pas = X_vitales[:, 0]
    pad = X_vitales[:, 1]

    probable_hta = (pas >= 140) | (pad >= 90)
    probable_hta, probable_hta.sum()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    # Mini-reto 3 (final) — Tamizaje clínico vectorizado

    **Dominio:** clínica / salud pública

    Usa una matriz `X_r3` con columnas:

    - `PAS` (col 0)
    - `PAD` (col 1)
    - `IMC` (col 2)

    **Tareas:**

    1) Extrae `pas_r3`, `pad_r3`, `imc_r3` como arrays 1D usando slicing.
    2) Crea una máscara `hta_r3` para probable HTA: `(PAS >= 140) | (PAD >= 90)`.
    3) Crea una máscara `alto_riesgo_r3` para “alto riesgo cardiometabólico”:
       - probable HTA **y** IMC >= 30
    4) Calcula `n_alto_riesgo_r3` (entero) con el conteo de `True`.

    **Restricción:** todo vectorizado, sin ciclos.
    """)
    return


@app.cell
def _(np):
    # Datos (no cambiar)
    # columnas: PAS, PAD, IMC
    X_r3 = np.array(
        [
            [118, 76, 23.5],
            [145, 92, 31.2],
            [132, 88, 29.8],
            [160, 95, 34.1],
            [138, 85, 30.0],
            [150, 89, 28.4],
            [128, 82, 35.0],
            [142, 91, 27.9],
        ],
        dtype=float,
    )

    # === TU TURNO (EDITA ESTA CELDA) ===
    # TODO: extraer columnas
    pas_r3 = None
    pad_r3 = None
    imc_r3 = None

    # TODO: máscaras
    hta_r3 = None
    alto_riesgo_r3 = None

    # TODO: conteo
    n_alto_riesgo_r3 = None

    print("hta:", hta_r3)
    print("alto_riesgo:", alto_riesgo_r3)
    print("n_alto_riesgo:", n_alto_riesgo_r3)
    return (
        X_r3,
        alto_riesgo_r3,
        hta_r3,
        imc_r3,
        n_alto_riesgo_r3,
        pad_r3,
        pas_r3,
    )


@app.cell(hide_code=True)
def _(mo):
    tip = mo.md(
        r"""
    ### Tip

    - Extraer columnas: `col = X[:, j]`
    - Criterio HTA: `(pas >= 140) | (pad >= 90)`
    - Combinar con AND: `mask1 & mask2`
    - Conteo: `int(mask.sum())`
    """
    )
    mo.accordion({"Tip": tip})
    return


@app.cell(hide_code=True)
def _(
    X_r3,
    alto_riesgo_r3,
    hta_r3,
    imc_r3,
    mo,
    n_alto_riesgo_r3,
    np,
    pad_r3,
    pas_r3,
):
    pas_ref = X_r3[:, 0]
    pad_ref = X_r3[:, 1]
    imc_ref = X_r3[:, 2]

    hta_ref = (pas_ref >= 140) | (pad_ref >= 90)
    alto_ref = hta_ref & (imc_ref >= 30)
    n_ref = int(alto_ref.sum())

    assert isinstance(pas_r3, np.ndarray) and np.array_equal(pas_r3, pas_ref)
    assert isinstance(pad_r3, np.ndarray) and np.array_equal(pad_r3, pad_ref)
    assert isinstance(imc_r3, np.ndarray) and np.array_equal(imc_r3, imc_ref)

    assert isinstance(hta_r3, np.ndarray) and hta_r3.dtype == bool
    assert np.array_equal(hta_r3, hta_ref)

    assert isinstance(alto_riesgo_r3, np.ndarray) and alto_riesgo_r3.dtype == bool
    assert np.array_equal(alto_riesgo_r3, alto_ref)

    assert int(n_alto_riesgo_r3) == n_ref

    mo.md("✅ Mini-reto 3 (final) superado.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cierre conceptual

    Hoy construiste el puente:

    **listas → arrays → operaciones vectorizadas**

    Esto te prepara para:
    - trabajar con datos numéricos a escala
    - expresar reglas clínicas/epidemiológicas como máscaras
    - producir resúmenes rápidos reproducibles

    En la próxima etapa, estos arrays serán la base para estructuras tabulares más ricas.
    """)
    return


if __name__ == "__main__":
    app.run()
