# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "numpy==2.4.2",
#     "pandas==3.0.1",
#     "pytest==9.0.2",
#     "requests==2.32.5",
#     "statsmodels==0.14.4",
# ]
# ///

import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")

with app.setup(hide_code=True):
    import marimo as mo
    import numpy as np
    import pandas as pd
    import statsmodels.api as sm

    from setup import TipContent, TestContent, find_data_file


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Semana 4 · Lección 1
    ## Introducción a la modelación estadística con statsmodels

    En esta sesión se introduce una transición importante dentro del curso:

    hasta ahora trabajaste principalmente con **descripción, organización y visualización** de datos;
    a partir de esta semana comenzaremos a trabajar con **modelos estadísticos explícitos**.

    El objetivo no es aprender una gran cantidad de funciones, sino comprender una idea fundamental:

    > un modelo estadístico permite expresar formalmente la relación entre una variable de interés y una o más variables explicativas.

    En esta primera lección trabajaremos exclusivamente con el caso más simple:

    - una variable respuesta numérica,
    - una variable explicativa numérica,
    - y un modelo lineal básico.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Propósito de la sesión

    Al finalizar esta lección deberías poder:

    - identificar la variable respuesta y la variable explicativa en una pregunta sencilla,
    - preparar los datos para un modelo lineal,
    - ajustar una regresión lineal con `statsmodels`,
    - reconocer las partes principales del output,
    - e interpretar de forma inicial un coeficiente de regresión.

    Esta sesión no busca todavía una discusión avanzada sobre supuestos, diagnóstico o causalidad.

    El foco está en construir una primera comprensión sólida del paso:

    **descripción → modelación**
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Contexto aplicado

    Supón que estás trabajando con una base clínica que contiene mediciones demográficas y cardiometabólicas.

    Una pregunta analítica razonable podría ser:

    **¿cómo se relaciona la edad con la presión arterial sistólica?**

    Esta pregunta es distinta de una pregunta puramente descriptiva.

    Por ejemplo:

    - calcular la media de presión arterial describe la muestra,
    - pero modelar la relación entre edad y presión arterial intenta cuantificar cómo cambian juntas ambas variables.

    Ese cambio de enfoque es el que da sentido al uso de un modelo estadístico.
    """)
    return


@app.cell
def _():
    data_path = find_data_file("public/dataset_clase_semana2_small.csv")
    datos = pd.read_csv(data_path)

    assert not datos.empty
    assert {"age", "sbp_mmHg", "ldl_mg_dL"}.issubset(datos.columns)

    datos.head()
    return (datos,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Variables de trabajo

    Para esta primera lección nos concentraremos en un número reducido de variables:

    - `age`: edad
    - `sbp_mmHg`: presión arterial sistólica
    - `ldl_mg_dL`: colesterol LDL

    Esta reducción deliberada del problema tiene un propósito pedagógico:

    antes de trabajar con modelos más complejos, conviene entender con claridad cómo se construye un modelo simple y cómo se interpreta su salida.
    """)
    return


@app.cell
def _(datos):
    datos[["age", "sbp_mmHg", "ldl_mg_dL"]].head()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Concepto clave: modelo estadístico

    Un modelo estadístico es una representación formal de una relación entre variables.

    En este caso, queremos expresar la idea de que la presión arterial sistólica puede variar en función de la edad.

    Eso puede escribirse, en términos conceptuales, como:

    **presión arterial = función(edad)**

    En esta primera aproximación utilizaremos una forma lineal sencilla.

    Esto implica que el modelo intentará estimar:

    - un intercepto,
    - y una pendiente asociada a la edad.

    La pendiente resume cuánto cambia, en promedio, la variable respuesta cuando la variable explicativa aumenta una unidad.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## ¿Qué hace statsmodels en esta lección?

    `statsmodels` permite ajustar modelos estadísticos y devolver una salida formal con:

    - coeficientes,
    - errores estándar,
    - valores p,
    - intervalos de confianza,
    - y medidas globales de ajuste.

    A diferencia de una operación descriptiva simple, aquí no solo transformamos datos.

    Aquí **estimamos parámetros**.

    Por eso el output del modelo debe leerse como una pieza analítica estructurada, no como un cálculo cualquiera.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Estructura mínima de un modelo lineal

    Para ajustar una regresión lineal simple con `statsmodels` necesitamos definir:

    1. una variable dependiente (`y`),
    2. una variable independiente (`X`),
    3. y una constante.

    En esta sesión:

    - `y` será la presión arterial sistólica,
    - `X` será la edad.

    La constante representa el intercepto del modelo.

    Aunque al inicio pueda parecer un detalle técnico, incluirla explícitamente es parte de la formulación correcta del modelo en `statsmodels`.
    """)
    return


@app.cell
def _(datos):
    y = datos["sbp_mmHg"]
    X = datos[["age"]]

    X = sm.add_constant(X)

    X.head()
    return X, y


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Ajuste del modelo

    Ahora ajustamos el modelo lineal:

    **sbp_mmHg ~ age**

    La idea no es memorizar la sintaxis, sino reconocer qué ocurre en este paso:

    - se toma la variable respuesta,
    - se toma la matriz de predictores,
    - y se estima la relación lineal entre ambas.

    El resultado no es un número aislado.

    Es un objeto de modelo ajustado que contiene múltiples componentes analíticos.
    """)
    return


