import marimo

__generated_with = "0.20.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Clase 01 — Introducción a Python para Ciencia de Datos (sesión guiada)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Plan sugerido

    **Estructura por bloques (orientativa):**
    1. Semántica y ejecución (10–15 min)
    2. Pseudocódigo + utilidades (10–15 min)
    3. Variables y expresiones (10–15 min)
    4. Condicionales (10–15 min)
    5. Secuencias (10–15 min)
    6. Funciones (15–20 min)
    7. Iteraciones (15–20 min)
    8. Diccionarios y conjuntos (10–15 min)
    9. Comprensiones (10–15 min)
    10. Mini-reto integrador (15–25 min)

    <!-- **Dinámica recomendada**
    - Docente: ejecuta las celdas “Live coding” y pregunta predicciones antes de correr.
    - Estudiantes: resuelven las celdas “Ejercicio” y luego ejecutan tests. -->
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # 1) Semántica: ejecución, nombres, objetos, mutabilidad

    ## Objetivo
    Comprender cómo Python evalúa el código y cómo la asignación enlaza nombres con objetos.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Live coding 1.1 — Orden de ejecución

    Antes de ejecutar, predice qué se imprime.

    Puntos a enfatizar:
    - Orden secuencial dentro de una celda
    - Reasignación de nombres
    """)
    return


@app.cell
def _():
    print("Inicio")
    x_sem_lc1 = 10
    print("x_sem_lc1 =", x_sem_lc1)
    x_sem_lc1 = x_sem_lc1 + 5
    print("x_sem_lc1 (nuevo) =", x_sem_lc1)
    print("Fin")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Live coding 1.2 — Identidad vs igualdad; mutabilidad

    Idea clave:
    - `==` compara contenido
    - `is` compara identidad (mismo objeto)
    """)
    return


@app.cell
def _():
    a_sem_lc2 = [1, 2, 3]
    b_sem_lc2 = a_sem_lc2

    print("a_sem_lc2 is b_sem_lc2:", a_sem_lc2 is b_sem_lc2)
    print("id(a):", id(a_sem_lc2))
    print("id(b):", id(b_sem_lc2))

    b_sem_lc2.append(4)
    print("a después de mutar b:", a_sem_lc2)

    u_sem_lc2 = [1, 2, 3]
    v_sem_lc2 = [1, 2, 3]
    print("u == v:", u_sem_lc2 == v_sem_lc2)
    print("u is v:", u_sem_lc2 is v_sem_lc2)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejercicio 1 — Referencias y copia

    Completa la celda siguiente. Luego ejecuta los tests.
    """)
    return


@app.cell
def _():
    # TODO:
    # 1) Define lista_ex1 como [10, 20]
    # 2) Define ref_ex1 apuntando al mismo objeto
    # 3) Agrega 30 usando ref_ex1
    # 4) Define copia_ex1 como una copia (objeto distinto) con el mismo contenido
    lista_ex1 = [10, 20]
    ref_ex1 = lista_ex1
    ref_ex1.append(30)
    copia_ex1 = lista_ex1.copy()
    return copia_ex1, lista_ex1, ref_ex1


@app.cell
def _(copia_ex1, lista_ex1, mo, ref_ex1):
    assert lista_ex1 == [10, 20, 30]
    assert ref_ex1 == [10, 20, 30]
    assert lista_ex1 is ref_ex1
    assert copia_ex1 == [10, 20, 30]
    assert copia_ex1 is not lista_ex1
    mo.md("✅ Ejercicio 1: OK")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # 2) Pseudocódigo y utilidades

    ## Objetivo
    Convertir especificaciones (inputs → proceso → outputs) en funciones verificables, usando utilidades estándar.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Live coding 2.1 — Del pseudocódigo al código (promedio)

    Pseudocódigo:
    1. Recibir secuencia numérica no vacía
    2. Validar longitud
    3. Sumar y dividir por n
    """)
    return


