# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "numpy==2.4.2",
#     "pandas==3.0.1",
#     "pytest==9.0.2",
#     "requests==2.32.5",
#     "scipy==1.15.3",
# ]
# ///

import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")

with app.setup(hide_code=True):
    import marimo as mo
    import numpy as np
    import pandas as pd
    from scipy import stats

    from setup import TipContent, TestContent, find_data_file


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Semana 4 · Lección 3
    ## Fundamentos de pruebas estadísticas con scipy.stats

    En esta sesión introducimos `scipy.stats` como una librería fundamental para realizar pruebas estadísticas clásicas en Python.

    El objetivo pedagógico de esta lección no es solamente aprender nuevas funciones.

    El propósito principal es comprender con mayor claridad qué ocurre cuando aplicamos una prueba estadística y qué información necesitamos preparar antes de ejecutarla.

    En sesiones anteriores trabajaste con herramientas como `pingouin` y `statsmodels`, que ofrecen salidas muy organizadas y orientadas a interpretación.

    En esta lección daremos un paso complementario:

    > trabajar con una librería más básica para ver con mayor transparencia cómo se construyen las pruebas estadísticas desde sus bloques esenciales.

    A lo largo de la sesión utilizaremos `scipy.stats` para trabajar con:

    - pruebas de normalidad,
    - comparación de medias,
    - asociación entre variables categóricas,
    - y correlación entre variables numéricas.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Propósito de la sesión

    Al finalizar esta lección deberías poder:

    - identificar qué datos necesita cada prueba estadística en `scipy.stats`,
    - preparar manualmente los vectores o tablas necesarios para ejecutar una prueba,
    - reconocer la salida básica que devuelve cada función,
    - interpretar estadísticos y valores p en un contexto aplicado,
    - y comparar conceptualmente esta forma de trabajo con librerías de nivel más alto vistas anteriormente.

    La idea central de la sesión es la siguiente:

    > una librería más básica obliga a pensar mejor la estructura del problema estadístico antes de ejecutar la técnica.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Contexto aplicado

    Vamos a suponer que trabajas con una base clínica que contiene información demográfica y mediciones cardiometabólicas.

    Algunas preguntas estadísticas razonables podrían ser:

    - ¿la presión arterial sistólica sigue una distribución aproximadamente normal?
    - ¿la presión arterial difiere entre hombres y mujeres?
    - ¿sexo y grupo etario parecen asociarse entre sí?
    - ¿edad y colesterol LDL muestran una asociación lineal?

    Estas preguntas son útiles porque muestran distintos tipos de estructura en los datos:

    - una sola variable numérica,
    - una variable numérica comparada entre dos grupos,
    - dos variables categóricas,
    - dos variables numéricas continuas.

    Cada una de estas estructuras conduce a una prueba distinta.
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

    En esta lección nos concentraremos principalmente en:

    - `age`: edad
    - `sex`: sexo reportado
    - `sbp_mmHg`: presión arterial sistólica
    - `ldl_mg_dL`: colesterol LDL

    Además, cuando sea necesario trabajar con variables categóricas adicionales, construiremos una variable derivada simple dentro de la propia sesión.

    Esta reducción del problema tiene una intención clara:

    mantener la atención en la lógica de la prueba y no dispersarla en demasiadas variables al mismo tiempo.
    """)
    return


@app.cell
def _(datos):
    datos[["age", "sex", "sbp_mmHg", "ldl_mg_dL"]].head()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## ¿Qué caracteriza a scipy.stats?

    `scipy.stats` proporciona implementaciones directas de pruebas estadísticas clásicas.

    A diferencia de librerías más orientadas a reportes tabulares, aquí se puede observar con más claridad:

    - qué datos entran a la función,
    - qué estadístico devuelve,
    - y cómo debe organizar previamente la información.

    Esto tiene una consecuencia importante:

    `scipy.stats` obliga a pensar con precisión en la estructura del problema antes de correr la prueba.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Primer bloque: normalidad

    Empezaremos con una pregunta sobre una sola variable numérica:

    > **¿la presión arterial sistólica parece compatible con una distribución aproximadamente normal?**

    En `scipy.stats`, la prueba de Shapiro-Wilk se aplica directamente sobre un vector de datos.

    Esto hace visible una idea fundamental:

    antes de correr una prueba, debemos extraer y limpiar correctamente la variable que queremos analizar.
    """)
    return


