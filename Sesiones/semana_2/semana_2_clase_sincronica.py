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
    import numpy as np
    import pandas as pd

    return mo, np, pd


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Semana 2 — Clase sincrónica

    **Enfoque:** repaso corto de Semana 1 + recorrido por los temas de Semana 2

    **Contexto único:** ejemplos en salud y salud pública (datos clínicos simulados).

    ---

    ## Agenda

    1) Repaso express (Semana 1): ejecución secuencial, variables, control de flujo, errores, funciones, bucles, estructuras básicas

    2) Semana 2:
    - (1) Módulos y librerías: `import`, alias, `from ... import ...`
    - (2) POO fundamentos: clase/objeto/atributo/método
    - (3) NumPy: arrays y vectorización
    - (4) pandas: Series/DataFrame y operaciones frecuentes
    - (5) pandas: `groupby`, `merge`, `agg`, `pivot_table`
    - (6) pandas (práctico): limpieza mínima y transformaciones comunes
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


@app.cell
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


@app.cell
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


@app.cell
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


@app.cell
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


@app.cell
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


@app.cell
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


@app.cell
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


@app.cell
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
    ## Dataset base

    Para practicar sin depender de archivos, usaremos un dataset pequeño con:

    - pacientes (`patient_id`)
    - sexo (`sex`)
    - edad (`age`)
    - peso y talla (`weight_kg`, `height_m`) para IMC
    - presión arterial sistólica (`sbp_mmHg`)
    - HbA1c (`hba1c_pct`)
    - hospital (`site`)
    - fecha de visita (`visit_date`)

    **Nota:** los valores son sintéticos; el objetivo es practicar programación.
    """)
    return


@app.cell
def _(np, pd):
    rng = np.random.default_rng(7)

    n = 48
    patient_id = np.arange(1001, 1001 + n)
    sex = rng.choice(["female", "male"], size=n, replace=True)
    age = rng.integers(18, 86, size=n)

    height_m = rng.normal(loc=1.68, scale=0.09, size=n).clip(1.45, 1.95)
    weight_kg = rng.normal(loc=74, scale=14, size=n).clip(45, 130)

    sbp_mmHg = rng.normal(loc=128, scale=18, size=n).round(0)
    hba1c_pct = rng.normal(loc=5.8, scale=0.7, size=n).round(1).clip(4.6, 10.5)

    site = rng.choice(["Hospital_A", "Hospital_B", "Clinic_C"], size=n, replace=True)

    # Fechas: últimos ~90 días
    base = np.datetime64("2026-02-28")
    offsets = rng.integers(0, 90, size=n)
    visit_date = base - offsets.astype("timedelta64[D]")

    df = pd.DataFrame(
        {
            "patient_id": patient_id,
            "sex": sex,
            "age": age,
            "height_m": height_m.round(2),
            "weight_kg": weight_kg.round(1),
            "sbp_mmHg": sbp_mmHg.astype(int),
            "hba1c_pct": hba1c_pct,
            "site": site,
            "visit_date": visit_date,
        }
    )

    df.head()
    return df, rng


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Repaso express (Semana 1)

    En Semana 1 vimos el "esqueleto" del pensamiento computacional:

    - Un programa es una **secuencia** de instrucciones.
    - Variables: nombres que referencian valores.
    - Expresiones: evaluación determinística y precedencia.
    - `if/elif/else`: cambiar el flujo con booleanos.
    - `try/except`: capturar excepciones esperadas.
    - Funciones: encapsular lógica repetible.
    - Bucles `for`/`while`: automatizar repetición.
    - Listas/tuplas/diccionarios: estructuras básicas.

    Vamos a validar ese repaso con dos ejercicios rápidos (muy cortos).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejercicio (Repaso 1): IMC con validación

    Implementa `bmi(weight_kg, height_m)` con:

    - Verificar entradas numéricas (`int` o `float`).
    - Verificar `height_m > 0`.
    - Retornar IMC = peso / talla² (float).

    > **Tip:** usa `isinstance(x, (int, float))` y lanza `ValueError` cuando corresponda.
    """)
    return


