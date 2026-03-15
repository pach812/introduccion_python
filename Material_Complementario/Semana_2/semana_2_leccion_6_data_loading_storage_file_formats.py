# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "numpy==2.4.2",
#     "pandas==3.0.1",
#     "pytest==9.0.2",
#     "requests==2.32.5",
#     "pyreadr==0.5.4",
# ]
# ///

import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")

with app.setup(hide_code=True):
    import json
    from pathlib import Path

    import marimo as mo
    import numpy as np
    import pandas as pd
    from setup import TipContent, TestContent


@app.cell(hide_code=True)
def _():
    try:
        import pyreadr
        use_r = True
        msg = "Inicio de actividad con soporte para archivos `.rds` de R."
    except ImportError:
        use_r = False
        msg = mo.md(r""" No se pudo instalar la librería `pyreadr`. Si quieres trabajar con archivos `.rds`, asegúrate de tener esta dependencia instalada en tu entorno de Python desde tu ordenador.

        Deberas saltar las partes relacionadas con archivos `.rds` en esta sesión, pero puedes seguir trabajando con los otros formatos sin problemas.""") 
    msg
    return pyreadr, use_r


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Semana 2 · Lección 6
    ## Carga de datos, almacenamiento y formatos de archivo

    **Idea central:** analizar datos no comienza en el cálculo, sino en la **entrada correcta de la información**.

    Antes de resumir, filtrar o transformar un dataset, necesitamos responder tres preguntas:

    1. **¿Dónde están los datos?**
       En un archivo de texto, un CSV, un TSV, un JSON, un archivo de Stata o un archivo serializado desde R.

    2. **¿Cómo están organizados?**
       Como texto libre, como tabla delimitada, como estructuras clave-valor o como objetos tabulares guardados por software estadístico.

    3. **¿Con qué herramienta conviene leerlos?**
       A veces basta con `open()`. En otras, `pandas.read_csv()`, `pandas.read_stata()` o `pyreadr.read_r()` permiten cargar directamente una estructura útil para análisis.

    En esta sesión construiremos una transición formal desde:

    **archivo en disco → lectura → interpretación estructurada → almacenamiento reproducible**
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Propósitos de aprendizaje

    Al finalizar la sesión deberías poder:

    - distinguir entre **texto plano**, **CSV**, **TSV**, **JSON**, **Stata (`.dta`)** y **RDS (`.rds`)**,
    - leer archivos simples con Python usando `open()`,
    - cargar tablas con pandas usando `read_csv()` y `read_stata()`,
    - leer objetos tabulares de R con `pyreadr.read_r()`,
    - controlar separadores y encabezados básicos,
    - guardar resultados con `to_csv()`,
    - y justificar por qué el formato de almacenamiento influye en la reproducibilidad del análisis.

    Trabajaremos exclusivamente con ejemplos de salud pública y datos clínicos sintéticos.
    """)
    return


@app.cell(hide_code=True)
def _(pyreadr, use_r):
    data_dir = Path("datos_leccion")
    data_dir.mkdir(exist_ok=True)

    pacientes_base = pd.DataFrame(
        {
            "id_paciente": [101, 102, 103, 104, 105, 106],
            "edad": [67, 54, 72, 49, 61, 58],
            "sexo": ["female", "male", "female", "female", "male", "male"],
            "hospital": [
                "Hospital Norte",
                "Hospital Sur",
                "Hospital Norte",
                "Hospital Centro",
                "Hospital Sur",
                "Hospital Centro",
            ],
            "diagnostico": ["HTN", "T2D", "HTN", "ASTHMA", "COPD", "T2D"],
            "pas": [148, 136, 154, 118, 142, 130],
            "dias_seguimiento": [30, 90, 30, 180, 60, 90],
        }
    )

    pacientes_base.to_csv(data_dir / "pacientes.csv", index=False)
    pacientes_base.to_csv(data_dir / "pacientes.tsv", sep="\t", index=False)
    pacientes_base.to_stata(data_dir / "pacientes_stata.dta", write_index=False)
    if use_r:
        pyreadr.write_rds(data_dir / "pacientes_r.rds", pacientes_base)


    lineas_notas = [
        "id_paciente|nota",
        "101|Presion arterial elevada en la primera visita",
        "102|Se recomienda control de HbA1c",
        "103|Se requiere repetir la medicion de presion arterial",
        "104|Sintomas respiratorios estables",
    ]
    (data_dir / "notas_clinicas.txt").write_text(
        "\n".join(lineas_notas),
        encoding="utf-8",
    )

    contenido_json = [
        {
            "id_paciente": 101,
            "vacunado_influenza": True,
            "comunidad": "urbana",
        },
        {
            "id_paciente": 102,
            "vacunado_influenza": False,
            "comunidad": "rural",
        },
        {
            "id_paciente": 103,
            "vacunado_influenza": True,
            "comunidad": "urbana",
        },
    ]
    (data_dir / "vacunacion.json").write_text(
        json.dumps(contenido_json, indent=2),
        encoding="utf-8",
    )

    indice_archivos = pd.DataFrame(
        {
            "nombre_archivo": [
                "pacientes.csv",
                "pacientes.tsv",
                "notas_clinicas.txt",
                "vacunacion.json",
                "pacientes_stata.dta",
                "pacientes_r.rds",
            ],
            "formato": ["csv", "tsv", "txt", "json", "dta", "rds"],
            "estructura_principal": [
                "tabla delimitada por comas",
                "tabla delimitada por tabulaciones",
                "texto plano linea por linea",
                "lista de diccionarios",
                "tabla tabular de Stata",
                "objeto tabular serializado desde R",
            ],
        }
    )

    indice_archivos
    return (data_dir,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 1) El mismo fenómeno puede almacenarse de varias maneras

    Un dataset no es solo “datos”. También es una **convención de almacenamiento**.

    En esta lección usaremos seis formatos frecuentes:

    - **TXT**: útil para texto libre o registros línea por línea.
    - **CSV**: útil para tablas delimitadas por coma.
    - **TSV**: similar al CSV, pero usa tabulación como separador.
    - **JSON**: útil para estructuras más flexibles basadas en clave-valor.
    - **Stata (`.dta`)**: útil cuando los datos provienen de flujos estadísticos en Stata.
    - **RDS (`.rds`)**: útil cuando los datos fueron guardados como objeto desde R.

    Ningún formato es “el mejor” en abstracto.

    Su utilidad depende de la estructura de los datos, del software de origen y del objetivo analítico.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 2) Texto plano con `open()`

    Cuando un archivo no es todavía una tabla limpia, conviene empezar por la lectura más elemental.

    Con `open()` podemos:

    - abrir un archivo,
    - leer su contenido completo o línea por línea,
    - inspeccionar su estructura real,
    - y decidir después cómo convertirlo en una tabla.

    Esta inspección es importante porque muchos errores analíticos no provienen del modelo,
    sino de haber supuesto mal el formato de entrada.
    """)
    return