@app.cell
def _(X, y):
    modelo = sm.OLS(y, X).fit()
    modelo.summary()
    return (modelo,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Cómo leer inicialmente el output

    En esta primera lección no es necesario interpretar todas las líneas del resumen.

    Basta con concentrarse en tres elementos:

    - el coeficiente de `age`,
    - el intercepto (`const`),
    - el valor p asociado a `age`.

    La interpretación básica es la siguiente:

    - el coeficiente de `age` indica cuánto cambia la presión arterial sistólica, en promedio, por cada año adicional de edad,
    - el intercepto representa el valor esperado de la variable respuesta cuando la edad es cero,
    - el valor p ayuda a evaluar si la asociación estimada es compatible con ausencia de relación lineal bajo el modelo.

    En esta etapa, lo importante es reconocer qué parte del output responde a la pregunta analítica inicial.
    """)
    return


@app.cell
def _(modelo):
    coef_age = float(modelo.params["age"])
    intercepto = float(modelo.params["const"])
    p_age = float(modelo.pvalues["age"])

    interpretacion_modelo = pd.Series(
        {
            "coeficiente_age": round(coef_age, 4),
            "intercepto": round(intercepto, 4),
            "p_value_age": round(p_age, 6),
        }
    )

    interpretacion_modelo
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Ejemplo de interpretación

    Si el coeficiente de edad fuera positivo, la lectura inicial sería:

    **a mayor edad, mayor presión arterial sistólica en promedio, según el modelo ajustado.**

    Si el coeficiente fuera negativo, la lectura inicial sería la opuesta.

    En ambos casos, la interpretación debe formularse como una **asociación estimada dentro del modelo**.

    En esta fase conviene evitar afirmaciones causales.

    Lo que el modelo lineal simple ofrece aquí es una cuantificación inicial de la relación entre dos variables.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto

    Ajusta ahora un segundo modelo lineal con esta estructura:

    - variable dependiente: `ldl_mg_dL`
    - variable independiente: `age`

    Guarda el modelo ajustado en una variable llamada:

    - `modelo_ldl`

    Este ejercicio busca comprobar que puedes reproducir la misma lógica de construcción del modelo con otra variable respuesta.
    """)
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    modelo_ldl = None
    return


@app.cell(hide_code=True)
def _():
    _tip_content = TipContent(
        items_raw=[
            r"""
    <Estructura del problema>
    Debes repetir la misma lógica del modelo anterior, pero cambiando la variable respuesta.

    Aquí la variable explicativa sigue siendo `age`.
    """,
            r"""
    <Preparación>
    Recuerda que `statsmodels` necesita:

    - una serie para `y`,
    - un `DataFrame` para `X`,
    - y una constante agregada con `sm.add_constant(...)`.
    """,
            r"""
    <Consistencia>
    La columna correcta para LDL en esta base es `ldl_mg_dL`.
    """,
            r"""
    <solucion>
    ```python
    y_ldl = datos["ldl_mg_dL"]
    X_ldl = sm.add_constant(datos[["age"]])
    modelo_ldl = sm.OLS(y_ldl, X_ldl).fit()
    ```
    """,
        ]
    )
    _tip_content.render()
    return


@app.cell(hide_code=True)
def _():
    _test_content = TestContent(
        items_raw=[
            r"""
    <Existencia del modelo>
    ```python
    assert modelo_ldl is not None
    print("El modelo fue definido.")
    ```
    """,
            r"""
    <Objeto ajustado>
    ```python
    assert hasattr(modelo_ldl, "params")
    assert hasattr(modelo_ldl, "pvalues")
    print("El objeto tiene componentes básicos de un modelo ajustado.")
    ```
    """,
            r"""
    <Parámetros esperados>
    ```python
    assert "const" in modelo_ldl.params.index
    assert "age" in modelo_ldl.params.index
    print("El modelo contiene intercepto y coeficiente para edad.")
    ```
    """,
            r"""
    <Variable respuesta correcta>
    ```python
    assert modelo_ldl.model.endog.shape[0] == datos.shape[0]
    print("La dimensión del modelo es consistente con la base.")
    ```
    """,
        ],
        namespace=globals(),
    )
    _test_content.render()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Integración conceptual

    En esta sesión introdujiste la idea de modelo estadístico como una representación formal de una relación entre variables.

    Aprendiste a:

    - definir una variable respuesta,
    - definir una variable explicativa,
    - preparar la matriz de diseño,
    - ajustar una regresión lineal simple,
    - y leer los componentes más importantes del output.

    Este paso marca una transición importante dentro del curso:

    **de análisis descriptivo a modelación estadística básica**.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Cierre

    `statsmodels` permite formalizar preguntas analíticas que ya no pueden responderse solo con tablas o gráficos descriptivos.

    En esta primera aproximación trabajaste con una regresión lineal simple.

    Más adelante será posible extender esta lógica hacia:

    - comparación de modelos,
    - inclusión de más variables,
    - diagnóstico,
    - y construcción de flujos analíticos más completos.

    La idea que conviene retener al cierre es esta:

    > un modelo estadístico no reemplaza el razonamiento analítico; lo obliga a volverse explícito.
    """)
    return


if __name__ == "__main__":
    app.run()
