# Semana 4 · Lección 1 · Estadística básica con statsmodels

import marimo as mo

app = mo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
# Semana 4 · Lección 1 · Estadística básica con statsmodels

## Propósito de la sesión

En esta lección introducimos el uso de **statsmodels** como herramienta para realizar análisis estadístico formal sobre datos clínicos.

Hasta ahora has trabajado con:

- pandas → manipulación de datos
- numpy → operaciones numéricas
- visualización → exploración

Ahora damos un paso más:

**Pasamos de describir datos a modelarlos estadísticamente.**

El objetivo es:

- estimar relaciones entre variables
- cuantificar asociaciones
- interpretar resultados con rigor

---
"""
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
## Contexto aplicado en salud

Imagina que trabajas con un dataset clínico que contiene:

- edad
- presión arterial sistólica (sbp)
- colesterol LDL
- sexo

Una pregunta clave en epidemiología es:

👉 ¿Cómo se relaciona la edad con la presión arterial?

Hasta ahora podrías:

- calcular promedios
- hacer gráficos

Pero ahora queremos:

👉 **modelar la relación de forma explícita**

---
"""
    )
    return


@app.cell
def _(pd):
    datos = pd.read_csv("dataset_clase_semana2_small.csv")
    datos
    return (datos,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
## Concepto clave: modelo estadístico

Un modelo estadístico es una representación formal de la relación entre variables.

En este caso:

- Variable explicativa: edad
- Variable respuesta: presión arterial

La forma más simple es:

👉 **regresión lineal**

Esto implica asumir:

- existe una relación aproximadamente lineal
- podemos estimar una pendiente

---
"""
    )
    return


@app.cell
def _(datos):
    datos[["age", "sbp"]].head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
## Introducción a statsmodels

La librería **statsmodels** permite:

- ajustar modelos estadísticos
- obtener coeficientes
- evaluar significancia

A diferencia de pandas:

👉 no solo transforma datos, sino que **estima parámetros**

---
"""
    )
    return


@app.cell
def _():
    import statsmodels.api as sm
    return (sm,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
## Preparación del modelo

Para ajustar un modelo lineal necesitamos:

1. Variable dependiente (y)
2. Variable independiente (X)
3. Agregar constante (intercepto)

---
"""
    )
    return


@app.cell
def _(datos, sm):
    y = datos["sbp"]
    X = datos[["age"]]

    X = sm.add_constant(X)

    X.head()
    return (X, y)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
## Ajuste del modelo

Ahora ajustamos un modelo de regresión lineal:

👉 sbp ~ age

---
"""
    )
    return


@app.cell
def _(X, y, sm):
    modelo = sm.OLS(y, X).fit()
    modelo.summary()
    return (modelo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
## Interpretación básica

En el output del modelo debes observar:

- coeficiente de edad
- intercepto
- p-value

Interpretación:

- El coeficiente indica cuánto cambia la presión arterial por cada año de edad
- El p-value indica si la relación es estadísticamente significativa

Este es el primer paso hacia análisis inferencial.

---
"""
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
## Ejemplo interpretado

Si el coeficiente de edad es:

👉 0.8

Entonces:

👉 Por cada año adicional, la presión arterial aumenta en promedio 0.8 unidades.

Esto tiene implicaciones clínicas importantes.

---
"""
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
## Mini-reto

Construye un modelo que relacione:

- variable dependiente: LDL
- variable independiente: edad

Guarda el modelo en una variable llamada:

👉 `modelo_ldl`

---
"""
    )
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    modelo_ldl = None
    return (modelo_ldl,)


@app.cell
def _(mo):
    from marimo import TipContent

    tip_content = TipContent(
        items_raw=[
            "Selecciona la columna 'ldl' como variable dependiente.",
            "Usa la edad como variable explicativa.",
            "Recuerda agregar constante con sm.add_constant().",
            "<solucion> y = datos['ldl']; X = sm.add_constant(datos[['age']]); modelo_ldl = sm.OLS(y, X).fit()",
        ]
    )
    tip_content.render()
    return


@app.cell
def _(modelo_ldl):
    from marimo import TestContent

    test_content = TestContent(
        items_raw=[
            """
assert modelo_ldl is not None
""",
            """
assert hasattr(modelo_ldl, "params")
""",
        ],
        namespace=globals(),
    )
    test_content.render()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
## Integración conceptual

Hasta ahora aprendiste:

- cómo definir variables para un modelo
- cómo ajustar una regresión lineal
- cómo interpretar coeficientes

Esto representa un cambio clave:

👉 De análisis descriptivo → análisis explicativo

Este paso es fundamental en:

- epidemiología
- investigación clínica
- salud pública

---
"""
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
## Cierre

statsmodels permite:

- formalizar relaciones
- cuantificar efectos
- fundamentar decisiones

En las siguientes lecciones avanzaremos hacia:

- evaluación de modelos
- diagnóstico
- construcción de pipelines analíticos

---
"""
    )
    return


if __name__ == "__main__":
    app.run()