# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
# ]
# ///

import marimo

__generated_with = "0.23.1"
app = marimo.App(width="columns")


@app.cell(column=0)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Semana 1 · Lección 1: Sintaxis del lenguaje Python

    Esta lección introduce los fundamentos formales de la escritura de programas en Python.

    El foco está en comprender cómo se escribe un programa válido, cómo se ejecuta, cómo se organizan sus instrucciones y cómo Python interpreta valores, expresiones y llamadas.

    Cada bloque desarrolla una idea central del lenguaje con ejemplos pequeños y progresivos.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Bloque 1 — ¿Qué significa escribir un programa en Python?

    ## Propósito

    En este primer bloque se introduce una idea fundacional: un programa es una secuencia de instrucciones que el computador ejecuta en orden.

    Antes de estudiar estructuras más complejas, es necesario entender cómo se comporta el lenguaje en su forma más básica. Python no reorganiza el código, no infiere la intención del autor y no completa instrucciones faltantes. Ejecuta exactamente lo que encuentra, línea por línea, en el orden en que está escrito.

    ## ¿Qué es un programa?

    Un programa es un conjunto de instrucciones escritas en un lenguaje que el computador puede interpretar.

    En Python, estas instrucciones se escriben como líneas de código, y el intérprete las ejecuta una tras otra. Esto significa que el orden del código no es un detalle superficial: forma parte del significado del programa.

    [Diagrama: una secuencia vertical de cajas conectadas por flechas. Cada caja representa una línea de código y las flechas muestran que Python avanza de arriba hacia abajo.]

    ## Idea central

    Cuando un programa se ejecuta, Python recorre el archivo desde el inicio hacia el final. Si las instrucciones están bien escritas, se ejecutan. Si aparece un error, la ejecución se detiene en ese punto.

    Esta idea parece simple, pero es la base de todo lo que viene después.
    """)
    return


@app.cell
def _():
    print("Inicio del registro")
    print("Paciente: María")
    print("Edad: 68")
    print("Presión: 145")
    print("Fin del registro")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Qué está ocurriendo en el ejemplo

    Cada línea se ejecuta en el orden exacto en que aparece:

    1. se imprime el inicio,
    2. luego el nombre,
    3. luego la edad,
    4. luego la presión,
    5. finalmente el cierre.

    Python no agrupa estas líneas por significado. No reconoce que unas son más importantes que otras. Solo ejecuta instrucciones válidas en secuencia.

    A esto se le llama ejecución secuencial.
    """)
    return


@app.cell
def _():
    print("Fin del registro")
    print("Paciente: María")
    print("Inicio del registro")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## El orden sí modifica el resultado

    El segundo ejemplo también es un programa válido. No contiene errores de sintaxis. Sin embargo, el resultado pierde coherencia porque el orden cambió.

    Esto permite introducir una intuición importante: la corrección de un programa no depende solamente de que las líneas estén bien escritas. También depende de que estén organizadas de una manera lógica.

    ## Qué pasa si aparece un error

    Cuando Python encuentra una línea inválida, la ejecución se interrumpe. No continúa con las líneas siguientes.

    Por eso, incluso en programas pequeños, conviene pensar cada línea como parte de una secuencia que debe estar completa y bien formada desde el inicio hasta el final.

    ## Cierre del bloque

    En este punto deberías poder reconocer que:

    - un programa es una secuencia de instrucciones,
    - Python ejecuta de arriba hacia abajo,
    - el orden de las líneas afecta el resultado,
    - un error detiene la ejecución del programa.
    """)
    return


@app.cell(column=1, hide_code=True)
def _(mo):
    mo.md(r"""
    # Bloque 2 — Sintaxis básica del lenguaje Python

    ## Propósito

    En este bloque se introduce la idea de sintaxis.

    La sintaxis corresponde a las reglas formales que determinan cómo debe escribirse un programa para que Python pueda interpretarlo correctamente. Un programa puede ser conceptualmente claro, pero si no cumple las reglas sintácticas del lenguaje, no se ejecuta.

    ## ¿Qué significa que Python tenga una sintaxis estricta?

    Python no intenta adivinar lo que quisiste escribir. Evalúa si cada instrucción respeta una forma válida.

    Esto implica que detalles como abrir y cerrar paréntesis, escribir correctamente comillas, completar una instrucción o respetar la estructura de una línea no son decorativos. Son parte de la definición misma del programa.

    ## Forma básica de una instrucción

    Una de las primeras formas que se aprende en Python es la llamada a `print()`.

    En esa estructura aparecen varios componentes:

    - el nombre de una función,
    - los paréntesis que indican llamada,
    - un argumento que será mostrado.
    """)
    return


@app.cell
def _():
    print("Paciente registrado")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Una instrucción por línea

    En Python, lo más habitual es escribir una instrucción por línea. Esto favorece la lectura y hace más evidente la secuencia de ejecución.
    """)
    return


