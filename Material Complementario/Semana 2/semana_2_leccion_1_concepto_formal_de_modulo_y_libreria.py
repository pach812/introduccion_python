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
    # Semana 2 — Lección 1
    ## Concepto formal de módulo y librería

    ### Propósito
    Formalizar **cómo se organiza código en Python** y cómo se reutiliza mediante `import`.

    En esta sesión vas a:
    - Diferenciar **script** vs **módulo** (y ubicar **paquete** y **librería** como conceptos del ecosistema).
    - Usar `import`, `from ... import ...` y **alias**.
    - Reconocer **espacios de nombres** (namespaces) como mecanismo para evitar colisiones.
    - Aplicar imports en mini-tareas orientadas a **salud / salud pública**.

    > Nota: Esta lección usa exclusivamente conceptos ya vistos (variables, funciones, condicionales, bucles, listas/diccionarios y comprensiones) y agrega el foco en `import`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
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
def _(mo):
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
def _(mo):
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
def _(mo):
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
def _(mo):
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
def _(mo):
    mo.md(r"""
    ## Mini-reto 1 (guiado) — Dosis por kg con redondeo seguro

    Contexto clínico:
    Vas a preparar una dosis proporcional al peso (mg/kg) y quieres **redondear hacia arriba**
    para no quedarte corto por el redondeo (situación hipotética de práctica pedagógica).

    **Tu tarea:** completar la función `dosis_total_mg(...)` usando `math.ceil`.

    Requisitos:
    1. `peso_kg` y `mg_por_kg` deben ser numéricos.
    2. Deben ser positivos.
    3. Retornar dosis total en mg (entero) redondeada hacia arriba.
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
def _(mo):
    _tip_content = mo.md(
        r"""
    - Recuerda el patrón de validación:
      - `isinstance(x, (int, float))`
      - Comprobar que `x > 0`
    - La dosis sin redondeo es: `peso_kg * mg_por_kg`
    - Para redondear hacia arriba: `math.ceil(...)`
    - La salida debería ser un **int**.

    > Evita “adivinar”: imprime resultados intermedios solo mientras pruebas.
    """
    )

    mo.accordion({"### Tip (Mini-reto 1)": _tip_content})
    return


@app.cell
def _():
    # Tests mínimos (no cambies estos asserts)
    # Nota: estos asserts asumen que implementaste la función.
    try:
        assert dosis_total_mg(70, 1.5) == 105
        assert dosis_total_mg(70, 1.51) == 106
    except TypeError:
        # Si todavía tienes pass, este bloque evita que el notebook se rompa
        # mientras editas. Cuando termines, debería no entrar aquí.
        pass
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6) Buenas prácticas mínimas de import

    1) Importa al inicio del archivo (en marimo, típicamente al inicio de la celda).
    2) Prefiere `import modulo` cuando:
       - quieres claridad de procedencia (`statistics.mean`, `math.sqrt`)
       - deseas evitar colisiones de nombres
    3) Usa `from modulo import x` cuando:
       - `x` es muy usado y el contexto lo hace inequívoco
    4) Usa alias con moderación (`import statistics as st`) cuando:
       - mejora legibilidad en un bloque largo

    En general: prioriza **legibilidad y trazabilidad**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Mini-reto 2 (guiado) — Corregir imports y colisiones

    Contexto: análisis rápido de un indicador clínico.

    Tienes una lista de valores (por ejemplo, **HbA1c** en %) y deseas:
    - media y desviación estándar (poblacional),
    - un “z-score” simple para un valor nuevo.

    **Tu tarea:** completar los espacios `TODO` para que el bloque funcione.

    Reglas:
    - Debes usar el módulo `statistics`.
    - Debes evitar sombrear nombres (por ejemplo, no uses `mean = ...`).
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
def _(mo):
    _tip_content = mo.md(
        r"""
    - `statistics.mean(lista)` calcula la media.
    - `statistics.pstdev(lista)` calcula la desviación estándar **poblacional**.
    - Alias típico: `import statistics as st` → `st.mean(...)`, `st.pstdev(...)`
    - Asegúrate de que `sd` no sea 0 (con datos reales esto se valida).
    """
    )

    mo.accordion({"### Tip (Mini-reto 2)": _tip_content})
    return


@app.cell
def _():
    def _():
        # Tests de referencia para el mini-reto 2.
        # (No dependen de tu alias; validan solo el resultado esperado.)
        import statistics as _st

        hba1c = [5.4, 5.8, 6.1, 5.6, 5.9, 6.5, 5.7]
        nuevo = 6.2
        media_ref = _st.mean(hba1c)
        sd_ref = _st.pstdev(hba1c)
        z_ref = (nuevo - media_ref) / sd_ref

        assert round(media_ref, 6) == round(5.857142857142857, 6)
        assert sd_ref > 0
        assert z_ref > 0
        return

    _()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7) `random` como módulo: simulación mínima (didáctica)

    En salud pública es común usar simulaciones sencillas para entender variabilidad
    (p. ej., muestreo de una cohorte “ficticia”).

    Aquí usaremos `random` para generar una muestra de IMC (hipotética) y resumirla.

    > Esto NO reemplaza análisis real: es un ejemplo controlado para practicar imports.
    """)
    return


