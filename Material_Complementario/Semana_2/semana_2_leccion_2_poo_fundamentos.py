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
    # Semana 2 · Lección 2 — Programación orientada a objetos (fundamentos)

    **Contexto:** En salud pública, rara vez trabajamos con un solo número aislado.
    Trabajamos con **entidades**: un paciente, una medición, una consulta, un registro de vacunas.

    La Programación Orientada a Objetos (POO) propone un modelo simple:

    - Una **clase** es una *plantilla* (tipo) que define:
      - **atributos**: datos que describen el objeto
      - **métodos**: funciones que operan sobre esos datos
    - Un **objeto** (instancia) es un “ejemplar” creado a partir de la clase.

    En esta sesión construiremos objetos pequeños (pero realistas) para modelar datos clínicos.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 1) Clase como “tipo” y objeto como “instancia”

    Antes de ver el código, piensa en el siguiente problema:

    En un sistema de historia clínica electrónica, cada **paciente** tiene información básica como:

    - un identificador,
    - su edad,
    - su sexo.

    En lugar de manejar estas variables por separado, la programación orientada a objetos propone **agrupar esa información dentro de una entidad**.

    Esa entidad será un **objeto**.

    Para crear objetos necesitamos primero definir una **clase**, que funciona como una **plantilla** que describe:

    - qué datos tendrá el objeto (**atributos**)
    - qué puede hacer el objeto (**métodos**)

    En el ejemplo que sigue observa tres cosas importantes:

    1. **La definición de la clase** (`class Paciente`)
    2. **El constructor `__init__`**, donde se guardan los datos del objeto
    3. **Un método (`describir`)** que usa esos datos para producir un resultado

    Luego verás cómo crear un objeto a partir de esa clase y cómo interactuar con él.
    """)
    return


@app.cell
def _():
    # Definimos una clase.
    # Una clase funciona como una plantilla para crear objetos.
    class Paciente:
        # El método __init__ es el constructor de la clase.
        # Se ejecuta automáticamente cuando se crea un objeto nuevo.
        # Su función es inicializar los atributos del objeto.
        def __init__(self, paciente_id, edad_anios, sexo):
            # Guardamos la información recibida dentro del objeto.
            # El prefijo self. indica que estos valores pasan a formar
            # parte del estado interno de la instancia.
            self.paciente_id = paciente_id
            self.edad_anios = edad_anios
            self.sexo = sexo

        # Este es un método de la clase.
        # Los métodos son funciones que trabajan con los datos del objeto.
        def describir(self):
            # Construimos una representación en texto del paciente.
            # Usamos los atributos almacenados en la propia instancia.
            return (
                f"Paciente(id={self.paciente_id}, edad={self.edad_anios}, sexo={self.sexo})"
            )

    # Creamos una instancia de la clase Paciente.
    # Es decir, un paciente concreto construido a partir de la plantilla.
    p1 = Paciente(paciente_id="EHR-0001", edad_anios=52, sexo="femenino")

    # Llamamos al método describir() del objeto.
    print(p1.describir())

    # Mostramos el tipo del objeto creado.
    # Esto confirma que p1 es una instancia de la clase Paciente.
    print("Tipo de p1:", type(p1))
    return (p1,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 2) Atributos: el estado interno del objeto

    Cuando creamos un objeto, ese objeto **guarda información dentro de sí mismo**.

    Esa información se llama **atributos**.

    Un atributo es simplemente una variable que pertenece al objeto.

    En Python accedemos a un atributo usando la notación con punto:

    ```python
    objeto.atributo
    ```

    Por ejemplo, en el caso de un paciente:

    - `edad_anios` puede representar la edad del paciente
    - `sexo` puede representar el sexo
    - `paciente_id` puede identificar el registro clínico

    Lo importante es que estos datos **permanecen asociados al objeto**.

    Si el objeto cambia, sus atributos también pueden cambiar.

    En el ejemplo que sigue observa dos cosas:

    1. cómo **leer** un atributo desde el objeto
    2. cómo **modificar** ese atributo
    """)
    return


