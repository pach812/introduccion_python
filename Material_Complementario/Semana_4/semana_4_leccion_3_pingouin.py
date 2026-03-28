# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "numpy==2.4.2",
#     "pandas==3.0.1",
#     "pingouin==0.5.5",
#     "pytest==9.0.2",
#     "requests==2.32.5",
# ]
# ///

import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")

with app.setup(hide_code=True):
    import marimo as mo
    import numpy as np
    import pandas as pd
    import pingouin as pg

    from setup import TipContent, TestContent, find_data_file


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Semana 4 · Lección 2
    ## Introducción al análisis estadístico con pingouin

    En esta sesión continuamos la transición iniciada en la lección anterior:

    hasta ahora ya no solo describimos datos, sino que comenzamos a formular preguntas inferenciales y a responderlas con herramientas estadísticas.

    En esta segunda lección introducimos **pingouin**, una librería orientada a hacer análisis estadístico aplicado de forma más directa y con outputs particularmente útiles para interpretación.

    El objetivo de la sesión no es reemplazar el razonamiento estadístico por una librería más cómoda.

    El objetivo es comprender que distintas herramientas pueden responder preguntas similares, pero con formas diferentes de organizar el resultado.

    En esta sesión trabajaremos con:

    - pruebas de normalidad,
    - comparación de medias,
    - asociación entre variables categóricas,
    - correlación entre variables numéricas,
    - y una primera extensión hacia comparación de más de dos grupos.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Propósito de la sesión

    Al finalizar esta lección deberías poder:

    - reconocer cuándo una pregunta estadística puede resolverse con una prueba clásica,
    - utilizar `pingouin` para ejecutar pruebas comunes con una sintaxis centrada en `DataFrame`,
    - identificar en el output medidas como valor p, intervalos de confianza y tamaños de efecto,
    - y comparar conceptualmente esta librería con otras herramientas estadísticas vistas en el curso.

    En términos pedagógicos, esta sesión amplía el repertorio del estudiante.

    La idea central es la siguiente:

    > una misma pregunta estadística puede resolverse con herramientas distintas, pero lo importante sigue siendo elegir correctamente la prueba e interpretar su resultado con criterio.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Contexto aplicado

    Supón que trabajas con una base clínica que contiene información demográfica y cardiometabólica.

    Algunas preguntas razonables en este contexto podrían ser:

    - ¿la presión arterial sistólica sigue una distribución aproximadamente normal?
    - ¿la presión arterial difiere entre hombres y mujeres?
    - ¿existe asociación entre sexo y una variable categórica clínica?
    - ¿edad y presión arterial parecen estar relacionadas?
    - ¿cómo se compara una variable continua entre más de dos grupos?

    Estas preguntas no requieren todavía modelos complejos.

    Requieren, antes que nada, una buena relación entre:

    - tipo de pregunta,
    - tipo de variable,
    - y prueba estadística adecuada.
    """)
    return


@app.cell
def _():
    data_path = find_data_file("public/dataset_clase_semana2_small.csv")
    datos = pd.read_csv(data_path)

    assert not datos.empty
    assert {"age", "sex", "sbp_mmHg", "ldl_mg_dL"}.issubset(datos.columns)

    datos.head()
    return (datos,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Variables de trabajo

    En esta lección trabajaremos principalmente con las siguientes variables:

    - `age`: edad
    - `sex`: sexo reportado
    - `sbp_mmHg`: presión arterial sistólica
    - `ldl_mg_dL`: colesterol LDL

    Además, cuando sea necesario trabajar con variables categóricas adicionales, se construirá una variable auxiliar dentro de la propia sesión.

    Esta decisión tiene un propósito didáctico:

    mantener el foco en la lógica estadística y no dispersar la atención en demasiadas columnas a la vez.
    """)
    return