@app.cell
def _():
    def bmi(weight_kg, height_m):
        if not isinstance(weight_kg, (int, float)):
            raise ValueError("weight_kg must be numeric")
        if not isinstance(height_m, (int, float)):
            raise ValueError("height_m must be numeric")
        if height_m <= 0:
            raise ValueError("height_m must be > 0")
        return float(weight_kg) / (float(height_m) ** 2)

    # Validaciones rápidas
    assert round(bmi(70, 1.75), 3) == round(70 / (1.75**2), 3)

    bmi(70, 1.75)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejercicio (Repaso 2): conteo por categoría usando diccionarios

    Objetivo: construir un diccionario `counts` que cuente cuántos pacientes hay por `site`.

    > **Tip:** recorre `df["site"]` con un `for` y usa `dict.get(k, 0)`.
    """)
    return


@app.cell
def _(df):
    counts = {}
    for s in df["site"]:
        counts[s] = counts.get(s, 0) + 1

    # Validaciones
    assert sum(counts.values()) == len(df)
    assert set(counts.keys()).issubset(set(df["site"].unique()))

    counts
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1) Concepto formal de módulo y librería

    - **Script**: archivo `.py` ejecutado como programa.
    - **Módulo**: archivo `.py` que puedes **importar**.
    - **Paquete**: carpeta con módulos (típicamente con `__init__.py`).
    - **Librería**: colección de módulos/paquetes (p.ej. `numpy`, `pandas`).

    En el ecosistema científico, `import` es la puerta de entrada para reutilizar trabajo bien probado.

    Formas comunes:

    - `import numpy as np`
    - `import pandas as pd`
    - `from math import sqrt`

    **Regla práctica:** usa alias cortos y estándar (`np`, `pd`) para claridad.
    """)
    return


@app.cell
def _():
    import math

    x = 9
    sqrt_x = math.sqrt(x)
    sqrt_x
    return


@app.cell
def _():
    from math import sqrt

    sqrt(16)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejercicio 1 (módulos): `math` para un indicador de salud

    Implementa `pulse_pressure(sbp, dbp)` que retorne `sbp - dbp`.

    - Valida que ambos sean numéricos.
    - Valida que `sbp >= dbp`.

    > **Tip:** en salud pública, una diferencia muy alta puede sugerir rigidez arterial, pero aquí solo practicamos validación y funciones.
    """)
    return


@app.cell
def _():
    def pulse_pressure(sbp, dbp):
        if not isinstance(sbp, (int, float)):
            raise ValueError("sbp must be numeric")
        if not isinstance(dbp, (int, float)):
            raise ValueError("dbp must be numeric")
        if sbp < dbp:
            raise ValueError("sbp must be >= dbp")
        return float(sbp) - float(dbp)

    assert pulse_pressure(120, 80) == 40.0
    pulse_pressure(135, 88)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejercicio 2 (módulos): convertir unidades con una función

    Crea `lb_to_kg(weight_lb)` usando el factor 0.453592.

    - Valida `weight_lb > 0`.
    - Retorna `float`.

    > **Tip:** mantén la conversión en **una sola** línea (expresión) después de validar.
    """)
    return


@app.cell
def _():
    def lb_to_kg(weight_lb):
        if not isinstance(weight_lb, (int, float)):
            raise ValueError("weight_lb must be numeric")
        if weight_lb <= 0:
            raise ValueError("weight_lb must be > 0")
        return float(weight_lb) * 0.453592

    assert round(lb_to_kg(220), 3) == 99.790
    lb_to_kg(180)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2) Programación orientada a objetos (POO): fundamentos

    **Idea central:** una clase define un "molde"; un objeto es una instancia.

    Vocabulario:
    - **Atributos**: datos asociados al objeto.
    - **Métodos**: funciones definidas dentro de la clase que operan sobre el objeto.

    En librerías científicas, la POO ayuda a empaquetar estado + operaciones (p.ej. un `DataFrame` tiene datos y métodos para operar).
    """)
    return


@app.cell
def _():
    class Patient:
        def __init__(self, patient_id, sex, age, height_m, weight_kg):
            self.patient_id = int(patient_id)
            self.sex = str(sex)
            self.age = int(age)
            self.height_m = float(height_m)
            self.weight_kg = float(weight_kg)

        def bmi(self):
            return self.weight_kg / (self.height_m**2)

        def is_obese(self):
            return self.bmi() >= 30

    p = Patient(1001, "female", 52, 1.61, 84)
    (round(p.bmi(), 2), p.is_obese())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejercicio 1 (POO): método para clasificar presión sistólica (simplificado)

    Extiende la clase `PatientVitals` con:

    - Atributos: `sbp_mmHg` y `hba1c_pct`
    - Método `sbp_category()` que retorne:
      - `"normal"` si SBP < 120
      - `"elevated"` si 120–129
      - `"high"` si >= 130

    > **Tip:** construye condiciones `if/elif/else` con rangos explícitos.
    """)
    return


