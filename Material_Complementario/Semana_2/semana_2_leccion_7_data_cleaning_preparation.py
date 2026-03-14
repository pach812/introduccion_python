# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "numpy==2.4.2",
#     "pandas==3.0.1",
#     "requests==2.32.5",
#     "pytest==9.0.2",
#     "pyreadr==0.5.4",
# ]
# ///

import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")

with app.setup(hide_code=True):
    import marimo as mo
    import numpy as np
    import pandas as pd
    import requests
    from setup import TipContent, TestContent


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Semana 2 · Lección 7
    ## Limpieza y preparación de datos

    **Idea central:** antes de resumir, agrupar o interpretar un dataset clínico, necesitamos volverlo **consistente, legible y analíticamente usable**.

    En esta sesión trabajaremos cuatro operaciones frecuentes de preparación de datos con `pandas`:

    - identificar y tratar valores faltantes,
    - detectar y remover duplicados,
    - estandarizar categorías inconsistentes,
    - construir una tabla final lista para análisis.

    ### Regla de trabajo

    En limpieza de datos, cada decisión debe responder una pregunta concreta:

    1. **¿Qué está mal o es inconsistente?**
    2. **¿Cómo lo corregimos sin perder trazabilidad?**
    3. **¿Qué validación confirma que la corrección funcionó?**

    Durante toda la lección seguiremos esta secuencia:

    **detectar → corregir → validar**
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Dataset de trabajo: seguimiento ambulatorio cardiometabólico

    Usaremos un dataset sintético de consultas de seguimiento en salud pública.

    Cada fila representa una observación clínica en una visita.

    Las columnas son:

    - `patient_id`: identificador del paciente
    - `visit_date`: fecha de la visita
    - `clinic`: sede de atención
    - `sex`: sexo reportado, con etiquetas inconsistentes
    - `age`: edad
    - `diagnosis`: diagnóstico principal, con algunas variaciones de escritura
    - `sbp`: presión arterial sistólica
    - `bmi`: índice de masa corporal
    - `adherence`: adherencia reportada

    El dataset fue construido **a propósito** con problemas comunes:

    - valores faltantes,
    - filas duplicadas,
    - categorías mal escritas,
    - y algunos valores imposibles.
    """)
    return


@app.cell(hide_code=True)
def _():
    visitas_brutas = pd.DataFrame(
        {
            "patient_id": [101, 102, 103, 104, 105, 106, 107, 108, 108, 109, 110, 111],
            "visit_date": [
                "2026-01-03",
                "2026-01-03",
                "2026-01-04",
                "2026-01-05",
                "2026-01-05",
                "2026-01-06",
                "2026-01-07",
                "2026-01-07",
                "2026-01-07",
                "2026-01-08",
                "2026-01-09",
                "2026-01-10",
            ],
            "clinic": [
                "Norte",
                "Norte",
                "Centro",
                "Sur",
                "Sur",
                "Centro",
                "Norte",
                "Centro",
                "Centro",
                "Sur",
                "Norte",
                "Sur",
            ],
            "sex": [
                "F",
                "female",
                "M",
                "male",
                "Female",
                "M",
                "f",
                "Male",
                "Male",
                "female",
                "male ",
                "F",
            ],
            "age": [45, 52, 61, 39, 150, 58, 47, 70, 70, 33, np.nan, 29],
            "diagnosis": [
                "HTN",
                "hypertension",
                "DM2",
                "T2D",
                "HTN",
                "asthma",
                "HTA",
                "DM2",
                "DM2",
                "Asthma",
                "HTA",
                "T2D",
            ],
            "sbp": [142, np.nan, 138, 126, 150, 118, np.nan, 144, 144, 121, 135, 128],
            "bmi": [28.4, 31.2, np.nan, 24.8, 29.1, 33.5, 27.0, np.nan, np.nan, 22.4, 26.8, 23.9],
            "adherence": ["high", "medium", None, "low", "medium", "high", None, "low", "low", "high", "medium", None],
        }
    )

    visitas_brutas["visit_date"] = pd.to_datetime(visitas_brutas["visit_date"])

    assert visitas_brutas.shape == (12, 9)
    visitas_brutas
    return (visitas_brutas,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 1) Inspección inicial: ver el problema antes de limpiar

    Limpiar no significa cambiar por cambiar.

    Primero debemos observar:

    - cuántos valores faltan por columna,
    - si existen filas repetidas,
    - y si algunas categorías no siguen una convención estable.

    Esta etapa convierte una impresión vaga de “el dataset está sucio” en una descripción concreta del problema.
    """)
    return


