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
def _(mo):
    mo.md(r"""
    ## 1) Clase como “tipo” y objeto como “instancia”

    Piensa en **clase** como el “molde” y en **objeto** como el “objeto fabricado”.

    En Python:

    - Definimos una clase con `class`.
    - Creamos objetos llamando la clase como si fuera una función: `obj = MiClase(...)`
    - Accedemos a atributos y métodos con `.` (dot notation).

    La palabra `self` es una referencia al *objeto actual* dentro de sus métodos.
    """)
    return


@app.cell
def _():
    class Patient:
        def __init__(self, patient_id, age_years, sex):
            self.patient_id = patient_id
            self.age_years = age_years
            self.sex = sex

        def describe(self):
            return (
                f"Patient(id={self.patient_id}, age={self.age_years}, sex={self.sex})"
            )

    p1 = Patient(patient_id="EHR-0001", age_years=52, sex="female")

    print(p1.describe())
    print("type(p1):", type(p1))
    return (p1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2) Atributos: estado interno del objeto

    Un atributo es una variable “dentro” del objeto: `obj.atributo`.

    En salud:
    - `age_years` es atributo del paciente
    - `systolic_bp_mmHg` podría ser atributo de una medición

    La clave es que el atributo *vive* asociado al objeto y viaja con él.
    """)
    return


@app.cell
def _(p1):
    print("Edad:", p1.age_years)
    p1.age_years = p1.age_years + 1  # el objeto cambia su estado
    print("Edad (un año después):", p1.age_years)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3) Métodos: comportamiento sobre el estado

    Un método es una función definida dentro de la clase.
    Conceptualmente, un método suele:

    - leer atributos
    - modificar atributos
    - devolver un resultado

    Ejemplo: una medición antropométrica puede calcular BMI a partir de peso y talla.
    """)
    return


@app.cell
def _():
    class Anthropometrics:
        def __init__(self, weight_kg, height_m):
            self.weight_kg = weight_kg
            self.height_m = height_m

        def bmi(self):
            return self.weight_kg / (self.height_m**2)

    a = Anthropometrics(weight_kg=72.0, height_m=1.80)
    print("BMI:", a.bmi())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    # Mini-retos (3)

    Completa los `# TODO` para que los tests (`assert`) pasen.

    Regla de oro:
    - El *resultado* debe pasar las pruebas.
    - Los tips te dan estructura, pero **no** sustituyen tu implementación.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Mini-reto 1 — Objeto clínico mínimo

    **Dominio:** clínica / antropometría

    Crea una clase `ClinicalProfile` que modele un perfil mínimo del paciente:

    Atributos:
    - `age_years` (int)
    - `weight_kg` (float)
    - `height_m` (float)

    Método:
    - `bmi()` → retorna el BMI como `weight_kg / (height_m ** 2)`

    Completa los `# TODO`.
    """)
    return


@app.cell
def _():
    class ClinicalProfile:
        # TODO: define __init__ with age_years, weight_kg, height_m
        def __init__(self, age_years, weight_kg, height_m):
            pass

        # TODO: define bmi method
        def bmi(self):
            pass

    profile_r1 = ClinicalProfile(age_years=45, weight_kg=81.0, height_m=1.74)
    print("R1 -> BMI:", profile_r1.bmi())
    return (profile_r1,)


@app.cell(hide_code=True)
def _(mo):
    _tip_content = mo.md(
        r"""
    ### Tip

    - En `__init__`, guarda cada parámetro como atributo:
      - `self.age_years = age_years` (y análogo para peso y talla)
    - En `bmi`, usa los atributos (`self.weight_kg`, `self.height_m`) y aplica la fórmula.
    - Si recibes un `TypeError` al dividir, revisa que estés devolviendo un número (no `None`).
    """
    )
    mo.accordion({"Tip (estructura lógica)": _tip_content})
    return


@app.cell(hide_code=True)
def _(mo, profile_r1):
    bmi_ref = 81.0 / (1.74**2)

    assert abs(profile_r1.bmi() - bmi_ref) < 1e-12
    assert profile_r1.age_years == 45

    mo.md("✅ Mini-reto 1 superado.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Mini-reto 2 — Registro de vacunación

    **Dominio:** salud pública / vacunación

    Crea una clase `VaccinationRecord` para una vacuna específica (por ejemplo, influenza).

    Atributos:
    - `vaccine_name` (str)
    - `doses_mg` (lista de floats) con las dosis aplicadas

    Métodos:
    - `add_dose(dose_mg)` → agrega una dosis a la lista
    - `total_dose_mg()` → suma todas las dosis en mg y retorna el total

    Completa los `# TODO`.
    """)
    return