@app.cell
def _(datos):
    sbp_values = datos["sbp_mmHg"].dropna()

    shapiro_stat, shapiro_p = stats.shapiro(sbp_values)

    shapiro_results = pd.Series(
        {
            "statistic": round(float(shapiro_stat), 6),
            "p_value": round(float(shapiro_p), 6),
        }
    )

    shapiro_results
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Cómo leer esta salida

    A diferencia de otras librerías, aquí no obtenemos una tabla completa con múltiples columnas.

    La función devuelve directamente dos componentes:

    - el estadístico de la prueba,
    - y el valor p.

    La interpretación inicial es la misma que en otros contextos:

    - si el valor p es grande, no hay evidencia suficiente para rechazar normalidad,
    - si el valor p es pequeño, los datos son menos compatibles con ese supuesto.

    Esta diferencia en el formato de salida es útil porque nos obliga a identificar explícitamente qué representa cada valor.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Segundo bloque: comparación de medias

    Pasamos ahora a una pregunta con una variable numérica y una variable de grupo:

    **¿la presión arterial sistólica difiere entre hombres y mujeres?**

    En `scipy.stats`, una prueba t de Student entre grupos no se construye a partir del `DataFrame` completo, sino a partir de dos vectores separados.

    Esta exigencia hace visible una operación que a veces queda oculta en librerías de nivel más alto:

    primero hay que construir correctamente los grupos antes de comparar sus medias.
    """)
    return


@app.cell
def _(datos):
    sbp_male = datos.loc[datos["sex"] == "Male", "sbp_mmHg"].dropna()
    sbp_female = datos.loc[datos["sex"] == "Female", "sbp_mmHg"].dropna()

    t_stat, t_p = stats.ttest_ind(sbp_male, sbp_female, equal_var=False)

    ttest_results = pd.Series(
        {
            "statistic": round(float(t_stat), 6),
            "p_value": round(float(t_p), 6),
            "n_male": int(sbp_male.shape[0]),
            "n_female": int(sbp_female.shape[0]),
        }
    )

    ttest_results
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Qué enseña este ejemplo

    Aquí conviene observar dos planos al mismo tiempo.

    Primero, el plano estadístico:

    - existe un estadístico de prueba,
    - existe un valor p,
    - y con ellos construimos una lectura básica sobre diferencia de medias.

    Segundo, el plano computacional:

    - el `DataFrame` no entra directamente a la función,
    - primero se filtran grupos,
    - luego se extraen vectores,
    - y finalmente se ejecuta la prueba.

    Esta secuencia ayuda a comprender mejor qué está comparando realmente una prueba t.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Tercer bloque: asociación entre variables categóricas

    Ahora trabajaremos con dos variables categóricas.

    Para ello construiremos una variable auxiliar de grupo etario y formularemos la pregunta:

    > **¿sexo y grupo etario parecen asociarse entre sí?**

    Aquí la estructura de datos cambia.

    Ya no necesitamos vectores numéricos, sino una **tabla de contingencia** que resuma conteos observados por categoría.

    Esto es importante porque muestra que cada prueba estadística exige una forma específica de organizar la información.
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

    contingency_table = pd.crosstab(datos_cat["sex"], datos_cat["age_group"])

    chi2_stat, chi2_p, chi2_dof, chi2_expected = stats.chi2_contingency(contingency_table)

    chi2_results = pd.Series(
        {
            "statistic": round(float(chi2_stat), 6),
            "p_value": round(float(chi2_p), 6),
            "degrees_of_freedom": int(chi2_dof),
        }
    )

    contingency_table, chi2_results
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Lectura de esta etapa

    Aquí aparecen dos objetos importantes:

    - una tabla de contingencia, que organiza los conteos observados,
    - y el resultado de la prueba de chi-cuadrado, que compara esos conteos con lo esperado bajo independencia.

    La lección conceptual es clara:

    no basta con elegir una función.

    Antes de eso, hay que construir correctamente la representación de los datos que la prueba necesita.

    En esta sesión, esa representación es la tabla de contingencia.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Cuarto bloque: correlación

    Pasamos ahora a una pregunta con dos variables numéricas:

    > **¿edad y colesterol LDL muestran una asociación lineal?**

    En `scipy.stats`, la correlación de Pearson se aplica directamente sobre dos vectores del mismo tamaño.

    Esto recupera una idea importante ya vista con otras herramientas:

    una correlación resume:

    - dirección,
    - magnitud,
    - y evidencia estadística de asociación lineal.
    """)
    return


