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
    # Semana 2 · Lección 1A
    ## Encapsulación de procesamiento en clases (Pandas + POO)

    **Idea central:** cuando un flujo de limpieza y resumen empieza a crecer, conviene **encapsularlo dentro de una clase**.

    Esto permite:

    - mantener un **estado** claro,
    - centralizar validaciones,
    - exponer una interfaz más limpia,
    - y reducir errores al reutilizar el mismo flujo.

    En esta sesión trabajaremos con un dataset sintético de consultas ambulatorias y medidas antropométricas para construir un pipeline encapsulado que permita:

    1. validar y limpiar datos,
    2. derivar nuevas variables,
    3. resumir resultados,
    4. y generar salidas formales listas para reporte.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 1) ¿Por qué encapsular un flujo de pandas en una clase?

    Cuando trabajas con pandas, es común empezar con unas pocas transformaciones sueltas.

    Por ejemplo:

    - convertir tipos,
    - filtrar filas inválidas,
    - crear una nueva columna,
    - resumir por grupos.

    Pero a medida que el flujo crece, empiezan a aparecer problemas frecuentes:

    - duplicación de lógica,
    - columnas repetidas escritas a mano,
    - validaciones dispersas,
    - dificultad para saber en qué estado está el DataFrame,
    - errores silenciosos difíciles de rastrear.

    La encapsulación con una clase ayuda a resolver esto porque permite reunir en un solo objeto:

    - el **DataFrame de trabajo**,
    - la **configuración del pipeline**,
    - y los **métodos** que transforman o validan los datos.

    La clase actúa como un contenedor del flujo completo.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 2) Dataset sintético: consultas ambulatorias y antropometría

    Trabajaremos con un dataset pequeño de ejemplo donde cada fila representa una consulta ambulatoria.

    Las variables son:

    - `patient_id`: identificador del paciente
    - `sex`: sexo reportado
    - `age`: edad en años
    - `weight_kg`: peso
    - `height_m`: talla
    - `visit_type`: tipo de consulta
    - `sbp`: presión arterial sistólica

    ### Propósito didáctico

    Este dataset incluye algunos valores problemáticos de forma intencional, por ejemplo:

    - números guardados como texto,
    - valores faltantes,
    - observaciones insuficientes para calcular IMC.

    La idea es que el pipeline encapsulado pueda encargarse de estas situaciones de forma controlada.
    """)
    return


@app.cell
def _():
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
    return (df_raw,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 3) Diseñar una clase que posea el DataFrame y el flujo

    Ahora construiremos una clase llamada `CohortProcessor`.

    La clase tendrá dos elementos principales:

    ### Estado

    La clase guardará internamente:

    - el DataFrame de trabajo,
    - y los nombres de columnas relevantes.

    ### Métodos

    La clase expondrá pequeñas acciones bien definidas, por ejemplo:

    - validar el esquema,
    - convertir tipos,
    - filtrar observaciones inválidas,
    - calcular IMC,
    - crear grupos etarios,
    - generar resúmenes,
    - construir tablas tipo pivot.

    La regla didáctica será esta:

    > **cada método hace una sola cosa bien**.

    Después, el flujo completo se construye encadenando métodos.
    """)
    return


