# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "pytest==9.0.2",
#     "requests==2.32.5",
# ]
# ///

import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")

with app.setup(hide_code=True):
    import marimo as mo
    from setup import TipContent, TestContent


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Semana 2 — Lección 1
    ## Concepto formal de módulo y librería

    ### Propósito
    Formalizar **cómo se organiza código en Python** y cómo se reutiliza mediante `import`.

    En esta sesión vas a:
    - Diferenciar **script** vs **módulo** (y ubicar **paquete** y **librería** como conceptos del ecosistema).
    - Usar `import`, `from ... import ...` y **alias**.
    - Reconocer **espacios de nombres** (namespaces) como mecanismo para evitar colisiones.
    - Aplicar imports en mini-tareas orientadas a **salud / salud pública**.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 1) ¿Qué es un módulo?

    Un **módulo** es, en términos prácticos, **un archivo `.py`** que contiene definiciones reutilizables:
    - variables,
    - funciones,
    - (más adelante: clases, etc.).

    ### Idea central
    Cuando escribes `import x`, Python carga el módulo `x` y te permite acceder a su contenido a través de un **namespace**:

    - `x.funcion(...)`
    - `x.CONSTANTE`

    Esto evita ambigüedades: el nombre `funcion` vive “dentro” de `x`.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 2) Script vs módulo (y dónde encaja una “librería”)

    - **Script**: archivo `.py` escrito para **ejecutarse** como programa (una tarea concreta).
    - **Módulo**: archivo `.py` pensado para **importarse** (reutilización).
    - **Paquete**: colección organizada de módulos.
    - **Librería**: término práctico para referirse a un conjunto de funcionalidades (a menudo un paquete), ya sea de la **biblioteca estándar** o instalada por terceros.

    En esta lección usaremos módulos de la **biblioteca estándar** (vienen con Python) como:
    - `math` (funciones matemáticas),
    - `statistics` (estadística descriptiva básica),
    - `random` (aleatoriedad controlada).
    """)
    return


@app.cell
def _():
    # En marimo (y en notebooks), el archivo se ejecuta como "__main__"
    print("__name__ =", __name__)
    assert __name__ == "__main__"
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 3) `import`: cargar un módulo y usar su namespace

    Ejemplo en salud pública: calcular un **IMC** y usar `math` para redondeo.

    Puntos clave:
    - `import math` crea el namespace `math`.
    - Accedes a funciones como `math.floor`, `math.ceil`, `math.sqrt`, etc.
    """)
    return


@app.cell
def _():
    def _():
        import math

        peso_kg = 72.5
        altura_m = 1.73
        imc = peso_kg / (altura_m**2)

        print("IMC (sin redondeo):", imc)
        print("IMC (floor):", math.floor(imc))
        print("IMC (ceil):", math.ceil(imc))
        return print("IMC (2 decimales con round):", round(imc, 2))

        assert math.floor(imc) <= imc <= math.ceil(imc)

    _()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 4) Alias: `import ... as ...`

    Los alias reducen ruido y aumentan legibilidad cuando un namespace se usa repetidamente.

    Convención típica:
    - `import math as m`
    """)
    return


@app.cell
def _():
    import math as m

    # Ejemplo: conversión simple para salud (kPa a mmHg)
    # 1 kPa ≈ 7.50062 mmHg
    presion_kpa = 13.3
    presion_mmhg = presion_kpa * 7.50062

    print("Presión arterial aproximada (mmHg):", m.floor(presion_mmhg))
    assert presion_mmhg > 0
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 5) Import selectivo: `from ... import ...`

    A veces quieres traer **solo** un símbolo (función/constante) al namespace local.

    Ejemplo:
    ```python
    from statistics import mean
    ```

    Ventaja: `mean(x)` en lugar de `statistics.mean(x)`.

    Riesgo: si importas muchos nombres, puede haber **colisiones** (dos cosas con el mismo nombre).
    """)
    return