@app.cell
def _():
    print("Paciente")
    print("Edad")
    print("Presión")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Qué ocurre si falta un elemento sintáctico

    Si una instrucción queda incompleta, Python genera un error de sintaxis. Un caso frecuente es dejar un paréntesis sin cerrar o unas comillas abiertas.

    Ese tipo de error impide que el programa continúe.

    ## Punto y coma

    En algunos lenguajes el punto y coma es obligatorio. En Python no lo es. Es posible escribir varias instrucciones en una misma línea separadas por `;`, pero esa práctica reduce la legibilidad y no es la forma esperada de escribir código en este nivel.
    """)
    return


@app.cell
def _():
    print("Paciente") ; print("Edad")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    La forma preferible es esta:
    """)
    return


@app.cell
def _():
    print("Paciente")
    print("Edad")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Espacios y legibilidad

    Python tolera ciertos espacios adicionales, pero eso no significa que cualquier forma de escritura sea igualmente clara.
    """)
    return


@app.cell
def _():
    print("Paciente")
    print(     "Paciente"             )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    La primera línea funciona, pero la segunda es más limpia y más fácil de leer.

    ## Cierre del bloque

    En este punto deberías poder reconocer que:

    - Python tiene reglas estrictas de escritura,
    - cada instrucción debe estar bien formada,
    - un error de sintaxis detiene la ejecución,
    - escribir correctamente es una condición para que el programa funcione.
    """)
    return


@app.cell(column=2, hide_code=True)
def _(mo):
    mo.md(r"""
    # Bloque 3 — Indentación como estructura del programa

    ## Propósito

    En este bloque se introduce una de las características más distintivas de Python: la estructura del programa no se define con llaves ni con palabras de cierre, sino con espacios.

    ## ¿Qué es la indentación?

    La indentación es el desplazamiento hacia la derecha de una línea de código mediante espacios al inicio.

    En muchos lenguajes la indentación mejora la lectura, pero no cambia el significado. En Python sí cambia el significado. Por eso no es un detalle visual: es parte de la sintaxis.

    ## Idea central

    La indentación indica qué instrucciones pertenecen a un mismo bloque.

    Un bloque es un conjunto de instrucciones que Python interpreta como una unidad estructural.
    """)
    return


@app.cell
def _():
    if True:
        print("Paciente válido")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    En este ejemplo todavía no importa estudiar la lógica del `if`. Lo importante aquí es la forma:

    - la línea termina en `:`,
    - la línea siguiente aparece indentada.

    Eso le indica a Python que la segunda línea pertenece al bloque iniciado por la primera.

    ## Dos puntos e indentación

    El símbolo `:` anuncia el inicio de un bloque. Todo lo que esté indentado debajo, con el mismo nivel de espacios, forma parte de ese bloque.
    """)
    return


@app.cell
def _():
    if True:
        print("Paciente")
        print("Edad")
        print("Presión")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Aquí las tres instrucciones están al mismo nivel de indentación, por lo que pertenecen al mismo bloque.

    ## Errores frecuentes

    Después de una línea que termina en `:`, Python espera un bloque indentado. Si ese bloque no aparece, se genera un error.

    También se produce un error si las líneas de un mismo bloque no tienen una indentación consistente.

    ## Convención práctica

    La convención más utilizada es emplear cuatro espacios por cada nivel de indentación. Esta convención facilita la lectura y evita inconsistencias.

    [Diagrama: una línea principal a la izquierda y, debajo de ella, tres líneas desplazadas hacia la derecha. El diagrama muestra que las líneas indentadas forman parte del mismo bloque.]

    ## Cierre del bloque

    En este punto deberías poder reconocer que:

    - la indentación define bloques de código,
    - los dos puntos anuncian el inicio de un bloque,
    - las líneas de un bloque deben mantener una indentación consistente,
    - errores en la indentación impiden la ejecución del programa.
    """)
    return