@app.cell
def _():
    class CohortProcessor:
        """
        Procesador mínimo de cohortes para un dataset de salud.
        Encapsula validación, limpieza, ingeniería de variables y resúmenes.
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
            # Guardamos los nombres de columnas como configuración del procesador
            self.patient_id_col = patient_id_col
            self.sex_col = sex_col
            self.age_col = age_col
            self.weight_col = weight_col
            self.height_col = height_col
            self.visit_type_col = visit_type_col
            self.sbp_col = sbp_col

            # Trabajamos sobre una copia para no modificar accidentalmente el original
            self.df = df.copy()

        def validate_schema(self) -> "CohortProcessor":
            # Verificamos que existan todas las columnas requeridas
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
            # Convertimos columnas numéricas; errores pasan a NaN
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

            # Normalizamos el texto de sexo de forma defensiva
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
            # Conservamos solo filas con antropometría disponible y plausible
            mask = self.df[self.height_col].between(
                min_height_m, max_height_m, inclusive="both"
            ) & self.df[self.weight_col].between(
                min_weight_kg, max_weight_kg, inclusive="both"
            )

            self.df = self.df.loc[mask].reset_index(drop=True)
            return self

        def add_bmi(self, bmi_col: str = "bmi") -> "CohortProcessor":
            # Calculamos IMC como variable derivada
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
            # Creamos una variable categórica de grupo etario
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
            # Resumen descriptivo agrupado por sexo y grupo etario
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
            # Tabla tipo pivot con distribución de tipo de visita
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
    return (CohortProcessor,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 4) Ejecutar un pipeline mínimo encapsulado

    Una vez definida la clase, podemos usarla para ejecutar un flujo completo de procesamiento.

    La secuencia será:

    1. validar esquema,
    2. convertir tipos,
    3. filtrar antropometría inválida,
    4. calcular IMC,
    5. crear grupo etario.

    Observa que ahora el pipeline se lee como una serie de pasos ordenados y con nombres claros.
    """)
    return


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
    return (processor,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Una vez el pipeline básico ha corrido, el objeto ya contiene un `DataFrame` limpio en su estado interno.

    Además, puede producir salidas formales mediante métodos de resumen.
    """)
    return


@app.cell
def _(processor):
    summary = processor.summarize_by_sex_age()
    summary
    return


@app.cell
def _(processor):
    prevalence_like = processor.prevalence_table_visit_type()
    prevalence_like
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 5) Encapsulación y contratos del pipeline

    Cuando un flujo de limpieza se vuelve más serio, no basta con transformar datos.

    También necesitamos **garantizar ciertas condiciones**.

    Por ejemplo:

    - que existan las columnas esperadas,
    - que ciertas variables estén en rangos plausibles,
    - que las categorías sean consistentes,
    - que el resultado de una transformación tenga sentido.

    Una forma útil de pensar estos chequeos es como **contratos del pipeline**.

    Los métodos de validación permiten detectar errores temprano y hacer el flujo más confiable.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto 1 — Validar rango plausible de IMC

    **Dominio:** control de calidad de variables derivadas

    En este reto agregarás un nuevo método a la clase para validar que los valores de IMC calculados estén dentro de un rango razonable.

    La idea no es modificar el DataFrame, sino verificar una condición y fallar de forma explícita si esta no se cumple.

    Antes de programar, piensa:

    - qué columna contiene la variable que debes validar,
    - cómo expresar un rango plausible en pandas,
    - y qué condición debe cumplirse para que el método pase sin error.
    """)
    return


@app.cell
def _(CohortProcessor, df_raw):
    # === TU TURNO (EDITA ESTA CELDA) ===
    # Implementa el método en la clase y luego úsalo aquí.

    processor_mr1 = (
        CohortProcessor(df_raw)
        .validate_schema()
        .coerce_types()
        .drop_invalid_anthropometrics()
        .add_bmi()
        .add_age_group()
    )

    # TODO: llamar aquí el método que implementes
    # Ejemplo esperado:
    # processor_mr1.assert_bmi_plausible(...)

    try:   
        assert hasattr(processor_mr1, "assert_bmi_plausible"), (
        "Define `assert_bmi_plausible()` en la clase."
    )
    except AssertionError as e:
        print(str(e))
    processor_mr1.df
    return (processor_mr1,)


@app.cell(hide_code=True)
def _():
    _tip_content = TipContent(
        items_raw=[
            r"""
    <Identificar la variable>
    Este método no debe recalcular el IMC, sino trabajar sobre la columna que ya fue creada previamente.

    Primero localiza correctamente esa columna dentro del DataFrame de trabajo.
    """,
            r"""
    <Construcción de la validación>
    Piensa cómo expresar en pandas que todos los valores deben caer dentro de un intervalo razonable.

    Puedes empezar construyendo una máscara booleana.
    """,
            r"""
    <Comportamiento esperado>
    El método no debe limpiar ni modificar filas.

    Su única responsabilidad es verificar una condición y lanzar un error si encuentra valores fuera del rango.
    """,
            r"""
    <solucion>

    ```python
    def assert_bmi_plausible(
        self,
        bmi_col: str = "bmi",
        min_bmi: float = 10.0,
        max_bmi: float = 80.0,
    ) -> "CohortProcessor":
        mask = self.df[bmi_col].between(min_bmi, max_bmi, inclusive="both")
        assert mask.all(), "Se encontraron valores de IMC fuera del rango plausible."
        return self
    ```
    """,
        ]
    )

    _tip_content.render()
    return