@app.cell
def _():
    class PatientVitals:
        def __init__(self, sbp_mmHg, hba1c_pct):
            self.sbp_mmHg = float(sbp_mmHg)
            self.hba1c_pct = float(hba1c_pct)

        def sbp_category(self):
            if self.sbp_mmHg < 120:
                return "normal"
            elif 120 <= self.sbp_mmHg <= 129:
                return "elevated"
            else:
                return "high"

    v = PatientVitals(128, 5.6)
    assert v.sbp_category() == "elevated"
    v.sbp_category()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejercicio 2 (POO): representar el objeto como texto

    Agrega a la clase `Patient` un método `summary()` que retorne un `str` con:

    - `patient_id`
    - `sex`
    - `age`
    - `BMI` con 1 decimal

    > **Tip:** usa `round(x, 1)` y un f-string.
    """)
    return


@app.cell
def _():
    class Patient:
        def __init__(self, patient_id, sex, age, height_m, weight_kg):
            self.patient_id = int(patient_id)
            self.sex = str(sex)
            self.age = int(age)
            self.height_m = float(height_m)
            self.weight_kg = float(weight_kg)

        def bmi(self):
            return self.weight_kg / (self.height_m**2)

        def summary(self):
            bmi_value = round(self.bmi(), 1)
            return f"Patient {self.patient_id} | {self.sex} | age={self.age} | BMI={bmi_value}"

    p2 = Patient(1002, "male", 44, 1.78, 76)
    assert "Patient 1002" in p2.summary()
    p2.summary()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ✅ Mini-reto 1 (10–12 min): clasificador de riesgo cardiometabólico (muy simple)

    Define una función `risk_flag(bmi_value, sbp_mmHg, hba1c_pct)` que retorne:

    - `"low"` si **todas** se cumplen:
      - BMI < 25
      - SBP < 130
      - HbA1c < 5.7

    - `"moderate"` si **alguna** está elevada pero **ninguna** está muy elevada:
      - BMI en [25, 30)
      - o SBP en [130, 140)
      - o HbA1c en [5.7, 6.5)

    - `"high"` si **cualquiera** está muy elevada:
      - BMI >= 30
      - o SBP >= 140
      - o HbA1c >= 6.5

    **Restricción:** usa `if/elif/else` y operadores lógicos (`and`, `or`).

    ### Tip (sin resolverte el reto)

    - Empieza por detectar `high` primero (un `or` grande).
    - Luego define la condición de `low` (un `and` grande).
    - Lo que quede puede ser `moderate`.
    """)
    return


