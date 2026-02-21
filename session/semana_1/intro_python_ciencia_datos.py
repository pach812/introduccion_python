import marimo

__generated_with = "0.19.11"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🐍 Introducción a Python para Ciencia de Datos

    **Basado en:** *Python for Everybody* (Severance) y *Python for Data Analysis* (McKinney)

    ---

    Bienvenido a este notebook interactivo. Aquí aprenderás los fundamentos del lenguaje Python
    con ejemplos prácticos y retos al final de cada sección.

    > 💡 **¿Cómo usar este notebook?** Puedes ejecutar cada celda de código y modificarla para experimentar.
    > Los retos al final de cada sección son tu oportunidad de practicar por tu cuenta.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 📌 MÓDULO 1 — Semántica del Lenguaje Python

    La **semántica** de un lenguaje define el *significado* de las instrucciones. Python fue diseñado
    para ser legible, casi como leer pseudocódigo en inglés.

    ### 1.1 Python como lenguaje interpretado

    A diferencia de lenguajes compilados (C, Java), Python ejecuta el código línea por línea.
    Esto lo hace ideal para exploración y ciencia de datos.
    """)
    return


@app.cell
def _():
    # Python ejecuta esto directamente, sin necesidad de compilar
    print("Hola, mundo de la ciencia de datos 🌍")
    print("Python es interpretado: cada línea se ejecuta de arriba hacia abajo")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1.2 Sensibilidad a mayúsculas (Case-Sensitive)
    """)
    return


@app.cell
def _():
    # Python distingue entre mayúsculas y minúsculas
    _nombre = "Ana"
    _Nombre = "Carlos"  # Esta es una variable DIFERENTE
    _NOMBRE = "María"   # Esta también es diferente

    print(_nombre)
    print(_Nombre)
    print(_NOMBRE)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1.3 Indentación (Sangría)

    En Python la **indentación no es opcional** — define la estructura del código.
    Donde otros lenguajes usan `{}`, Python usa espacios.
    """)
    return


@app.cell
def _():
    # La indentación define los bloques de código
    temperatura = 38.5

    if temperatura > 37.5:
        print("⚠️  Fiebre detectada")          # Este código está DENTRO del if
        print("Se recomienda descanso")         # Este también
    print("Revisión completada")                # Este está FUERA del if (siempre se ejecuta)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1.4 Comentarios
    """)
    return


@app.cell
def _():
    # Esto es un comentario de una línea — Python lo ignora al ejecutar

    """
    Esto es un string multilínea que también se usa como comentario
    cuando aparece al inicio de una función o módulo (docstring).
    """

    _x = 42  # También puedes comentar al final de una línea
    print(_x)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### 🏆 Mini-Reto 1 — Semántica

    **Objetivo:** Entender indentación y case-sensitivity.

    En la celda de abajo, el código tiene errores de indentación y de nombres de variables.
    Corrígelos para que imprima correctamente el mensaje.

    ```python
    # Código con errores — corrígelo:
    Ciudad = "Bogotá"
    pais = "Colombia"

    if ciudad = = "Bogotá":
    print(f"La ciudad {Ciudad} está en {Pais}")
    ```

    **Pista:** Hay 3 errores: case-sensitivity (×2) e indentación (×1).
    """)
    return


@app.cell
def _():
    # ✏️ Escribe tu solución aquí:
    _Ciudad = "Bogotá"
    _pais = "Colombia"

    # Corrige los errores...
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 📌 MÓDULO 2 — Pseudocódigo y Utilidades Básicas

    ### 2.1 ¿Qué es el pseudocódigo?

    El pseudocódigo es una forma de planear un algoritmo en lenguaje natural antes de escribir código real.
    Python es tan legible que muchas veces se parece mucho al pseudocódigo.
    """)
    return


@app.cell
def _():
    # PSEUDOCÓDIGO:
    # Si el estudiante tiene nota >= 60, aprobó
    # Si no, reprobó

    # CÓDIGO PYTHON (casi idéntico):
    nota = 75

    if nota >= 60:
        _estado = "Aprobado ✅"
    else:
        _estado = "Reprobado ❌"

    print(f"Nota: {nota} → {_estado}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2.2 La función `print()` — Tu herramienta de exploración
    """)
    return


@app.cell
def _():
    # print básico
    print("Texto simple")

    # print con múltiples argumentos
    print("Nombre:", "Ana", "| Edad:", 22)

    # f-strings (forma moderna y recomendada)
    _nombre = "Carlos"
    _edad = 25
    print(f"Hola, soy {_nombre} y tengo {_edad} años")

    # print con separador personalizado
    print("manzana", "naranja", "uva", sep=" 🍎 ")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2.3 La función `input()` — Recibir datos del usuario
    """)
    return