@app.cell(hide_code=True)
def _(data_dir):
    ruta_notas = data_dir / "notas_clinicas.txt"

    with open(ruta_notas, encoding="utf-8") as archivo_notas:
        notes_text = archivo_notas.read()

    notes_lines = notes_text.splitlines()

    assert len(notes_lines) == 5
    assert notes_lines[0] == "id_paciente|nota"
    return (notes_text,)


@app.cell(hide_code=True)
def _(notes_text):
    mo.vstack(
        [
            mo.md(r"""
    Observa que este archivo **todavía no fue tratado como una tabla de pandas**.

    Primero lo interpretamos como texto. Eso permite reconocer:

    - el separador real (`|`),
    - la fila de encabezado,
    - y el hecho de que cada línea representa un registro.

    Ese diagnóstico preliminar orienta la siguiente decisión de carga.

    ---
    """),
            mo.md("### Vista cruda del archivo"),
            mo.md(f"```text\n{notes_text}\n```"),
        ]
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto 1 — Contar registros clínicos en un archivo de texto

    Queremos determinar cuántos registros reales contiene `notas_clinicas.txt`.

    Recuerda:

    - la primera línea corresponde al encabezado,
    - las demás líneas representan observaciones,
    - y ya dispones de una lista con el contenido separado por líneas.

    Antes de escribir código, piensa cuál es exactamente la diferencia entre:

    - número total de líneas,
    - y número real de registros.
    """)
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    n_registros_notas = None
    return


@app.cell(hide_code=True)
def _():
    tip_content_reto_1 = TipContent(
        items_raw=[
            r"""
    <Encabezado vs datos>
    No todas las líneas del archivo representan observaciones clínicas.

    Primero identifica cuál línea cumple una función estructural y no debe contarse como dato.
    """,
            r"""
    <Pensar en la lista completa>
    Ya tienes las líneas separadas en una lista.

    A partir de esa estructura, el conteo correcto debería salir de una operación muy simple.
    """,
            r"""
    <solucion>

    ```python
    n_registros_notas = len(notes_lines) - 1
    ```
    """,
        ]
    )

    tip_content_reto_1.render()
    return


@app.cell(hide_code=True)
def _():
    test_content_reto_1 = TestContent(
        items_raw=[
            r"""
    <Valor definido>
    Verifica que hayas asignado un valor a la variable pedida.

    ```python
    assert n_registros_notas is not None, (
        "Debes asignar un valor a `n_registros_notas`."
    )
    print("Variable definida correctamente.")
    ```
    """,
            r"""
    <Conteo correcto>
    Verifica que el conteo incluya solo filas de datos y no el encabezado.

    ```python
    assert n_registros_notas == 4, (
        "Debes contar solo las filas de datos, no el encabezado."
    )
    print("Conteo correcto.")
    ```
    """,
        ],
        namespace=globals(),
    )

    test_content_reto_1.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 3) De texto tabular a `DataFrame` con `read_csv()`

    Cuando el archivo ya tiene estructura rectangular, `pandas.read_csv()` permite cargarlo como tabla de trabajo.

    Aunque el nombre de la función dice `csv`, también puede leer otros delimitadores
    si especificamos el argumento `sep`.

    Conceptualmente, `read_csv()` hace dos cosas a la vez:

    1. **lee** el archivo,
    2. **interpreta** su contenido como tabla.

    Ese paso es importante porque a partir de ahí podemos aplicar selección,
    filtrado, descripción y transformación con la sintaxis tabular de pandas.
    """)
    return