@app.cell
def _(datos):
    datos[["age", "sex", "sbp_mmHg", "ldl_mg_dL"]].head()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## ¿Qué aporta pingouin?

    `pingouin` es una librería estadística que resulta especialmente útil en contextos aplicados porque devuelve resultados organizados como tablas.

    Esto tiene varias ventajas:

    - la salida puede leerse con rapidez,
    - es fácil convertirla en parte de un reporte,
    - y suele incluir no solo el valor p, sino también tamaños de efecto e intervalos de confianza.

    En otras palabras, `pingouin` no cambia la lógica de la prueba estadística.

    Lo que cambia es la forma en que se estructuran y se presentan los resultados.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Primer bloque: normalidad

    Antes de aplicar algunas pruebas, puede ser útil examinar si una variable numérica sigue o no una distribución aproximadamente normal.

    Esta evaluación no debe entenderse como una decisión automática que define por sí sola toda la estrategia analítica.

    Sin embargo, sí constituye una referencia importante para:

    - interpretar supuestos,
    - elegir entre alternativas paramétricas y no paramétricas,
    - y comprender mejor la forma de los datos.

    En esta sesión utilizaremos una prueba de normalidad sobre la presión arterial sistólica.
    """)
    return


@app.cell
def _(datos):
    normality_sbp = pg.normality(data=datos)

    normality_sbp
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Cómo leer el output de normalidad

    En esta salida conviene concentrarse, sobre todo, en:

    - el estadístico de la prueba,
    - el valor p,
    - y la decisión lógica asociada al contraste.

    La lectura inicial suele ser:

    - si el valor p es grande, no hay evidencia suficiente para rechazar normalidad,
    - si el valor p es pequeño, los datos son menos compatibles con ese supuesto.

    Esta interpretación debe tomarse como una pieza del razonamiento, no como un veredicto aislado.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Segundo bloque: comparación de medias

    Una de las preguntas más frecuentes en estadística aplicada es si una variable numérica difiere entre dos grupos.

    En este caso la pregunta será:

    **¿la presión arterial sistólica difiere entre hombres y mujeres?**

    Esta pregunta combina:

    - una variable numérica (`sbp_mmHg`),
    - y una variable de agrupación (`sex`).

    Por tanto, una prueba t de Student constituye una primera respuesta razonable.
    """)
    return


@app.cell
def _(datos):
    sbp_male = datos.loc[datos["sex"] == "Male", "sbp_mmHg"].dropna()
    sbp_female = datos.loc[datos["sex"] == "Female", "sbp_mmHg"].dropna()

    ttest_sbp_sex = pg.ttest(x=sbp_male, y=sbp_female)

    ttest_sbp_sex
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Qué tiene de útil esta salida

    A diferencia de una implementación mínima de una prueba t, aquí aparecen de forma integrada varios elementos importantes:

    - el estadístico de la prueba,
    - el valor p,
    - el intervalo de confianza,
    - y una medida de tamaño de efecto.

    Esto es especialmente valioso porque en investigación aplicada no basta con decir si una diferencia parece “significativa”.

    También interesa preguntarse:

    - cuál es la magnitud de esa diferencia,
    - y con qué incertidumbre está estimada.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Tercer bloque: asociación entre variables categóricas

    No todas las preguntas se refieren a medias o relaciones lineales.

    A veces el interés está en evaluar si dos variables categóricas parecen asociarse entre sí.

    Para ilustrarlo, construiremos una variable auxiliar de edad agrupada y luego preguntaremos:

    **¿el sexo se distribuye del mismo modo entre grupos etarios, o parece haber asociación entre ambas variables?**

    Este ejemplo no reemplaza un análisis epidemiológico completo.

    Su función es mostrar la lógica de una prueba de independencia dentro de un flujo de trabajo claro.
    """)
    return


@app.cell
def _(datos):
    datos_cat = datos.copy()

    datos_cat["age_group"] = pd.cut(
        datos_cat["age"],
        bins=[0, 49, 64, np.inf],
        labels=["<50", "50-64", "65+"],
        right=True,
    )

    tabla_contingencia = pd.crosstab(datos_cat["sex"], datos_cat["age_group"])

    chi2_results = pg.chi2_independence(data=datos_cat, x="sex", y="age_group")
    return chi2_results, datos_cat, tabla_contingencia


@app.cell
def _(tabla_contingencia):
    tabla_contingencia
    return


@app.cell
def _(chi2_results):
    mo.vstack(
        [
            mo.md("Valores esperados"),
            chi2_results[0],
            mo.md("Valores encontrados en los datos"),
            chi2_results[1],
            mo.md("Pruebas estadisticas"),
            chi2_results[2],
        ]
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Qué observar en esta etapa

    Aquí aparecen dos objetos complementarios:

    - una tabla de contingencia, que resume los conteos observados,
    - y la salida de la prueba de chi-cuadrado, que permite evaluar si esos conteos son compatibles con independencia.

    Esta secuencia es pedagógicamente importante:

    primero se observa la estructura de los datos categóricos,
    luego se formaliza la evaluación estadística.

    De nuevo, la prueba no sustituye la lectura de la tabla.
    La complementa.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Cuarto bloque: correlación

    Cuando el interés recae sobre dos variables numéricas, una pregunta frecuente es si ambas parecen variar conjuntamente.

    En este caso formularemos la pregunta:

    **¿edad y presión arterial sistólica están asociadas linealmente?**

    La correlación de Pearson permite resumir esta relación mediante un coeficiente que expresa:

    - dirección,
    - magnitud,
    - y evidencia estadística de asociación lineal.
    """)
    return