@app.cell
def _():
    def promedio_lc2(x_lc2):
        if len(x_lc2) == 0:
            raise ValueError("Secuencia vacía.")
        return sum(x_lc2) / len(x_lc2)

    print(promedio_lc2([10, 20, 30]))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Live coding 2.2 — `type`, `isinstance`, `len`, `sorted`, `help` (idea)

    En clase: mostrar que *aprender a leer docs* es parte del trabajo técnico.
    """)
    return


@app.cell
def _():
    datos_lc2b = [3, 1, 2]
    print("type(datos):", type(datos_lc2b))
    print("len(datos):", len(datos_lc2b))
    print("sorted(datos):", sorted(datos_lc2b))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejercicio 2 — Resumen numérico (dict)

    Implementa `resumen_numerico_ex2(x)`:
    - valida que x sea lista/tupla no vacía
    - valida que elementos sean int/float
    - retorna dict con: n, minimo, maximo, suma, promedio
    """)
    return


@app.function
def resumen_numerico_ex2(x_ex2):
    if not isinstance(x_ex2, (list, tuple)):
        raise TypeError("x debe ser lista o tupla.")
    if len(x_ex2) == 0:
        raise ValueError("x no puede estar vacío.")
    for i_ex2, v_ex2 in enumerate(x_ex2):
        if not isinstance(v_ex2, (int, float)):
            raise TypeError(f"Elemento no numérico en {i_ex2}: {v_ex2!r}")
    n_ex2 = len(x_ex2)
    minimo_ex2 = min(x_ex2)
    maximo_ex2 = max(x_ex2)
    suma_ex2 = sum(x_ex2)
    promedio_ex2 = suma_ex2 / n_ex2
    return {
        "n": n_ex2,
        "minimo": minimo_ex2,
        "maximo": maximo_ex2,
        "suma": suma_ex2,
        "promedio": promedio_ex2,
    }


@app.cell
def _(mo):
    out_ex2 = resumen_numerico_ex2([10, 20, 30])
    assert out_ex2["n"] == 3
    assert out_ex2["minimo"] == 10
    assert out_ex2["maximo"] == 30
    assert out_ex2["suma"] == 60
    assert out_ex2["promedio"] == 20.0
    mo.md("✅ Ejercicio 2: OK")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # 3) Variables y expresiones

    ## Objetivo
    Escribir expresiones aritméticas, comparativas y lógicas con precedencia correcta.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Live coding 3.1 — Precedencia y paréntesis

    Pedir predicción:
    - `2 + 3 * 4`
    - `(2 + 3) * 4`
    """)
    return


@app.cell
def _():
    res_lc3a = 2 + 3 * 4
    res_lc3b = (2 + 3) * 4
    print("2 + 3 * 4 =", res_lc3a)
    print("(2 + 3) * 4 =", res_lc3b)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejercicio 3 — Clasificador de signo

    Implementa `clasificar_signo_ex3(x)`:
    - TypeError si no es numérico
    - retorna: "positivo", "negativo" o "cero"
    """)
    return


@app.function
def clasificar_signo_ex3(x_ex3):
    if not isinstance(x_ex3, (int, float)):
        raise TypeError("x debe ser numérico.")
    if x_ex3 > 0:
        return "positivo"
    if x_ex3 < 0:
        return "negativo"
    return "cero"


@app.cell
def _(mo):
    assert clasificar_signo_ex3(10) == "positivo"
    assert clasificar_signo_ex3(-1.5) == "negativo"
    assert clasificar_signo_ex3(0) == "cero"
    mo.md("✅ Ejercicio 3: OK")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # 4) Ejecución condicional

    ## Objetivo
    Codificar reglas de decisión con `if/elif/else` y validaciones.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Live coding 4.1 — Categorizar una nota

    Regla:
    - >= 4.5: Excelente
    - >= 3.5: Aprobado
    - else: Reprobado
    """)
    return


@app.cell
def _():
    nota_lc4 = 3.7
    if nota_lc4 >= 4.5:
        cat_lc4 = "Excelente"
    elif nota_lc4 >= 3.5:
        cat_lc4 = "Aprobado"
    else:
        cat_lc4 = "Reprobado"
    print(cat_lc4)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejercicio 4 — Clasificar IMC

    Implementa `clasificar_imc_ex4(peso_kg, altura_m)`:
    - TypeError si entradas no numéricas
    - ValueError si altura <= 0
    - retorna categorías: Bajo peso / Normal / Sobrepeso / Obesidad
    """)
    return