@app.cell
def _():
    def risk_flag(bmi_value, sbp_mmHg, hba1c_pct):
        if (bmi_value >= 30) or (sbp_mmHg >= 140) or (hba1c_pct >= 6.5):
            return "high"
        if (bmi_value < 25) and (sbp_mmHg < 130) and (hba1c_pct < 5.7):
            return "low"
        return "moderate"

    # Pruebas básicas
    assert risk_flag(23.0, 118, 5.4) == "low"
    assert risk_flag(27.0, 128, 5.4) == "moderate"
    assert risk_flag(24.0, 142, 5.4) == "high"

    risk_flag(28.2, 134, 6.1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3) NumPy: arrays y vectorización

    **Motivación:** cuando el dato es numérico y grande, el array permite operaciones *element-wise* y vectorización.

    - Lista: contenedor general.
    - `np.array`: contenedor numérico con operaciones vectorizadas.

    Aquí calcularemos IMC para todos los pacientes.
    """)
    return


@app.cell
def _(df):
    heights = df["height_m"].to_numpy()
    weights = df["weight_kg"].to_numpy()

    bmi_vec = weights / (heights**2)

    # Validación: mismo tamaño que n
    assert bmi_vec.shape == (len(df),)

    bmi_vec[:5]
    return (bmi_vec,)


@app.cell
def _(bmi_vec):
    # Guardamos BMI en el DataFrame
    df = df.copy()
    df["bmi"] = bmi_vec.round(1)

    df[["patient_id", "height_m", "weight_kg", "bmi"]].head()
    return (df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejercicio 1 (NumPy): z-score (estandarización) de SBP

    Implementa `zscore(x)` donde `x` es un `np.ndarray`:

    - Retorna `(x - mean) / std`
    - Usa `x.mean()` y `x.std()`

    > **Tip:** asegúrate de retornar un array del mismo tamaño.
    """)
    return


@app.cell
def _(df, np):
    def zscore(x):
        x = np.asarray(x, dtype=float)
        return (x - x.mean()) / x.std()

    sbp = df["sbp_mmHg"].to_numpy()
    z = zscore(sbp)

    assert z.shape == sbp.shape
    assert abs(z.mean()) < 1e-9
    round(z.std(), 6)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejercicio 2 (NumPy): conteo vectorizado con condición

    Calcula cuántos pacientes tienen `bmi >= 30`.

    > **Tip:** `mask = (df["bmi"].to_numpy() >= 30)` y luego `mask.sum()`.
    """)
    return


@app.cell
def _(df):
    obese_mask = df["bmi"].to_numpy() >= 30
    n_obese = int(obese_mask.sum())

    assert 0 <= n_obese <= len(df)
    n_obese
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4) pandas: estructura tabular

    - **Series**: una columna (vector con índice).
    - **DataFrame**: tabla (columnas = Series) con un índice.

    Operaciones frecuentes para análisis rápido:

    - `df.head()`, `df.shape`, `df.dtypes`
    - `df.describe()` (numéricas)
    - selección: `df["col"]`, `df[[...]]`
    - filtrado booleano
    - indexación: `loc` (por etiqueta), `iloc` (por posición)
    """)
    return


@app.cell
def _(df):
    (df.shape, df.dtypes.head())
    return


@app.cell
def _(df):
    df.describe(numeric_only=True).loc[["count", "mean", "min", "max"], ["age", "bmi", "sbp_mmHg", "hba1c_pct"]]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejercicio 1 (pandas básico): filtrar cohorte

    Crea `df_adults` con pacientes:

    - `age >= 40`
    - `sbp_mmHg >= 130`

    Luego muestra `patient_id`, `age`, `sbp_mmHg`, `bmi`.

    > **Tip:** construye una máscara booleana con `&` y paréntesis.
    """)
    return


@app.cell
def _(df):
    df_adults = df[(df["age"] >= 40) & (df["sbp_mmHg"] >= 130)][
        ["patient_id", "age", "sbp_mmHg", "bmi"]
    ]

    assert set(df_adults.columns) == {"patient_id", "age", "sbp_mmHg", "bmi"}
    df_adults.head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejercicio 2 (pandas básico): `loc` vs `iloc`

    1) Con `iloc`, toma las primeras 3 filas y columnas `patient_id`, `sex`, `age`.

    2) Con `loc`, filtra por `sex == "female"` y retorna `patient_id` y `bmi`.

    > **Tip:** `iloc` usa posiciones; `loc` usa etiquetas (nombres de columnas / índice).
    """)
    return


