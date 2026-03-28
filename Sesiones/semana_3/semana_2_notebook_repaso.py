# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "marimo",
#     "numpy==2.4.2",
#     "pandas==3.0.1",
# ]
# ///

import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")

with app.setup(hide_code=True):
    import re
    import pickle

    import marimo as mo
    import numpy as np
    import pandas as pd

    from pathlib import Path


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Semana 2 · Notebook de repaso
    ## Código en vivo

    ### Propósito
    Este notebook reorganiza el repaso de la semana 2 usando los datasets simulados con caracteristicas de poblacion Colombiana:

    - `poblacion_inicial.csv`
    - `dataset_sucio.csv`
    - `diccionario_datos.csv`

    Vamos a trabajar con **dos versiones del mismo fenómeno**:

    1. una versión más estable para entender estructura y análisis (`poblacion_inicial`),
    2. una versión con problemas realistas para limpieza y preparación (`dataset_sucio`).
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Hoja de ruta

    ### Temas integrados de la semana

    1. **Módulos y librerías** para organizar el flujo.
    2. **POO mínima** para encapsular reglas repetidas.
    3. **NumPy** para cálculos vectorizados.
    4. **pandas** para inspección, filtrado y derivación.
    5. **Carga y almacenamiento** de datos y resultados.
    6. **Limpieza y preparación** con datos sucios.
    7. **Wrangling** con `groupby`, `agg`, `merge` y `pivot_table`.

    ### Estructura de uso de datasets

    - `poblacion_inicial`: lo usaremos para entender forma, variables y resúmenes.
    - `dataset_sucio`: lo usaremos para limpieza, estandarización y validación.
    - `diccionario_datos`: lo usaremos como referencia formal de significado y tipo esperado.
    """)
    return


@app.cell
def _():
    # Define file paths once so the notebook is portable inside the course folder.
    data_dir = mo.notebook_dir() / "public/"
    path_population = data_dir / "poblacion_inicial.csv"
    path_dirty = data_dir / "dataset_sucio.csv"
    path_dictionary = data_dir / "diccionario_datos.csv"

    file_map = {
        "population": path_population,
        "dirty": path_dirty,
        "dictionary": path_dictionary,
    }

    file_map
    return path_dictionary, path_dirty, path_population


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 1) Módulos e imports

    ### Qué usaremos hoy

    - `pathlib` para rutas reproducibles.
    - `re` para limpieza textual.
    - `pickle` para serializar objetos Python.
    - `numpy` para operaciones vectorizadas.
    - `pandas` para carga, transformación y resumen.
    """)
    return


@app.cell
def _(path_dictionary, path_dirty, path_population):
    # Carga los datasets y haz un resumen rápido de filas y columnas para cada uno, usando el diccionario como referencia.
    dictionary_df = pd.read_csv(path_dictionary)
    population_df = pd.read_csv(path_population)
    dirty_df = pd.read_csv(path_dirty)

    resumen_archivos = pd.DataFrame(
        {
            "dataset": ["diccionario", "poblacion_inicial", "dataset_sucio"],
            "filas": [
                dictionary_df.shape[0],
                population_df.shape[0],
                dirty_df.shape[0],
            ],
            "columnas": [
                dictionary_df.shape[1],
                population_df.shape[1],
                dirty_df.shape[1],
            ],
        }
    )
    resumen_archivos
    return dictionary_df, population_df


@app.cell
def _(dictionary_df):
    dictionary_df.head(10)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 2) Primer reconocimiento del problema analítico

    Antes de limpiar o modelar, conviene responder tres preguntas:

    1. ¿Qué variables hay?
    2. ¿Qué tipo de variable representa cada una?
    3. ¿Qué tabla será la referencia “más confiable” para comparar?

    Aquí el diccionario funciona como documento técnico y `poblacion_inicial` como versión base del dataset.
    """)
    return


@app.cell
def _(dictionary_df, population_df):
    # Construyamos una tabla que compare la estructura del dataset limpio con lo que dice el diccionario.
    estructa_df = pd.DataFrame(
        {"variable": population_df.columns, "tipo_de_dato": population_df.dtypes}
    )

    df_unido = pd.merge(
        estructa_df,
        dictionary_df[["variable", "tipo", "categoria"]],
        on="variable",
        how="left",
    )
    df_unido
    return


@app.cell
def _(population_df):
    # Separamos las variables en grupos para facilitar ejercicios posteriores de análisis y limpieza.
    sociodemographic_vars = [
        "id_paciente",
        "edad",
        "sexo",
        "etnia",
        "region",
        "zona",
        "quintil_ingreso",
        "educacion",
    ]
    lifestyle_vars = ["tabaquismo", "actividad_fisica", "dieta", "alcohol"]
    clinical_vars = [
        "imc",
        "categoria_imc",
        "sbp",
        "dbp",
        "glucosa",
        "ldl",
        "hdl",
        "trigliceridos",
        "hba1c",
        "creatinina",
        "egfr",
        "riesgo_global",
    ]
    comorbidity_vars = ["hipertension", "diabetes", "epoc", "erc", "depresion"]

    # Mostramos un vistazo rápido a las variables agrupadas por tipo, para entender mejor la estructura del dataset.
    population_df[
        sociodemographic_vars + lifestyle_vars + clinical_vars + comorbidity_vars
    ]
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 3) POO mínima para validar y derivar reglas

    No necesitamos una jerarquía compleja de clases. Basta una clase pequeña que nos ayude a:

    - validar presencia de columnas,
    - crear bandas de edad,
    - etiquetar riesgo clínico,
    - resumir prevalencias.
    """)
    return