@app.cell(hide_code=True)
def _(processor_mr1):
    _test_content = TestContent(
        items_raw=[
            r"""
    <Existencia del método>
    Verifica que el método haya sido agregado a la clase.

    ```python
    assert hasattr(processor_mr1, "assert_bmi_plausible"), (
        "Debes definir `assert_bmi_plausible()` en la clase."
    )
    print("Método definido correctamente.")
    ```
    """,
            r"""
    <Columna necesaria>
    Verifica que el DataFrame ya contenga la columna de IMC antes de validar.

    ```python
    assert "bmi" in processor_mr1.df.columns, (
        "La columna `bmi` debe existir antes de aplicar la validación."
    )
    print("Columna de IMC disponible.")
    ```
    """,
            r"""
    <Rango plausible>
    Verifica que todos los IMC actuales queden dentro del rango esperado.

    ```python
    mask = processor_mr1.df["bmi"].between(10.0, 80.0, inclusive="both")
    assert mask.all(), "Hay valores de IMC fuera del rango plausible esperado."
    print("Rango plausible correcto.")
    ```
    """,
        ],
        namespace=globals(),
    )

    processor_mr1
    _test_content.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto 2 — Estandarizar categorías de sexo

    **Dominio:** control de calidad de variables categóricas

    En datos reales, una misma categoría puede aparecer escrita de varias maneras.

    Por ejemplo:

    - `f`
    - `female`
    - `FEMALE`
    - `m`
    - `male`

    En este reto crearás un método que:

    - normalice el texto,
    - estandarice valores comunes,
    - y valide que el resultado final quede dentro de las categorías esperadas.

    Antes de programar, piensa:

    - qué transformaciones de texto conviene aplicar primero,
    - cómo definir un mapeo de valores equivalentes,
    - y cómo verificar que no quedaron categorías inesperadas.
    """)
    return


@app.cell(hide_code=True)
def _():
    _tip_content = TipContent(
        items_raw=[
            r"""
    <Normalización inicial>
    Antes de reemplazar categorías, conviene limpiar el texto.

    Piensa en operaciones como convertir a string, quitar espacios y pasar a minúsculas.
    """,
            r"""
    <Estandarización>
    Una vez normalizados los valores, puedes mapear variantes frecuentes hacia un conjunto reducido de categorías.

    Un diccionario de reemplazo suele ser suficiente para esta tarea.
    """,
            r"""
    <Validación final>
    Después de estandarizar, el método debe verificar que no sobrevivan valores inesperados.

    La validación debe hacerse sobre el conjunto final de categorías permitidas.
    """,
            r"""
    <solucion>

    ```python
    def standardize_sex(
        self,
        allowed: set[str] = {"female", "male"},
    ) -> "CohortProcessor":
        self.df[self.sex_col] = (
            self.df[self.sex_col].astype(str).str.strip().str.lower()
        )

        self.df[self.sex_col] = self.df[self.sex_col].replace(
            {
                "f": "female",
                "female": "female",
                "m": "male",
                "male": "male",
            }
        )

        assert self.df[self.sex_col].isin(allowed).all(), (
            "Se encontraron categorías de sexo no permitidas."
        )
        return self
    ```
    """,
        ]
    )

    _tip_content.render()
    return


@app.cell
def _(CohortProcessor, df_raw, processor_mr1):
    # === TU TURNO (EDITA ESTA CELDA) ===
    # Implementa standardize_sex() en la clase y úsalo aquí.

    processor_mr2 = (
        CohortProcessor(df_raw)
        .validate_schema()
        .coerce_types()
        # TODO: agregar aquí la llamada a standardize_sex(...)
        .drop_invalid_anthropometrics()
        .add_bmi()
        .add_age_group()
    )


    try:   
        assert hasattr(processor_mr2, "standardize_sex"), (
        "Define `standardize_sex()` en la clase."
    )
    except AssertionError as e:
        print(str(e))
    
    processor_mr1.df

    processor_mr2.df[[processor_mr2.patient_id_col, processor_mr2.sex_col]].head()
    return (processor_mr2,)


@app.cell(hide_code=True)
def _(processor_mr2):
    _test_content = TestContent(
        items_raw=[
            r"""
    <Existencia del método>
    Verifica que el método haya sido agregado a la clase.

    ```python
    assert hasattr(processor_mr2, "standardize_sex"), (
        "Debes definir `standardize_sex()` en la clase."
    )
    print("Método definido correctamente.")
    ```
    """,
            r"""
    <Categorías permitidas>
    Verifica que la columna final de sexo solo contenga valores esperados.

    ```python
    valores = set(processor_mr2.df[processor_mr2.sex_col].unique())
    assert valores.issubset({"female", "male"}), (
        "La columna de sexo contiene valores no permitidos."
    )
    print("Categorías correctas.")
    ```
    """,
            r"""
    <Tipo de salida>
    Verifica que la estandarización haya quedado reflejada dentro del DataFrame del objeto.

    ```python
    assert processor_mr2.sex_col in processor_mr2.df.columns, (
        "La columna de sexo debe seguir existiendo en el DataFrame."
    )
    print("Salida consistente dentro del objeto.")
    ```
    """,
        ],
        namespace=globals(),
    )

    processor_mr2
    _test_content.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 6) Salidas formales del pipeline

    Una ventaja importante de encapsular un flujo es que los productos del análisis también quedan organizados.

    Por ejemplo, dentro del mismo objeto puedes distinguir entre:

    - el **DataFrame limpio** como producto intermedio,
    - y los **resúmenes finales** como productos listos para reporte.

    Esto hace que el pipeline sea más reutilizable y más fácil de explicar.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto 3 — Crear un método `run_basic_report()`

    **Dominio:** orquestación de pipelines reproducibles

    En este reto final implementarás un método que funcione como orquestador del flujo básico.

    La idea es que un solo método:

    1. ejecute el pipeline mínimo,
    2. produzca varias salidas,
    3. y las devuelva en una estructura ordenada.

    Este ejercicio integra:

    - encapsulación,
    - composición de métodos,
    - y diseño de outputs estructurados.

    Antes de programar, piensa:

    - qué pasos deben ejecutarse en orden,
    - qué resultados quieres conservar,
    - y cómo representarlos de forma clara para el usuario del pipeline.
    """)
    return