@app.cell
def _():
    # En notebooks, simulamos el input con una variable
    # En un script normal usarías: nombre_usuario = input("¿Cómo te llamas? ")

    nombre_usuario = "Estudiante"  # Simula la entrada del usuario
    print(f"¡Bienvenido/a, {nombre_usuario}! 🎉")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2.4 `type()` — Conocer el tipo de un dato
    """)
    return


@app.cell
def _():
    # type() es esencial para depurar código
    print(type(42))           # int
    print(type(3.14))         # float
    print(type("Hola"))       # str
    print(type(True))         # bool
    print(type([1, 2, 3]))    # list
    print(type(None))         # NoneType
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2.5 `help()` y documentación interna
    """)
    return


@app.cell
def _():
    # help() muestra la documentación de cualquier función
    help(print)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### 🏆 Mini-Reto 2 — Pseudocódigo y Utilidades

    **Objetivo:** Convertir pseudocódigo a Python real.

    Dado este pseudocódigo:
    ```
    INICIO
      Pedir al usuario su temperatura corporal
      SI temperatura > 37.5 ENTONCES
        Mostrar "Posible fiebre, consulta un médico"
      SINO SI temperatura < 36.0 ENTONCES
        Mostrar "Temperatura baja, abrígate"
      SINO
        Mostrar "Temperatura normal"
      FIN SI
    FIN
    ```

    Implementa este pseudocódigo en Python. Usa una variable `temp` con diferentes valores para probarlo.
    """)
    return


@app.cell
def _():
    # ✏️ Tu implementación aquí:
    temp = 38.0  # Cambia este valor para probar diferentes casos
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 📌 MÓDULO 3 — Variables, Semántica y Expresiones

    ### 3.1 Variables — Cajas de memoria

    Una variable es un **nombre que apunta a un valor** en memoria.
    En Python no necesitas declarar el tipo — Python lo infiere automáticamente.
    """)
    return


@app.cell
def _():
    # Asignación básica
    poblacion = 51_000_000       # int — puedes usar _ como separador de miles
    pib_per_capita = 6_104.10    # float
    pais = "Colombia"             # str
    es_capital = True             # bool

    print(f"País: {pais}")
    print(f"Población: {poblacion:,}")
    print(f"PIB per cápita: ${pib_per_capita:,.2f}")
    print(f"¿Es capital? {es_capital}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.2 Tipos de datos básicos
    """)
    return


@app.cell
def _():
    # ENTEROS (int)
    alumnos = 35
    _año = 2024

    # FLOTANTES (float)
    promedio = 8.75
    pi = 3.14159

    # CADENAS (str)
    universidad = "Universidad Nacional"
    inicial = 'U'  # También puedes usar comillas simples

    # BOOLEANOS (bool)
    aprobado = True
    tiene_beca = False

    # NULO (NoneType)
    dato_faltante = None

    print(f"Tipo de alumnos: {type(alumnos)}")
    print(f"Tipo de promedio: {type(promedio)}")
    print(f"Tipo de universidad: {type(universidad)}")
    print(f"Tipo de aprobado: {type(aprobado)}")
    print(f"Tipo de dato_faltante: {type(dato_faltante)}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.3 Expresiones aritméticas
    """)
    return


@app.cell
def _():
    a = 10
    b = 3

    print(f"Suma:            {a} + {b} = {a + b}")
    print(f"Resta:           {a} - {b} = {a - b}")
    print(f"Multiplicación:  {a} * {b} = {a * b}")
    print(f"División:        {a} / {b} = {a / b:.4f}")    # Siempre retorna float
    print(f"División entera: {a} // {b} = {a // b}")       # Trunca decimales
    print(f"Módulo/Resto:    {a} % {b} = {a % b}")         # Muy útil en programación
    print(f"Potencia:        {a} ** {b} = {a ** b}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.4 Expresiones con strings
    """)
    return


@app.cell
def _():
    # Concatenación
    nombre = "María"
    apellido = "García"
    nombre_completo = nombre + " " + apellido
    print(nombre_completo)

    # Repetición
    separador = "=" * 30
    print(separador)

    # Longitud
    print(f"El nombre tiene {len(nombre_completo)} caracteres")

    # Métodos de string
    texto = "  hola mundo en python  "
    print(texto.strip())           # Elimina espacios al inicio y fin
    print(texto.strip().upper())   # Convierte a mayúsculas
    print(texto.strip().title())   # Primera letra de cada palabra en mayúscula
    print(texto.strip().replace("mundo", "universo"))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.5 Conversión de tipos (casting)
    """)
    return