@app.cell
def _(data_dir):
    pacientes_csv = pd.read_csv(data_dir / "pacientes.csv")

    assert pacientes_csv.shape == (6, 7)
    assert list(pacientes_csv.columns) == [
        "id_paciente",
        "edad",
        "sexo",
        "hospital",
        "diagnostico",
        "pas",
        "dias_seguimiento",
    ]

    pacientes_csv
    return (pacientes_csv,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Aquí cada fila representa un paciente y cada columna una variable.

    Una vez cargado el archivo como `DataFrame`, ya podemos trabajar con operaciones conocidas:

    - inspección,
    - selección,
    - filtros,
    - descripciones resumidas.
    """)
    return


@app.cell
def _(pacientes_csv):
    pacientes_csv.describe(include="all")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 4) El separador importa

    Dos archivos pueden contener la misma información y, aun así, no usar el mismo separador.

    Si un archivo TSV se lee como si fuera CSV, pandas no separará correctamente las columnas.

    Por eso, cuando el delimitador no es la coma, debemos declararlo explícitamente.
    """)
    return


@app.cell
def _(data_dir):
    pacientes_tsv = pd.read_csv(data_dir / "pacientes.tsv", sep="\t")

    assert pacientes_tsv.equals(pd.read_csv(data_dir / "pacientes.csv"))

    pacientes_tsv
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto 2 — Cargar un archivo con separador no estándar

    Ahora debes cargar `notas_clinicas.txt` como una tabla.

    Ya sabes que:

    - el archivo usa `|` como separador,
    - la primera línea contiene encabezados,
    - y el resultado debe ser un `DataFrame` con dos columnas.

    Antes de programar, piensa:

    - qué función sigue siendo válida aunque el archivo termine en `.txt`,
    - qué argumento controla el separador,
    - y cómo comprobarías después que la carga quedó bien.
    """)
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    notes_df = None
    return


@app.cell(hide_code=True)
def _():
    tip_content_reto_2 = TipContent(
        items_raw=[
            r"""
    <Extensión vs estructura>
    La extensión `.txt` no impide que el archivo pueda leerse como tabla.

    Lo importante no es el nombre del archivo, sino la forma en que están delimitadas sus columnas.
    """,
            r"""
    <Separador explícito>
    El paso clave consiste en indicar correctamente cómo se separan los campos.

    Sin ese detalle, pandas no podrá reconstruir la tabla como esperas.
    """,
            r"""
    <Validar la carga>
    Después de leer el archivo, conviene revisar forma y nombres de columnas.

    Eso te permite confirmar que la interpretación estructural fue correcta.
    """,
            r"""
    <solucion>

    ```python
    notes_df = pd.read_csv(data_dir / "notas_clinicas.txt", sep="|")
    ```
    """,
        ]
    )

    tip_content_reto_2.render()
    return


@app.cell(hide_code=True)
def _():
    test_content_reto_2 = TestContent(
        items_raw=[
            r"""
    <Objeto creado>
    Verifica que hayas construido una tabla.

    ```python
    assert notes_df is not None, (
        "Debes asignar un DataFrame a `notes_df`."
    )
    print("DataFrame definido correctamente.")
    ```
    """,
            r"""
    <Forma esperada>
    Verifica que la tabla tenga el tamaño correcto.

    ```python
    assert notes_df.shape == (4, 2), (
        "La tabla debe tener 4 filas y 2 columnas."
    )
    print("Forma correcta.")
    ```
    """,
            r"""
    <Columnas correctas>
    Verifica que los nombres de columnas coincidan con la estructura esperada.

    ```python
    assert list(notes_df.columns) == ["id_paciente", "nota"], (
        "Las columnas deben ser `id_paciente` y `nota`."
    )
    print("Columnas correctas.")
    ```
    """,
        ],
        namespace=globals(),
    )

    test_content_reto_2.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 5) JSON como estructura clave-valor

    No todos los datos llegan como tabla plana.

    En salud es frecuente encontrar estructuras donde cada registro se representa como
    un pequeño diccionario con claves semánticas, por ejemplo:

    - identificador,
    - estado vacunal,
    - pertenencia comunitaria,
    - atributos administrativos.

    JSON es útil cuando los datos conservan una organización más flexible que un CSV.

    En Python puede leerse primero con `json.load()` y luego convertirse a `DataFrame` si conviene.
    """)
    return