@app.cell
def _(population_df):
    class PopulationAnalyzer:
        # - validar presencia de columnas,
        # - crear bandas de edad,
        # - etiquetar riesgo clínico,
        # - resumir prevalencias.
        required_columns = {
            "edad",
            "sexo",
            "imc",
            "sbp",
            "dbp",
            "glucosa",
            "riesgo_global",
            "hipertension",
            "diabetes",
        }

        def __init__(self, df: pd.DataFrame):
            self.df = df.copy()
            self._validate_columns()

        def _validate_columns(self):
            missing_columns = self.required_columns.difference(self.df.columns)

            if missing_columns:
                raise ValueError(
                    f"Le faltan las columnas: {missing_columns}",
                )

        def add_band_age(self):
            bins = [0, 29, 44, 59, 74, np.inf]
            labels = ["0-29", "30-44", "45-59", "60-74", "75+"]
            self.df["banda_edad"] = pd.cut(
                self.df["edad"], bins=bins, labels=labels, right=True
            )
            return self.df

        def add_risk(self, threshold=7.5):
            self.df["alto_riesgo"] = self.df["riesgo_global"] >= threshold
            return self.df

        def resumen_prevalencias(self):
            summary = (
                self.df.groupby("sexo")[["hipertension", "diabetes"]]
                .mean()
                .mul(100)
                .round(2)
                .rename(
                    columns={
                        "hipertension": "Prev_hipertension",
                        "diabetes": "Prev_diabetes",
                    }
                )
                .reset_index()
            )
            return summary


    limpiador = PopulationAnalyzer(population_df)

    limpiador.add_band_age()
    limpiador.add_risk()
    limpiador.resumen_prevalencias()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 4) NumPy para cálculos vectorizados

    Ahora usamos `NumPy` para pensar como analistas:

    - crear umbrales,
    - clasificar observaciones,
    - resumir distribuciones,
    - comparar subgrupos.

    ### Ejercicio de clase
    Construyamos una clasificación rápida de presión arterial sistólica y revisemos percentiles de riesgo.
    """)
    return


@app.cell
def _(population_df):
    # Extracción a arrays de NumPy
    # - to_numpy(): permite operaciones vectorizadas eficientes
    sbp_values = population_df["sbp"].to_numpy()
    risk_values = population_df["riesgo_global"].to_numpy()

    # Clasificación de PAS
    # - np.select: asigna categorías según condiciones
    # - condlist: reglas en orden de evaluación
    # - choicelist: etiquetas correspondientes
    condlist = [
        sbp_values < 120, # normal
        sbp_values < 140, # elevada
        sbp_values >= 140, # alta
    ]

    choicelist = [
        "normal",
        "elevada",
        "alta"
    ]

    sbp_status = np.select(condlist, choicelist, default="no_clasificada")

    # Percentiles de riesgo
    # - np.percentile: resume la distribución en puntos clave
    # - [10, 25, 50, 75, 90]: percentiles comunes (incluye mediana = 50)
    risk_percentiles = np.percentile(
        risk_values,
        [10,25,50,75,90]
    )

    # Resumen numérico
    # - mean: promedio
    # - sum(condición): conteo de casos que cumplen criterio
    numpy_summary = {
        "media sbp": np.mean(sbp_values),
        "media risk": np.mean(risk_values),
        "percentil de riesgo": risk_percentiles,
        "presion elevada cuenta": np.sum(sbp_status == "alta")
    }

    # Resultado final
    numpy_summary
    return


@app.cell
def _():
    # Copia del dataset
    # - evita modificar el DataFrame original


    # Añadir clasificación de PAS
    # - estado_sbp_numpy: categorías creadas con np.select


    # Vista de resultados
    # - selección de columnas clave
    # - head(10): primeras 10 filas para inspección rápida
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 5) pandas: inspección, filtrado y resúmenes útiles

    Con la versión limpia del dataset podemos practicar preguntas de análisis exploratorio sin distraernos todavía con problemas de calidad.

    ### Preguntas para resolver en vivo

    1. ¿Cómo se distribuye la población por sexo y región?
    2. ¿Cuál es el riesgo promedio por banda de edad?
    3. ¿Qué combinación de comorbilidades aparece con más frecuencia?
    """)
    return