@app.cell(hide_code=True)
def _():
    _tip_content = TipContent(
        items_raw=[
            r"""
    <Método orquestador>
    Este método no necesita inventar lógica nueva.

    Su responsabilidad principal es coordinar otros métodos que ya existen dentro de la misma clase.
    """,
            r"""
    <Secuencia de ejecución>
    Piensa en el orden natural del pipeline: primero limpieza y validación, después variables derivadas, y finalmente resúmenes.

    Mantener ese orden es parte importante del diseño del método.
    """,
            r"""
    <Estructura del resultado>
    El método debe devolver varias salidas al mismo tiempo.

    Un diccionario puede ser útil cuando quieres devolver objetos con nombres explícitos.
    """,
            r"""
    <solucion>

    ```python
    def run_basic_report(self) -> dict:
        self.validate_schema()
        self.coerce_types()
        self.drop_invalid_anthropometrics()
        self.add_bmi()
        self.add_age_group()

        return {
            "clean_df": self.df,
            "summary": self.summarize_by_sex_age(),
            "prevalence_like": self.prevalence_table_visit_type(),
        }
    ```
    """,
        ]
    )

    _tip_content.render()
    return


@app.cell
def _(CohortProcessor, df_raw):
    # === TU TURNO (EDITA ESTA CELDA) ===
    # Implementa run_basic_report() en la clase y úsalo aquí.

    processor_mr3 = CohortProcessor(df_raw)

    # TODO: llamar aquí el método implementado
    # Ejemplo esperado:
    # report = processor_mr3.run_basic_report()


    try:   
        assert hasattr(processor_mr3, "run_basic_report"), (
            "Define `run_basic_report()` en la clase."
        )
    except AssertionError as e:
        print(str(e))

    # Cuando lo implementes, deberías poder inspeccionar:
    # report["clean_df"], report["summary"], report["prevalence_like"]
    return (processor_mr3,)


@app.cell(hide_code=True)
def _(processor_mr3):
    _test_content = TestContent(
        items_raw=[
            r"""
    <Existencia del método>
    Verifica que el método haya sido agregado a la clase.

    ```python
    assert hasattr(processor_mr3, "run_basic_report"), (
        "Debes definir `run_basic_report()` en la clase."
    )
    print("Método definido correctamente.")
    ```
    """,
            r"""
    <Estructura del reporte>
    Una vez implementado, el método debe devolver una estructura con tres productos bien identificados.

    ```python
    report = processor_mr3.run_basic_report()

    assert isinstance(report, dict), "`run_basic_report()` debe devolver un diccionario."
    assert set(report.keys()) == {"clean_df", "summary", "prevalence_like"}, (
        "Las claves esperadas son: clean_df, summary, prevalence_like."
    )
    print("Estructura del reporte correcta.")
    ```
    """,
            r"""
    <Tipo de cada salida>
    Verifica que cada producto del reporte tenga tipo tabular.

    ```python
    report = processor_mr3.run_basic_report()

    assert isinstance(report["clean_df"], pd.DataFrame), "`clean_df` debe ser un DataFrame."
    assert isinstance(report["summary"], pd.DataFrame), "`summary` debe ser un DataFrame."
    assert isinstance(report["prevalence_like"], pd.DataFrame), (
        "`prevalence_like` debe ser un DataFrame."
    )
    print("Tipos de salida correctos.")
    ```
    """,
        ],
        namespace=globals(),
    )

    processor_mr3
    _test_content.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Cierre: qué deberías poder explicar al final

    Al terminar esta lección, deberías poder explicar con claridad:

    - por qué una clase es útil para encapsular un flujo de pandas,
    - cómo distinguir entre estado del objeto y métodos del pipeline,
    - cómo diseñar métodos con responsabilidades claras,
    - cómo usar validaciones como contratos del procesamiento,
    - y cómo organizar salidas formales a partir de un flujo reproducible.

    La idea más importante no es solo “usar una clase”.

    Es entender que una clase puede convertirse en el **contenedor conceptual del análisis**:

    **datos + reglas + transformaciones + salidas**
    """)
    return


if __name__ == "__main__":
    app.run()