@app.function
def clasificar_imc_ex4(peso_kg_ex4, altura_m_ex4):
    if not isinstance(peso_kg_ex4, (int, float)) or not isinstance(altura_m_ex4, (int, float)):
        raise TypeError("Peso y altura deben ser numéricos.")
    if altura_m_ex4 <= 0:
        raise ValueError("La altura debe ser mayor que 0.")
    imc_ex4 = peso_kg_ex4 / (altura_m_ex4 ** 2)
    if imc_ex4 < 18.5:
        return "Bajo peso"
    if imc_ex4 < 25:
        return "Normal"
    if imc_ex4 < 30:
        return "Sobrepeso"
    return "Obesidad"


@app.cell
def _(mo):
    assert clasificar_imc_ex4(50, 1.70) == "Bajo peso"
    assert clasificar_imc_ex4(65, 1.70) == "Normal"
    assert clasificar_imc_ex4(80, 1.70) == "Sobrepeso"
    assert clasificar_imc_ex4(95, 1.70) == "Obesidad"
    mo.md("✅ Ejercicio 4: OK")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # 5) Secuencias (list, tuple, str)

    ## Objetivo
    Usar indexación, slicing y métodos básicos para manipular datos ordenados.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Live coding 5.1 — Slicing como herramienta de exploración

    Demostrar:
    - `seq[0]`, `seq[-1]`
    - `seq[1:5]`
    - `seq[::-1]`
    """)
    return


@app.cell
def _():
    seq_lc5 = [0, 1, 2, 3, 4, 5, 6]
    print("seq[0]:", seq_lc5[0])
    print("seq[-1]:", seq_lc5[-1])
    print("seq[1:5]:", seq_lc5[1:5])
    print("seq[::-1]:", seq_lc5[::-1])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejercicio 5 — Analizar secuencia

    Implementa `analizar_secuencia_ex5(seq)`:
    - acepta list/tuple no vacía
    - retorna dict con: longitud, primer_elemento, ultimo_elemento, invertida
    """)
    return


@app.function
def analizar_secuencia_ex5(seq_ex5):
    if not isinstance(seq_ex5, (list, tuple)):
        raise TypeError("seq debe ser lista o tupla.")
    if len(seq_ex5) == 0:
        raise ValueError("seq no puede estar vacía.")
    return {
        "longitud": len(seq_ex5),
        "primer_elemento": seq_ex5[0],
        "ultimo_elemento": seq_ex5[-1],
        "invertida": seq_ex5[::-1],
    }


@app.cell
def _(mo):
    out_ex5 = analizar_secuencia_ex5([10, 20, 30])
    assert out_ex5["longitud"] == 3
    assert out_ex5["primer_elemento"] == 10
    assert out_ex5["ultimo_elemento"] == 30
    assert out_ex5["invertida"] == [30, 20, 10]
    mo.md("✅ Ejercicio 5: OK")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # 6) Funciones

    ## Objetivo
    Diseñar funciones con validaciones, docstrings y retornos claros.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Live coding 6.1 — Función con docstring y validación

    Ejemplo: normalización a [0, 1].
    """)
    return


@app.cell
def _():
    def normalizar_0_1_lc6(x_min_lc6, x_max_lc6, x_lc6):
        """Normaliza x al rango [0, 1] dados x_min y x_max."""
        if x_max_lc6 <= x_min_lc6:
            raise ValueError("x_max debe ser mayor que x_min.")
        if not (x_min_lc6 <= x_lc6 <= x_max_lc6):
            raise ValueError("x debe estar dentro de [x_min, x_max].")
        return (x_lc6 - x_min_lc6) / (x_max_lc6 - x_min_lc6)

    print(normalizar_0_1_lc6(0, 10, 5))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejercicio 6 — Evaluación de aprobación

    Implementa `evaluar_aprobacion_ex6(nota)`:
    - TypeError si no numérica
    - ValueError si fuera de 0–5
    - retorna "Aprobado" si >= 3; si no, "Reprobado"
    """)
    return


