# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "numpy==2.4.2",
#     "pandas==3.0.1",
#     "requests==2.32.5",
#     "pytest==9.0.2",
# ]
# ///

import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")

with app.setup(hide_code=True):
    import marimo as mo
    import numpy as np
    import pandas as pd
    from setup import TipContent, TestContent


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Semana 2 · Lección A2
    ## Diseño de un procesador de dataset (`DatasetProcessor`)

    **Idea central:** pasar de ejecutar pasos aislados en distintas celdas a construir un **objeto** que encapsula un flujo mínimo de procesamiento y produce **salidas estructuradas**.

    En esta sesión construiremos una clase `DatasetProcessor` que:

    1. recibe un `DataFrame`,
    2. valida condiciones mínimas,
    3. aplica una limpieza reproducible,
    4. calcula métricas agregadas,
    5. y devuelve resultados con una estructura estable.

    **Contexto aplicado:** trabajaremos con un dataset sintético de tamizaje cardiometabólico en atención primaria.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 1) Dataset sintético: tamizaje cardiometabólico

    Vamos a trabajar con una tabla pequeña de ejemplo que contiene variables frecuentes en tamizaje clínico y epidemiológico:

    - `patient_id`: identificador del paciente
    - `age`: edad
    - `sex`: sexo biológico reportado
    - `bmi`: índice de masa corporal
    - `sbp`: presión sistólica
    - `smoker`: fumador actual (0/1)
    - `hba1c`: hemoglobina glicosilada

    El objetivo del dataset no es representar una cohorte real, sino servir como base para practicar diseño de pipelines.

    Además, introduciremos intencionalmente algunos problemas comunes de calidad:

    - valores faltantes,
    - valores extremos,
    - y posibles inconsistencias numéricas.
    """)
    return


@app.cell
def _():
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

    # Introducimos algunos problemas comunes de calidad
    df_raw.loc[rng.choice(n, size=18, replace=False), "bmi"] = np.nan
    df_raw.loc[rng.choice(n, size=10, replace=False), "sbp"] = np.nan
    df_raw.loc[rng.choice(n, size=6, replace=False), "hba1c"] = np.nan

    # Introducimos algunos outliers de forma intencional
    df_raw.loc[rng.choice(n, size=3, replace=False), "bmi"] = [6.0, 65.0, 80.0]
    df_raw.loc[rng.choice(n, size=3, replace=False), "sbp"] = [60.0, 240.0, 260.0]
    df_raw.loc[rng.choice(n, size=3, replace=False), "hba1c"] = [3.2, 14.5, 18.0]

    df_raw.head()
    return (df_raw,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 2) ¿Qué significa “procesar un dataset”?

    Procesar un dataset no es simplemente “hacer operaciones”.

    En términos formales, significa aplicar una secuencia ordenada de pasos para convertir una tabla original en una versión más:

    - **coherente**,
    - **limpia**,
    - **reutilizable**,
    - y **auditable**.

    En esta lección nos quedaremos con una secuencia mínima:

    **validar → limpiar → resumir**

    La pregunta importante es esta:

    > ¿Dónde vive ese flujo?

    En lugar de repartirlo en muchas celdas, vamos a encapsularlo dentro de un objeto.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 3) Contrato mínimo de un `DatasetProcessor`

    Un procesador bien diseñado define con claridad **qué entra** y **qué sale**.

    ### Entrada
    - una tabla (`pd.DataFrame`)
    - un conjunto de reglas mínimas
    - decisiones explícitas de limpieza

    ### Salida
    - una versión limpia de la tabla
    - un conjunto de métricas estructuradas
    - una tabla resumen pequeña

    Esta idea de contrato es importante porque hace que el procesador sea:

    - más fácil de explicar,
    - más fácil de reutilizar,
    - y más fácil de comprobar.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto 1 — Reglas de validación mínimas

    **Dominio:** control de calidad tabular

    Antes de limpiar o resumir una tabla, conviene verificar que cumpla unas condiciones mínimas.

    En este reto construirás una función `validate_schema(df)` que actúe como verificación inicial del dataset.

    La idea no es transformar la tabla, sino confirmar que tiene la estructura esperada.

    Antes de programar, piensa:

    - qué columnas deben existir obligatoriamente,
    - qué variable debe ser numérica y estar en un rango razonable,
    - y cómo validar categorías permitidas sin dejar que los faltantes rompan la lógica.
    """)
    return