@app.cell
def _(datos):
    corr_age_sbp = pg.pairwise_corr(data=datos,columns=["age", "sbp_mmHg"])

    corr_age_sbp
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Cómo leer una correlación

    En esta salida conviene observar tres componentes principales:

    - el coeficiente `r`,
    - el valor p,
    - y el intervalo de confianza.

    La interpretación básica es:

    - el signo de `r` indica la dirección de la asociación,
    - su magnitud resume qué tan intensa parece esa relación lineal,
    - y el valor p informa sobre la compatibilidad del resultado con ausencia de correlación bajo el contraste planteado.

    Esta lectura sigue siendo una lectura de asociación, no de causalidad.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Quinto bloque: comparación de más de dos grupos

    Cuando la comparación involucra más de dos categorías, una prueba t ya no es suficiente.

    En esos casos, una estrategia clásica es usar ANOVA.

    Para ilustrarlo, construiremos un ejemplo simple con grupos etarios y preguntaremos:

    **¿la presión arterial sistólica media parece diferir entre estos grupos de edad?**

    Esto extiende naturalmente la lógica de comparación de medias hacia un escenario con mayor número de grupos.
    """)
    return


@app.cell
def _(datos_cat):
    anova_sbp_agegroup = pg.anova(
        data=datos_cat, dv="sbp_mmHg", between="age_group"
    )

    anova_sbp_agegroup
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Qué aporta este bloque a la progresión de la lección

    Con esta prueba ya aparece una idea importante:

    `pingouin` no se limita a una sola prueba o a un solo tipo de dato.

    Ofrece una familia de herramientas coherente para responder preguntas estadísticas frecuentes, manteniendo una sintaxis relativamente homogénea y outputs organizados como tablas.

    Eso facilita el aprendizaje inicial y también hace más directa la integración de resultados en informes o tablas de salida.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Relación con la lección anterior

    En la sesión anterior trabajaste con `statsmodels` para introducir la idea de modelación estadística explícita.

    La diferencia central con `pingouin` es la siguiente:

    - `pingouin` resulta especialmente cómodo para pruebas estadísticas puntuales y salidas tabulares compactas,
    - mientras que `statsmodels` es particularmente fuerte cuando se requiere formular y ajustar modelos más estructurados.

    Por eso no debe pensarse en ambas librerías como excluyentes.

    Más bien cumplen roles complementarios dentro del repertorio analítico.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto

    Utiliza `pingouin` para evaluar la correlación entre:

    - `age`
    - `ldl_mg_dL`

    Guarda el resultado en una variable llamada:

    - `corr_ldl`

    El objetivo de este ejercicio es comprobar que puedes reproducir la lógica de una correlación con una variable distinta de la trabajada en el ejemplo principal.
    """)
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    corr_ldl = None
    return


@app.cell(hide_code=True)
def _():
    _tip_content = TipContent(
        items_raw=[
            r"""
    <Estructura del problema>
    Necesitas una correlación entre dos variables numéricas dentro del mismo `DataFrame`.
    """,
            r"""
    <Función>
    La función adecuada en `pingouin` es `pg.corr(...)`.
    """,
            r"""
    <Variables correctas>
    En esta base, la variable de LDL se llama `ldl_mg_dL`.
    """,
            r"""
    <solucion>
    ```python
    corr_ldl = pg.corr(data=datos, x="age", y="ldl_mg_dL")
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
    <Existencia del resultado>
    ```python
    assert corr_ldl is not None
    print("La salida fue definida.")
    ```
    """,
            r"""
    <Tipo de objeto>
    ```python
    assert isinstance(corr_ldl, pd.DataFrame)
    print("La salida es un DataFrame.")
    ```
    """,
            r"""
    <Columnas esperadas>
    ```python
    assert "r" in corr_ldl.columns
    assert "p-val" in corr_ldl.columns
    print("La salida contiene coeficiente y valor p.")
    ```
    """,
            r"""
    <Dimensión mínima>
    ```python
    assert corr_ldl.shape[0] >= 1
    print("La salida tiene al menos una fila de resultados.")
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

    En esta sesión ampliaste el repertorio de estadística aplicada del curso.

    Aprendiste a utilizar `pingouin` para:

    - evaluar normalidad,
    - comparar medias,
    - estudiar asociación entre variables categóricas,
    - estimar correlaciones,
    - y extender la comparación a más de dos grupos.

    La lección deja una idea importante:

    > la herramienta puede cambiar, pero la lógica analítica sigue dependiendo de la pregunta, del tipo de variable y de la interpretación cuidadosa del output.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Cierre

    `pingouin` ofrece una forma directa y organizada de ejecutar pruebas estadísticas comunes, especialmente útil cuando se desea una salida clara y fácil de integrar en un flujo de trabajo aplicado.

    En combinación con otras librerías del curso, esto permite construir una caja de herramientas más completa:

    - unas funciones son más cómodas para pruebas puntuales,
    - otras son más apropiadas para modelación formal,
    - y todas requieren el mismo principio de fondo:

    **pensar bien la pregunta antes de ejecutar la técnica**.
    """)
    return


if __name__ == "__main__":
    app.run()