@app.cell
def _(p1):
    # Accedemos al atributo edad_anios del objeto p1
    print("Edad:", p1.edad_anios)

    # Modificamos el atributo del objeto.
    # Esto cambia el estado interno de p1.
    p1.edad_anios = p1.edad_anios + 1

    # Volvemos a leer el atributo para observar el cambio
    print("Edad (un año después):", p1.edad_anios)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 3) Métodos: comportamiento del objeto

    Hasta ahora vimos que un objeto **almacena información** mediante atributos.

    Pero los objetos también pueden **realizar acciones**.

    Esas acciones se definen mediante **métodos**.

    Un método es simplemente una función que pertenece a una clase.

    En general, un método puede:

    - leer atributos del objeto
    - modificar atributos
    - calcular valores derivados a partir de esos atributos

    En salud es muy común que los métodos representen **cálculos clínicos**.

    Por ejemplo:

    - calcular BMI a partir de peso y talla
    - calcular riesgo cardiovascular
    - resumir una medición fisiológica

    En el siguiente ejemplo verás una clase simple que almacena:

    - peso
    - talla

    y define un método que calcula el **BMI**.
    """)
    return


@app.cell
def _():
    # Definimos una clase que representa una medición de antropometría
    class Antropometria:
        # El constructor guarda peso y talla dentro del objeto
        def __init__(self, peso_kg, talla_m):
            self.peso_kg = peso_kg
            self.talla_m = talla_m

        # Este método calcula el BMI usando los atributos del objeto
        def bmi(self):
            # Fórmula estándar del BMI
            return self.peso_kg / (self.talla_m**2)

    # Creamos una instancia de la clase
    medicion = Antropometria(peso_kg=72.0, talla_m=1.80)

    # Llamamos al método bmi() del objeto
    print("BMI:", medicion.bmi())
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---

    # Mini-retos (3)

    Hasta ahora viste tres ideas centrales:

    - una **clase** como plantilla,
    - un **objeto** como instancia concreta,
    - y la diferencia entre **atributos** (estado) y **métodos** (comportamiento).

    Ahora vas a pasar de observar ejemplos a **construir tus propias clases**.

    En los siguientes retos tendrás que decidir:

    - qué información debe vivir dentro del objeto,
    - qué métodos necesita,
    - y cómo organizar correctamente la lógica dentro de la clase.

    En cada reto encontrarás:

    - un contexto breve del dominio,
    - una celda editable para completar,
    - tips progresivos,
    - y tests para comprobar tu implementación.

    Recomendación de trabajo:

    1. lee primero el reto completo,
    2. identifica los atributos y métodos antes de escribir código,
    3. implementa una primera versión simple,
    4. usa los tips solo si realmente los necesitas,
    5. interpreta los tests como una ayuda para razonar mejor tu solución.

    La meta no es memorizar estructuras, sino practicar cómo traducir una idea del mundo real a un objeto en Python.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto 1 — Objeto clínico mínimo

    **Dominio:** clínica / antropometría

    En este primer reto vas a construir una clase sencilla que represente un perfil clínico básico.

    El propósito es reforzar dos ideas fundamentales:

    - un objeto puede **guardar información propia**,
    - y un método puede **usar esa información** para producir un resultado.

    Tu tarea será modelar una entidad individual con datos antropométricos y permitir que esa entidad genere un cálculo derivado a partir de su estado interno.

    Antes de programar, piensa:

    - qué datos deben quedar almacenados dentro del objeto,
    - qué comportamiento corresponde naturalmente a ese objeto,
    - y qué información debería reutilizar el método sin pedirla de nuevo.
    """)
    return


@app.cell
def _():
    class ClinicalProfile:
        # TODO: complete the constructor
        def __init__(self, age_years, weight_kg, height_m):
            pass

        # TODO: complete the method
        def bmi(self):
            pass

    profile_r1 = ClinicalProfile(age_years=45, weight_kg=81.0, height_m=1.74)
    print("R1 -> BMI:", profile_r1.bmi())
    return (profile_r1,)