@app.cell
def _():
    from statistics import mean, median

    # Ejemplo epidemiológico: resumen de edades en una muestra pequeña
    edades = [34, 40, 29, 51, 46, 46, 38]

    print("Edad media:", mean(edades))
    print("Mediana:", median(edades))

    assert mean(edades) >= min(edades)
    assert mean(edades) <= max(edades)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto 1 (guiado) — Dosis por kg con redondeo seguro

    ### Contexto clínico

    En la práctica clínica, muchas dosis se calculan en función del peso del paciente, por ejemplo en **mg/kg**.
    Cuando el cálculo produce un valor decimal, puede ser importante aplicar una regla de redondeo adecuada para evitar administrar una dosis menor a la esperada por el protocolo.

    En este ejercicio vas a construir una función que calcule una **dosis total en miligramos** a partir de:

    - el peso del paciente (`peso_kg`)
    - la dosis prescrita por kilogramo (`mg_por_kg`)

    ### Tu objetivo

    Completa la función `dosis_total_mg(...)` para que:

    1. verifique que las entradas sean válidas,
    2. realice el cálculo de la dosis total,
    3. y devuelva un resultado final listo para usarse.

    ### Qué debes tener en cuenta

    - No todo valor recibido por una función debe asumirse como correcto.
    - En programación clínica y científica, validar entradas es tan importante como calcular bien.
    - También debes pensar qué tipo de dato debería devolver la función al final.

    ### Recomendación

    Antes de completar los `TODO`, revisa la documentación oficial de Python sobre:

    - validación de tipos,
    - el módulo `math`,
    - y funciones de redondeo.

    La documentación no solo sirve para “buscar respuestas”: también ayuda a elegir la herramienta correcta y a entender su comportamiento con precisión.

    > Consejo: prueba casos sencillos mientras desarrollas, pero evita adivinar. Usa ejemplos pequeños y comprueba que el resultado tenga sentido.
    """)
    return


@app.function
# === TU TURNO (EDITA ESTA CELDA) ===
def dosis_total_mg(peso_kg, mg_por_kg):
    # 1) Validar tipos numéricos
    # TODO:
    pass

    # 2) Validar positividad
    # TODO:
    pass

    # 3) Calcular dosis y redondear hacia arriba
    # TODO:
    dosis = None
    return dosis


@app.cell(hide_code=True)
def _():
    _tip_content = TipContent(
        items_raw=[
            r"""
    <Validación de tipos>
    Antes de calcular, piensa qué tipo de valores debería aceptar la función.

    Una función clínica no debería asumir que todo lo que recibe es válido.  
    Revisa en la documentación cómo comprobar si un valor es numérico en Python.

    > Pista: busca una forma de aceptar tanto enteros como decimales.
    """,
            r"""
    <Validación de positividad>
    Después del tipo, piensa en el significado clínico de los datos.

    ¿Tiene sentido un peso negativo?  
    ¿Tiene sentido una dosis por kg negativa o igual a cero?

    La función debería detectar entradas que no sean razonables antes de continuar.
    """,
            r"""
    <Cálculo de la dosis>
    Una vez que las entradas sean válidas, identifica cuál sería la operación base para obtener la dosis total.

    Si tienes dudas, escribe el cálculo en papel primero y luego llévalo a Python.

    > Verifica el resultado intermedio antes de aplicar cualquier redondeo.
    """,
            r"""
    <Redondeo seguro>
    No todos los redondeos hacen lo mismo.

    En este reto necesitas un redondeo que evite quedarte por debajo de la dosis calculada.  
    Consulta la documentación del módulo `math` y compara las funciones de redondeo disponibles.

    > La función correcta redondea siempre hacia arriba.
    """,
            r"""
    <Tipo de salida>
    Piensa en cómo debería verse el resultado final.

    La dosis total en mg, tal como se pide en este reto, no debería quedar como un valor ambiguo o parcialmente procesado.

    > Revisa qué tipo de dato produce la función de redondeo que elijas.
    """,
            r"""
    <solucion>

    ### Implementación esperada

    ```python
    import math

    def dosis_total_mg(peso_kg, mg_por_kg):

        # 1. Validar tipos numéricos
        if not isinstance(peso_kg, (int, float)) or not isinstance(mg_por_kg, (int, float)):
            raise TypeError("peso_kg y mg_por_kg deben ser numéricos")

        # 2. Validar positividad
        if peso_kg <= 0 or mg_por_kg <= 0:
            raise ValueError("peso_kg y mg_por_kg deben ser positivos")

        # 3. Calcular dosis total
        dosis = peso_kg * mg_por_kg

        # 4. Redondear hacia arriba
        dosis_redondeada = math.ceil(dosis)

        return dosis_redondeada
    ```

    ### Explicación paso a paso

    **1. Validación de tipos**

    ```python
    isinstance(x, (int, float))
    ```

    Permite aceptar tanto números enteros como decimales.

    ---

    **2. Validación clínica**

    Se evita calcular dosis con valores negativos o inválidos.

    Esto es importante en funciones usadas en contextos clínicos o científicos.

    ---

    **3. Cálculo de la dosis**

    La fórmula base es:

    ```python
    dosis = peso_kg * mg_por_kg
    ```

    Esto produce la dosis teórica sin redondeo.

    ---

    **4. Redondeo seguro**

    ```python
    math.ceil(...)
    ```

    Siempre redondea **hacia arriba**, lo que evita que la dosis final sea menor que la calculada.
    """
        ]
    )

    _tip_content.render()
    return


@app.cell(hide_code=True)
def _():
    def _():
        _test_content = TestContent(
            items_raw=[
                r"""
    <Comportamiento básico>
    Comprueba que un perfil de bajo riesgo produzca 0.

    ```python
    assert puntaje_riesgo(22, 110) == 0, (
        "Un perfil de bajo riesgo debería producir puntaje 0."
    )
    print("Caso basal correcto.")
    ```
    """,
                r"""
    <Tipo de salida>
    La función debe retornar un entero.

    ```python
    resultado = puntaje_riesgo(28, 130)

    assert resultado is not None, (
        "La función devolvió `None`. Probablemente todavía contiene `pass` "
        "o no retorna un valor."
    )

    assert isinstance(resultado, int), (
        f"La función debe retornar un entero. "
        f"Tipo obtenido: {type(resultado).__name__}"
    )

    print("Tipo de salida correcto.")
    ```
    """,
                r"""
    <solucion>
    Los tests ayudan a verificar que tu implementación cumple el comportamiento esperado.
    """
            ],
            namespace=globals()
        )

        return _test_content.render()

    _()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 6) Buenas prácticas mínimas de import

    1.  Importa al inicio del archivo (en marimo, típicamente al inicio de la celda).
    2. Prefiere `import modulo` cuando:
       - quieres claridad de procedencia (`statistics.mean`, `math.sqrt`)
       - deseas evitar colisiones de nombres
    3. Usa `from modulo import x` cuando:
       - `x` es muy usado y el contexto lo hace inequívoco
    4. Usa alias con moderación (`import statistics as st`) cuando:
       - mejora legibilidad en un bloque largo

    En general: prioriza **legibilidad y trazabilidad**.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto 2 (guiado) — Corregir imports y colisiones

    ### Contexto

    Estás realizando un análisis rápido de un indicador clínico: **HbA1c (%)**.

    Tienes una pequeña muestra de valores y deseas calcular:

    - la **media**
    - la **desviación estándar poblacional**
    - un **z-score** para un nuevo valor observado

    El z-score permite comparar un valor con respecto a la distribución de referencia:

    z = (x − media) / desviación_estándar

    ### Tu tarea

    Completa los espacios `TODO` para que el código funcione correctamente.

    Debes:

    1. importar el módulo adecuado,
    2. calcular las estadísticas necesarias,
    3. calcular el z-score.

    ### Reglas importantes

    - Debes usar el módulo `statistics`.
    - Debes importar el módulo usando **un alias corto**.
    - Evita **colisiones de nombres** (por ejemplo, no sobrescribas `mean` o `statistics`).

    ### Recomendación

    Si no recuerdas alguna función, consulta la documentación de Python del módulo `statistics`.

    > En análisis de datos, saber **qué función buscar** en la documentación es una habilidad tan importante como escribir el código.
    """)
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    # TODO: importa statistics con un alias corto
    # import ??? as ???
    pass

    hba1c = [5.4, 5.8, 6.1, 5.6, 5.9, 6.5, 5.7]
    nuevo = 6.2

    # TODO: calcula media y stdev usando el alias
    media = None
    sd = None

    # z = (x - media) / sd
    z = None

    print("media:", media)
    print("sd:", sd)
    print("z:", z)
    return