@app.cell
def _():
    # str a int/float
    edad_texto = "22"
    edad_numero = int(edad_texto)
    print(f"'{edad_texto}' → {edad_numero} (tipo: {type(edad_numero).__name__})")

    # int a float
    entero = 5
    flotante = float(entero)
    print(f"{entero} → {flotante}")

    # numero a str (útil para concatenar)
    año = 2024
    mensaje = "Año: " + str(año)
    print(mensaje)

    # ⚠️ Conversión inválida — genera error
    try:
        int("hola")
    except ValueError as e:
        print(f"Error de conversión: {e}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.6 Operadores de comparación y lógicos
    """)
    return


@app.cell
def _():
    x = 15

    # Comparación
    print(f"x = {x}")
    print(f"x > 10:   {x > 10}")
    print(f"x == 15:  {x == 15}")
    print(f"x != 20:  {x != 20}")
    print(f"x <= 15:  {x <= 15}")

    print()

    # Lógicos: and, or, not
    edad = 20
    tiene_id = True

    puede_entrar = edad >= 18 and tiene_id
    print(f"Edad: {edad}, Tiene ID: {tiene_id}")
    print(f"¿Puede entrar? {puede_entrar}")
    print(f"¿NO puede entrar? {not puede_entrar}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### 🏆 Mini-Reto 3 — Variables y Expresiones

    **Objetivo:** Calcular el índice de masa corporal (IMC).

    Fórmula: `IMC = peso (kg) / altura (m)²`

    1. Define variables para `peso` (en kg) y `altura` (en metros)
    2. Calcula el IMC
    3. Imprime el resultado con 2 decimales
    4. Imprime el tipo de dato del resultado
    5. **Bonus:** Convierte el IMC a string y muéstralo concatenado con el texto "Mi IMC es: "
    """)
    return


@app.cell
def _():
    # ✏️ Tu solución aquí:
    peso = 70    # kg
    altura = 1.75  # metros

    # Calcula el IMC...
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 📌 MÓDULO 4 — Ejecución Condicional

    ### 4.1 `if` simple

    Permite ejecutar código **solo si** una condición es verdadera.
    """)
    return


@app.cell
def _():
    llueve = True

    if llueve:
        print("🌂 Lleva paraguas")

    print("Que tengas buen día")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.2 `if-else`
    """)
    return


@app.cell
def _():
    _saldo = 150_000  # pesos colombianos

    if _saldo >= 100_000:
        print("✅ Fondos suficientes para la transacción")
    else:
        print("❌ Saldo insuficiente")

    print(f"Saldo actual: ${_saldo:,}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.3 `if-elif-else` — Múltiples condiciones
    """)
    return


@app.cell
def _():
    calificacion = 85

    if calificacion >= 90:
        letra = "A"
        descripcion = "Excelente"
    elif calificacion >= 80:
        letra = "B"
        descripcion = "Bueno"
    elif calificacion >= 70:
        letra = "C"
        descripcion = "Aceptable"
    elif calificacion >= 60:
        letra = "D"
        descripcion = "Suficiente"
    else:
        letra = "F"
        descripcion = "Reprobado"

    print(f"Calificación: {calificacion} → {letra} ({descripcion})")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.4 Condicionales anidados
    """)
    return


@app.cell
def _():
    usuario_activo = True
    es_admin = False
    tiene_permiso = True

    if usuario_activo:
        print("Usuario activo")
        if es_admin:
            print("  → Acceso completo al sistema")
        elif tiene_permiso:
            print("  → Acceso limitado con permisos especiales")
        else:
            print("  → Acceso básico solamente")
    else:
        print("Usuario inactivo — acceso denegado")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.5 Expresión condicional (ternaria) — forma compacta
    """)
    return


@app.cell
def _():
    # Forma tradicional
    _numero = -5

    if _numero >= 0:
        tipo = "positivo"
    else:
        tipo = "negativo"

    # Forma ternaria (en una línea)
    tipo_compacto = "positivo" if _numero >= 0 else "negativo"

    print(f"{_numero} es {tipo}")
    print(f"{_numero} es {tipo_compacto}")  # Mismo resultado
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.6 Operador `in` — muy útil en condicionales
    """)
    return