@app.cell(column=3, hide_code=True)
def _(mo):
    mo.md(r"""
    # Bloque 4 — Comentarios y lectura del código

    ## Propósito

    El código no solo debe ejecutarse. También debe poder leerse, entenderse y revisarse más adelante.

    A medida que los programas crecen, se vuelve necesario dejar explícito qué hace una parte del código, por qué se hace y cómo debe interpretarse un valor o una sección. Para eso se utilizan los comentarios.

    ## ¿Qué es un comentario?

    Un comentario es texto que Python ignora completamente durante la ejecución.

    En Python, los comentarios comienzan con `#`.
    """)
    return


@app.cell
def _():
    # Este es un comentario
    print("Paciente")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    En el ejemplo anterior, la primera línea no produce ninguna acción en la ejecución. Python la ignora. La única instrucción ejecutada es la llamada a `print()`.

    ## Comentarios al final de una línea

    También es posible escribir comentarios después de una instrucción. En ese caso, Python ejecuta la parte anterior al `#` e ignora todo lo que sigue.
    """)
    return


@app.cell
def _():
    print("Edad: 68")  # Edad del paciente en años
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Para qué sirven los comentarios

    Los comentarios permiten documentar el sentido del código. Esto es útil cuando el código ya no es obvio por sí mismo, una decisión necesita explicación o quieres poder releer el programa más tarde con facilidad.

    ## Qué no debería hacer un comentario

    Un comentario no debería repetir de manera trivial lo que la línea ya muestra. Debe aportar contexto o significado adicional.
    """)
    return


@app.cell
def _():
    # Información básica del paciente
    print("Paciente: Ana")

    # Edad en años
    print("Edad: 72")

    # Diagnóstico principal
    print("Diagnóstico: hipertensión")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Desactivar temporalmente una instrucción

    Un comentario también puede usarse para impedir temporalmente que una línea se ejecute sin borrarla.
    """)
    return


@app.cell
def _():
    # print("Paciente")
    print("Otra línea sí se ejecuta")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cierre del bloque

    En este punto deberías poder reconocer que:

    - los comentarios son ignorados por Python,
    - sirven para explicar y documentar el código,
    - mejoran la legibilidad,
    - no forman parte de la ejecución del programa.
    """)
    return


@app.cell(column=4, hide_code=True)
def _(mo):
    mo.md(r"""
    # Bloque 5 — Tipos de datos básicos

    ## Propósito

    Hasta ahora has trabajado con valores, pero no todos los valores son iguales. Python clasifica los datos en distintos tipos, y eso determina qué representan, cómo se comportan y qué operaciones pueden realizarse sobre ellos.

    Comprender esto es esencial para anticipar cómo responderá el lenguaje.

    ## ¿Qué es un tipo de dato?

    Un tipo de dato define la naturaleza de un valor.

    Por ejemplo:

    - `72` representa un entero,
    - `36.7` representa un decimal,
    - `"Ana"` representa texto,
    - `True` representa un valor lógico.
    """)
    return


@app.cell
def _():
    edad = 72
    temperatura = 36.7
    nombre = "Ana"
    tiene_hipertension = True

    print(edad)
    print(temperatura)
    print(nombre)
    print(tiene_hipertension)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Tipos básicos

    ### Enteros (`int`)
    Se usan para contar o representar cantidades discretas.

    ### Decimales (`float`)
    Se usan para valores con parte fraccionaria.

    ### Texto (`str`)
    Se escriben entre comillas y representan cadenas de caracteres.

    ### Booleanos (`bool`)
    Solo pueden tomar dos valores: `True` o `False`.

    ## Por qué importa el tipo

    El tipo determina el significado de una operación. El mismo operador puede comportarse de manera diferente según el tipo de los datos involucrados.
    """)
    return


@app.cell
def _():
    print(10 + 5)
    print("10" + "5")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    En la primera línea, `+` realiza una suma numérica. En la segunda, `+` concatena dos cadenas de texto. La sintaxis es similar, pero el tipo cambia el comportamiento.

    ## Conversión de tipos

    En ocasiones es necesario convertir explícitamente un valor de un tipo a otro. Una situación muy común es transformar un número en texto para poder combinarlo con una cadena.
    """)
    return


@app.cell
def _():
    def _():
        edad = 60
        return print("Edad: " + str(edad))

    _()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Identificar el tipo de un valor

    La función `type()` permite inspeccionar el tipo de una variable o de un valor.
    """)
    return


@app.cell
def _():
    def _():
        edad = 70
        return type(edad)

    _()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cierre del bloque

    En este punto deberías poder:

    - reconocer los tipos básicos de datos,
    - entender sus diferencias,
    - relacionar el tipo con el comportamiento de una operación,
    - identificar la necesidad de convertir tipos cuando corresponde.
    """)
    return