@app.cell(hide_code=True)
def _():
    _tip_content = TipContent(
        items_raw=[
            r"""
    <Importación del módulo>

    Primero necesitas importar el módulo correcto.

    Consulta la documentación de Python sobre el módulo **statistics**.

    Una práctica común es usar un **alias corto** al importar un módulo.

    > Esto permite escribir llamadas más compactas en el código.
    """,
            r"""
    <Calcular la media>

    Una vez importado el módulo, revisa qué función calcula la **media** de una lista.

    La función recibe una secuencia de valores numéricos.

    ```python
    funcion(lista)
    ```
    """,
            r"""
    <Desviación estándar poblacional>

    El módulo `statistics` tiene más de una función para desviación estándar.

    En este ejercicio necesitas la versión **poblacional**, no la muestral.

    Consulta la documentación para encontrar la función correcta.
    """,
            r"""
    <Calcular el z-score>

    Una vez tengas la media y la desviación estándar, puedes calcular:

    ```python
    z = (x - media) / sd
    ```

    En este caso:

    - `x` es el nuevo valor
    - `media` es el promedio de la lista
    - `sd` es la desviación estándar.
    """,
            r"""
    <solucion>

    ### Implementación esperada

    ```python
    import statistics as st

    hba1c = [5.4, 5.8, 6.1, 5.6, 5.9, 6.5, 5.7]
    nuevo = 6.2

    # calcular media
    media = st.mean(hba1c)

    # desviación estándar poblacional
    sd = st.pstdev(hba1c)

    # calcular z-score
    z = (nuevo - media) / sd

    print("media:", media)
    print("sd:", sd)
    print("z:", z)
    ```

    ### Explicación

    1. Se importa `statistics` con el alias `st` para escribir llamadas más cortas.

    2. `st.mean(...)` calcula la media de los valores.

    3. `st.pstdev(...)` calcula la desviación estándar **poblacional**.

    4. El z-score se calcula con la fórmula:

    ```python
    z = (x - media) / sd
    ```

    Esto indica cuántas desviaciones estándar está el valor nuevo respecto a la media.
    """
        ]
    )

    _tip_content.render()
    return