@app.cell
def _(visitas_brutas):
    resumen_faltantes = visitas_brutas.isna().sum().rename("n_missing")
    n_filas_duplicadas = int(visitas_brutas.duplicated().sum())
    valores_sexo = sorted(visitas_brutas["sex"].unique().tolist())
    valores_diagnostico = sorted(visitas_brutas["diagnosis"].unique().tolist())

    print("Valores faltantes por columna:")
    print(resumen_faltantes)
    print("\nFilas completamente duplicadas:", n_filas_duplicadas)
    print("\nEtiquetas observadas en sex:", valores_sexo)
    print("Etiquetas observadas en diagnosis:", valores_diagnostico)

    assert resumen_faltantes["sbp"] == 2
    assert resumen_faltantes["bmi"] == 3
    assert n_filas_duplicadas == 1
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 2) Valores faltantes: ausencia no es lo mismo que error, pero sí afecta el análisis

    En análisis de salud, los valores faltantes pueden surgir por múltiples razones:

    - una medición no realizada,
    - un dato no digitado,
    - una respuesta no disponible,
    - o una variable no aplicable.

    En esta lección trabajaremos una versión introductoria del problema:

    - para variables numéricas, imputaremos con una medida simple de tendencia central;
    - para variables categóricas, usaremos una etiqueta explícita.

    No estamos diciendo que esta sea siempre la mejor decisión clínica o estadística.

    Estamos practicando una **estrategia mínima, explícita y reproducible**.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto 1 — Completar `bmi` y `adherence`

    Construye una versión llamada `reto_faltantes` en la que:

    - `bmi` quede sin faltantes usando la **mediana** de `bmi`,
    - `adherence` quede sin faltantes usando la categoría `"unknown"`.

    Luego valida que ambas columnas ya no tengan valores faltantes.
    """)
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    reto_faltantes = None
    return


@app.cell(hide_code=True)
def _():
    tip_content_reto_faltantes = TipContent(
        items_raw=[
            r"""
    <Preservar la tabla original>
    Empieza creando una copia del dataset original.

    Eso evita modificar accidentalmente la tabla de partida.
    """,
            r"""
    <Variable numérica>
    Para `bmi`, necesitas una medida de tendencia central calculada sobre los valores observados.

    Piensa cuál función de pandas produce esa medida de manera directa.
    """,
            r"""
    <Variable categórica>
    En `adherence`, la idea no es estimar una categoría “probable”, sino dejar explícito que el valor no está disponible.

    Para eso puedes usar una etiqueta fija.
    """,
            r"""
    <solucion>

    ```python
    reto_faltantes = visitas_brutas.copy()
    reto_faltantes["bmi"] = reto_faltantes["bmi"].fillna(
        reto_faltantes["bmi"].median()
    )
    reto_faltantes["adherence"] = reto_faltantes["adherence"].fillna("unknown")
    ```
    """,
        ]
    )

    tip_content_reto_faltantes.render()
    return


@app.cell(hide_code=True)
def _():
    test_content_reto_faltantes = TestContent(
        items_raw=[
            r"""
    <Objeto definido>
    Verifica que hayas creado la tabla pedida.

    ```python
    assert reto_faltantes is not None, (
        "Debes asignar un DataFrame a `reto_faltantes`."
    )
    print("Tabla definida correctamente.")
    ```
    """,
            r"""
    <Sin faltantes en BMI>
    Verifica que la columna `bmi` ya no tenga valores faltantes.

    ```python
    assert reto_faltantes["bmi"].isna().sum() == 0, (
        "`bmi` no debería tener faltantes después de la imputación."
    )
    print("Imputación de BMI correcta.")
    ```
    """,
            r"""
    <Sin faltantes en adherencia>
    Verifica que la columna `adherence` ya no tenga valores faltantes.

    ```python
    assert reto_faltantes["adherence"].isna().sum() == 0, (
        "`adherence` no debería tener faltantes después del reemplazo."
    )
    print("Imputación de adherencia correcta.")
    ```
    """,
        ],
        namespace=globals(),
    )

    test_content_reto_faltantes.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Observa que aquí no “inventamos” estructura nueva.

    Solo hicimos explícito cómo resolver una ausencia para que el dataset pueda seguir avanzando en el flujo analítico.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 3) Duplicados: una fila repetida puede sesgar conteos y resúmenes

    Una fila duplicada puede aparecer por:

    - doble digitación,
    - unión errónea de archivos,
    - reprocesamiento de registros,
    - o fallas en exportación.

    Si no controlamos esto, el análisis puede sobreestimar volumen de visitas, frecuencias o promedios.

    Primero identificamos el problema, luego definimos **qué combinación de columnas representa una visita única**.
    """)
    return