@app.cell(column=5, hide_code=True)
def _(mo):
    mo.md(r"""
    # Bloque 6 — Variables como modelos de memoria

    ## Propósito

    En este bloque se refina una idea que suele enseñarse de forma simplificada: una variable no contiene directamente un valor, sino que referencia un objeto en memoria.

    Este modelo ayuda a entender mejor qué es una asignación, qué ocurre cuando una variable cambia y por qué dos nombres pueden relacionarse con el mismo valor sin ser lo mismo que una copia física.
    """)
    return


@app.cell
def _():
    def _():
        edad = 70
        edad = 75
        return print(edad)

    _()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Reasignación

    Cuando escribes:

    ```python
    edad = 70
    edad = 75
    ```

    no estás “editando” el `70`. Lo que ocurre es que el nombre `edad` deja de referenciar el valor anterior y pasa a referenciar el nuevo.

    Esta idea es importante porque permite distinguir entre el nombre de una variable y el objeto al que apunta.

    ## Copia de referencias
    """)
    return


@app.cell
def _():
    x = 10
    y = x
    x = 20

    print(x)
    print(y)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    En este ejemplo, `y` conserva el valor anterior aunque `x` cambie después. Eso ocurre porque la reasignación de `x` no modifica retrospectivamente lo que `y` referenciaba.

    ## Identidad en memoria

    El operador `is` permite preguntar si dos nombres refieren exactamente al mismo objeto.
    """)
    return


@app.cell
def _():
    def _():
        x = 100
        y = 100
        return x is y

    _()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Aunque este detalle depende de cómo Python gestione internamente ciertos objetos pequeños, el punto conceptual sigue siendo útil: valor e identidad no son la misma idea.

    ## Tipos inmutables

    En los tipos básicos vistos hasta ahora (`int`, `float`, `str`, `bool`), los cambios producen nuevos objetos en lugar de modificar el objeto original.
    """)
    return


@app.cell
def _():
    def _():
        nombre = "Pedro"
        nombre = nombre + " Pérez"
        return print(nombre)

    _()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Modelo mental simplificado

    Una variable puede pensarse como una etiqueta con nombre que apunta a un objeto. No es solo una caja donde “se guarda” algo, sino una referencia lógica.

    ## Cierre del bloque

    En este punto deberías poder:

    - entender que las variables son referencias,
    - interpretar correctamente la reasignación,
    - distinguir entre nombre y valor,
    - anticipar el comportamiento general de los tipos inmutables.
    """)
    return


@app.cell(column=6, hide_code=True)
def _(mo):
    mo.md(r"""
    # Bloque 7 — Expresiones y evaluación

    ## Propósito

    En este bloque se formaliza cómo Python construye, interpreta y evalúa expresiones.

    Prácticamente todo programa se apoya en expresiones: operaciones aritméticas, comparaciones, concatenaciones de texto, condiciones lógicas y llamadas más complejas se basan en ellas.

    ## ¿Qué es una expresión?

    Una expresión es cualquier construcción válida que, al evaluarse, produce un valor.
    """)
    return


@app.cell
def _():
    10 + 5
    return