@app.cell
def _():
    import random
    import statistics as st

    random.seed(123)

    # IMC ficticio: centrado ~ 26 con variación limitada
    imc_muestra = [round(random.uniform(20, 35), 1) for _ in range(30)]

    print("n =", len(imc_muestra))
    print("media IMC:", round(st.mean(imc_muestra), 2))
    print("min/max:", min(imc_muestra), max(imc_muestra))

    assert len(imc_muestra) == 30
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Mini-reto 3 (final, guiado) — Pipeline mínimo con imports

    Contexto: triage muy simplificado (didáctico) para priorizar seguimiento de riesgo cardiometabólico
    a partir de:
    - IMC (kg/m²)
    - Presión arterial sistólica (mmHg)

    **Objetivo:** implementar `puntaje_riesgo(...)` que:
    1) Valide entradas numéricas y positivas.
    2) Construya un puntaje aditivo:
       - IMC alto suma más,
       - PA sistólica alta suma más.
    3) Use `math` para **acotar** el puntaje a un rango [0, 10] (clipping).

    Reglas:
    - Solo puedes usar `import math` (o alias).
    - Debes usar `if/elif/else` para definir rangos.
    - Retorna un `int`.
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
def _(mo):
    tip_content = mo.md(r"""
    ### Tip (Mini-reto 3)

    - Una estrategia simple:
      - `score = 0`
      - Si `imc` está en cierto rango, `score += ...`
      - Si `pas_sistolica` está en cierto rango, `score += ...`
    - Para “clipping”:
      - `score_final = max(0, min(10, score))`
    - Mantén el puntaje como entero.
    """)
    return


@app.cell
def _():
    # Tests mínimos (no cambies estos asserts)
    try:
        assert puntaje_riesgo(22, 110) == 0
        assert 0 <= puntaje_riesgo(40, 180) <= 10
        assert puntaje_riesgo(30, 140) >= puntaje_riesgo(23, 110)
    except TypeError:
        pass
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cierre

    Lo esencial que debes llevarte:

    - `import modulo` crea un **namespace** y mejora trazabilidad.
    - `import ... as ...` reduce ruido cuando el módulo se usa mucho.
    - `from modulo import x` simplifica llamadas, pero puede crear colisiones.
    - “Módulo” es la unidad básica de reutilización; “librería” es el conjunto funcional que consumes en tu proyecto.

    Siguiente: consolidaremos estas ideas para entender cómo se organizan proyectos
    más grandes dentro del ecosistema científico (sin adelantar contenido).
    """)
    return


if __name__ == "__main__":
    app.run()