@app.cell
def _(visitas_brutas):
    mascara_duplicados_llave = visitas_brutas.duplicated(
        subset=["patient_id", "visit_date", "clinic"],
        keep=False,
    )

    visitas_brutas.loc[
        mascara_duplicados_llave,
        ["patient_id", "visit_date", "clinic", "sex", "diagnosis", "sbp"],
    ]
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto 2 — Remover visitas repetidas

    Crea una tabla llamada `reto_sin_duplicados` a partir de `reto_faltantes` donde elimines duplicados usando como llave:

    - `patient_id`
    - `visit_date`
    - `clinic`

    Conserva la primera ocurrencia.

    Luego verifica que esa combinación ya no tenga duplicados.
    """)
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    reto_sin_duplicados = None
    return (reto_sin_duplicados,)


@app.cell(hide_code=True)
def _():
    tip_content_reto_duplicados = TipContent(
        items_raw=[
            r"""
    <No todos los duplicados son idénticos en toda la fila>
    Aquí la definición de duplicado depende de una llave específica, no necesariamente de todas las columnas.
    """,
            r"""
    <Método apropiado>
    Existe una función en pandas diseñada específicamente para remover duplicados a partir de un subconjunto de columnas.
    """,
            r"""
    <Validación consistente>
    Después de limpiar, conviene verificar el resultado usando exactamente la misma llave con la que definiste el duplicado.
    """,
            r"""
    <solucion>

    ```python
    reto_sin_duplicados = reto_faltantes.drop_duplicates(
        subset=["patient_id", "visit_date", "clinic"],
        keep="first",
    ).reset_index(drop=True)
    ```
    """,
        ]
    )

    tip_content_reto_duplicados.render()
    return


@app.cell(hide_code=True)
def _():
    test_content_reto_duplicados = TestContent(
        items_raw=[
            r"""
    <Objeto definido>
    Verifica que hayas creado la tabla deduplicada.

    ```python
    assert reto_sin_duplicados is not None, (
        "Debes asignar un DataFrame a `reto_sin_duplicados`."
    )
    print("Tabla definida correctamente.")
    ```
    """,
            r"""
    <Sin duplicados según la llave>
    Verifica que la combinación `patient_id`, `visit_date`, `clinic` ya no tenga duplicados.

    ```python
    duplicados_restantes = reto_sin_duplicados.duplicated(
        subset=["patient_id", "visit_date", "clinic"]
    ).sum()

    assert duplicados_restantes == 0, (
        "Todavía existen duplicados según la llave definida."
    )
    print("Duplicados removidos correctamente.")
    ```
    """,
            r"""
    <Número esperado de filas>
    Verifica que al eliminar una repetición quede el número correcto de observaciones.

    ```python
    assert reto_sin_duplicados.shape[0] == 11, (
        "La tabla debería quedar con 11 filas."
    )
    print("Número de filas correcto.")
    ```
    """,
        ],
        namespace=globals(),
    )

    test_content_reto_duplicados.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 4) Estandarización de categorías: mismo fenómeno, distintas etiquetas

    En datos clínicos es frecuente encontrar varias etiquetas para una misma categoría.

    Ejemplos:

    - `F`, `f`, `Female`, `female`
    - `HTN`, `HTA`, `hypertension`
    - `T2D`, `DM2`

    Desde el punto de vista analítico, estas variantes fragmentan el conteo de categorías.

    Una estrategia simple y poderosa es definir un **diccionario de recodificación** y aplicarlo con `replace()`.
    """)
    return


