# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "numpy==2.4.2",
#     "pandas==2.3.0",
# ]
# ///

import marimo

__generated_with = "0.20.2"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import numpy as np
    import pandas as pd
    from pathlib import Path

    return mo, pd


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Semana 2 — Clase sincrónica

    **Enfoque:** repaso corto de Semana 1 + recorrido por los temas de la Semana 2 (muestras pequeñas, práctica guiada).

    **Contexto único:** ejemplos en salud y salud pública (datos clínico-sociales sintéticos).

    ---

    ## Agenda

    1) Repaso express (Semana 1): ejecución, variables, control de flujo, errores, funciones, bucles, estructuras básicas

    2) Semana 2:
    - (1) Módulos y librerías: `import`, alias, `from ... import ...`
    - (2) POO fundamentos: clase/objeto/atributo/método
    - (3) NumPy: arrays y vectorización
    - (4) pandas: Series/DataFrame y operaciones frecuentes
    - (5) pandas: `groupby`, `agg`, `merge`, `pivot_table`
    - (6) pandas (práctico): chequeos mínimos de calidad
    - (7) Diseño mínimo: `DatasetProcessor` (modularidad y reutilización)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Modelo de Programa y Ejecución

    Un programa es una secuencia ordenada de instrucciones que el intérprete ejecuta de arriba hacia abajo. Cada línea modifica el estado interno del programa antes de continuar con la siguiente.

    Conceptos clave:

    - Ejecución secuencial.
    - Estado del programa.
    - Determinismo.
    - Errores como parte del proceso.
    - Depuración sistemática.

    ---

    ## Ejemplo

    ```python
    print("Paso 1")
    x = 10
    y = x * 2
    print("Resultado:", y)
    ```

    Orden de ejecución:

    1. Se imprime "Paso 1".
    2. Se asigna 10 a `x`.
    3. Se calcula `x * 2`.
    4. Se imprime el resultado.

    La ejecución siempre respeta el orden, salvo que una estructura de control lo modifique.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Variables como Modelos de Memoria

    Una variable es un nombre que referencia un objeto en memoria. El valor no “vive dentro” del nombre; el nombre apunta al objeto.

    Tipos básicos:

    - `int`
    - `float`
    - `str`
    - `bool`

    Aspectos fundamentales:

    - `=` es asignación.
    - El tipo determina el comportamiento.
    - Python es dinámicamente tipado.

    ---

    ## Ejemplo

    ```python
    a = 5
    b = a
    a = 10

    print(a)  # 10
    print(b)  # 5
    ```

    `b` mantiene la referencia original al valor 5. Cambiar `a` no modifica `b`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Ejecución Condicional

    Las estructuras condicionales permiten modificar el flujo del programa según una expresión booleana.

    Estructura general:

    ```python
    if condicion:
        ...
    elif otra_condicion:
        ...
    else:
        ...
    ```

    Conceptos clave:

    - Expresiones booleanas.
    - Comparaciones.
    - Operadores lógicos.

    ---

    ## Ejemplo

    ```python
    edad = 20

    if edad >= 18:
        print("Mayor de edad")
    else:
        print("Menor de edad")
    ```

    La condición se evalúa primero; solo el bloque verdadero se ejecuta.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Secuencias

    Una secuencia es una colección ordenada de elementos.

    Tipos principales:

    ## `list`

    Esquema general:
    ```python
    my_list = [element1, element2, element3]
    ```
    Caracteristicas:
    - Son elementos mutables (pueden cambiar después de ser creadas).
    - Pueden contener elementos de diferentes tipos (números, cadenas, otras listas, etc.).
    - Permiten operaciones como agregar, eliminar o modificar elementos.
    - Pueden anidarse (listas dentro de listas).
    - Tienen métodos incorporados como `append()`, `remove()`, `sort()`, etc.

    ## `tuple`

    Esquema general:
    ```python
    my_tuple = (element1, element2, element3)
    ```

    Caracteristicas:
    - Son inmutables (no pueden cambiar después de ser creadas).
    - Pueden contener elementos de diferentes tipos.
    - Permiten operaciones de acceso pero no de modificación (no puedes agregar, eliminar o modificar elementos).
    - Pueden anidarse (tuplas dentro de tuplas).
    - No tienen métodos para modificar la tupla, pero sí métodos para contar elementos o encontrar índices.

    Propiedades conjuntas:

    - Indexación.
    - Slicing.
    - Iterabilidad.

    ---

    ## Ejemplo

    ```python
    numeros = [10, 20, 30, 40]

    print(numeros[0])     # 10
    print(numeros[1:3])   # [20, 30]

    numeros.append(50)
    print(numeros)
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Funciones

    Una función encapsula lógica reutilizable y promueve modularidad.

    ```python
    def function_name(parameters):
        # cuerpo de la función
        return result
    ```

    Conceptos clave:

    - Parámetros.
    - Argumentos.
    - Retorno.
    - Ámbito local.

    ---

    ## Ejemplo

    ```python
    def calcular_imc(peso, altura):
        return peso / (altura ** 2)

    imc = calcular_imc(70, 1.75)
    print(imc)
    ```

    La función recibe datos, procesa y devuelve un resultado.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Iteraciones

    Las iteraciones permiten repetir instrucciones bajo condiciones definidas.

    Tipos:

    - `for` (iteración sobre secuencias).
    - `while` (iteración condicional).

    Esquema general:
    ```python
    for variable in secuencia:
        # bloque de código a repetir

    while condición:
        # bloque de código a repetir
    ```
    ---

    ## Ejemplo

    ```python
    for i in range(5):
        print(i)
    ```

    ```python
    contador = 0
    while contador < 3:
        print(contador)
        contador += 1
    ```

    La condición de parada es esencial para evitar bucles infinitos.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Comprensiones

    Las comprensiones permiten construir colecciones de manera declarativa.

    Estructura:
    ```python
    [expresión for item in iterable if condición]
    ```

    Ventajas:

    - Sintaxis compacta.
    - Mayor expresividad.
    - Código más limpio cuando se usa correctamente.

    ---

    ## Ejemplo

    ```python
    cuadrados = [x**2 for x in range(6)]
    print(cuadrados)
    ```

    ```python
    pares = [x for x in range(10) if x % 2 == 0]
    print(pares)
    ```

    Se combinan iteración y condición en una sola expresión.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Diccionarios y Conjuntos

    ## Diccionarios

    Estructuras clave–valor ideales para datos estructurados.

    Estructura general:
    ```python
    my_dict = {
        "key1": value1,
        "key2": value2,
        ...
    }
    ```

    Caracteristicas:
    - acceso rápido por clave
    - no ordenados (hasta Python 3.7, ahora mantienen orden de inserción)
    - valores pueden ser de cualquier tipo (incluso otros diccionarios)
    - útiles para representar objetos, configuraciones, etc.
    - operaciones comunes: `dict.get()`, `dict.keys()`, `dict.values()`, `dict.items()`

    ## Conjuntos

    Colecciones no ordenadas sin duplicados.

    estructura general:
    ```python
    my_set = {element1, element2, ...}
    ```
    Caracteristicas:
    - no permiten elementos duplicados
    - operaciones matemáticas: unión, intersección, diferencia
    - útiles para eliminar duplicados, verificar pertenencia, operaciones de conjunto
    - operaciones comunes: `set.union()`, `set.intersection()`, `set.difference()`, `in` para pertenencia

    ---

    ## Ejemplo

    ```python
    persona = {
        "nombre": "Ana",
        "edad": 30
    }
    print(persona["nombre"]) #> 'Ana'
    ```

    ```python
    a = {1, 2, 3}
    b = {3, 4, 5}

    print(a.union(b))
    print(a.intersection(b))
    ```

    Los diccionarios organizan información; los conjuntos permiten operaciones matemáticas.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Pseudocódigo y Utilidades

    El pseudocódigo permite estructurar la lógica antes de programar.

    Ventajas:

    - Claridad conceptual.
    - Independencia del lenguaje.
    - Mejor planificación.

    ---

    ## Ejemplo

    ```text
    SI temperatura > 38
        MOSTRAR "Fiebre"
    SINO
        MOSTRAR "Normal"
    FIN
    ```

    Utilidades frecuentes:

    ```python
    type(10)
    len([1, 2, 3])
    help(print)
    ```

    Estas herramientas ayudan a inspeccionar y comprender el comportamiento del programa.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Dataset de trabajo (reducido)

    Usaremos un dataset clínico-social (sintético) con tamaño moderado para practicar operaciones típicas en salud pública.

    **Archivo:** `./public/dataset_clase_semana2_small.csv`

    **Variables principales:**
    - Demografía: `ID`, `age`, `sex`, `ethnicity`, `residence_area`, `education_grouped`
    - Factores / exposiciones: `smoking_status`, `alcohol_use`, `physical_inactivity`, `bmi_category`
    - Condiciones: `hypertension`, `Diabetes`, `high_cholesterol`, `anxiety`, `hearing_impairment`, `vision_impairment`
    - Funcionalidad: `functional_decline`, `functional_dementia`, `score_movilidad_cat`
    - Variables numéricas (simuladas): `sbp_mmHg`, `glucose_mg_dL`, `ldl_mg_dL`
    - Categorías derivadas: `sbp_cat`, `glucose_cat`, `ldl_cat`

    **Objetivo didáctico:** practicar importación, POO básica, NumPy vectorizado y pandas (`groupby`, `merge`, `pivot_table`) en un escenario realista.
    """)
    return


@app.cell
def _(mo, pd):
    # Preparación de carpeta y ruta basada en notebook_dir
    nb_dir = mo.notebook_dir()
    if nb_dir is None:
        raise RuntimeError(
            "No se pudo determinar el directorio del notebook con mo.notebook_dir()."
        )

    public_dir = nb_dir / "public"
    public_dir.mkdir(parents=True, exist_ok=True)

    data_file = public_dir / "dataset_clase_semana2_small.csv"
    if not data_file.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo: {data_file}. "
            "Ubica dataset_clase_semana2_small.csv dentro de ./public/."
        )

    df = pd.read_csv(data_file)

    # Validación mínima de columnas esperadas
    expected = {"ID", "age", "sex", "sbp_mmHg", "sbp_cat"}
    assert expected.issubset(set(df.columns))

    df.head()
    return (df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Repaso express (Semana 1)

    Haremos dos ejercicios cortos para reconectar con habilidades mínimas:

    - Funciones con validación
    - Conteos con diccionarios
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejercicio (Repaso 1): validación de entrada

    Implementa `validate_age(age)`:

    - valida que `age` sea numérico (`int` o `float`)
    - valida que `age` esté en el rango [0, 110]
    - retorna `int(age)`
    """)
    return


@app.function
def validate_age(age):
    """TODO: implementa validación y retorna int(age)."""
    age = int(age)  # valida que sea numérico
    if not (0 <= age <= 110):
        raise ValueError("age must be between 0 and 110")
    return age
    raise NotImplementedError


@app.cell(hide_code=True)
def _(mo):
    try:
        _out = validate_age(34)
        assert _out == 34
        mo.md(" `validate_age` pasó una prueba mínima.")
    except NotImplementedError:
        mo.md("(i) Implementa `validate_age` para que pasen las verificaciones.")
    except Exception as e:
        mo.md(f"(!!!) Revisa tu implementación: {e}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejercicio (Repaso 2): conteo con diccionarios

    Construye un diccionario `counts` que cuente cuántas filas hay por `residence_area`.
    """)
    return


@app.cell
def _():
    counts = {}

    # TODO: completa el conteo
    # for area in df["residence_area"]:
    #     ...
    return (counts,)


@app.cell(hide_code=True)
def _(counts, df, mo):
    if counts:
        try:
            assert sum(counts.values()) == len(df)
            mo.md(" `counts` parece consistente (suma = n de filas).")
        except Exception as e:
            mo.md(f"(!!!) `counts` no es consistente: {e}")
    else:
        mo.md("(i) Completa el diccionario `counts` para ver la verificación.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1) Concepto formal de módulo y librería

    - **Script**: archivo `.py` ejecutado como programa.
    - **Módulo**: archivo `.py` que puedes importar.
    - **Paquete**: carpeta con módulos (típicamente con `__init__.py`).
    - **Librería**: colección de módulos/paquetes (p.ej. `numpy`, `pandas`).

    Forma típica en análisis científico:
    - `import numpy as np`
    - `import pandas as pd`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejercicio 1 (módulos): presión de pulso

    Implementa `pulse_pressure(sbp, dbp)` que retorne `sbp - dbp`.

    - valida que ambos sean numéricos
    - valida que `sbp >= dbp`
    """)
    return


@app.function
def pulse_pressure(sbp, dbp):
    """TODO: implementa validaciones y retorna la presión de pulso."""
    raise NotImplementedError


@app.cell(hide_code=True)
def _(mo):
    try:
        _out = pulse_pressure(120, 80)
        assert _out == 40.0
        mo.md(" `pulse_pressure` pasó una prueba mínima.")
    except NotImplementedError:
        mo.md("(i) Implementa `pulse_pressure` para que pasen las verificaciones.")
    except Exception as e:
        mo.md(f"(!!!) Revisa tu implementación: {e}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejercicio 2 (módulos): conversión simple

    Implementa `mmol_l_to_mg_dl_glucose(x)`:

    - glucosa mg/dL ≈ mmol/L * 18
    - valida `x > 0`
    """)
    return


@app.function
def mmol_l_to_mg_dl_glucose(x):
    """TODO: implementa validación y conversión."""
    raise NotImplementedError


@app.cell(hide_code=True)
def _(mo):

    try:
        _out = mmol_l_to_mg_dl_glucose(5)
        assert _out == 90.0
        mo.md(" `mmol_l_to_mg_dl_glucose` pasó una prueba mínima.")
    except NotImplementedError:
        mo.md(
            "(i) Implementa `mmol_l_to_mg_dl_glucose` para que pasen las verificaciones."
        )
    except Exception as e:
        mo.md(f"(!!!) Revisa tu implementación: {e}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2) Programación orientada a objetos (POO): fundamentos

    Una clase define un molde; un objeto es una instancia.

    - **Atributos**: datos del objeto
    - **Métodos**: operaciones asociadas al objeto

    En librerías científicas, esto explica por qué objetos (como `DataFrame`) traen “datos + métodos”.
    """)
    return


@app.class_definition
class PatientRecord:
    def __init__(self, pid, sex, age, sbp_mmHg, glucose_mg_dL):
        self.pid = int(pid)
        self.sex = str(sex)
        self.age = int(age)
        self.sbp_mmHg = float(sbp_mmHg)
        self.glucose_mg_dL = float(glucose_mg_dL)

    def sbp_is_high(self):
        return self.sbp_mmHg >= 140


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejercicio 1 (POO): categoría simplificada de SBP

    Agrega a `PatientRecord` un método `sbp_category()` que retorne:

    - `"normal"` si SBP < 120
    - `"elevated"` si 120–129
    - `"high"` si >= 130
    """)
    return


@app.cell
def _():
    # TODO: implementa sbp_category() en PatientRecord.
    # Nota: edita la clase en la celda donde fue definida.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejercicio 2 (POO): resumen del objeto

    Agrega a `PatientRecord` un método `summary()` que retorne un `str` con:

    - `pid`, `sex`, `age`, `sbp_mmHg`, `glucose_mg_dL`
    """)
    return


@app.cell
def _():
    # TODO: implementa summary() en PatientRecord.
    # Nota: edita la clase en la celda donde fue definida.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##  Mini-reto 1: bandera de riesgo cardiometabólico

    Define `risk_flag(sbp_mmHg, glucose_mg_dL, ldl_mg_dL)` que retorne:

    - `"high"` si cualquiera:
      - SBP >= 140
      - glucosa >= 126
      - LDL >= 160

    - `"low"` si todas:
      - SBP < 130
      - glucosa < 100
      - LDL < 130

    - `"moderate"` en cualquier otro caso.
    """)
    return


@app.function
def risk_flag(sbp_mmHg, glucose_mg_dL, ldl_mg_dL):
    """TODO: implementa la clasificación."""
    raise NotImplementedError


@app.cell(hide_code=True)
def _(mo):
    try:
        assert risk_flag(118, 95, 110) == "low"
        assert risk_flag(142, 95, 110) == "high"
        mo.md(" `risk_flag` pasó pruebas mínimas.")
    except NotImplementedError:
        mo.md("(i) Implementa `risk_flag` para que pasen las verificaciones.")
    except Exception as e:
        mo.md(f"(!!!) Revisa tu implementación: {e}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3) NumPy: arrays y vectorización

    NumPy permite operar sobre arrays numéricos de forma vectorizada:

    - operaciones element-wise
    - máscaras booleanas
    - estadísticas rápidas (`mean`, `std`, etc.)

    Aquí trabajaremos con `sbp_mmHg`, `glucose_mg_dL` y `ldl_mg_dL`.
    """)
    return


@app.cell
def _(df):
    sbp = df["sbp_mmHg"].to_numpy(dtype=float)
    glucose = df["glucose_mg_dL"].to_numpy(dtype=float)

    assert sbp.shape == (len(df),)
    assert glucose.shape == (len(df),)

    sbp[:5], glucose[:5]
    return (sbp,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejercicio 1 (NumPy): z-score de SBP

    Implementa `zscore(x)` donde `x` es un `np.ndarray`:

    - retorna `(x - mean) / std`
    - usa `x.mean()` y `x.std()`
    """)
    return


@app.function
def zscore(x):
    """TODO: implementa z-score."""
    raise NotImplementedError


@app.cell(hide_code=True)
def _(mo, sbp):
    try:
        z = zscore(sbp)
        assert z.shape == sbp.shape
        mo.md(" `zscore` retornó un array del tamaño correcto.")
    except NotImplementedError:
        mo.md("(i) Implementa `zscore` para que pasen las verificaciones.")
    except Exception as e:
        mo.md(f"(!!!) Revisa tu implementación: {e}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejercicio 2 (NumPy): conteo vectorizado

    Calcula cuántos registros cumplen `sbp_mmHg >= 140` y guarda el resultado en `n_high`.
    """)
    return


@app.cell
def _():
    n_high = None

    # TODO: calcula el conteo vectorizado
    return (n_high,)


@app.cell(hide_code=True)
def _(df, mo, n_high):
    if n_high is None:
        mo.md("(i) Completa `n_high` para ver la verificación.")
    else:
        try:
            assert 0 <= int(n_high) <= len(df)
            mo.md(" `n_high` está en un rango válido.")
        except Exception as e:
            mo.md(f"(!!!) Revisa tu cálculo: {e}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4) pandas: estructura tabular (Series/DataFrame)

    Operaciones frecuentes:
    - inspección: `head`, `shape`, `dtypes`, `describe`
    - selección y filtros
    - `loc` vs `iloc`
    """)
    return


@app.cell
def _(df):
    df.shape, df.dtypes.head()
    return


@app.cell
def _(df):
    df.describe().loc[
        ["count", "mean", "min", "max"],
        ["age", "sbp_mmHg", "glucose_mg_dL", "ldl_mg_dL"],
    ]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejercicio 1 (pandas): filtrar cohorte

    Crea `df_cohort` filtrando:
    - `age >= 60`
    - `sex == "female"`

    Retorna columnas: `ID`, `age`, `sex`, `sbp_mmHg`, `glucose_mg_dL`.
    """)
    return


@app.cell
def _():
    df_cohort = None

    # TODO: filtra y selecciona columnas
    return (df_cohort,)


@app.cell(hide_code=True)
def _(df_cohort, mo):
    if df_cohort is None:
        mo.md("(i) Completa `df_cohort` para ver la verificación.")
    else:
        try:
            assert set(df_cohort.columns) == {
                "ID",
                "age",
                "sex",
                "sbp_mmHg",
                "glucose_mg_dL",
            }
            assert (df_cohort["age"] >= 60).all()
            assert (df_cohort["sex"] == "female").all()
            mo.md(" `df_cohort` cumple condiciones básicas.")
        except Exception as e:
            mo.md(f"(!!!) Revisa tu filtrado: {e}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejercicio 2 (pandas): `loc` vs `iloc`

    1) Con `iloc`, toma las primeras 5 filas y columnas `ID`, `sex`, `age`.

    2) Con `loc`, filtra `sbp_mmHg >= 140` y retorna `ID`, `sbp_mmHg`, `sbp_cat`.
    """)
    return


@app.cell
def _():
    sample_iloc = None
    sample_loc = None

    # TODO: completa sample_iloc y sample_loc
    return sample_iloc, sample_loc


@app.cell(hide_code=True)
def _(mo, sample_iloc, sample_loc):
    if (sample_iloc is None) or (sample_loc is None):
        mo.md("(i) Completa `sample_iloc` y `sample_loc` para ver la verificación.")
    else:
        try:
            assert set(sample_iloc.columns) == {"ID", "sex", "age"}
            assert sample_iloc.shape[0] == 5
            assert set(sample_loc.columns) == {"ID", "sbp_mmHg", "sbp_cat"}
            mo.md(" Selecciones con `iloc` y `loc` parecen correctas.")
        except Exception as e:
            mo.md(f"(!!!) Revisa tus selecciones: {e}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5) pandas: `groupby`, `merge`, `pivot_table`

    En análisis en salud pública es muy común:

    - agrupar por subpoblaciones (`sex`, `ethnicity`, `education_grouped`)
    - resumir métricas (`mean`, `count`, proporciones)
    - pivotear para obtener tablas comparativas

    A continuación construimos un pivot **paso a paso** hasta el resultado final.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Construcción paso a paso del pivot (hasta el ejemplo final)

    Objetivo: media de `sbp_mmHg` por:

    - filas: `sex`
    - columnas: `sbp_cat`
    - valores: `sbp_mmHg`
    - agregación: `mean`
    """)
    return


@app.cell
def _(df):
    # Paso 1: seleccionar solo columnas necesarias
    df_class = df[["sex", "sbp_cat", "sbp_mmHg"]].copy()
    df_class.head()
    return (df_class,)


@app.cell
def _(df_class):
    # Paso 2: inspeccionar categorías disponibles
    df_class["sex"].unique(), df_class["sbp_cat"].unique()
    return


@app.cell
def _(df_class):
    # Paso 3: construir el pivot (ejemplo final solicitado)
    pivot = df_class.pivot_table(
        index="sex",
        columns="sbp_cat",
        values="sbp_mmHg",
        aggfunc="mean",
        observed=True,
    ).round(1)

    pivot
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejercicio 1 (groupby/agg): proporción de hipertensión por sexo

    Define `has_htn = (sbp_mmHg >= 140)` y luego calcula por `sex`:

    - `n` (conteo)
    - `prop_htn` (promedio de `has_htn`)
    """)
    return


@app.cell
def _():
    htn_by_sex = None

    # TODO: construye la tabla con groupby/agg
    return (htn_by_sex,)


@app.cell(hide_code=True)
def _(htn_by_sex, mo):
    if htn_by_sex is None:
        mo.md("(i) Completa `htn_by_sex` para ver la verificación.")
    else:
        try:
            assert set(htn_by_sex.columns).issuperset({"sex", "n", "prop_htn"})
            assert htn_by_sex["prop_htn"].between(0, 1).all()
            mo.md(" `htn_by_sex` luce consistente.")
        except Exception as e:
            mo.md(f"(!!!) Revisa tu agregación: {e}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejercicio 2 (merge): metadatos simples de etnia

    Crea un DataFrame `eth_map` con:
    - `ethnicity`
    - `eth_group` (p.ej. `"majority"` vs `"minority"`)

    Luego haz `merge` para crear `df_with_eth` con `eth_group`.
    """)
    return


@app.cell
def _():
    df_with_eth = None

    # TODO: construye eth_map y haz el merge
    return (df_with_eth,)


@app.cell(hide_code=True)
def _(df_with_eth, mo):
    if df_with_eth is None:
        mo.md("(i) Completa `df_with_eth` para ver la verificación.")
    else:
        try:
            assert "eth_group" in df_with_eth.columns
            mo.md(" Merge completado: existe la columna `eth_group`.")
        except Exception as e:
            mo.md(f"(!!!) Revisa tu merge: {e}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##  Mini-reto 2 (12–15 min): resumen por sexo y glucosa

    Construye `cohort_summary` con:

    1) Filtra `age >= 60`.
    2) Agrupa por `sex` y `glucose_cat`.
    3) Calcula:
       - `n` (conteo)
       - `mean_sbp` (media de `sbp_mmHg`)
    """)
    return


@app.cell
def _():
    cohort_summary = None

    # TODO: filtra y resume
    return (cohort_summary,)


@app.cell(hide_code=True)
def _(cohort_summary, mo):
    if cohort_summary is None:
        mo.md("(i) Completa `cohort_summary` para ver la verificación.")
    else:
        try:
            assert set(cohort_summary.columns).issuperset(
                {"sex", "glucose_cat", "n", "mean_sbp"}
            )
            mo.md(" `cohort_summary` tiene columnas esperadas.")
        except Exception as e:
            mo.md(f"(!!!) Revisa tu resumen: {e}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6) pandas (práctico): chequeos mínimos de calidad

    Antes de cualquier análisis, verifica:

    - faltantes
    - rangos plausibles
    - tipos mínimos

    Aquí haremos chequeos sin modificar el dataset original.
    """)
    return


@app.cell
def _(df):
    missing = df.isna().sum().sort_values(ascending=False)
    missing.head(10)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejercicio 1 (calidad): chequeo de rangos

    Usa `assert` para validar:
    - `age` en [0, 110]
    - `sbp_mmHg` en [70, 250]
    """)
    return


@app.cell
def _():
    # TODO: agrega asserts de rangos
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejercicio 2 (calidad): tipos mínimos

    Crea `df_typed` (copia) y convierte:
    - `ID` -> `int`
    - `age` -> `int`
    """)
    return


@app.cell
def _():
    df_typed = None

    # TODO: crea df_typed con tipos mínimos
    return (df_typed,)


@app.cell(hide_code=True)
def _(df_typed, mo):
    if df_typed is None:
        mo.md("(i) Completa `df_typed` para ver la verificación.")
    else:
        try:
            assert str(df_typed["ID"].dtype).startswith("int")
            assert str(df_typed["age"].dtype).startswith("int")
            mo.md(" Tipos mínimos correctos.")
        except Exception as e:
            mo.md(f"(!!!) Revisa tipos: {e}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7) Diseño mínimo: `DatasetProcessor`

    Cuando el análisis crece, conviene encapsular un flujo repetible:

    - recibe un `DataFrame`
    - `clean()` (tipos mínimos + variables derivadas)
    - `compute_metrics()` (resúmenes estructurados)

    No incluimos visualización en esta sesión.
    """)
    return


@app.cell
def _(pd):
    class DatasetProcessor:
        def __init__(self, df):
            if not isinstance(df, pd.DataFrame):
                raise ValueError("df must be a pandas DataFrame")
            self.df = df.copy()

        def clean(self):
            """TODO: implementa limpieza mínima y retorna self."""
            raise NotImplementedError

        def compute_metrics(self):
            """TODO: retorna métricas agregadas en un diccionario."""
            raise NotImplementedError

    return (DatasetProcessor,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejercicio 1 (DatasetProcessor): implementar `clean()`

    En `clean()`:
    - convierte `ID` y `age` a `int`
    - crea `has_htn = (sbp_mmHg >= 140)`
    - retorna `self`
    """)
    return


@app.cell(hide_code=True)
def _(DatasetProcessor, df, mo):
    try:
        _proc = DatasetProcessor(df).clean()
        assert "has_htn" in _proc.df.columns
        mo.md(" `clean()` creó `has_htn` (verificación mínima).")
    except NotImplementedError:
        mo.md(
            "(i) Implementa `clean()` en `DatasetProcessor` para pasar la verificación."
        )
    except Exception as e:
        mo.md(f"(!!!) Revisa tu `clean()`: {e}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejercicio 2 (DatasetProcessor): implementar `compute_metrics()`

    En `compute_metrics()` retorna un diccionario con:
    - `by_sex`: tabla por `sex` con `n`, `mean_sbp`, `prop_htn`
    """)
    return


@app.cell(hide_code=True)
def _(DatasetProcessor, df, mo):
    try:
        _proc = DatasetProcessor(df).clean()
        _out = _proc.compute_metrics()
        assert isinstance(_out, dict)
        assert "by_sex" in _out
        mo.md(
            " `compute_metrics()` retornó un diccionario con `by_sex` (verificación mínima)."
        )
    except NotImplementedError:
        mo.md("(i) Implementa `compute_metrics()` para pasar la verificación.")
    except Exception as e:
        mo.md(f"(!!!) Revisa tu `compute_metrics()`: {e}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##  Mini-reto 3 (final!!!): pipeline mínimo + pivot

    Construye un pipeline reproducible (sin librerías nuevas):

    1) `_proc = DatasetProcessor(df).clean()`
    2) Filtra cohorte con `age` entre 45 y 75.
    3) Construye un `pivot_table` con:
       - filas = `sex`
       - columnas = `sbp_cat`
       - valores = `sbp_mmHg`
       - métrica = media
    4) Redondea a 1 decimal y guarda en `final_pivot`.
    """)
    return


@app.cell
def _():
    final_pivot = None

    # TODO: implementa el pipeline del mini-reto
    return (final_pivot,)


@app.cell(hide_code=True)
def _(final_pivot, mo):
    if final_pivot is None:
        mo.md("(i) Completa `final_pivot` para ver el resultado.")
    else:
        mo.md(" Pivot construido (revisa que filas = sex y columnas = sbp_cat).")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cierre

    En esta sesión conectamos:

    - `import` (módulos/librerías)
    - POO (clase/objeto/métodos)
    - NumPy (vectorización)
    - pandas (`groupby`, `merge`, `pivot_table`)
    - diseño mínimo con `DatasetProcessor` para reproducibilidad
    """)
    return


if __name__ == "__main__":
    app.run()