@app.cell(hide_code=True)
def _():
    def _():
        import math

        _test_content = TestContent(
            items_raw=[
                r"""
    <Import del módulo>
    Verifica que el módulo `statistics` haya sido importado correctamente antes de calcular los resultados.

    ```python
    assert "statistics" in globals(), (
        "No se encontró el módulo `statistics` en el entorno global. "
        "Debes importarlo antes de calcular `media`, `sd` y `z`."
    )
    print("Import de `statistics` detectado correctamente.")
    ```
    """,
                r"""
    <Variables calculadas>
    Comprueba que las variables principales ya no estén en `None`.

    ```python
    assert media is not None, (
        "La variable `media` sigue siendo `None`. "
        "Debes calcularla usando una función del módulo `statistics`."
    )

    assert sd is not None, (
        "La variable `sd` sigue siendo `None`. "
        "Debes calcular la desviación estándar poblacional."
    )

    assert z is not None, (
        "La variable `z` sigue siendo `None`. "
        "Debes calcular el z-score usando la fórmula indicada."
    )

    print("Las variables `media`, `sd` y `z` fueron definidas.")
    ```
    """,
                r"""
    <Cálculo de la media>
    Comprueba que `media` coincida con el valor esperado para la lista `hba1c`.

    ```python
    expected_media = statistics.mean(hba1c)

    assert math.isclose(media, expected_media, rel_tol=1e-6), (
        f"La media no es correcta. Esperado ≈ {expected_media:.4f}, "
        f"obtenido {media:.4f}. "
        "Revisa que estés usando la función adecuada del módulo `statistics`."
    )

    print(f"Media correcta: {expected_media:.4f}")
    ```
    """,
                r"""
    <Desviación estándar poblacional>
    Comprueba que `sd` corresponda a la desviación estándar poblacional, no a la muestral.

    ```python
    expected_sd = statistics.pstdev(hba1c)

    assert math.isclose(sd, expected_sd, rel_tol=1e-6), (
        f"La desviación estándar poblacional no es correcta. "
        f"Esperado ≈ {expected_sd:.4f}, obtenido {sd:.4f}. "
        "Asegúrate de usar la función poblacional del módulo `statistics`."
    )

    print(f"Desviación estándar correcta: {expected_sd:.4f}")
    ```
    """,
                r"""
    <Cálculo del z-score>
    Comprueba que `z` haya sido calculado con la fórmula correcta a partir de `nuevo`, `media` y `sd`.

    ```python
    expected_media = statistics.mean(hba1c)
    expected_sd = statistics.pstdev(hba1c)
    expected_z = (nuevo - expected_media) / expected_sd

    assert math.isclose(z, expected_z, rel_tol=1e-6), (
        f"El z-score no es correcto. Esperado ≈ {expected_z:.4f}, "
        f"obtenido {z:.4f}. "
        "Revisa la fórmula: z = (x - media) / sd."
    )

    print(f"Z-score correcto: {expected_z:.4f}")
    ```
    """,
            ],
            namespace=globals()
        )

        return _test_content.render()
    _()

    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 7) `random` como módulo: simulación mínima (didáctica)

    En salud pública es común usar simulaciones sencillas para entender variabilidad
    (p. ej., muestreo de una cohorte “ficticia”).

    Aquí usaremos `random` para generar una muestra de IMC (hipotética) y resumirla.
    """)
    return


@app.cell
def _():
    import random
    import statistics as st

    random.seed(123) # semilla para reproducibilidad

    # IMC ficticio: centrado ~ 26 con variación limitada
    imc_muestra = [round(random.uniform(20, 35), 1) for _ in range(30)]

    print("n =", len(imc_muestra))
    print("media IMC:", round(st.mean(imc_muestra), 2))
    print("min/max:", min(imc_muestra), max(imc_muestra))

    assert len(imc_muestra) == 30
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto 3 (final, guiado) — Pipeline mínimo con imports

    ### Contexto

    Imagina un triage muy simplificado para priorizar seguimiento de **riesgo cardiometabólico**.

    Dispones de dos indicadores clínicos:

    - **IMC (kg/m²)**
    - **Presión arterial sistólica (mmHg)**

    En este ejercicio construirás una función que transforme estos valores en un **puntaje simple de riesgo**.

    El objetivo no es crear un modelo clínico real, sino practicar un **pipeline básico de validación + lógica + control de valores**.

    ### Tu tarea

    Implementar la función:

    ```python
    puntaje_riesgo(imc, pas_sistolica)
    ```

    La función debe:

    1. Validar que las entradas sean numéricas.
    2. Validar que los valores sean positivos.
    3. Construir un **puntaje aditivo** usando rangos.
    4. Asegurar que el puntaje final quede dentro del rango **[0, 10]**.

    ### Reglas

    - Solo puedes usar el módulo `math`.
    - Debes usar `if / elif / else` para definir los rangos.
    - El resultado final debe ser un **int**.

    ### Recomendación

    Divide el problema en pasos pequeños:

    1. validar entradas
    2. calcular el puntaje
    3. limitar el resultado

    Este tipo de estructura es muy común en **pipelines clínicos simples**.
    """)
    return