@app.cell(hide_code=True)
def _():
    _tip_content = TipContent(
        items_raw=[
            r"""
    <Estado del objeto>
    Empieza identificando qué información debe permanecer asociada a cada instancia.

    Si un dato forma parte del perfil clínico, debería quedar guardado dentro del objeto desde el momento en que se crea.
    """,
            r"""
    <Método y estado interno>
    El método de este reto no debería depender de variables externas.

    Su trabajo consiste en usar la información ya almacenada en la instancia para producir un valor nuevo.
    """,
            r"""
    <Resultado derivado>
    Aquí no se pide guardar un resultado fijo, sino calcularlo a partir de atributos numéricos del objeto.

    Revisa con calma cuál es la operación que conecta esos atributos y dónde debe implementarse.
    """,
            r"""
    <solucion>

    ```python
    class ClinicalProfile:
        def __init__(self, age_years, weight_kg, height_m):
            self.age_years = age_years
            self.weight_kg = weight_kg
            self.height_m = height_m

        def bmi(self):
            return self.weight_kg / (self.height_m ** 2)
    ```
    """,
        ]
    )

    _tip_content.render()
    return


@app.cell(hide_code=True)
def _(profile_r1):
    _test_content = TestContent(
        items_raw=[
            r"""
    <Persistencia del estado>
    Verifica que la instancia conserve correctamente la información con la que fue creada.

    ```python
    assert profile_r1.age_years == 45, "La edad no quedó almacenada correctamente."
    assert profile_r1.weight_kg == 81.0, "El peso no quedó almacenado correctamente."
    assert profile_r1.height_m == 1.74, "La talla no quedó almacenada correctamente."
    print("Estado interno correcto.")
    ```
    """,
            r"""
    <Salida del método>
    Verifica que el método produzca un valor y no una salida vacía.

    ```python
    resultado = profile_r1.bmi()

    assert resultado is not None, (
        "`bmi()` devolvió `None`. Revisa si el método sigue incompleto "
        "o si olvidaste retornar el resultado."
    )

    print("El método devuelve un valor.")
    ```
    """,
            r"""
    <Resultado esperado>
    Verifica que el cálculo coincida con el valor esperado para esta instancia.

    ```python
    bmi_ref = 81.0 / (1.74 ** 2)

    assert abs(profile_r1.bmi() - bmi_ref) < 1e-12, (
        f"BMI incorrecto. Esperado {bmi_ref}, obtenido {profile_r1.bmi()}"
    )

    print("Cálculo correcto.")
    ```
    """,
        ],
        namespace=globals(),
    )

    profile_r1
    _test_content.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto 2 — Registro de vacunación

    **Dominio:** salud pública / vacunación

    En este reto vas a construir una clase que represente un registro simple asociado a una vacuna.

    A diferencia del reto anterior, aquí el objeto no solo debe guardar información: también debe poder **actualizarse con el tiempo**.

    La idea central es trabajar con un objeto cuyo estado interno cambia a medida que se incorporan nuevos datos.

    Antes de programar, piensa:

    - qué información identifica al registro,
    - qué parte de la información puede crecer o acumularse,
    - y qué operación permitiría resumir ese historial.
    """)
    return


@app.cell
def _():
    class VaccinationRecord:
        # TODO: complete the constructor
        def __init__(self, vaccine_name):
            pass

        # TODO: complete the method
        def add_dose(self, dose_mg):
            pass

        # TODO: complete the method
        def total_dose_mg(self):
            pass

    vac_r2 = VaccinationRecord("influenza")
    vac_r2.add_dose(15.0)
    vac_r2.add_dose(15.0)
    vac_r2.add_dose(7.5)


    try:
        print("R2 -> vacuna:", vac_r2.vaccine_name, "| total mg:", vac_r2.total_dose_mg())
    except Exception as e:
        print("Error al ejecutar el código de prueba:", e)
    return (vac_r2,)


@app.cell(hide_code=True)
def _():
    _tip_content = TipContent(
        items_raw=[
            r"""
    <Estado inicial>
    Todo objeto necesita un estado inicial coherente desde el momento en que se crea.

    Piensa qué información está disponible desde el inicio y qué estructura debería empezar vacía.
    """,
            r"""
    <Cambio de estado>
    Uno de los métodos de este reto no devuelve un cálculo, sino que modifica el contenido interno del objeto.

    Identifica con precisión qué atributo debe actualizarse cuando aparece una nueva observación.
    """,
            r"""
    <Resumen de lo acumulado>
    El otro método debe producir un resumen numérico de todo lo que el objeto ha ido registrando.

    Antes de implementarlo, piensa qué debería pasar cuando ya existen varios valores guardados.
    """,
            r"""
    <solucion>

    ```python
    class VaccinationRecord:
        def __init__(self, vaccine_name):
            self.vaccine_name = vaccine_name
            self.doses_mg = []

        def add_dose(self, dose_mg):
            self.doses_mg.append(dose_mg)

        def total_dose_mg(self):
            total = 0.0
            for dose in self.doses_mg:
                total += dose
            return total
    ```
    """,
        ]
    )

    _tip_content.render()
    return


@app.cell(hide_code=True)
def _(vac_r2):
    _test_content = TestContent(
        items_raw=[
            r"""
    <Identidad del objeto>
    Verifica que el registro conserve correctamente la información con la que fue creado.

    ```python
    assert vac_r2.vaccine_name == "influenza", (
        "El nombre de la vacuna no quedó almacenado correctamente."
    )
    print("Identidad del objeto correcta.")
    ```
    """,
            r"""
    <Actualización del estado>
    Verifica que las observaciones añadidas hayan quedado registradas dentro del objeto.

    ```python
    assert vac_r2.doses_mg == [15.0, 15.0, 7.5], (
        "Las dosis registradas no coinciden con lo esperado."
    )
    print("Actualización del estado correcta.")
    ```
    """,
            r"""
    <Resumen numérico>
    Verifica que el método de resumen produzca el total correcto.

    ```python
    total = vac_r2.total_dose_mg()

    assert total is not None, (
        "`total_dose_mg()` devolvió `None`. Revisa si el método sigue incompleto "
        "o si olvidaste retornar el resultado."
    )

    assert abs(total - 37.5) < 1e-12, (
        f"Total incorrecto. Esperado 37.5, obtenido {total}"
    )

    print("Resumen numérico correcto.")
    ```
    """,
        ],
        namespace=globals(),
    )

    vac_r2
    _test_content.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto 3 — Triage simple basado en signos vitales

    **Dominio:** urgencias / triage

    Este último reto integra varias ideas al mismo tiempo:

    - almacenamiento de atributos,
    - lógica condicional dentro de un método,
    - y manejo básico de errores cuando la entrada no es interpretable.

    Vas a construir una clase que produzca una clasificación cualitativa a partir de dos mediciones clínicas.

    Aquí ya no basta con guardar datos: también necesitas organizar correctamente una secuencia de decisiones dentro del método.

    Antes de programar, piensa:

    - qué datos debe conservar la instancia,
    - en qué orden conviene evaluar las reglas,
    - y qué salida debería producirse cuando la información de entrada no puede usarse de forma segura.
    """)
    return