@app.cell
def _(df):
    sample_iloc = df.iloc[:3][["patient_id", "sex", "age"]]
    sample_loc = df.loc[df["sex"] == "female", ["patient_id", "bmi"]]

    assert sample_iloc.shape[0] == 3
    assert set(sample_loc.columns) == {"patient_id", "bmi"}

    (sample_iloc, sample_loc.head())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5) pandas: agregación y combinación (resumen estructurado)

    En salud pública, gran parte del trabajo es:

    - **Agrupar** (por sexo, hospital, edad)
    - **Resumir** (medias, conteos)
    - **Combinar tablas** (p.ej. una tabla de pacientes + tabla de visitas)

    Herramientas clave:

    - `groupby(...).agg(...)`
    - `merge(...)`
    - `pivot_table(...)`

    Vamos a construir una tabla resumen por `site` y `sex`.
    """)
    return


@app.cell
def _(df):
    summary_site_sex = (
        df.groupby(["site", "sex"], as_index=False)
        .agg(
            n_patients=("patient_id", "count"),
            mean_age=("age", "mean"),
            mean_bmi=("bmi", "mean"),
            mean_sbp=("sbp_mmHg", "mean"),
        )
    )

    summary_site_sex.head()
    return


@app.cell
def _(df):
    pivot_mean_bmi = df.pivot_table(
        index="site",
        columns="sex",
        values="bmi",
        aggfunc="mean",
    )

    pivot_mean_bmi
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejercicio 1 (groupby/agg): prevalencia simplificada de obesidad por sitio

    Crea una tabla `obesity_by_site` con:

    - `site`
    - `n_patients`
    - `n_obese`
    - `prop_obese`

    Definición: obeso si `bmi >= 30`.

    > **Tip:** crea una columna booleana `is_obese` y usa `sum` (en booleanos funciona como conteo).
    """)
    return


@app.cell
def _(df):
    tmp = df.copy()
    tmp["is_obese"] = tmp["bmi"] >= 30

    obesity_by_site = (
        tmp.groupby("site", as_index=False)
        .agg(n_patients=("patient_id", "count"), n_obese=("is_obese", "sum"))
        .assign(prop_obese=lambda d: d["n_obese"] / d["n_patients"])
    )

    assert obesity_by_site["prop_obese"].between(0, 1).all()
    obesity_by_site
    return (obesity_by_site,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejercicio 2 (merge): añadir metadatos del sitio

    Crea un DataFrame `site_info` con dos columnas:

    - `site`
    - `region` (valores sugeridos: "North", "South")

    Luego haz un `merge` con `obesity_by_site` para tener `region` en el resumen.

    > **Tip:** `pd.DataFrame({...})` + `merge(..., on="site", how="left")`.
    """)
    return


@app.cell
def _(obesity_by_site, pd):
    site_info = pd.DataFrame(
        {
            "site": ["Hospital_A", "Hospital_B", "Clinic_C"],
            "region": ["North", "South", "South"],
        }
    )

    obesity_by_site2 = obesity_by_site.merge(site_info, on="site", how="left")

    assert obesity_by_site2["region"].isna().sum() == 0
    obesity_by_site2
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ✅ Mini-reto 2 (12–15 min): cohorte y tasa por grupo

    Construye `cohort_summary` con el siguiente flujo:

    1) Filtra pacientes con `age >= 50`.
    2) Define una variable categórica `risk_group` basada en HbA1c:
       - `"normoglycemia"` si HbA1c < 5.7
       - `"prediabetes"` si 5.7 <= HbA1c < 6.5
       - `"diabetes"` si HbA1c >= 6.5
    3) Agrupa por `sex` y `risk_group` y calcula:
       - `n` (conteo)
       - `mean_bmi`

    ### Tip (sin resolver)

    - Usa `np.where` anidado *o* un `apply` simple con `if/elif/else`.
    - Mantén la lógica de clasificación en una función pequeña.
    - Valida que la suma de `n` sea el tamaño de la cohorte filtrada.
    """)
    return