@app.cell
def _(data_dir):
    ruta_json = data_dir / "vacunacion.json"

    with open(ruta_json, encoding="utf-8") as archivo_json:
        vaccination_raw = json.load(archivo_json)

    vaccination_df = pd.DataFrame(vaccination_raw)

    assert vaccination_df.shape == (3, 3)
    assert set(vaccination_df.columns) == {
        "id_paciente",
        "vacunado_influenza",
        "comunidad",
    }

    vaccination_df
    return (vaccination_raw,)


@app.cell(hide_code=True)
def _(vaccination_raw):
    mo.vstack([mo.md(r"""
    Aquí el paso conceptual fue diferente:

    - primero cargamos una **lista de diccionarios**,
    - después la convertimos a tabla.

    Esto muestra que **tabularizar** no siempre es el primer paso,
    pero sí suele ser el paso que habilita el análisis sistemático.
    """),
    mo.md(f"```python\n{vaccination_raw}\n```")])
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 6) Archivos de Stata (`.dta`)

    En muchos equipos de investigación y salud pública, los datos circulan entre distintos programas estadísticos.

    Uno de los formatos frecuentes es **Stata (`.dta`)**.

    Cuando un archivo proviene de Stata y representa una tabla rectangular,
    pandas permite leerlo directamente con `read_stata()`.

    La ventaja conceptual es que no necesitamos “convertirlo a CSV” manualmente antes de analizarlo.
    """)
    return


@app.cell
def _(data_dir):
    pacientes_stata = pd.read_stata(data_dir / "pacientes_stata.dta")

    assert pacientes_stata.shape == (6, 7)
    assert list(pacientes_stata.columns) == [
        "id_paciente",
        "edad",
        "sexo",
        "hospital",
        "diagnostico",
        "pas",
        "dias_seguimiento",
    ]

    pacientes_stata
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Desde el punto de vista analítico, una vez cargado el archivo de Stata como `DataFrame`,
    el trabajo posterior es el mismo que con un CSV:

    - selección,
    - filtrado,
    - resumen,
    - exportación.

    Lo importante es reconocer que el **formato de origen cambia la función de lectura**,
    pero no necesariamente la lógica analítica posterior.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 7) Archivos de R (`.rds`)

    En ecosistemas de análisis con R, es muy común guardar objetos con extensión `.rds`.

    Un archivo `.rds` puede contener un objeto serializado, por ejemplo:

    - un `data.frame`,
    - una tabla procesada,
    - una salida intermedia del análisis.

    Para leer este tipo de archivo desde Python, una herramienta útil es `pyreadr`.

    Conceptualmente, aquí la idea no es “leer texto delimitado”, sino **recuperar un objeto que ya fue guardado por otro entorno estadístico**.
    """)
    return