@app.cell
def _(df_raw):
    def validate_schema(df: pd.DataFrame) -> None:
        """
        Valida condiciones mínimas de esquema para un dataset de tamizaje.

        Parameters
        ----------
        df:
            DataFrame de entrada.

        Returns
        -------
        None

        Raises
        ------
        AssertionError
            Si alguna validación falla.
        """
        required_cols = {"patient_id", "age", "sex", "bmi", "sbp", "smoker", "hba1c"}
        assert required_cols.issubset(set(df.columns)), (
            f"Missing required columns: {sorted(required_cols - set(df.columns))}"
        )

        # Validación de edad
        assert pd.api.types.is_numeric_dtype(df["age"]), "Column 'age' must be numeric."
        age_ok = df["age"].dropna().between(0, 120).all()
        assert age_ok, "Column 'age' must be within [0, 120]."

        # Validación de sexo
        sex_ok = df["sex"].dropna().isin({"female", "male"}).all()
        assert sex_ok, "Column 'sex' must be 'female' or 'male'."

        return None

    validate_schema(df_raw)
    return (validate_schema,)


@app.cell(hide_code=True)
def _():
    _tip_content = TipContent(
        items_raw=[
            r"""
    <Validación estructural>
    El primer paso es comprobar que el DataFrame contenga todas las columnas necesarias.

    Piensa cómo comparar un conjunto de nombres requeridos con las columnas realmente disponibles.
    """,
            r"""
    <Rangos numéricos>
    Para la edad no basta con que la columna exista.

    También debe ser numérica y permanecer dentro de un rango razonable.
    """,
            r"""
    <Categorías permitidas>
    La validación de una variable categórica debe ignorar faltantes y concentrarse solo en los valores observados.

    Esto te permite revisar si todos pertenecen al conjunto esperado.
    """,
            r"""
    <solucion>

    ```python
    def validate_schema(df: pd.DataFrame) -> None:
        required_cols = {"patient_id", "age", "sex", "bmi", "sbp", "smoker", "hba1c"}
        assert required_cols.issubset(set(df.columns)), (
            f"Missing required columns: {sorted(required_cols - set(df.columns))}"
        )

        assert pd.api.types.is_numeric_dtype(df["age"]), "Column 'age' must be numeric."
        age_ok = df["age"].dropna().between(0, 120).all()
        assert age_ok, "Column 'age' must be within [0, 120]."

        sex_ok = df["sex"].dropna().isin({"female", "male"}).all()
        assert sex_ok, "Column 'sex' must be 'female' or 'male'."

        return None
    ```
    """,
        ]
    )

    _tip_content.render()
    return