@app.cell
def _(df):
    df_50 = df[df["age"] >= 50].copy()

    def gly_group(hba1c):
        if hba1c < 5.7:
            return "normoglycemia"
        elif hba1c < 6.5:
            return "prediabetes"
        else:
            return "diabetes"

    df_50["risk_group"] = df_50["hba1c_pct"].apply(gly_group)

    cohort_summary = (
        df_50.groupby(["sex", "risk_group"], as_index=False)
        .agg(n=("patient_id", "count"), mean_bmi=("bmi", "mean"))
        .sort_values(["sex", "risk_group"], ascending=True)
    )

    assert cohort_summary["n"].sum() == len(df_50)
    cohort_summary
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6) pandas (práctico): limpieza mínima

    En proyectos reales, antes de modelar necesitas asegurar:

    - tipos correctos
    - valores faltantes manejados
    - variables derivadas reproducibles

    Aquí simularemos un poco de *missingness* y aplicaremos:

    - `isna()` y conteos
    - imputación simple (mediana) para un ejemplo
    - creación de una columna derivada

    **Nota:** el objetivo no es la imputación óptima, sino practicar el pipeline.
    """)
    return


@app.cell
def _(df, np, rng):
    df_dirty = df.copy()

    # Introducimos faltantes sintéticos en SBP
    missing_idx = rng.choice(df_dirty.index.to_numpy(), size=5, replace=False)
    df_dirty.loc[missing_idx, "sbp_mmHg"] = np.nan

    missing_counts = df_dirty.isna().sum().sort_values(ascending=False)
    missing_counts.head(10)
    return df_dirty, missing_idx


@app.cell
def _(df_dirty, missing_idx):
    sbp_median = float(df_dirty["sbp_mmHg"].median())
    df_clean = df_dirty.copy()
    df_clean["sbp_mmHg"] = df_clean["sbp_mmHg"].fillna(sbp_median).astype(int)

    assert df_clean["sbp_mmHg"].isna().sum() == 0
    (sbp_median, df_clean.loc[missing_idx, ["patient_id", "sbp_mmHg"]].head())
    return (df_clean,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejercicio 1 (limpieza): crear una variable derivada de hipertensión (simplificada)

    En `df_clean`, crea `has_htn` (booleano) definido como:

    - `True` si `sbp_mmHg >= 140`
    - `False` si no

    Luego calcula la proporción total `has_htn.mean()`.

    > **Tip:** en pandas, una columna booleana tiene `.mean()` interpretado como proporción de `True`.
    """)
    return


@app.cell
def _(df_clean):
    def _():
        df_clean = df_clean.copy()
        df_clean["has_htn"] = df_clean["sbp_mmHg"] >= 140

        prop_htn = float(df_clean["has_htn"].mean())

        assert 0 <= prop_htn <= 1
        return prop_htn


    _()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejercicio 2 (limpieza): chequeo de consistencia rápida

    Valida con `assert` que:

    - todas las edades estén entre 0 y 110
    - todas las tallas estén entre 1.2 y 2.2

    > **Tip:** usa `.between(a, b).all()`.
    """)
    return


@app.cell
def _(df_clean):
    assert df_clean["age"].between(0, 110).all()
    assert df_clean["height_m"].between(1.2, 2.2).all()

    "Checks passed"
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7) Diseño mínimo: `DatasetProcessor`

    Cuando el análisis crece, conviene encapsular un flujo repetible.

    **Diseño mínimo (ya visto en semana 2):**

    - una clase que recibe un `DataFrame`
    - métodos con responsabilidades claras:
      - `clean()` (tipos, faltantes, columnas derivadas)
      - `compute_metrics()` (resúmenes estructurados)

    No construiremos visualizaciones (eso es un tema posterior del curso).
    """)
    return