@app.function
# === TU TURNO (EDITA ESTA CELDA) ===
def puntaje_riesgo(imc, pas_sistolica):
    # 1) Validar tipos numéricos
    # TODO:
    pass

    # 2) Validar positividad
    # TODO:
    pass

    # 3) Puntaje base por rangos
    # TODO: define score = 0 y luego suma según rangos
    score = None

    # 4) Acotar a [0, 10] usando math
    # TODO: clipping con min/max (o floor/ceil si aplica)
    score_final = None
    return score_final


@app.cell(hide_code=True)
def _():
    _tip_content = TipContent(
        items_raw=[
            r"""
    <Estructura del pipeline>

    Empieza separando mentalmente el problema en tres partes:

    1. validación de entradas  
    2. cálculo del puntaje  
    3. control del rango final

    Esto ayuda a que la función sea más clara y fácil de depurar.
    """,
            r"""
    <Validación de entradas>

    Antes de calcular cualquier puntaje:

    - verifica que los valores sean **numéricos**
    - verifica que sean **positivos**

    Puedes reutilizar el patrón que ya usaste en retos anteriores.
    """,
            r"""
    <Puntaje por rangos>

    Una estrategia simple es empezar con:

    ```python
    score = 0
    ```

    Luego sumar puntos dependiendo del rango:

    ```python
    if condicion:
        score += valor
    ```

    Haz esto para **IMC** y **presión sistólica**.
    """,
            r"""
    <Acotar el resultado>

    El puntaje final debe quedar entre **0 y 10**.

    Una forma común de hacerlo es aplicar **clipping**:

    ```python
    score_final = max(0, min(10, score))
    ```

    Esto evita valores fuera del rango esperado.
    """,
            r"""
    <solucion>

    ### Implementación esperada

    ```python
    import math

    def puntaje_riesgo(imc, pas_sistolica):

        # 1. Validar tipos
        if not isinstance(imc, (int, float)) or not isinstance(pas_sistolica, (int, float)):
            raise TypeError("Los valores deben ser numéricos")

        # 2. Validar positividad
        if imc <= 0 or pas_sistolica <= 0:
            raise ValueError("Los valores deben ser positivos")

        # 3. Puntaje base
        score = 0

        # IMC
        if imc >= 35:
            score += 4
        elif imc >= 30:
            score += 3
        elif imc >= 25:
            score += 1

        # Presión sistólica
        if pas_sistolica >= 160:
            score += 4
        elif pas_sistolica >= 140:
            score += 3
        elif pas_sistolica >= 120:
            score += 1

        # 4. Clipping a rango [0, 10]
        score_final = max(0, min(10, score))

        return int(score_final)
    ```

    ### Explicación

    1. Se validan tipos y valores antes de calcular el puntaje.

    2. Se usa un sistema **aditivo**: cada variable suma puntos según su rango.

    3. El puntaje se limita al rango `[0,10]` usando:

    ```python
    max(0, min(10, score))
    ```

    Esto asegura que el valor final nunca salga del rango esperado.
    """
        ]
    )

    _tip_content.render()
    return