@app.cell
def _(datos):
    age_values = datos["age"].dropna()
    ldl_values = datos.loc[age_values.index, "ldl_mg_dL"].dropna()

    common_index = datos[["age", "ldl_mg_dL"]].dropna().index
    age_corr = datos.loc[common_index, "age"]
    ldl_corr = datos.loc[common_index, "ldl_mg_dL"]

    pearson_r, pearson_p = stats.pearsonr(age_corr, ldl_corr)

    correlation_results = pd.Series(
        {
            "r": round(float(pearson_r), 6),
            "p_value": round(float(pearson_p), 6),
            "n_pairs": int(len(common_index)),
        }
    )

    correlation_results
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Qué observar en una correlación

    En esta salida conviene concentrarse en:

    - el coeficiente de correlación `r`,
    - el valor p,
    - y el número de pares de observaciones utilizados.

    La interpretación inicial es la siguiente:

    - el signo de `r` indica dirección,
    - su magnitud resume intensidad lineal,
    - y el valor p permite evaluar si la asociación observada es compatible con ausencia de correlación bajo el contraste planteado.

    De nuevo, el formato de salida es simple, pero suficiente para construir una lectura analítica básica.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Relación con otras librerías del curso

    Después de esta sesión debería quedar clara una idea importante.

    Distintas librerías pueden responder preguntas estadísticas similares, pero organizan el trabajo de forma distinta.

    En términos generales:

    - `scipy.stats` hace más visible la estructura mínima de la prueba,
    - `pingouin` organiza mejor la salida para interpretación,
    - `statsmodels` resulta especialmente útil cuando la pregunta exige un modelo explícito.

    Ninguna herramienta reemplaza a las otras por completo.

    Más bien forman capas complementarias dentro del repertorio analítico del curso.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Mini-reto

    Utiliza `scipy.stats` para evaluar la correlación entre:

    - `age`
    - `ldl_mg_dL`

    Guarda el resultado en una variable llamada:

    - `corr_ldl`

    En este caso, `corr_ldl` debe quedar como una tupla o estructura equivalente que contenga el coeficiente de correlación y el valor p.

    El objetivo del ejercicio es comprobar que puedes preparar correctamente las dos variables y ejecutar la prueba con la sintaxis de `scipy.stats`.
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
    Necesitas dos vectores numéricos del mismo tamaño y sin valores faltantes en las posiciones utilizadas.
    """,
            r"""
    <Preparación>
    Una forma segura es seleccionar ambas columnas a la vez y luego usar `.dropna()`.
    """,
            r"""
    <Función>
    La función adecuada es `stats.pearsonr(...)`.
    """,
            r"""
    <solucion>
    ```python
    pares_ldl = datos[["age", "ldl_mg_dL"]].dropna()
    corr_ldl = stats.pearsonr(pares_ldl["age"], pares_ldl["ldl_mg_dL"])
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
    <Estructura mínima>
    ```python
    assert hasattr(corr_ldl, "__len__")
    assert len(corr_ldl) >= 2
    print("La salida contiene al menos dos componentes.")
    ```
    """,
            r"""
    <Tipos numéricos>
    ```python
    assert isinstance(float(corr_ldl[0]), float)
    assert isinstance(float(corr_ldl[1]), float)
    print("El coeficiente y el valor p son numéricos.")
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

    En esta sesión trabajaste con `scipy.stats` para ejecutar pruebas estadísticas clásicas desde una perspectiva más básica y explícita.

    Aprendiste a:

    - preparar un vector para una prueba de normalidad,
    - separar grupos antes de comparar medias,
    - construir una tabla de contingencia antes de aplicar chi-cuadrado,
    - y alinear dos variables numéricas para calcular una correlación.

    Esta lección deja una idea importante:

    > comprender la forma de entrada de una prueba estadística ayuda a comprender mejor qué está haciendo realmente la técnica.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Cierre

    `scipy.stats` ocupa un lugar fundamental en el ecosistema científico de Python porque ofrece implementaciones directas de muchas pruebas estadísticas clásicas.

    En esta sesión lo utilizaste no solo como herramienta de cálculo, sino como una forma de hacer más visible la estructura del razonamiento estadístico.

    La idea final que conviene retener es la siguiente:

    > una prueba estadística no comienza cuando llamas a una función; comienza cuando organizas correctamente los datos que la prueba necesita.
    """)
    return


if __name__ == "__main__":
    app.run()