@app.cell
def _():
    frutas_disponibles = ["manzana", "banano", "mango", "fresa"]
    pedido = "mango"

    if pedido in frutas_disponibles:
        print(f"✅ Tenemos {pedido} disponible")
    else:
        print(f"❌ Lo sentimos, no tenemos {pedido}")

    # También funciona con strings
    correo = "usuario@universidad.edu.co"
    if ".edu" in correo:
        print("📚 Correo institucional educativo")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### 🏆 Mini-Reto 4 — Ejecución Condicional

    **Objetivo:** Clasificar el riesgo de crédito de una persona.

    Dadas estas variables:
    - `ingreso_mensual`: salario mensual en pesos
    - `deuda_total`: deuda actual en pesos
    - `tiene_historial_crediticio`: True/False

    Reglas:
    1. Si la deuda es más del 50% del ingreso → riesgo **Alto**
    2. Si la deuda está entre 30% y 50% del ingreso → riesgo **Medio**
    3. Si la deuda es menos del 30% del ingreso:
       - Si tiene historial crediticio → riesgo **Bajo**
       - Si no tiene historial → riesgo **Medio-Bajo**
    4. Imprime el nivel de riesgo y una recomendación

    **Pista:** Calcula el ratio: `ratio = deuda_total / ingreso_mensual`
    """)
    return


@app.cell
def _():
    # ✏️ Tu solución aquí:
    ingreso_mensual = 3_000_000       # pesos
    deuda_total = 1_200_000           # pesos
    tiene_historial_crediticio = True

    # Calcula el ratio y clasifica el riesgo...
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 📌 MÓDULO 5 — Estructuras Integradas: Secuencias

    Python tiene varias estructuras de datos integradas. Las más importantes son:
    **listas**, **tuplas**, **diccionarios** y **conjuntos**.

    ### 5.1 Listas — colecciones ordenadas y mutables
    """)
    return


@app.cell
def _():
    # Crear una lista
    notas = [85, 92, 78, 95, 88, 72]
    print(f"Notas: {notas}")

    # Acceso por índice (empieza en 0)
    print(f"Primera nota: {notas[0]}")
    print(f"Última nota:  {notas[-1]}")   # Índice negativo cuenta desde el final

    # Slicing — obtener una porción
    print(f"Primeras 3:   {notas[:3]}")
    print(f"Últimas 2:    {notas[-2:]}")
    print(f"Del 2 al 4:   {notas[1:4]}")
    return


@app.cell
def _():
    # Operaciones básicas con listas
    _materias = ["Estadística", "Programación", "Cálculo"]

    # Agregar elementos
    _materias.append("Álgebra Lineal")
    print(f"Después de append: {_materias}")

    # Insertar en posición específica
    _materias.insert(1, "Bases de Datos")
    print(f"Después de insert: {_materias}")

    # Eliminar por valor
    _materias.remove("Cálculo")
    print(f"Después de remove: {_materias}")

    # Longitud
    print(f"Total materias: {len(_materias)}")

    # Verificar si existe
    print(f"¿Está Estadística? {'Estadística' in _materias}")
    return


@app.cell
def _():
    # Funciones útiles para listas numéricas
    datos = [23, 45, 12, 67, 34, 89, 11, 56]

    print(f"Datos: {datos}")
    print(f"Mínimo:  {min(datos)}")
    print(f"Máximo:  {max(datos)}")
    print(f"Suma:    {sum(datos)}")
    print(f"Promedio: {sum(datos)/len(datos):.2f}")
    print(f"Ordenado: {sorted(datos)}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 5.2 Tuplas — colecciones ordenadas e inmutables
    """)
    return


@app.cell
def _():
    # Las tuplas no pueden modificarse después de crearse
    coordenadas = (4.7110, -74.0721)   # Latitud y Longitud de Bogotá
    rgb_rojo = (255, 0, 0)
    dimensiones = (1920, 1080)

    print(f"Bogotá: {coordenadas}")
    print(f"Color rojo RGB: {rgb_rojo}")
    print(f"Resolución: {dimensiones[0]}x{dimensiones[1]}")

    # Desempaquetado (unpacking) — muy útil
    lat, lon = coordenadas
    print(f"Latitud: {lat}, Longitud: {lon}")

    # Las tuplas son inmutables
    try:
        coordenadas[0] = 5.0
    except TypeError as e:
        print(f"Error: {e}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 5.3 Diccionarios — pares clave:valor
    """)
    return


@app.cell
def _():
    # Diccionarios: clave → valor
    _estudiante = {
        "nombre": "Luisa Martínez",
        "edad": 21,
        "carrera": "Ingeniería de Datos",
        "semestre": 4,
        "promedio": 4.2
    }

    # Acceso
    print(f"Nombre: {_estudiante['nombre']}")
    print(f"Promedio: {_estudiante['promedio']}")

    # Acceso seguro (evita error si la clave no existe)
    ciudad = _estudiante.get("ciudad", "No registrada")
    print(f"Ciudad: {ciudad}")

    # Agregar/modificar
    _estudiante["ciudad"] = "Medellín"
    _estudiante["semestre"] = 5
    print(f"\nEstudiante actualizado:")
    for clave, valor in _estudiante.items():
        print(f"  {clave}: {valor}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 5.4 Conjuntos (Sets) — colecciones sin duplicados
    """)
    return


@app.cell
def _():
    # Los conjuntos eliminan duplicados automáticamente
    respuestas = ["A", "B", "A", "C", "B", "A", "D"]
    respuestas_unicas = set(respuestas)
    print(f"Respuestas: {respuestas}")
    print(f"Únicas: {respuestas_unicas}")

    # Operaciones de conjuntos (teoría de conjuntos)
    grupo_A = {"Ana", "Carlos", "María", "Pedro"}
    grupo_B = {"Carlos", "Laura", "María", "Luis"}

    print(f"\nGrupo A: {grupo_A}")
    print(f"Grupo B: {grupo_B}")
    print(f"Intersección (en ambos): {grupo_A & grupo_B}")
    print(f"Unión (en alguno): {grupo_A | grupo_B}")
    print(f"Solo en A: {grupo_A - grupo_B}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 5.5 Indexación y slicing avanzado
    """)
    return