@app.cell
def _():
    class TriageRule:
        # TODO: complete the constructor
        def __init__(self, systolic_bp_mmHg, heart_rate_bpm):
            pass

        # TODO: complete the method
        def hemodynamic_risk(self):
            pass

    t_ok = TriageRule(systolic_bp_mmHg=86, heart_rate_bpm=95)
    t_mod = TriageRule(systolic_bp_mmHg=96, heart_rate_bpm=88)
    t_low = TriageRule(systolic_bp_mmHg=118, heart_rate_bpm=72)
    t_bad = TriageRule(systolic_bp_mmHg="?", heart_rate_bpm=72)

    print("R3 -> ok:", t_ok.hemodynamic_risk())
    print("R3 -> mod:", t_mod.hemodynamic_risk())
    print("R3 -> low:", t_low.hemodynamic_risk())
    print("R3 -> bad:", t_bad.hemodynamic_risk())
    return t_bad, t_low, t_mod, t_ok


@app.cell(hide_code=True)
def _():
    _tip_content = TipContent(
        items_raw=[
            r"""
    <Preparación de la entrada>
    Antes de aplicar reglas de clasificación, conviene asegurarte de que los valores puedan tratarse como números.

    Si ese paso falla, la lógica posterior ya no tendría sentido.
    """,
            r"""
    <Prioridad de reglas>
    Cuando varias categorías son posibles, el orden de evaluación importa.

    Piensa cuál categoría debería revisarse primero para evitar clasificaciones incorrectas.
    """,
            r"""
    <Condiciones clínicas>
    La clasificación depende de dos mediciones distintas.

    Revisa con cuidado cuándo una sola condición basta para activar una categoría y cuándo debe continuar la evaluación.
    """,
            r"""
    <Manejo de errores>
    Este reto también pide una salida segura cuando la entrada no puede interpretarse correctamente.

    El objetivo no es detener el programa, sino devolver una etiqueta consistente ante datos inválidos.
    """,
            r"""
    <solucion>

    ```python
    class TriageRule:
        def __init__(self, systolic_bp_mmHg, heart_rate_bpm):
            self.systolic_bp_mmHg = systolic_bp_mmHg
            self.heart_rate_bpm = heart_rate_bpm

        def hemodynamic_risk(self):
            try:
                sbp = float(self.systolic_bp_mmHg)
                hr = float(self.heart_rate_bpm)
            except (TypeError, ValueError):
                return "invalid"

            if sbp < 90 or hr > 120:
                return "high"
            elif 90 <= sbp <= 100 or 100 <= hr <= 120:
                return "moderate"
            else:
                return "low"
    ```
    """,
        ]
    )

    _tip_content.render()
    return