@app.cell(hide_code=True)
def _(validate_schema):
    _test_content = TestContent(
        items_raw=[
            r"""
    <Salida esperada>
    Verifica que la función pueda ejecutarse sin devolver un valor distinto de `None`.

    ```python
    resultado = validate_schema(df_raw)
    assert resultado is None, "La función debe retornar `None` si todo está bien."
    print("Salida correcta.")
    ```
    """,
            r"""
    <Columnas requeridas>
    Verifica que el dataset de ejemplo sí cumpla la validación estructural.

    ```python
    required_cols = {"patient_id", "age", "sex", "bmi", "sbp", "smoker", "hba1c"}
    assert required_cols.issubset(set(df_raw.columns)), (
        "Faltan columnas requeridas en el dataset."
    )
    print("Esquema básico correcto.")
    ```
    """,
            r"""
    <Coherencia de edad y sexo>
    Verifica que las dos validaciones principales sean compatibles con el dataset de ejemplo.

    ```python
    assert pd.api.types.is_numeric_dtype(df_raw["age"]), "La edad debe ser numérica."
    assert df_raw["age"].dropna().between(0, 120).all(), "La edad debe estar en [0, 120]."
    assert df_raw["sex"].dropna().isin({"female", "male"}).all(), (
        "La columna `sex` debe contener solo categorías permitidas."
    )
    print("Validaciones semánticas correctas.")
    ```
    """,
        ],
        namespace=globals(),
    )

    validate_schema
    _test_content.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 4) Limpieza mínima del dataset

    Una vez validada la estructura, el siguiente paso es limpiar la tabla.

    En esta lección aplicaremos un esquema muy simple y explícito:

    - convertir columnas numéricas,
    - transformar valores fuera de plausibilidad en `NaN`,
    - imputar faltantes con la mediana.

    ### Rango plausible simplificado

    - BMI: [12, 60]
    - SBP: [70, 220]
    - HbA1c: [3.5, 15]

    La lógica aquí no busca ser clínica en detalle, sino mostrar cómo convertir reglas explícitas en código reproducible.
    """)
    return


@app.cell
def _(df_raw):
    def clean_screening_data(df: pd.DataFrame) -> pd.DataFrame:
        """
        Limpia un dataset de tamizaje cardiometabólico usando reglas simples.

        Steps
        -----
        1) Copiar el dataframe.
        2) Convertir columnas numéricas.
        3) Reemplazar valores implausibles por NaN.
        4) Imputar faltantes con la mediana.

        Returns
        -------
        pd.DataFrame
            Dataset limpio.
        """
        df_clean = df.copy()

        # Convertimos columnas numéricas de forma robusta
        numeric_cols = ["age", "bmi", "sbp", "smoker", "hba1c"]
        for col in numeric_cols:
            df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")

        # Reemplazamos valores implausibles por NA
        df_clean.loc[~df_clean["bmi"].between(12, 60), "bmi"] = pd.NA
        df_clean.loc[~df_clean["sbp"].between(70, 220), "sbp"] = pd.NA
        df_clean.loc[~df_clean["hba1c"].between(3.5, 15), "hba1c"] = pd.NA

        # Imputación simple por mediana
        for col in ["bmi", "sbp", "hba1c"]:
            med = df_clean[col].median(skipna=True)
            df_clean[col] = df_clean[col].fillna(med)

        # Contratos mínimos posteriores a la limpieza
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
    mo.md(r"""
    ## 5) Métricas estructuradas: de tabla a diccionario

    Un procesador de datos no solo limpia tablas.

    También debe producir salidas estables y fáciles de reutilizar.

    Una opción útil es construir un **diccionario de métricas**, donde cada entrada tenga un significado claro.

    En este ejemplo construiremos dos métricas didácticas:

    - prevalencia de hipertensión probable por sexo,
    - prevalencia de alto riesgo cardiometabólico por grupo etario.

    Esta idea es importante porque obliga a pensar no solo en cálculos, sino también en **cómo organizar el resultado**.
    """)
    return


@app.cell
def _(df_clean):
    def compute_metrics(df: pd.DataFrame) -> dict:
        """
        Calcula métricas básicas para un dataset de tamizaje.

        Returns
        -------
        dict
            Diccionario con:
            - "n_rows"
            - "hypertension_prev_by_sex"
            - "high_risk_prev_by_age_group"
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
    return (compute_metrics,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto 2 — Tabla resumen con `groupby` + `agg`

    **Dominio:** resumen descriptivo tabular

    En este reto construirás una tabla resumen por sexo.

    El objetivo es transformar una tabla limpia en una salida pequeña y estructurada, con métricas agregadas fáciles de interpretar.

    La tabla final debe incluir:

    - conteo,
    - promedios de variables numéricas,
    - y prevalencia de tabaquismo.

    Antes de programar, piensa:

    - qué variable define los grupos,
    - qué columnas deben resumirse,
    - y cómo nombrar el resultado para que sea claro.
    """)
    return


@app.cell
def _(df_clean):
    def build_summary_table(df: pd.DataFrame) -> pd.DataFrame:
        """
        Construye una tabla resumen compacta por sexo.

        Returns
        -------
        pd.DataFrame
            Columnas: n, mean_bmi, mean_sbp, mean_hba1c, smoker_prev
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

        expected = {"sex", "n", "mean_bmi", "mean_sbp", "mean_hba1c", "smoker_prev"}
        assert expected.issubset(set(summary.columns))
        return summary

    summary_table = build_summary_table(df_clean)
    summary_table
    return build_summary_table, summary_table


@app.cell(hide_code=True)
def _():
    _tip_content = TipContent(
        items_raw=[
            r"""
    <Variable de agrupación>
    La tabla final debe tener una fila por categoría de sexo.

    Eso define directamente cómo debe comenzar el `groupby`.
    """,
            r"""
    <Métricas agregadas>
    Debes producir varias columnas resumen en un solo paso.

    Piensa qué métrica corresponde a cada variable y qué nombres debe tener cada salida.
    """,
            r"""
    <Prevalencia binaria>
    Si una variable está codificada como 0 y 1, su promedio puede interpretarse como proporción.

    Esa idea es especialmente útil para variables de presencia/ausencia.
    """,
            r"""
    <solucion>

    ```python
    def build_summary_table(df: pd.DataFrame) -> pd.DataFrame:
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
        return summary
    ```
    """,
        ]
    )

    _tip_content.render()
    return


@app.cell(hide_code=True)
def _(summary_table):
    _test_content = TestContent(
        items_raw=[
            r"""
    <Estructura básica>
    Verifica que la tabla resumen sea un DataFrame con la columna de agrupación esperada.

    ```python
    assert isinstance(summary_table, pd.DataFrame), (
        "`summary_table` debe ser un DataFrame."
    )
    assert "sex" in summary_table.columns, (
        "La columna `sex` debe existir en la tabla resumen."
    )
    print("Estructura básica correcta.")
    ```
    """,
            r"""
    <Columnas requeridas>
    Verifica que todas las columnas resumen estén presentes.

    ```python
    expected = {"sex", "n", "mean_bmi", "mean_sbp", "mean_hba1c", "smoker_prev"}
    assert expected.issubset(set(summary_table.columns)), (
        "Faltan columnas requeridas en la tabla resumen."
    )
    print("Columnas requeridas correctas.")
    ```
    """,
            r"""
    <Coherencia del conteo>
    Verifica que la suma de `n` coincida con el número total de filas del dataset limpio.

    ```python
    assert int(summary_table["n"].sum()) == int(df_clean.shape[0]), (
        "La suma de `n` debe coincidir con el número total de filas."
    )
    print("Conteo total consistente.")
    ```
    """,
        ],
        namespace=globals(),
    )

    summary_table
    _test_content.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 6) Implementación de `DatasetProcessor`

    Ahora convertiremos el flujo completo en un objeto.

    La idea es encapsular cuatro responsabilidades principales:

    - validar,
    - limpiar,
    - calcular métricas,
    - y construir una tabla resumen.

    Además, definiremos un método `run()` que orqueste todo en el orden correcto.

    Este tipo de diseño es útil porque obliga a separar responsabilidades y a hacer explícito el estado interno del procesador.
    """)
    return


@app.cell
def _(
    build_summary_table,
    clean_screening_data,
    compute_metrics,
    df_raw,
    validate_schema,
):
    class DatasetProcessor:
        """
        Procesador mínimo de dataset para tamizaje cardiometabólico.

        Implementa un pipeline simple:
        validate -> clean -> compute -> summary

        Attributes
        ----------
        data_raw:
            DataFrame original.
        data_clean:
            DataFrame limpio.
        metrics:
            Diccionario de métricas.
        summary_table:
            Tabla resumen final.
        """

        def __init__(self, data_raw: pd.DataFrame):
            # Guardamos una copia del dataset original
            self.data_raw = data_raw.copy()
            self.data_clean: pd.DataFrame | None = None
            self.metrics: dict | None = None
            self.summary_table: pd.DataFrame | None = None

        def validate(self) -> None:
            # Validamos la estructura de entrada
            validate_schema(self.data_raw)

        def clean(self) -> pd.DataFrame:
            # Aplicamos la limpieza reproducible
            self.data_clean = clean_screening_data(self.data_raw)
            return self.data_clean

        def compute(self) -> dict:
            # Calculamos métricas a partir del dataset limpio
            assert self.data_clean is not None, "Run clean() before compute()."
            self.metrics = compute_metrics(self.data_clean)
            return self.metrics

        def summary(self) -> pd.DataFrame:
            # Construimos la tabla resumen a partir del dataset limpio
            assert self.data_clean is not None, "Run clean() before summary()."
            self.summary_table = build_summary_table(self.data_clean)
            return self.summary_table

        def run(self) -> dict:
            """
            Ejecuta el pipeline completo y devuelve salidas estructuradas.
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
    return (DatasetProcessor,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 7) Extender el procesador sin romper el contrato

    Una vez tienes un procesador funcional, una de las ventajas del diseño orientado a objetos es que puedes extenderlo.

    Pero hacerlo bien significa **agregar comportamiento nuevo sin romper el contrato principal**.

    En este contexto, extender significa añadir nuevos métodos que:

    - modifiquen la entrada,
    - preparen subconjuntos,
    - o ajusten el pipeline,

    sin alterar la lógica básica del objeto.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto 3 — Extender el procesador con `filter_adults()`

    **Dominio:** preparación de subconjuntos analíticos

    En este reto crearás una versión extendida del procesador que permita filtrar la cohorte por edad mínima antes de ejecutar el pipeline.

    La idea es agregar un método nuevo, pero sin mezclar responsabilidades.

    El método debe:

    - filtrar la tabla original,
    - actualizar el estado interno,
    - y devolver el DataFrame filtrado.

    Después, el pipeline normal debe seguir funcionando sobre esa nueva entrada.

    Antes de programar, piensa:

    - qué atributo del objeto representa la fuente del pipeline,
    - qué debe cambiar para que `run()` use el dataset filtrado,
    - y por qué conviene que filtrar y ejecutar el pipeline sigan siendo acciones separadas.
    """)
    return


@app.cell
def _(DatasetProcessor, df_raw):
    class DatasetProcessorV2(DatasetProcessor):
        def filter_adults(self, min_age: int = 18):
            """
            Filtra los datos originales por una edad mínima.

            Parameters
            ----------
            min_age:
                Edad mínima a conservar.

            Returns
            -------
            pd.DataFrame
                DataFrame filtrado.
            """
            df_filt = self.data_raw[self.data_raw["age"] >= min_age].copy()
            self.data_raw = df_filt
            return df_filt

    proc2 = DatasetProcessorV2(df_raw)
    _df40 = proc2.filter_adults(min_age=40)
    out2 = proc2.run()

    assert out2["data_clean"]["age"].min() >= 40
    out2["summary_table"]
    return


@app.cell(hide_code=True)
def _():
    _tip_content = TipContent(
        items_raw=[
            r"""
    <Estado interno del objeto>
    El pipeline usa como entrada la tabla guardada en el propio objeto.

    Si quieres que el filtro afecte el procesamiento posterior, debes actualizar esa fuente interna.
    """,
            r"""
    <Separación de responsabilidades>
    Este método debe encargarse solo de filtrar.

    No conviene que ejecute automáticamente limpieza, métricas o resúmenes, porque eso mezclaría responsabilidades distintas.
    """,
            r"""
    <Compatibilidad con `run()`}
    El objetivo no es crear un pipeline nuevo, sino preparar la entrada para que el pipeline existente funcione sobre un subconjunto distinto.
    """,
            r"""
    <solucion>

    ```python
    class DatasetProcessorV2(DatasetProcessor):
        def filter_adults(self, min_age: int = 18):
            df_filt = self.data_raw[self.data_raw["age"] >= min_age].copy()
            self.data_raw = df_filt
            return df_filt
    ```
    """,
        ]
    )

    _tip_content.render()
    return


@app.cell(hide_code=True)
def _():
    _test_content = TestContent(
        items_raw=[
            r"""
    <Existencia del método>
    Verifica que la nueva versión del procesador tenga el método adicional.

    ```python
    proc_test = DatasetProcessorV2(df_raw)
    assert hasattr(proc_test, "filter_adults"), (
        "La clase extendida debe definir `filter_adults()`."
    )
    print("Método agregado correctamente.")
    ```
    """,
            r"""
    <Actualización de la entrada>
    Verifica que el filtro modifique la fuente del pipeline.

    ```python
    proc_test = DatasetProcessorV2(df_raw)
    proc_test.filter_adults(min_age=40)
    assert proc_test.data_raw["age"].min() >= 40, (
        "Después del filtro, `data_raw` debe contener solo adultos >= 40."
    )
    print("Estado interno actualizado correctamente.")
    ```
    """,
            r"""
    <Compatibilidad con el pipeline>
    Verifica que el pipeline completo funcione después del filtrado.

    ```python
    proc_test = DatasetProcessorV2(df_raw)
    proc_test.filter_adults(min_age=40)
    out_test = proc_test.run()

    assert out_test["data_clean"]["age"].min() >= 40, (
        "El pipeline debería ejecutarse sobre el subconjunto filtrado."
    )
    print("Compatibilidad con `run()` correcta.")
    ```
    """,
        ],
        namespace=globals(),
    )

    _test_content.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Cierre: checklist conceptual

    Al terminar esta lección, deberías poder explicar por qué una clase como `DatasetProcessor` es útil en análisis tabular.

    En particular, deberías reconocer que sirve para:

    - definir un contrato claro de entrada y salida,
    - centralizar validaciones y limpieza,
    - producir métricas con estructura estable,
    - organizar resúmenes reproducibles,
    - y extender el comportamiento sin perder coherencia.

    La idea más importante no es solo “usar clases”.

    Es entender que una clase puede convertirse en el contenedor lógico del flujo completo:

    **datos + reglas + transformaciones + salidas**
    """)
    return


if __name__ == "__main__":
    app.run()