@app.cell
def _():
    # Indexación: positiva y negativa
    letras = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    #           0    1    2    3    4    5    6      → índices positivos
    #          -7   -6   -5   -4   -3   -2   -1      → índices negativos

    print(f"Lista: {letras}")
    print(f"letras[0]:   {letras[0]}")    # 'a'
    print(f"letras[-1]:  {letras[-1]}")   # 'g'
    print(f"letras[2:5]: {letras[2:5]}")  # ['c', 'd', 'e']
    print(f"letras[::2]: {letras[::2]}")  # Cada 2 elementos: ['a', 'c', 'e', 'g']
    print(f"letras[::-1]:{letras[::-1]}") # Invertida
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### 🏆 Mini-Reto 5 — Estructuras de Datos

    **Objetivo:** Analizar datos de un grupo de estudiantes.

    Tienes la siguiente lista de calificaciones de un examen:
    ```python
    calificaciones = [72, 85, 91, 63, 78, 95, 82, 55, 88, 74, 91, 67, 83, 79, 88]
    ```

    1. ¿Cuántos estudiantes presentaron el examen?
    2. ¿Cuál fue la nota más alta y la más baja?
    3. ¿Cuál es el promedio del grupo?
    4. ¿Cuántas notas diferentes (únicas) hay en la lista? (usa `set`)
    5. Crea un diccionario `resumen` con las claves: `total`, `max`, `min`, `promedio`, `notas_unicas`
    6. **Bonus:** ¿Cuántos estudiantes obtuvieron nota mayor o igual a 80?
    """)
    return


@app.cell
def _():
    # ✏️ Tu solución aquí:
    calificaciones = [72, 85, 91, 63, 78, 95, 82, 55, 88, 74, 91, 67, 83, 79, 88]

    # Explora y analiza los datos...
    return


@app.cell
def _(mo):
    mo.accordion({
        "Pista!":mo.md("puedes usar un for para hacer el conteo!"),
        "Respuesta avanzada":mo.md("""
        ```python 
        len([n for n in calificaciones if n >= 80]
        ```""")
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 📌 MÓDULO 6 — Funciones

    Las funciones son **bloques de código reutilizables** que realizan una tarea específica.
    Son el corazón de la programación modular.

    ### 6.1 Definir y llamar funciones
    """)
    return


@app.cell
def _():
    # Definición
    def saludar():
        """Imprime un saludo simple."""
        print("¡Hola! Bienvenido al mundo de Python 🐍")

    # Llamada
    saludar()
    saludar()  # Las funciones se pueden llamar múltiples veces
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 6.2 Funciones con parámetros
    """)
    return


@app.cell
def _():
    def saludar_persona(nombre, saludo="Hola"):
        """
        Saluda a una persona.

        Args:
            nombre: El nombre de la persona
            saludo: El tipo de saludo (default: "Hola")
        """
        print(f"{saludo}, {nombre}! 👋")

    # Llamadas con diferentes argumentos
    saludar_persona("Ana")                    # Usa el saludo por defecto
    saludar_persona("Carlos", "Buenos días") # Saludo personalizado
    saludar_persona(saludo="Buenas noches", nombre="María")  # Argumentos por nombre
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 6.3 Funciones que retornan valores
    """)
    return