@app.cell
def _():
    "Hola" + " mundo"
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    En ambos casos, Python toma una estructura sintáctica y la resuelve hasta obtener un resultado.

    ## Evaluación

    Evaluar una expresión significa:

    1. interpretar sus componentes,
    2. aplicar reglas de precedencia,
    3. producir un valor final.

    Ese valor puede mostrarse, compararse o asignarse a una variable.
    """)
    return


@app.cell
def _():
    resultado = 2 + 3 * 4
    print(resultado)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Tabla de operadores y expresiones

    ### Operadores aritméticos

    | Expresión | Significado | Detalle conceptual | Ejemplo |
    |---|---|---|---|
    | `+` | Suma | Combina dos valores numéricos | `10 + 5` |
    | `-` | Resta | Calcula la diferencia | `10 - 5` |
    | `*` | Multiplicación | Producto entre valores | `10 * 5` |
    | `/` | División | Siempre retorna un `float` | `10 / 5` |
    | `//` | División entera | Descarta la parte decimal | `10 // 3` |
    | `%` | Módulo | Devuelve el residuo | `10 % 3` |
    | `**` | Potencia | Eleva un valor a otro | `2 ** 3` |

    ### Operadores de comparación

    | Expresión | Significado | Detalle conceptual | Ejemplo |
    |---|---|---|---|
    | `==` | Igualdad | Evalúa equivalencia de valor | `10 == 10` |
    | `!=` | Diferente | Evalúa desigualdad | `10 != 5` |
    | `>` | Mayor que | Comparación estricta | `10 > 5` |
    | `<` | Menor que | Comparación estricta | `5 < 10` |
    | `>=` | Mayor o igual | Incluye igualdad | `10 >= 10` |
    | `<=` | Menor o igual | Incluye igualdad | `5 <= 10` |

    ### Operadores lógicos

    | Expresión | Significado | Detalle conceptual | Ejemplo |
    |---|---|---|---|
    | `and` | Conjunción | Verdadero si ambas condiciones son verdaderas | `True and False` |
    | `or` | Disyunción | Verdadero si al menos una condición es verdadera | `True or False` |
    | `not` | Negación | Invierte un valor lógico | `not True` |

    ### Operadores con texto (`str`)

    | Expresión | Significado | Detalle conceptual | Ejemplo |
    |---|---|---|---|
    | `+` | Concatenación | Une cadenas de texto | `"Hola" + " mundo"` |
    | `*` | Repetición | Repite una cadena varias veces | `"ha" * 3` |

    ### Operadores de identidad

    | Expresión | Significado | Detalle conceptual | Ejemplo |
    |---|---|---|---|
    | `is` | Misma referencia | Evalúa identidad en memoria | `a is b` |
    | `is not` | Diferente referencia | Evalúa si no son el mismo objeto | `a is not b` |

    ### Operadores de pertenencia

    | Expresión | Significado | Detalle conceptual | Ejemplo |
    |---|---|---|---|
    | `in` | Pertenece | Verifica inclusión | `"a" in "Ana"` |
    | `not in` | No pertenece | Verifica exclusión | `"x" not in "Ana"` |

    ## Precedencia de operadores

    Python no evalúa siempre de izquierda a derecha. Sigue un orden. En general:

    - primero paréntesis,
    - luego aritmética,
    - luego comparaciones,
    - luego lógica.
    """)
    return


@app.cell
def _():
    2 + 3 * 4
    (2 + 3) * 4
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Los paréntesis permiten modificar el orden y hacer explícita la intención.

    ## Variables dentro de expresiones

    Una variable puede participar en una expresión igual que un valor literal. Python sustituye la variable por su valor y luego evalúa.
    """)
    return


@app.cell
def _():
    def _():
        edad = 60
        edad_en_10 = edad + 10
        return print(edad_en_10)

    _()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Errores comunes

    Un error muy frecuente es mezclar tipos incompatibles, por ejemplo intentar sumar texto y números sin conversión explícita.

    Otro error frecuente es asumir un orden de evaluación incorrecto.

    ## Cierre del bloque

    En este punto deberías poder:

    - identificar expresiones,
    - interpretar cómo se evalúan,
    - usar operadores básicos correctamente,
    - reconocer el papel de la precedencia.
    """)
    return


@app.cell(column=7, hide_code=True)
def _(mo):
    mo.md(r"""
    # Bloque 8 — Control de flujo condicional

    ## Propósito

    Hasta ahora todos los programas se han ejecutado de manera secuencial. En este bloque se introduce la posibilidad de modificar el flujo de ejecución según una condición.

    Esto permite que el programa tome decisiones y ejecute diferentes caminos.

    ## ¿Qué es el control de flujo?

    El control de flujo define el orden en que se ejecutan las instrucciones. Uno de los mecanismos más importantes para hacerlo es el uso de condicionales.
    """)
    return


@app.cell
def _():
    def _():
        edad = 70

        if edad > 65:
            print("Mayor de 65")

    _()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    La estructura `if` evalúa una condición. Si la condición es verdadera, se ejecuta el bloque indentado. Si es falsa, se omite.

    ## Caso contrario: `else`
    """)
    return


@app.cell
def _():
    def _():
        edad = 50

        if edad > 65:
            print("Mayor de 65")
        else:
            print("Menor o igual a 65")

    _()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Múltiples condiciones: `elif`

    Cuando existen varios casos posibles, Python evalúa cada condición en orden y ejecuta el primer bloque que resulte verdadero.
    """)
    return