@app.cell
def _():
    class VaccinationRecord:
        # TODO: define __init__ with vaccine_name and create empty doses_mg list
        def __init__(self, vaccine_name):
            pass

        # TODO: define add_dose method (mutates doses_mg)
        def add_dose(self, dose_mg):
            pass

        # TODO: define total_dose_mg method (returns float)
        def total_dose_mg(self):
            pass

    vac_r2 = VaccinationRecord("influenza")
    vac_r2.add_dose(15.0)
    vac_r2.add_dose(15.0)
    vac_r2.add_dose(7.5)

    print("R2 -> vacuna:", vac_r2.vaccine_name, "| total mg:", vac_r2.total_dose_mg())
    return (vac_r2,)


@app.cell(hide_code=True)
def _(mo):
    _tip_content = mo.md(
        r"""
    ### Tip

    - En `__init__`, inicializa la lista vacía:
      - `self.doses_mg = []`
    - Para agregar:
      - usa el método de lista `.append(...)`
    - Para sumar sin usar librerías:
      - puedes recorrer con `for` y acumular en una variable `total`
    """
    )
    mo.accordion({"Tip (estructura lógica)": _tip_content})
    return


@app.cell(hide_code=True)
def _(mo, vac_r2):
    assert vac_r2.vaccine_name == "influenza"
    assert vac_r2.doses_mg == [15.0, 15.0, 7.5]
    assert abs(vac_r2.total_dose_mg() - 37.5) < 1e-12

    mo.md("✅ Mini-reto 2 superado.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Mini-reto 3 — Triage simple basado en signos vitales (final)

    **Dominio:** urgencias / triage

    Implementa una clase `TriageRule` que evalúe riesgo hemodinámico con reglas simples.

    Atributos:
    - `systolic_bp_mmHg` (float)
    - `heart_rate_bpm` (float)

    Método:
    - `hemodynamic_risk()` → retorna un string:
      - `"high"` si PAS < 90 **o** FC > 120
      - `"moderate"` si PAS está entre 90 y 100 (inclusive) **o** FC entre 100 y 120 (inclusive)
      - `"low"` en cualquier otro caso

    Requisito adicional:
    - Incluye manejo básico de errores con `try/except` dentro del método:
      - Si alguno de los valores no puede interpretarse como float, retorna `"invalid"`

    Completa los `# TODO`.
    """)
    return


@app.cell
def _():
    class TriageRule:
        # TODO: define __init__ with systolic_bp_mmHg and heart_rate_bpm
        def __init__(self, systolic_bp_mmHg, heart_rate_bpm):
            pass

        # TODO: implement hemodynamic_risk with try/except + if/elif/else
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
def _(mo):
    tip_content = mo.md(
        r"""
    ### Tip

    - En `hemodynamic_risk`, intenta convertir:
      - `sbp = float(self.systolic_bp_mmHg)`
      - `hr = float(self.heart_rate_bpm)`
      - Si falla, atrapa la excepción y retorna `"invalid"`.
    - Luego aplica reglas con `if/elif/else`:
      - Prioriza `"high"` primero (reglas más críticas).
      - Después `"moderate"`.
      - Finalmente `"low"`.
    - En reglas combinadas, usa `or` para “cualquiera de las condiciones”.
    """
    )
    mo.accordion({"Tip (estructura lógica)": tip_content})
    return


@app.cell(hide_code=True)
def _(mo, t_bad, t_low, t_mod, t_ok):
    assert t_ok.hemodynamic_risk() == "high"
    assert t_mod.hemodynamic_risk() == "moderate"
    assert t_low.hemodynamic_risk() == "low"
    assert t_bad.hemodynamic_risk() == "invalid"

    mo.md("✅ Mini-reto 3 superado.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Cierre conceptual

    Hoy usaste POO para:

    - **encapsular** datos + lógica (atributos + métodos)
    - tratar cada entidad de salud como un “objeto” con estado y comportamiento
    - preparar el camino para diseño modular en análisis de datos (sin adelantar librerías)

    En la siguiente progresión, esta forma de pensar será clave cuando trabajemos con
    estructuras y APIs más complejas.
    """)
    return


if __name__ == "__main__":
    app.run()