@app.cell
def _():
    def calcular_imc(peso, altura):
        """
        Calcula el Índice de Masa Corporal.

        Args:
            peso: Peso en kilogramos
            altura: Altura en metros

        Returns:
            float: El valor del IMC
        """
        imc = peso / (altura ** 2)
        return imc

    def clasificar_imc(imc):
        """Clasifica el IMC según estándares de la OMS."""
        if imc < 18.5:
            return "Bajo peso"
        elif imc < 25:
            return "Peso normal"
        elif imc < 30:
            return "Sobrepeso"
        else:
            return "Obesidad"

    # Usar las funciones
    mi_imc = calcular_imc(70, 1.75)
    clasificacion = clasificar_imc(mi_imc)

    print(f"IMC: {mi_imc:.2f}")
    print(f"Clasificación: {clasificacion}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 6.4 Funciones que retornan múltiples valores
    """)
    return


@app.cell
def _():
    def estadisticas_basicas(datos):
        """Calcula estadísticas básicas de una lista de números."""
        n = len(datos)
        promedio = sum(datos) / n
        minimo = min(datos)
        maximo = max(datos)
        rango = maximo - minimo

        return promedio, minimo, maximo, rango  # Retorna una tupla

    # Desempaquetando el resultado
    ventas = [1200, 1800, 950, 2100, 1600, 1350, 2400]
    prom, mín, máx, rang = estadisticas_basicas(ventas)

    print(f"Ventas diarias: {ventas}")
    print(f"Promedio: ${prom:,.2f}")
    print(f"Mínimo:   ${mín:,}")
    print(f"Máximo:   ${máx:,}")
    print(f"Rango:    ${rang:,}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 6.5 Alcance de variables (Scope)
    """)
    return


@app.cell
def _(variable_local):
    variable_global = "Soy global"  # Existe en todo el programa

    def mostrar_scope():
        variable_local = "Soy local"  # Solo existe dentro de esta función
        print(f"Dentro de la función: {variable_global}")  # Puede acceder a la global
        print(f"Variable local: {variable_local}")

    mostrar_scope()
    print(f"Fuera de la función: {variable_global}")

    # Esto generaría error: print(variable_local) — no existe aquí
    try:
        print(variable_local)
    except NameError as e:
        print(f"Error: {e}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 6.6 Funciones Lambda (funciones anónimas)
    """)
    return


@app.cell
def _():
    # Lambda: funciones pequeñas de una línea
    cuadrado = lambda x: x ** 2
    suma = lambda a, b: a + b
    es_par = lambda n: n % 2 == 0

    print(f"Cuadrado de 7: {cuadrado(7)}")
    print(f"Suma 3 + 4: {suma(3, 4)}")
    print(f"¿8 es par? {es_par(8)}")

    # Muy útiles para ordenar listas de diccionarios
    estudiantes = [
        {"nombre": "Ana", "promedio": 4.5},
        {"nombre": "Luis", "promedio": 3.8},
        {"nombre": "Sofía", "promedio": 4.9},
        {"nombre": "Pedro", "promedio": 4.1},
    ]

    # Ordenar por promedio
    ordenados = sorted(estudiantes, key=lambda e: e["promedio"], reverse=True)
    print("\nRanking por promedio:")
    for i, est in enumerate(ordenados, 1):
        print(f"  {i}. {est['nombre']}: {est['promedio']}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### 🏆 Mini-Reto 6 — Funciones

    **Objetivo:** Crear funciones para un sistema de notas.

    Implementa las siguientes funciones:

    1. `letra_a_numero(letra)`: Convierte letra (A, B, C, D, F) a número (4.0, 3.0, 2.0, 1.0, 0.0)
    2. `numero_a_letra(numero)`: Convierte número (0-4) a letra según la escala anterior
    3. `promedio_ponderado(notas, creditos)`: Calcula el promedio ponderado dado:
       - `notas`: lista de notas numéricas (e.g., [3.5, 4.0, 2.8])
       - `creditos`: lista de créditos de cada materia (e.g., [3, 4, 2])
       - Fórmula: `sum(nota * credito) / sum(creditos)`

    Prueba tus funciones con:
    ```python
    notas_ejemplo = [3.5, 4.0, 2.8, 4.5, 3.2]
    creditos_ejemplo = [3, 4, 2, 3, 2]
    ```
    """)
    return


@app.cell
def _():
    # ✏️ Tu solución aquí:

    def letra_a_numero(letra):
        pass  # Implementa esta función

    def numero_a_letra(numero):
        pass  # Implementa esta función

    def promedio_ponderado(notas, creditos):
        pass  # Implementa esta función

    # Prueba tus funciones:
    notas_ejemplo = [3.5, 4.0, 2.8, 4.5, 3.2]
    creditos_ejemplo = [3, 4, 2, 3, 2]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 📌 MÓDULO 7 — Iteraciones

    Las iteraciones permiten **repetir acciones** sin escribir el mismo código múltiples veces.
    Python tiene dos tipos principales: `for` y `while`.

    ### 7.1 El bucle `for` — iterar sobre una secuencia
    """)
    return


@app.cell
def _():
    # Iterar sobre una lista
    frutas = ["manzana", "banano", "fresa", "mango"]

    print("Lista de frutas:")
    for fruta in frutas:
        print(f"  🍓 {fruta.capitalize()}")
    return


@app.cell
def _():
    # Iterar sobre un rango de números
    print("Tabla de multiplicar del 3:")
    for _i in range(1, 11):
        print(f"  3 × {_i:2d} = {3*_i:3d}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 7.2 `range()` — generar secuencias numéricas
    """)
    return