@app.function
def evaluar_aprobacion_ex6(nota_ex6):
    if not isinstance(nota_ex6, (int, float)):
        raise TypeError("La nota debe ser numérica.")
    if not (0 <= nota_ex6 <= 5):
        raise ValueError("La nota debe estar entre 0 y 5.")
    return "Aprobado" if nota_ex6 >= 3 else "Reprobado"


@app.cell
def _(mo):
    assert evaluar_aprobacion_ex6(4) == "Aprobado"
    assert evaluar_aprobacion_ex6(2.5) == "Reprobado"
    mo.md("✅ Ejercicio 6: OK")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # 7) Iteraciones

    ## Objetivo
    Recorrer colecciones y construir algoritmos iterativos con patrones claros.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Live coding 7.1 — Patrón acumulador

    Suma manual vs `sum()`:
    - comprender el patrón ayuda a construir algoritmos más generales.
    """)
    return


@app.cell
def _():
    datos_lc7 = [2, 4, 6, 8]
    suma_lc7 = 0
    for v_lc7 in datos_lc7:
        suma_lc7 += v_lc7
    print("Suma acumulada:", suma_lc7)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejercicio 7 — Factorial (iterativo)

    Implementa `factorial_ex7(n)`:
    - TypeError si n no int
    - ValueError si n < 0
    - calcular factorial con bucle `for`
    """)
    return


@app.function
def factorial_ex7(n_ex7):
    if not isinstance(n_ex7, int):
        raise TypeError("n debe ser entero.")
    if n_ex7 < 0:
        raise ValueError("n debe ser no negativo.")
    out_ex7 = 1
    for i_ex7 in range(1, n_ex7 + 1):
        out_ex7 *= i_ex7
    return out_ex7


@app.cell
def _(mo):
    assert factorial_ex7(0) == 1
    assert factorial_ex7(5) == 120
    mo.md("✅ Ejercicio 7: OK")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # 8) Diccionarios y conjuntos

    ## Objetivo
    Modelar datos categóricos y conteos con `dict`, y deduplicar/operar conjuntos con `set`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Live coding 8.1 — Conteo con diccionarios (patrón EDA)

    Estrategia estándar:
    - inicializar dict vacío
    - actualizar con `get(clave, 0) + 1`
    """)
    return


@app.cell
def _():
    etiquetas_lc8 = ["HTA", "DM2", "HTA", "EPOC", "HTA"]
    conteo_lc8 = {}
    for e_lc8 in etiquetas_lc8:
        conteo_lc8[e_lc8] = conteo_lc8.get(e_lc8, 0) + 1
    print(conteo_lc8)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejercicio 8 — Resumen categórico (dict + set)

    Implementa `resumen_categorico_ex8(lista_etiquetas)`:
    - valida list/tuple no vacío
    - valida elementos string
    - retorna dict con: unicos (set), conteo (dict)
    """)
    return


@app.function
def resumen_categorico_ex8(lista_etiquetas_ex8):
    if not isinstance(lista_etiquetas_ex8, (list, tuple)):
        raise TypeError("La entrada debe ser una lista o tupla.")
    if len(lista_etiquetas_ex8) == 0:
        raise ValueError("La secuencia no puede estar vacía.")
    for i_ex8, v_ex8 in enumerate(lista_etiquetas_ex8):
        if not isinstance(v_ex8, str):
            raise TypeError(f"Elemento no string en {i_ex8}: {v_ex8!r}")
    unicos_ex8 = set(lista_etiquetas_ex8)
    conteo_ex8 = {}
    for v_ex8b in lista_etiquetas_ex8:
        conteo_ex8[v_ex8b] = conteo_ex8.get(v_ex8b, 0) + 1
    return {"unicos": unicos_ex8, "conteo": conteo_ex8}