@app.cell
def _(df_dirty, pd):
    class DatasetProcessor:
        def __init__(self, df):
            if not isinstance(df, pd.DataFrame):
                raise ValueError("df must be a pandas DataFrame")
            self.df = df.copy()

        def clean(self):
            # Tipos mínimos
            self.df["patient_id"] = self.df["patient_id"].astype(int)
            self.df["age"] = self.df["age"].astype(int)
            self.df["height_m"] = self.df["height_m"].astype(float)
            self.df["weight_kg"] = self.df["weight_kg"].astype(float)

            # BMI derivado
            self.df["bmi"] = (self.df["weight_kg"] / (self.df["height_m"] ** 2)).round(1)

            # Imputación simple de SBP si falta
            if self.df["sbp_mmHg"].isna().any():
                med = float(self.df["sbp_mmHg"].median())
                self.df["sbp_mmHg"] = self.df["sbp_mmHg"].fillna(med)

            self.df["sbp_mmHg"] = self.df["sbp_mmHg"].astype(int)

            # Flag htn
            self.df["has_htn"] = self.df["sbp_mmHg"] >= 140

            return self

        def compute_metrics(self):
            # Resumen simple por sitio
            by_site = (
                self.df.groupby("site", as_index=False)
                .agg(
                    n=("patient_id", "count"),
                    mean_age=("age", "mean"),
                    mean_bmi=("bmi", "mean"),
                    prop_htn=("has_htn", "mean"),
                )
                .sort_values("n", ascending=False)
            )

            # Resumen por sexo
            by_sex = (
                self.df.groupby("sex", as_index=False)
                .agg(
                    n=("patient_id", "count"),
                    mean_bmi=("bmi", "mean"),
                    mean_sbp=("sbp_mmHg", "mean"),
                    prop_htn=("has_htn", "mean"),
                )
                .sort_values("sex")
            )

            return {"by_site": by_site, "by_sex": by_sex}

    processor = DatasetProcessor(df_dirty).clean()
    metrics = processor.compute_metrics()

    metrics["by_site"]
    return (DatasetProcessor,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejercicio 1 (DatasetProcessor): método para filtrar por rango de edad

    Agrega a `DatasetProcessor` un método `subset_by_age(min_age, max_age)` que:

    - valide `min_age <= max_age`
    - retorne un **nuevo** `DatasetProcessor` con el subset de filas

    > **Tip:** retorna `DatasetProcessor(self.df[mask].copy())`.
    """)
    return


@app.cell
def _(df_dirty, pd):
    class DatasetProcessor:
        def __init__(self, df):
            if not isinstance(df, pd.DataFrame):
                raise ValueError("df must be a pandas DataFrame")
            self.df = df.copy()

        def clean(self):
            self.df["patient_id"] = self.df["patient_id"].astype(int)
            self.df["age"] = self.df["age"].astype(int)
            self.df["height_m"] = self.df["height_m"].astype(float)
            self.df["weight_kg"] = self.df["weight_kg"].astype(float)
            self.df["bmi"] = (self.df["weight_kg"] / (self.df["height_m"] ** 2)).round(1)

            if self.df["sbp_mmHg"].isna().any():
                med = float(self.df["sbp_mmHg"].median())
                self.df["sbp_mmHg"] = self.df["sbp_mmHg"].fillna(med)

            self.df["sbp_mmHg"] = self.df["sbp_mmHg"].astype(int)
            self.df["has_htn"] = self.df["sbp_mmHg"] >= 140
            return self

        def subset_by_age(self, min_age, max_age):
            if not isinstance(min_age, (int, float)) or not isinstance(max_age, (int, float)):
                raise ValueError("min_age and max_age must be numeric")
            if min_age > max_age:
                raise ValueError("min_age must be <= max_age")
            mask = (self.df["age"] >= min_age) & (self.df["age"] <= max_age)
            return DatasetProcessor(self.df.loc[mask].copy())

        def compute_metrics(self):
            by_site = (
                self.df.groupby("site", as_index=False)
                .agg(
                    n=("patient_id", "count"),
                    mean_age=("age", "mean"),
                    mean_bmi=("bmi", "mean"),
                    prop_htn=("has_htn", "mean"),
                )
                .sort_values("n", ascending=False)
            )
            by_sex = (
                self.df.groupby("sex", as_index=False)
                .agg(
                    n=("patient_id", "count"),
                    mean_bmi=("bmi", "mean"),
                    mean_sbp=("sbp_mmHg", "mean"),
                    prop_htn=("has_htn", "mean"),
                )
                .sort_values("sex")
            )
            return {"by_site": by_site, "by_sex": by_sex}

    proc = DatasetProcessor(df_dirty).clean()
    proc_40_60 = proc.subset_by_age(40, 60).clean()

    assert proc_40_60.df["age"].between(40, 60).all()
    proc_40_60.compute_metrics()["by_sex"]
    return (DatasetProcessor,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejercicio 2 (DatasetProcessor): métrica adicional

    En `compute_metrics()`, agrega una métrica `prop_obese` por sexo:

    - obeso si `bmi >= 30`

    > **Tip:** crea una columna booleana temporal y usa `.mean()`.
    """)
    return