@app.cell
def _():
    # range(stop)          → 0 hasta stop-1
    # range(start, stop)   → start hasta stop-1
    # range(start, stop, step) → con paso personalizado

    print(f"range(5):          {list(range(5))}")
    print(f"range(2, 8):       {list(range(2, 8))}")
    print(f"range(0, 20, 5):   {list(range(0, 20, 5))}")
    print(f"range(10, 0, -2):  {list(range(10, 0, -2))}")  # Conteo regresivo
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 7.3 `enumerate()` — iterar con índice
    """)
    return


@app.cell
def _():
    materias = ["Estadística", "Álgebra Lineal", "Programación", "Bases de Datos"]

    print("Plan de estudios:")
    for numero, materia in enumerate(materias, start=1):
        print(f"  {numero}. {materia}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 7.4 `zip()` — iterar sobre dos listas en paralelo
    """)
    return


@app.cell
def _():
    asignaturas = ["Estadística", "Cálculo", "Programación"]
    creditos = [3, 4, 3]
    profesores = ["Dr. Rodríguez", "Dra. López", "Ing. Martínez"]

    print(f"{'Materia':<20} {'Créditos':<10} {'Profesor'}")
    print("-" * 50)
    for mat, cred, prof in zip(asignaturas, creditos, profesores):
        print(f"{mat:<20} {cred:<10} {prof}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 7.5 Iterar sobre diccionarios
    """)
    return


@app.cell
def _():
    puntajes = {
        "Ana": 92,
        "Carlos": 78,
        "María": 95,
        "Luis": 85
    }

    print("Resultados del examen:")
    for estudiante, puntaje in puntajes.items():
        estado = "✅" if puntaje >= 80 else "❌"
        print(f"  {estado} {estudiante}: {puntaje}")

    aprobados = sum(1 for p in puntajes.values() if p >= 80)
    print(f"\nAprobados: {aprobados}/{len(puntajes)}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 7.6 El bucle `while` — repetir mientras se cumple una condición
    """)
    return


@app.cell
def _():
    # while es ideal cuando no sabes cuántas veces iterar
    saldo = 1_000_000
    tasa_mensual = 0.005  # 0.5% mensual
    meta = 1_200_000
    meses = 0

    print(f"Inversión inicial: ${saldo:,}")
    print(f"Meta:              ${meta:,}")
    print(f"Tasa mensual:       {tasa_mensual*100}%\n")

    while saldo < meta:
        saldo = saldo * (1 + tasa_mensual)
        meses += 1

    print(f"🎯 Meta alcanzada en {meses} meses")
    print(f"Saldo final: ${saldo:,.2f}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 7.7 `break` y `continue` — control del bucle
    """)
    return


@app.cell
def _():
    # break — detiene el bucle completamente
    print("Buscando el primer número divisible por 7:")
    for n in range(1, 100):
        if n % 7 == 0:
            print(f"  ¡Encontrado! {n}")
            break

    # continue — salta a la siguiente iteración
    print("\nNúmeros del 1 al 10 que NO son múltiplos de 3:")
    for n in range(1, 11):
        if n % 3 == 0:
            continue        # Salta este número
        print(f"  {n}", end=" ")
    print()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 7.8 Comprensión de listas (List Comprehension) — Python idiomático
    """)
    return