@app.cell(hide_code=True)
def _(t_bad, t_low, t_mod, t_ok):
    _test_content = TestContent(
        items_raw=[
            r"""
    <Clasificación de alto riesgo>
    Verifica que un caso claramente alterado se clasifique en la categoría más alta.

    ```python
    assert t_ok.hemodynamic_risk() == "high", (
        "La clasificación de alto riesgo no es correcta."
    )
    print("Clasificación de alto riesgo correcta.")
    ```
    """,
            r"""
    <Clasificación intermedia>
    Verifica que un caso limítrofe se clasifique en la categoría intermedia.

    ```python
    assert t_mod.hemodynamic_risk() == "moderate", (
        "La clasificación moderada no es correcta."
    )
    print("Clasificación intermedia correcta.")
    ```
    """,
            r"""
    <Clasificación de bajo riesgo>
    Verifica que un caso sin criterios de alerta quede en la categoría baja.

    ```python
    assert t_low.hemodynamic_risk() == "low", (
        "La clasificación de bajo riesgo no es correcta."
    )
    print("Clasificación de bajo riesgo correcta.")
    ```
    """,
            r"""
    <Manejo de entrada inválida>
    Verifica que la implementación devuelva una salida estable cuando la entrada no puede interpretarse como numérica.

    ```python
    assert t_bad.hemodynamic_risk() == "invalid", (
        "La entrada inválida debería producir la etiqueta `invalid`."
    )
    print("Manejo de entrada inválida correcto.")
    ```
    """,
        ],
        namespace=globals(),
    )

    t_bad, t_low, t_mod, t_ok
    _test_content.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---

    ## Cierre conceptual

    En esta lección trabajaste con tres ideas fundamentales de la programación orientada a objetos:

    - **atributos**, para representar el estado interno de una entidad,
    - **métodos**, para definir su comportamiento,
    - y **objetos**, como unidades que combinan datos y lógica.

    También viste que una clase puede servir para modelar situaciones de salud de forma clara y organizada:

    - un perfil clínico,
    - un registro de vacunación,
    - una regla simple de triage.

    Esta forma de pensar será importante más adelante, cuando empieces a trabajar con estructuras y librerías más complejas.
    """)
    return


if __name__ == "__main__":
    app.run()