@app.cell(hide_code=True)
def _(data_dir, pyreadr, use_r):
    if use_r:
        resultado_rds = pyreadr.read_r(data_dir / "pacientes_r.rds")
        rds_keys = list(resultado_rds.keys())
        pacientes_rds = resultado_rds[None]

        assert pacientes_rds.shape == (6, 7)
        assert list(pacientes_rds.columns) == [
            "id_paciente",
            "edad",
            "sexo",
            "hospital",
            "diagnostico",
            "pas",
            "dias_seguimiento",
        ]

        pacientes_rds
    else:
        rds_keys = None
        mo.md(r"""No se pudo leer el archivo `.rds` porque no está disponible la librería `pyreadr`. Si quieres trabajar con archivos `.rds`, asegúrate de tener esta dependencia instalada en tu entorno de Python desde tu ordenador. Deberas saltar las partes relacionadas con archivos `.rds` en esta sesión, pero puedes seguir trabajando con los otros formatos sin problemas.""")
    return (rds_keys,)


@app.cell(hide_code=True)
def _(rds_keys):
    mo.md(rf"""
    En un archivo `.rds`, normalmente recuperamos un solo objeto.

    En este caso, el contenido puede convertirse directamente en una tabla de pandas y continuar el análisis como de costumbre.

    Esto es especialmente útil cuando colaboras con equipos que trabajan en R y necesitas reutilizar sus salidas sin rehacer toda la exportación a mano.


    Claves recuperadas al leer el archivo RDS: {rds_keys}
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 8) Almacenar resultados: guardar también es parte del análisis

    Un análisis reproducible no solo lee datos: también **escribe salidas**.

    Guardar resultados permite:

    - compartir tablas limpias,
    - documentar pasos intermedios,
    - evitar rehacer procesos manuales,
    - y dejar evidencia del estado de un análisis en un momento dado.

    En contextos de salud pública, esto es importante para auditoría, trazabilidad y comunicación entre equipos.
    """)
    return


@app.cell
def _(data_dir, pacientes_csv):
    pacientes_hta = pacientes_csv.loc[
        pacientes_csv["diagnostico"] == "HTN",
        ["id_paciente", "hospital", "pas", "dias_seguimiento"],
    ]

    output_path = data_dir / "pacientes_hta_exportacion.csv"
    pacientes_hta.to_csv(output_path, index=False)

    recargado_hta = pd.read_csv(output_path)

    assert recargado_hta.equals(pacientes_hta.reset_index(drop=True))

    recargado_hta
    return (output_path,)