@app.cell
def _():
    def _():
        edad = 70

        if edad < 18:
            print("Menor de edad")
        elif edad < 65:
            print("Adulto")
        else:
            print("Adulto mayor")

    _()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Condiciones complejas

    Es posible combinar condiciones mediante operadores lógicos como `and`, `or` y `not`.
    """)
    return


@app.cell
def _():
    def _():
        edad = 70
        tiene_hipertension = True

        if edad > 65 and tiene_hipertension:
            print("Alto riesgo")

    _()
    return


@app.cell
def _():
    def _():
        edad = 40
        tiene_hipertension = True

        if edad > 65 or tiene_hipertension:
            print("Requiere evaluación")

    _()
    return


@app.cell
def _():
    tiene_diabetes = False

    if not tiene_diabetes:
        print("No presenta diabetes")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Errores comunes

    Algunos errores frecuentes son:

    - olvidar la indentación del bloque,
    - escribir condiciones incompletas,
    - usar `=` en lugar de `==` en una comparación.

    ## Cierre del bloque

    En este punto deberías poder:

    - escribir estructuras `if`, `elif` y `else`,
    - entender el orden de evaluación de condiciones,
    - combinar condiciones con operadores lógicos,
    - reconocer errores frecuentes en condicionales.
    """)
    return


@app.cell(column=8, hide_code=True)
def _(mo):
    mo.md(r"""
    # Bloque 9 — Todo es un objeto y llamadas a funciones

    ## Propósito

    Este bloque introduce dos ideas centrales en Python:

    1. todo valor es un objeto,
    2. las funciones son objetos que pueden ser llamados.

    Estas ideas ayudan a unificar la comprensión del lenguaje y preparan el terreno para entender métodos y estructuras más complejas.

    ## Todo es un objeto

    En Python, números, textos, booleanos y funciones existen como objetos. Cada objeto tiene:

    - un tipo,
    - un valor,
    - y ciertos comportamientos asociados.
    """)
    return


@app.cell
def _():
    x_1 = 10
    type(x_1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Objetos y comportamiento

    Los objetos no solo almacenan datos. También tienen operaciones asociadas. En Python, muchas de esas operaciones aparecen como métodos.
    """)
    return


@app.cell
def _():
    texto = "Francisco"
    texto.upper()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Aquí `"ana"` es un objeto de tipo `str`, y `upper()` es un método que pertenece a ese objeto.

    ## Funciones

    Una función es un objeto que puede ser ejecutado. La forma general de una llamada es:

    `funcion(argumentos)`

    Cuando escribes una llamada, Python evalúa primero los argumentos y luego ejecuta la función.
    """)
    return


@app.cell
def _():
    print("Paciente")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Función vs método

    Una función se llama por su nombre y recibe argumentos:

    `len(texto)`

    Un método se llama sobre un objeto usando punto:

    `texto.upper()`

    La diferencia conceptual es importante:

    - en la función, el objeto aparece como argumento;
    - en el método, el comportamiento aparece asociado al objeto mismo.
    """)
    return


@app.cell
def _():
    texto_nuevo = "python"

    print(len(texto_nuevo))
    print(texto_nuevo.upper())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Encadenamiento de métodos

    Como muchas operaciones devuelven nuevos objetos, es posible encadenarlas.
    """)
    return


@app.cell
def _():
    otro_texto = "python"
    otro_texto.upper().replace("P", "J")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Errores comunes

    Errores frecuentes en este punto son:

    - olvidar los paréntesis y referirse a la función sin llamarla,
    - intentar usar como función algo que en realidad es un método,
    - llamar métodos sobre tipos que no los soportan.

    ## Cierre del bloque

    En este punto deberías poder:

    - entender que todo en Python es un objeto,
    - reconocer la diferencia entre función y método,
    - interpretar llamadas básicas,
    - relacionar el tipo de un objeto con los comportamientos que ofrece.
    """)
    return


@app.cell(column=9, hide_code=True)
def _(mo):
    mo.md(r"""
    # Cierre de la lección

    A lo largo de estos bloques se construyó una base formal del lenguaje Python:

    - qué es un programa,
    - cómo se escribe con sintaxis válida,
    - cómo se organiza mediante indentación,
    - cómo se documenta con comentarios,
    - qué tipos de datos básicos existen,
    - cómo funcionan las variables como referencias,
    - cómo se evalúan expresiones,
    - cómo se altera el flujo mediante condicionales,
    - y cómo entender funciones, métodos y objetos.

    Esta base será necesaria para los temas siguientes del curso, donde se extenderan los conceptos introducidos aquí y se aplicarán a problemas más complejos.
    """)
    return


if __name__ == "__main__":
    app.run()
