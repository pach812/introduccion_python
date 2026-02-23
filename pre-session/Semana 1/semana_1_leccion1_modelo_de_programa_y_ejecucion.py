import marimo

__generated_with = "0.19.11"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    img_path = mo.notebook_dir() / "public"
    return img_path, mo


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Semana 1 · Lección 1 — Modelo de programa y ejecución (Python)

    ## Propósito

    En esta lección se construye una idea operativa y verificable de qué es un *programa* en Python y qué significa que el intérprete lo ejecute **de forma secuencial**.

    El objetivo no es memorizar comandos, sino comprender el modelo mental mínimo para:

    - Escribir instrucciones en un orden lógico.
    - Predecir qué ocurrirá cuando el intérprete “lea” el código.
    - Interpretar errores como parte del proceso formal de depuración.
    """)
    return


@app.cell(hide_code=True)
def _(img_path, mo):
    mo.md(rf"""
    ## 1) ¿Qué es un programa?

    Un **programa** es una *secuencia* de instrucciones escritas en un lenguaje que el computador puede ejecutar.

    En Python:

    - Un archivo con extensión `.py` suele llamarse **script**.
    - El **intérprete** de Python ejecuta el programa instrucción por instrucción.
    - En un notebook (como marimo), se ejecutan celdas; **dentro de cada celda**, la ejecución también es secuencial.

    {mo.image(src=img_path/"Gemini_Generated_Image_q81h44q81h44q81h-2.png")}
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2) La idea clave: ejecución secuencial

    La ejecución secuencial significa:

    1. Python empieza arriba.
    2. Ejecuta la primera instrucción.
    3. Continúa con la siguiente, en orden, hasta terminar el archivo (o la celda).

    Esto es crucial para salud pública, porque análisis reproducibles (por ejemplo, un resumen diario de vigilancia epidemiológica) dependen de que el flujo sea:

    **entrada → procesamiento → salida**, en un orden estable y auditable.
    """)
    return


@app.cell
def _():
    # Demostración mínima de ejecución secuencial (salud pública)
    print("Informe de vigilancia — ejemplo mínimo")
    print("1) Recolección: consolidar notificaciones del día")
    print("2) Procesamiento: verificar consistencia básica de los registros")
    print("3) Salida: preparar resumen para el equipo de respuesta")
    return


@app.cell(hide_code=True)
def _(img_path, mo):
    mo.md(rf"""
    ## 3) Dos modos comunes de ejecutar Python

    ### 3.1 Modo interactivo (conversación)
    En el intérprete (por ejemplo, al ejecutar `python` en una terminal), aparece un prompt `>>>`.
    Ese prompt se puede leer como: **“¿qué quieres que ejecute ahora?”**.

    Este modo se usa para probar ideas rápidamente.

    {mo.image(src=img_path/"interpreter.png")}


    ### 3.2 Modo script (archivo `.py`)
    En lugar de escribir una línea a la vez, se ejecuta un archivo completo:

    - Escribes el código en un `.py`.
    - Ejecutas el archivo con Python.
    - Python recorre el archivo de arriba hacia abajo.

    {mo.image(src=img_path/"script.png")}

    **Marimo** es un entorno intermedio: combina un documento explicativo con celdas ejecutables para aprendizaje y demostración.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4) ¿Qué puede salir mal?

    En esta etapa inicial, lo más importante es reconocer que los errores **no** son un fracaso: son señales del intérprete para que ajustemos el código.

    Tres categorías útiles:

    - **Errores de sintaxis (SyntaxError):** la “gramática” del código no es válida.
    - **Errores en tiempo de ejecución (Runtime error):** el código es “legible” pero algo falla al ejecutarlo.
    - **Errores semánticos o lógicos:** el programa corre, pero produce un resultado distinto al que querías.

    En esta lección nos concentramos en el modelo de ejecución; los mecanismos formales de manejo de errores se abordarán más adelante.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejemplo conceptual de error de sintaxis (NO ejecutar)

    Si se escribe mal una instrucción, el intérprete no puede continuar.

    ```python
    pritn("Hola")  # error: nombre mal escrito
    ```

    La idea pedagógica aquí es simple:

    - Python necesita instrucciones **precisas**.
    - Un detalle pequeño puede detener la ejecución del programa.

    (En la práctica, aprenderemos a leer cuidadosamente el mensaje de error).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5) Mini-laboratorio guiado: “tres líneas, una historia”

    La meta es practicar el modelo mental:

    - Cada línea se ejecuta en orden.
    - El orden define el “relato” del programa.

    ### Actividad A (demostración)
    En el siguiente bloque, observa cómo el programa produce una narrativa ordenada sobre una jornada de vacunación.
    """)
    return


@app.cell
def _():
    print("Jornada de vacunación — narrativa secuencial")
    print("Paso 1: Recepción de biológicos y verificación de cadena de frío")
    print("Paso 2: Registro de personas vacunadas en el sistema")
    print("Paso 3: Cierre: consolidación y reporte de dosis aplicadas")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Actividad B (TU TURNO)

    **Instrucciones:**

    1. Crea un bloque de *tres* `print(...)`.
    2. Cada línea debe corresponder a una fase típica de un proceso de salud pública.
    3. El orden debe ser coherente y sin saltos.

    Sugerencias de temas (elige uno):
    - Triage en urgencias
    - Toma y transporte de muestras
    - Investigación de brotes (búsqueda activa, verificación, informe)

    **Regla didáctica:** no uses variables ni estructuras de control todavía; solo secuencia.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "Guía (una posible solución)": mo.md(
                r"""
    ```python
    print("Investigación de brote — ejemplo")
    print("Paso 1: Identificar y listar casos sospechosos")
    print("Paso 2: Verificar definición de caso y recolectar datos básicos")
    print("Paso 3: Elaborar un resumen preliminar para intervención")
    ```

    **Criterio de calidad:** si cambias el orden de los pasos, el relato pierde coherencia.
    """
            )
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6) Mini-reto final

    **Reto:** Crea una nueva celda y redacta un “micro-programa” de 5 líneas (5 `print(...)`) que simule la salida textual de un reporte breve de vigilancia semanal.

    Debe incluir (en orden):

    1. Título del reporte.
    2. Periodo (por ejemplo, “Semana epidemiológica 08”).
    3. Evento (por ejemplo, IRA, dengue, COVID-19, EDA).
    4. Resumen narrativo (una línea).
    5. Cierre (por ejemplo, “Fin del reporte”).
    """)
    return


@app.cell
def _():
    # Ejemplo de mini-reto (modelo)
    print("Ejemplo!")
    print("Reporte de vigilancia semanal")
    print("Periodo: Semana epidemiológica 08")
    print("Evento: Infección respiratoria aguda (IRA)")
    print("Resumen: Se observa estabilidad general con aumento leve en consultas.")
    print("Fin del reporte")
    return


if __name__ == "__main__":
    app.run()