@app.cell
def _():
    # ---------------------------
    # Tabla: sexo x región
    # ---------------------------
    # - groupby: cruza dos variables categóricas
    # - size(): cuenta número de filas por combinación
    # - reset_index: convierte a DataFrame
    # - sort_values: ordena por sexo y frecuencia


    # ---------------------------
    # Riesgo por banda de edad
    # ---------------------------
    # - groupby: agrupa por categoría de edad
    # - agg: calcula múltiples métricas
    #   - mean: promedio
    #   - median: robusto a outliers
    #   - count: tamaño del grupo
    # - rename: nombres más claros para salida


    # ---------------------------
    # Perfil de comorbilidades
    # ---------------------------
    # - assign: crea variable combinada (perfil)
    # - concatenación: une estados de HTA, DM y ERC
    # - groupby + size: cuenta frecuencia de cada perfil
    # - head(10): top perfiles más comunes


    # Vista rápida de la primera tabla
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 6) Ahora sí: limpieza con el dataset sucio

    Aqui vamos a **detectar y corregir problemas** como si fuera un dataset real.

    ### Problemas que sí aparecen en `dataset_sucio`

    - faltantes,
    - etiquetas inconsistentes,
    - unidades incrustadas en celdas,
    - porcentajes donde debería haber números,
    - comas decimales,
    - columnas numéricas leídas como texto.

    La regla clave es que el diccionario define la intención semántica de la variable, mientras que el CSV sucio muestra cómo llegó realmente el dato.
    """)
    return


@app.cell
def _():
    # Construcción de overview del dataset "sucio"
    # - resume estructura, tipos y calidad de datos por variable


    # Ordenar variables
    # - primero por mayor % de faltantes
    # - luego alfabéticamente


    # Vista rápida (top 20 variables más problemáticas)
    return


@app.cell
def _():
    # Función auxiliar para limpiar variables numéricas
    # - pensada para columnas con texto mezclado con unidades o símbolos
    def clean_numeric_series(series: pd.Series) -> pd.Series:
        pass


    # Columnas numéricas a limpiar
    # - estas variables deberían quedar como tipo numérico tras la limpieza
    numeric_columns_to_clean = [
        "sbp",
        "dbp",
        "glucosa",
        "ldl",
        "hdl",
        "trigliceridos",
        "hba1c",
        "creatinina",
        "albuminuria",
        "frecuencia_cardiaca",
    ]

    # Columnas categóricas a estandarizar
    # - el objetivo es uniformar escritura y formato
    categorical_columns_to_standardize = [
        "sexo",
        "etnia",
        "region",
        "zona",
        "educacion",
        "tabaquismo",
        "actividad_fisica",
        "dieta",
        "alcohol",
        "categoria_imc",
    ]

    # Copia de trabajo
    # - evita modificar el DataFrame original


    # Limpieza de variables numéricas
    # - aplica la función a cada columna definida arriba


    # Estandarización básica de variables categóricas
    # - astype("string"): usa tipo texto consistente
    # - strip(): elimina espacios sobrantes
    # - title(): uniforma mayúsculas/minúsculas


    # Correcciones puntuales en sexo
    # - resuelve variantes equivalentes o con espacios residuales


    # Correcciones puntuales en zona
    # - unifica etiquetas semánticamente equivalentes


    # Correcciones puntuales en actividad física
    # - armoniza una categoría intermedia


    # Inspección rápida del resultado
    # - permite verificar limpieza numérica y estandarización categórica
    return


@app.cell
def _(dirty_cleaned):
    # Definición de reglas de plausibilidad
    # - establece rangos clínicamente razonables por variable
    # - valores fuera de estos rangos se considerarán inválidos
    plausibility_rules = {
        "sbp": (70, 260),
        "dbp": (40, 160),
        "glucosa": (40, 500),
        "ldl": (20, 400),
        "hdl": (10, 150),
        "trigliceridos": (20, 1200),
        "hba1c": (3, 20),
        "creatinina": (0.2, 15),
        "frecuencia_cardiaca": (30, 220),
    }

    # Contenedor para registrar problemas de calidad
    quality_flags = []

    # Copia de trabajo
    # - permite aplicar reglas sin alterar directamente el dataset previo
    dirty_val = dirty_cleaned.copy()

    # Aplicación de reglas de plausibilidad


    # Resumen de calidad
    # - DataFrame con conteo de valores fuera de rango por variable


    # Resultado
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 7) Validar contra el diccionario

    El diccionario no limpia por sí mismo, pero permite responder preguntas muy útiles:

    - ¿qué variables deberían ser numéricas?,
    - ¿qué variables deberían ser categóricas?,
    - ¿qué columnas del CSV están incumpliendo esa expectativa?

    Este paso ayuda a enseñar pensamiento reproducible: no se trata solo de “arreglar”, sino de justificar por qué una corrección tiene sentido.
    """)
    return