@app.cell
def _(mo):
    out_ex8 = resumen_categorico_ex8(["a", "b", "a", "c", "b", "a"])
    assert out_ex8["unicos"] == {"a", "b", "c"}
    assert out_ex8["conteo"]["a"] == 3
    assert out_ex8["conteo"]["b"] == 2
    assert out_ex8["conteo"]["c"] == 1
    mo.md("✅ Ejercicio 8: OK")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # 9) Comprensiones

    ## Objetivo
    Construir colecciones de manera expresiva, controlando complejidad y manteniendo legibilidad.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Live coding 9.1 — List comprehension con filtro

    Ejemplo:
    - extraer pares
    - transformar impares
    """)
    return


@app.cell
def _():
    x_lc9 = [1, 2, 3, 4, 5, 6]
    pares_lc9 = [v_lc9 for v_lc9 in x_lc9 if v_lc9 % 2 == 0]
    cuadrados_impares_lc9 = [v_lc9 ** 2 for v_lc9 in x_lc9 if v_lc9 % 2 != 0]
    print("pares:", pares_lc9)
    print("cuadrados_impares:", cuadrados_impares_lc9)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ejercicio 9 — Pipeline simple con comprehensions

    Implementa `pipeline_simple_ex9(x)`:
    - valida list/tuple
    - valida que todos sean enteros
    - retorna dict con:
      - pares (list comprehension)
      - cuadrados_impares (list comprehension)
      - mapa_paridad (dict comprehension)
    """)
    return


@app.function
def pipeline_simple_ex9(x_ex9):
    if not isinstance(x_ex9, (list, tuple)):
        raise TypeError("x debe ser lista o tupla.")
    for i_ex9, v_ex9 in enumerate(x_ex9):
        if not isinstance(v_ex9, int):
            raise TypeError(f"Elemento no entero en {i_ex9}: {v_ex9!r}")
    pares_ex9 = [v_ex9 for v_ex9 in x_ex9 if v_ex9 % 2 == 0]
    cuadrados_impares_ex9 = [v_ex9 ** 2 for v_ex9 in x_ex9 if v_ex9 % 2 != 0]
    mapa_paridad_ex9 = {v_ex9: ("par" if v_ex9 % 2 == 0 else "impar") for v_ex9 in x_ex9}
    return {
        "pares": pares_ex9,
        "cuadrados_impares": cuadrados_impares_ex9,
        "mapa_paridad": mapa_paridad_ex9,
    }