@app.cell(hide_code=True)
def _(output_path):
    mo.vstack(
        [
            mo.md(r"""
    En este punto ya cerramos un ciclo mínimo completo:

    **archivo original → carga → selección analítica → nuevo archivo de salida**

    Ese ciclo es la base de muchos pipelines posteriores.
    """),
            mo.md(f"Archivo generado: '{output_path}'")
        ]
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 9) Comparación conceptual de formatos

    Una misma cohorte puede almacenarse de maneras distintas.

    La decisión depende de la pregunta, de la estructura y del software de origen:

    - **TXT**: útil para texto libre, notas o inspección manual.
    - **CSV/TSV**: útil para tablas simples, intercambio y análisis tabular.
    - **JSON**: útil para estructuras más flexibles o semánticas.
    - **Stata (`.dta`)**: útil cuando el flujo proviene de Stata.
    - **RDS (`.rds`)**: útil cuando los datos fueron guardados como objeto desde R.

    En términos didácticos, conviene pensar así:

    - si el archivo ya “parece una tabla”, pandas suele ser una buena puerta de entrada;
    - si el archivo viene de otro software estadístico, conviene usar el lector específico;
    - si el archivo no es todavía claramente tabular, conviene inspeccionarlo primero como texto.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Ejercicio guiado de aplicación

    Supón que recibes un archivo exportado desde vigilancia epidemiológica o desde otro equipo analítico.

    Antes de abrirlo, conviene formular estas preguntas:

    1. ¿Cada fila representa un caso, una visita o una persona?
    2. ¿Cuál es el separador real, si existe uno?
    3. ¿La primera fila contiene encabezados?
    4. ¿El archivo parece texto libre, tabla delimitada u objeto serializado?
    5. ¿Proviene de otro software como Stata o R?
    6. ¿La salida del análisis debe guardarse para uso posterior?

    Estas preguntas no son accesorias.

    Forman parte del razonamiento analítico.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto 3 — Resumen final y salida tabular mínima

    Construye una tabla llamada `resumen_seguimiento` a partir de `pacientes_csv`.

    La tabla final debe representar un resumen por diagnóstico.

    Requisitos conceptuales:

    - una fila por diagnóstico,
    - una métrica promedio de seguimiento,
    - nombres de columnas claros,
    - y orden estable en la salida.

    Antes de programar, piensa:

    - cuál será la unidad analítica final del resultado,
    - qué variable numérica debe resumirse,
    - y cómo dejar la tabla lista para ser compartida o exportada.
    """)
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    resumen_seguimiento = None
    return


@app.cell(hide_code=True)
def _():
    tip_content_reto_3 = TipContent(
        items_raw=[
            r"""
    <Unidad del resultado>
    La tabla final ya no representa pacientes individuales.

    Debe representar grupos definidos por diagnóstico.
    """,
            r"""
    <Métrica resumida>
    Solo necesitas resumir una variable numérica dentro de cada grupo.

    Identifica cuál es esa variable y qué función de agregación corresponde.
    """,
            r"""
    <Salida clara>
    Una tabla útil no solo calcula bien: también nombra bien sus columnas y mantiene un orden consistente.

    Eso la vuelve más fácil de interpretar y reutilizar.
    """,
            r"""
    <solucion>

    ```python
    resumen_seguimiento = (
        pacientes_csv.groupby("diagnostico", as_index=False)
        .agg(media_dias_seguimiento=("dias_seguimiento", "mean"))
        .sort_values("diagnostico")
        .reset_index(drop=True)
    )
    ```
    """,
        ]
    )

    tip_content_reto_3.render()
    return


@app.cell(hide_code=True)
def _():
    test_content_reto_3 = TestContent(
        items_raw=[
            r"""
    <Objeto definido>
    Verifica que hayas construido una tabla final.

    ```python
    assert resumen_seguimiento is not None, (
        "Debes asignar un DataFrame a `resumen_seguimiento`."
    )
    print("Tabla definida correctamente.")
    ```
    """,
            r"""
    <Columnas esperadas>
    Verifica que la salida use nombres de columnas claros y exactos.

    ```python
    assert list(resumen_seguimiento.columns) == [
        "diagnostico",
        "media_dias_seguimiento",
    ], (
        "Las columnas deben ser `diagnostico` y `media_dias_seguimiento`."
    )
    print("Columnas correctas.")
    ```
    """,
            r"""
    <Estructura y orden>
    Verifica que haya una fila por diagnóstico y que el resultado esté ordenado.

    ```python
    assert resumen_seguimiento.shape[0] == 4, (
        "Debe haber una fila por diagnóstico."
    )
    assert list(resumen_seguimiento["diagnostico"]) == sorted(
        resumen_seguimiento["diagnostico"].tolist()
    ), (
        "La tabla debe quedar ordenada por diagnóstico."
    )
    print("Estructura y orden correctos.")
    ```
    """,
        ],
        namespace=globals(),
    )

    test_content_reto_3.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Cierre conceptual

    En esta sesión no estudiamos todavía limpieza avanzada ni conexión con bases de datos.

    El foco estuvo en algo más fundamental:

    **cómo entra y cómo sale la información**.

    Idea de cierre:

    > una parte importante del análisis de datos consiste en reconocer correctamente la forma del archivo antes de operar sobre él.

    Si puedes identificar:

    - qué representa cada fila,
    - cómo se separan las columnas,
    - qué herramienta conviene usar para leer,
    - cuándo hace falta un lector específico para Stata o R,
    - y cómo guardar una salida reproducible,

    entonces ya controlas el primer tramo formal de un pipeline analítico.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Resumen operativo

    Hoy usamos estas ideas clave:

    - `open()` para inspección básica de archivos de texto,
    - `pd.read_csv()` para carga tabular,
    - `sep=` para declarar delimitadores,
    - `json.load()` para estructuras clave-valor,
    - `pd.read_stata()` para archivos de Stata,
    - `pyreadr.read_r()` para archivos `.rds` de R,
    - `pd.DataFrame()` para tabularizar,
    - `to_csv()` para guardar resultados.

    Estas operaciones parecen simples, pero sostienen gran parte del trabajo posterior en análisis de datos.
    """)
    return


if __name__ == "__main__":
    app.run()