@app.cell
def _(reto_sin_duplicados):
    mapa_sexo = {
        "F": "female",
        "f": "female",
        "Female": "female",
        "female": "female",
        "M": "male",
        "Male": "male",
        "male": "male",
        "male ": "male",
    }

    mapa_diagnostico = {
        "HTN": "hypertension",
        "HTA": "hypertension",
        "hypertension": "hypertension",
        "DM2": "t2d",
        "T2D": "t2d",
        "asthma": "asthma",
        "Asthma": "asthma",
    }

    try: 
        tabla_estandarizada = reto_sin_duplicados.copy()
        tabla_estandarizada["sex"] = tabla_estandarizada["sex"].replace(mapa_sexo)
        tabla_estandarizada["diagnosis"] = tabla_estandarizada["diagnosis"].replace(
            mapa_diagnostico
        )
    
        print("Categorías limpias de sex:", sorted(tabla_estandarizada["sex"].unique().tolist()))
        print(
            "Categorías limpias de diagnosis:",
            sorted(tabla_estandarizada["diagnosis"].unique().tolist()),
        )
    
        assert set(tabla_estandarizada["sex"].unique()) == {"female", "male"}
        assert set(tabla_estandarizada["diagnosis"].unique()) == {
            "asthma",
            "hypertension",
            "t2d",
        }
    
        tabla_estandarizada[["patient_id", "sex", "diagnosis"]]
    except Exception as e:
        print("Aún no haz hecho el anterior reto, o hay un error en la recodificación:", e)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 5) Filtros de plausibilidad y tabla lista para análisis

    No toda inconsistencia es una ausencia o una etiqueta mal escrita.

    A veces el valor existe, pero no es plausible.

    En esta tabla observamos dos casos básicos:

    - una edad imposible (`150`),
    - una edad faltante.

    En un flujo introductorio, podemos decidir quedarnos solo con edades plausibles para análisis de adultos.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto 3 — Construir `tabla_analisis`

    A partir de `tabla_estandarizada`, construye una tabla final llamada `tabla_analisis` que cumpla estas condiciones:

    1. conservar solo edades entre `18` y `90`,
    2. completar `sbp` faltante con la **mediana** de `sbp`,
    3. renombrar `visit_date` a `date`,
    4. ordenar por `clinic` y `patient_id`.

    Al final valida que:

    - no haya edades faltantes,
    - no haya `sbp` faltante,
    - y que todas las edades estén en el rango definido.
    """)
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    tabla_analisis = None
    return (tabla_analisis,)


@app.cell(hide_code=True)
def _():
    tip_content_reto_final = TipContent(
        items_raw=[
            r"""
    <Filtrado por plausibilidad>
    Primero necesitas decidir qué filas son admisibles según la regla de edad.

    Esa decisión debe hacerse antes de completar otras variables.
    """,
            r"""
    <Imputación posterior al filtro>
    Una vez filtradas las edades no plausibles, puedes completar los faltantes de `sbp` con una medida resumen calculada sobre la tabla resultante.
    """,
            r"""
    <Transformaciones finales>
    Además de corregir valores, debes dejar la tabla con un nombre de columna más claro y con un orden estable para análisis posterior.
    """,
            r"""
    <solucion>

    ```python
    tabla_analisis = tabla_estandarizada.copy()
    tabla_analisis = tabla_analisis[tabla_analisis["age"].between(18, 90)].copy()
    tabla_analisis["sbp"] = tabla_analisis["sbp"].fillna(
        tabla_analisis["sbp"].median()
    )
    tabla_analisis = tabla_analisis.rename(columns={"visit_date": "date"})
    tabla_analisis = tabla_analisis.sort_values(
        ["clinic", "patient_id"]
    ).reset_index(drop=True)
    ```
    """,
        ]
    )

    tip_content_reto_final.render()
    return


@app.cell(hide_code=True)
def _():
    test_content_reto_final = TestContent(
        items_raw=[
            r"""
    <Objeto definido>
    Verifica que hayas creado la tabla final de análisis.

    ```python
    assert tabla_analisis is not None, (
        "Debes asignar un DataFrame a `tabla_analisis`."
    )
    print("Tabla definida correctamente.")
    ```
    """,
            r"""
    <Sin faltantes críticos>
    Verifica que no queden faltantes en edad ni en presión sistólica.

    ```python
    assert tabla_analisis["age"].isna().sum() == 0, (
        "No deberían quedar faltantes en `age`."
    )
    assert tabla_analisis["sbp"].isna().sum() == 0, (
        "No deberían quedar faltantes en `sbp`."
    )
    print("Faltantes resueltos correctamente.")
    ```
    """,
            r"""
    <Plausibilidad y estructura>
    Verifica que todas las edades queden en el rango definido y que la columna renombrada exista.

    ```python
    assert tabla_analisis["age"].between(18, 90).all(), (
        "Todas las edades deben estar entre 18 y 90."
    )
    assert "date" in tabla_analisis.columns, (
        "La columna `visit_date` debería haberse renombrado a `date`."
    )
    print("Plausibilidad y estructura correctas.")
    ```
    """,
        ],
        namespace=globals(),
    )

    test_content_reto_final.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Cierre conceptual

    En esta sesión no hicimos modelamiento ni visualización.

    Hicimos algo más fundamental: **preparar el terreno** para que un análisis posterior tenga sentido.

    Las operaciones clave fueron:

    - detectar valores faltantes,
    - imputar de forma explícita,
    - remover duplicados con una llave definida,
    - recodificar categorías inconsistentes,
    - y filtrar valores no plausibles.

    En términos analíticos, un dataset limpio no es “perfecto”.

    Es un dataset donde las reglas de preparación fueron **explícitas, justificables y verificables**.
    """)
    return


@app.cell
def _(tabla_analisis):
    try:
        resumen_por_sede = (
            tabla_analisis.groupby("clinic", as_index=False)
            .agg(
                n_visitas=("patient_id", "count"),
                media_edad=("age", "mean"),
                media_sbp=("sbp", "mean"),
            )
            .sort_values("clinic")
        )
    
        assert resumen_por_sede.shape[0] == 3
        resumen_por_sede = resumen_por_sede.round({"media_edad": 1, "media_sbp": 1})
    except Exception as e:
        print("Error al generar el resumen por sede:", e)
        resumen_por_sede = None
    resumen_por_sede
    return


if __name__ == "__main__":
    app.run()