@app.cell
def _():
    # Identificar variables que deberían ser numéricas
    # - filtra diccionario de datos por tipo esperado
    # - incluye variables continuas, enteras y binarias


    # Comparación de tipos entre datasets
    # - variable: nombre de la columna
    # - dtype_poblacion: tipo en dataset limpio/objetivo
    # - dtype_sucio: tipo en dataset original (antes de limpieza)
    # - esperado_numerico: indica si la variable debería ser numérica según diccionario


    # Detección de inconsistencias
    # - variables que deberían ser numéricas pero están como "object"
    # - típicamente indica presencia de texto, símbolos o errores de parsing
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 8) Wrangling: comparar versión limpia vs versión corregida

    Ya tenemos dos tablas útiles:

    - `poblacion_inicial`: referencia base,
    - `dirty_validated`: versión corregida del dataset sucio.

    Ahora el ejercicio interesante es comparar qué tanto cambian algunos resúmenes después de limpiar.
    """)
    return


@app.cell
def _():
    # Comparación de métricas entre dataset limpio y dataset corregido
    # - permite evaluar si la limpieza introdujo sesgos relevantes


    # Diferencia absoluta
    # - cuantifica desviación entre datasets
    # - abs(): ignora dirección del cambio
    # - round(3): precisión suficiente para inspección


    # Resultado final
    # - útil para auditoría de calidad post-limpieza
    return


@app.cell
def _():
    # Enriquecimiento del dataset validado
    # - assign: añade nuevas variables derivadas sin modificar el original


    # Resumen por sexo y banda de edad
    # - groupby: define estratos poblacionales
    # - agg: calcula métricas clave


    # Conversión de proporción a porcentaje
    # - facilita interpretación


    # Redondeo general
    # - homogeneiza presentación


    # Vista rápida
    # - inspección inicial de resultados
    return


@app.cell
def _():
    # Transformación a formato largo
    # - melt: convierte columnas de comorbilidades en filas
    # - id_vars: variables que se mantienen (identificación y estratificación)
    # - value_vars: variables binarias de comorbilidad


    # Resumen y pivot
    # - groupby: agrupa por banda de edad y tipo de comorbilidad
    # - mean: proporción de presencia (True=1, False=0)
    # - mul(100): convierte a porcentaje
    # - pivot: reorganiza a formato ancho (tabla tipo heatmap)


    # Resultado final
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 9) Guardado de outputs

    Un cierre útil para la clase es dejar salidas listas para reutilización:

    - tablas en CSV,
    - múltiples hojas en Excel,
    - objetos Python serializados con `pickle`.

    No es solo “guardar archivos”. Es **hacer reproducible el trabajo analítico**.
    """)
    return


@app.cell
def _():
    # Pasar de formato ancho a formato largo
    # - melt: convierte varias columnas de comorbilidades en una sola columna de nombres
    # - esto facilita resumir y comparar múltiples condiciones con la misma estructura


    # Resumir prevalencia por banda de edad y comorbilidad
    # - groupby: forma combinaciones de grupo de edad + comorbilidad
    # - mean: en variables binarias, equivale a proporción
    # - mul(100): convierte a porcentaje
    # - pivot: reorganiza la tabla para que cada comorbilidad quede en su propia columna


    # Mostrar resultado final
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 10) Cierre

    ### Qué se repasa realmente con este notebook

    - organización de imports,
    - uso funcional de una clase simple,
    - vectorización con NumPy,
    - inspección y transformación con pandas,
    - lectura crítica del diccionario de datos,
    - limpieza reproducible de columnas problemáticas,
    - validación de plausibilidad,
    - resúmenes con `groupby`, `agg`, `merge` y `pivot_table`,
    - y persistencia de outputs.
    """)
    return


if __name__ == "__main__":
    app.run()