@app.cell
def _(mo):
    out_ex9 = pipeline_simple_ex9([1, 2, 3, 4, 5])
    assert out_ex9["pares"] == [2, 4]
    assert out_ex9["cuadrados_impares"] == [1, 9, 25]
    assert out_ex9["mapa_paridad"][1] == "impar"
    assert out_ex9["mapa_paridad"][2] == "par"
    assert out_ex9["mapa_paridad"][5] == "impar"
    mo.md("✅ Ejercicio 9: OK")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Mini-reto integrador (final)

    ## Enunciado

    Implementa una función `perfil_paciente(registros)` donde:

    **Entrada**
    - `registros`: lista de diccionarios, donde cada diccionario representa un paciente con llaves:
      - `id` (str, requerida)
      - `edad` (int/float, requerida)
      - `dx` (str, requerida; diagnóstico)
      - `peso_kg` (int/float, opcional)
      - `altura_m` (int/float, opcional)

    **Proceso**
    1. Validar que `registros` sea lista no vacía.
    2. Validar que cada registro tenga `id`, `edad`, `dx` con tipos adecuados.
    3. Construir y retornar un diccionario con:
       - `n`: número de pacientes
       - `dx_unicos`: set de diagnósticos únicos
       - `conteo_dx`: dict con frecuencias por dx
       - `ids_mayores`: lista con ids de pacientes con edad >= 65 (usar list comprehension)
       - `imc_por_id`: dict {id: imc} solo para pacientes con peso_kg y altura_m válidos (altura>0)
     (usar dict comprehension; omitir pacientes sin datos completos)

    **Salida**
    - dict con esas llaves exactas.

    Este reto integra: validación, condicionales, iteraciones, dict/set y comprensiones.
    """)
    return


@app.function
def perfil_paciente_ex_final(registros_ex_final):

    if not isinstance(registros_ex_final, list):
        raise TypeError("registros debe ser una lista.")
    if len(registros_ex_final) == 0:
        raise ValueError("registros no puede estar vacío.")

    # Validación y preparación
    dx_list_ex_final = []
    ids_mayores_tmp = []

    for i_ex_final, r_ex_final in enumerate(registros_ex_final):
        if not isinstance(r_ex_final, dict):
            raise TypeError(f"Registro no dict en posición {i_ex_final}.")

        if "id" not in r_ex_final or "edad" not in r_ex_final or "dx" not in r_ex_final:
            raise ValueError(f"Faltan llaves requeridas en posición {i_ex_final}.")

        if not isinstance(r_ex_final["id"], str):
            raise TypeError(f"id debe ser str en posición {i_ex_final}.")
        if not isinstance(r_ex_final["edad"], (int, float)):
            raise TypeError(f"edad debe ser numérica en posición {i_ex_final}.")
        if not isinstance(r_ex_final["dx"], str):
            raise TypeError(f"dx debe ser str en posición {i_ex_final}.")

        dx_list_ex_final.append(r_ex_final["dx"])

        if r_ex_final["edad"] >= 65:
            ids_mayores_tmp.append(r_ex_final["id"])

    # Conteo dx (patrón dict)
    conteo_dx_ex_final = {}
    for dx_ex_final in dx_list_ex_final:
        conteo_dx_ex_final[dx_ex_final] = conteo_dx_ex_final.get(dx_ex_final, 0) + 1

    dx_unicos_ex_final = set(dx_list_ex_final)

    # list comprehension para ids mayores (se pide explícitamente)
    ids_mayores_ex_final = [r["id"] for r in registros_ex_final if r["edad"] >= 65]

    # dict comprehension para imc_por_id, omitiendo incompletos
    def _imc_valido(r):
        return (
            "peso_kg" in r
            and "altura_m" in r
            and isinstance(r["peso_kg"], (int, float))
            and isinstance(r["altura_m"], (int, float))
            and r["altura_m"] > 0
        )

    imc_por_id_ex_final = {
        r["id"]: (r["peso_kg"] / (r["altura_m"] ** 2))
        for r in registros_ex_final
        if _imc_valido(r)
    }

    return {
        "n": len(registros_ex_final),
        "dx_unicos": dx_unicos_ex_final,
        "conteo_dx": conteo_dx_ex_final,
        "ids_mayores": ids_mayores_ex_final,
        "imc_por_id": imc_por_id_ex_final,
    }


@app.cell
def _(mo):
    registros_t_final = [
        {"id": "P1", "edad": 70, "dx": "HTA", "peso_kg": 80, "altura_m": 1.70},
        {"id": "P2", "edad": 40, "dx": "DM2"},
        {"id": "P3", "edad": 66, "dx": "HTA", "peso_kg": 65, "altura_m": 1.60},
    ]

    out_t_final = perfil_paciente_ex_final(registros_t_final)

    assert out_t_final["n"] == 3
    assert out_t_final["dx_unicos"] == {"HTA", "DM2"}
    assert out_t_final["conteo_dx"]["HTA"] == 2
    assert out_t_final["conteo_dx"]["DM2"] == 1
    assert out_t_final["ids_mayores"] == ["P1", "P3"]
    assert "P2" not in out_t_final["imc_por_id"]
    assert round(out_t_final["imc_por_id"]["P1"], 6) == round(80 / (1.70 ** 2), 6)
    assert round(out_t_final["imc_por_id"]["P3"], 6) == round(65 / (1.60 ** 2), 6)

    mo.md(
        r"""
    ✅ Mini-reto integrador: OK

    Sugerencia para cierre de clase:
    - discutir decisiones de validación
    - discutir cómo extender a más variables (por ejemplo, sexo, biomarcadores)
    - señalar que en ciencia de datos esto evoluciona a estructuras tabulares (pandas)
    """
    )
    return


if __name__ == "__main__":
    app.run()