@app.cell
def _():
    # Forma tradicional (con for)
    cuadrados_tradicional = []
    for _i in range(1, 11):
        cuadrados_tradicional.append(_i ** 2)

    # Forma con comprensión de lista (más pythonica)
    cuadrados = [_i ** 2 for i in range(1, 11)]
    print(f"Cuadrados: {cuadrados}")

    # Con condición
    pares = [_i for _i in range(1, 21) if _i % 2 == 0]
    print(f"Pares del 1 al 20: {pares}")

    # Transformar una lista
    nombres = ["ana", "carlos", "maría", "luis"]
    nombres_capitalizados = [n.title() for n in nombres]
    print(f"Capitalizados: {nombres_capitalizados}")

    # Comprensión de diccionario
    celsius = [0, 10, 20, 30, 40]
    fahrenheit = {c: c * 9/5 + 32 for c in celsius}
    print(f"Conversión C→F: {fahrenheit}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### 🏆 Mini-Reto 7 — Iteraciones

    **Objetivo:** Analizar datos de ventas con bucles.

    Tienes este registro de ventas semanales (en millones de pesos):
    ```python
    ventas_semanales = [12.5, 8.3, 15.7, 11.2, 9.8, 18.4, 14.1, 7.6, 16.3, 13.5]
    ```

    Usando bucles y/o comprensiones de lista:

    1. Imprime cada semana con su número y ventas (ej: "Semana 1: $12.5M")
    2. Calcula el total acumulado semana a semana e imprímelo
    3. Identifica e imprime las semanas donde las ventas superaron el promedio
    4. Crea una lista `rendimiento` que tenga "Alto" si ventas > 13M, "Medio" si entre 10-13M, "Bajo" si < 10M
    5. **Bonus:** Encuentra la racha consecutiva más larga de ventas superiores al promedio
    """)
    return


@app.cell
def _():
    # ✏️ Tu solución aquí:
    ventas_semanales = [12.5, 8.3, 15.7, 11.2, 9.8, 18.4, 14.1, 7.6, 16.3, 13.5]

    # 1. Imprime semanas con número...

    # 2. Acumulado...

    # 3. Semanas sobre el promedio...

    # 4. Lista de rendimiento...
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 🎯 Proyecto Integrador Final

    Combina todos los conceptos aprendidos para construir un **analizador de datos estudiantiles**.

    ### Especificaciones:

    Tienes los siguientes datos de un grupo universitario:

    ```python
    estudiantes = [
        {"nombre": "Ana Gómez",     "notas": [85, 92, 78, 95, 88]},
        {"nombre": "Carlos Pérez",  "notas": [72, 65, 80, 75, 68]},
        {"nombre": "María López",   "notas": [95, 98, 92, 97, 96]},
        {"nombre": "Luis Torres",   "notas": [55, 60, 48, 70, 58]},
        {"nombre": "Sofía Ruiz",    "notas": [80, 85, 79, 88, 82]},
    ]
    ```

    **Construye funciones para:**

    1. `calcular_promedio(notas)` → promedio de la lista
    2. `asignar_estado(promedio)` → "Aprobado" (>=70) o "Reprobado" (<70)
    3. `generar_reporte(estudiantes)` → imprime un reporte formateado con:
       - Nombre del estudiante
       - Promedio (2 decimales)
       - Estado (Aprobado/Reprobado)
       - Mejor y peor nota
    4. `estadisticas_grupo(estudiantes)` → retorna un diccionario con:
       - `mejor_estudiante`: nombre del que tiene mayor promedio
       - `peor_estudiante`: nombre del que tiene menor promedio
       - `promedio_grupal`: promedio de todos los promedios
       - `tasa_aprobacion`: porcentaje de aprobados

    Finalmente, llama a ambas funciones e imprime los resultados.
    """)
    return


@app.cell
def _():
    # ✏️ Tu proyecto integrador aquí:

    estudiantes_data = [
        {"nombre": "Ana Gómez",     "notas": [85, 92, 78, 95, 88]},
        {"nombre": "Carlos Pérez",  "notas": [72, 65, 80, 75, 68]},
        {"nombre": "María López",   "notas": [95, 98, 92, 97, 96]},
        {"nombre": "Luis Torres",   "notas": [55, 60, 48, 70, 58]},
        {"nombre": "Sofía Ruiz",    "notas": [80, 85, 79, 88, 82]},
    ]

    def calcular_promedio(notas):
        pass

    def asignar_estado(promedio):
        pass

    def generar_reporte(estudiantes):
        pass

    def estadisticas_grupo(estudiantes):
        pass

    # Llama a tus funciones:
    # generar_reporte(estudiantes_data)
    # stats = estadisticas_grupo(estudiantes_data)
    # print(stats)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 📚 Resumen de Conceptos

    | Módulo | Conceptos clave |
    |--------|----------------|
    | **Semántica** | Interpretado, case-sensitive, indentación, comentarios |
    | **Pseudocódigo y Utilidades** | `print()`, `input()`, `type()`, `help()` |
    | **Variables y Expresiones** | Tipos de datos, aritmética, strings, casting, operadores |
    | **Condicionales** | `if`, `elif`, `else`, operador ternario, `in` |
    | **Estructuras de datos** | listas, tuplas, diccionarios, conjuntos, slicing |
    | **Funciones** | definición, parámetros, retorno, scope, lambda |
    | **Iteraciones** | `for`, `while`, `range`, `enumerate`, `zip`, `break`, `continue`, list comprehension |

    ---

    ### 🔗 Recursos para continuar aprendiendo

    - **Python for Everybody** — Charles Severance (base de este notebook)
    - **Python for Data Analysis** — Wes McKinney (NumPy, Pandas, análisis de datos)
    - Documentación oficial: [docs.python.org/es](https://docs.python.org/es/3/)
    - Práctica interactiva: [exercism.io/tracks/python](https://exercism.io/tracks/python)

    > 🚀 **¡Felicitaciones por completar el módulo!** El siguiente paso es aprender
    > NumPy y Pandas para análisis de datos real.
    """)
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


if __name__ == "__main__":
    app.run()