@app.cell
def _(df_dirty, pd):
    class DatasetProcessor:
        def __init__(self, df):
            if not isinstance(df, pd.DataFrame):
                raise ValueError("df must be a pandas DataFrame")
            self.df = df.copy()

        def clean(self):
            self.df["patient_id"] = self.df["patient_id"].astype(int)
            self.df["age"] = self.df["age"].astype(int)
            self.df["height_m"] = self.df["height_m"].astype(float)
            self.df["weight_kg"] = self.df["weight_kg"].astype(float)
            self.df["bmi"] = (self.df["weight_kg"] / (self.df["height_m"] ** 2)).round(1)

            if self.df["sbp_mmHg"].isna().any():
                med = float(self.df["sbp_mmHg"].median())
                self.df["sbp_mmHg"] = self.df["sbp_mmHg"].fillna(med)

            self.df["sbp_mmHg"] = self.df["sbp_mmHg"].astype(int)
            self.df["has_htn"] = self.df["sbp_mmHg"] >= 140
            return self

        def compute_metrics(self):
            df2 = self.df.copy()
            df2["is_obese"] = df2["bmi"] >= 30

            by_sex = (
                df2.groupby("sex", as_index=False)
                .agg(
                    n=("patient_id", "count"),
                    mean_bmi=("bmi", "mean"),
                    mean_sbp=("sbp_mmHg", "mean"),
                    prop_htn=("has_htn", "mean"),
                    prop_obese=("is_obese", "mean"),
                )
                .sort_values("sex")
            )

            return {"by_sex": by_sex}

    proc2 = DatasetProcessor(df_dirty).clean()
    out = proc2.compute_metrics()["by_sex"]

    assert out["prop_obese"].between(0, 1).all()
    out
    return (DatasetProcessor,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ✅ Mini-reto 3 (final, 15–18 min): pipeline mínimo sobre una cohorte

    Usa **solo** lo visto hasta ahora (Semana 2 lecciones 1–7) para construir un pipeline reproducible:

    1) Crea `proc_final = DatasetProcessor(df_dirty).clean()`.
    2) Filtra una cohorte `age` entre 45 y 75.
    3) En esa cohorte, calcula un resumen por `site` con:
       - `n`
       - `mean_bmi`
       - `prop_htn`
    4) Ordena el resumen por `prop_htn` descendente.

    ### Tip (sin resolver)

    - Reusa `subset_by_age` si la tienes; si no, filtra con una máscara.
    - `groupby(...).agg(...)` + `.sort_values(...)`.
    - Valida con `assert` que `prop_htn` esté entre 0 y 1.
    """)
    return


@app.cell
def _(DatasetProcessor, df_dirty):
    # Implementación final (ejemplo ejecutable)
    proc_final = DatasetProcessor(df_dirty).clean()

    cohort = proc_final.df[(proc_final.df["age"] >= 45) & (proc_final.df["age"] <= 75)].copy()

    cohort_summary_site = (
        cohort.groupby("site", as_index=False)
        .agg(
            n=("patient_id", "count"),
            mean_bmi=("bmi", "mean"),
            prop_htn=("has_htn", "mean"),
        )
        .sort_values("prop_htn", ascending=False)
    )

    assert cohort_summary_site["prop_htn"].between(0, 1).all()
    cohort_summary_site
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cierre

    En esta sesión conectamos:

    - **import** (módulos/librerías) como reutilización
    - POO para encapsular estado y operaciones
    - NumPy para cálculo vectorizado
    - pandas para manipulación tabular y resúmenes
    - diseño mínimo con `DatasetProcessor` para reproducibilidad

    La siguiente etapa del curso (más adelante) será convertir estos outputs en análisis más completo y visualización.
    """)
    return


if __name__ == "__main__":
    app.run()