@app.cell(hide_code=True)
def _():
    _test_content = TestContent(
        items_raw=[
            r"""
    <Comportamiento básico>
    Comprueba que un perfil de bajo riesgo produzca 0.

    ```python
    assert puntaje_riesgo(22, 110) == 0
    print("Caso basal correcto.")
    ```
    """,
            r"""
    <Rango del puntaje>
    Comprueba que el resultado final quede en el rango [0, 10].

    ```python
    resultado = puntaje_riesgo(40, 180)
    assert 0 <= resultado <= 10
    print("Resultado dentro del rango esperado.")
    ```
    """,
            r"""
    <Validación de tipos>
    La función debe rechazar entradas no numéricas.

    ```python
    try:
        puntaje_riesgo("25", 120)
        raise AssertionError("Se esperaba TypeError para IMC no numérico.")
    except TypeError:
        print("TypeError detectado correctamente.")
    ```
    """,
            r"""
    <solucion>
    Estos tests revisan:

    1. comportamiento básico,
    2. clipping correcto,
    3. validación de errores.
    """,
        ],
        namespace=globals(),
    )

    puntaje_riesgo
    mo.accordion(_test_content.items)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Cierre

    Lo esencial que debes llevarte:

    - `import modulo` crea un **namespace** y mejora trazabilidad.
    - `import ... as ...` reduce ruido cuando el módulo se usa mucho.
    - `from modulo import x` simplifica llamadas, pero puede crear colisiones.
    - “Módulo” es la unidad básica de reutilización; “librería” es el conjunto funcional que consumes en tu proyecto.
    """)
    return


if __name__ == "__main__":
    app.run()
