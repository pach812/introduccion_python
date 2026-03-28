# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "numpy==2.4.2",
#     "pandas==3.0.1",
#     "pingouin==0.5.5",
#     "pytest==9.0.2",
#     "requests==2.32.5",
#     "scipy==1.15.3",
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
    import pingouin as pg
    import statsmodels.api as sm
    from scipy import stats

    from setup import find_data_file


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Semana 4 · Código en vivo
    ## Comparación práctica entre `scipy.stats`, `pingouin` y `statsmodels`

    En esta sesión el objetivo no es profundizar en teoría, sino comparar **cómo se ve el mismo flujo analítico** usando tres librerías estadísticas distintas.

    La lógica de trabajo será siempre la misma:

    1. formular una pregunta,
    2. preparar los datos,
    3. aplicar una función,
    4. leer el output.

    La diferencia estará en la forma en que cada librería organiza el código y presenta los resultados.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Ruta de la clase

    Hoy compararemos tres librerías:

    - `scipy.stats` → funciones estadísticas clásicas y explícitas,
    - `pingouin` → sintaxis más compacta y outputs tabulares,
    - `statsmodels` → modelación estadística explícita.

    La dinámica será:

    - primero ver rápidamente cómo “se ve” cada librería en código,
    - después ejecutar ejemplos equivalentes,
    - y al final comparar outputs.
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
    ## Dataset de trabajo

    Usaremos el mismo dataset clínico de sesiones anteriores.

    Variables principales para esta clase:

    - `age`
    - `sex`
    - `sbp_mmHg`
    - `ldl_mg_dL`

    Nos concentraremos en dos tipos de tareas:

    - pruebas estadísticas puntuales,
    - un modelo lineal simple.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## ¿Por qué varias librerías estadísticas?

    En Python no existe una sola forma de hacer análisis estadístico.

    Distintas librerías resuelven problemas similares, pero con enfoques diferentes:

    - algunas son más **explícitas y cercanas a la matemática**,
    - otras son más **compactas y orientadas a interpretación**,
    - y otras están diseñadas para **modelos estadísticos completos**.

    En esta clase veremos tres perspectivas complementarias del mismo flujo analítico.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## scipy.stats → la base

    `scipy.stats` es una de las librerías más fundamentales del ecosistema científico en Python.

    Características principales:

    - Implementa pruebas estadísticas clásicas directamente
    - Requiere preparar explícitamente los datos (vectores o tablas)
    - Devuelve salidas simples (estadístico + p-value)

    Idea clave:

    > Es la forma más cercana a cómo se definen las pruebas en estadística clásica
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## ¿Cómo pensar scipy.stats?

    Cuando usas `scipy.stats`, tú controlas:

    - qué datos entran,
    - cómo se agrupan,
    - y qué estructura tiene la prueba.

    Esto lo hace ideal para:

    - entender qué está pasando realmente,
    - enseñar fundamentos,
    - y depurar análisis.

    Trade-off:

    - más control → más trabajo manual
    """)
    return


@app.cell(hide_code=True)
def _():
    scipy_code = """from scipy import stats

    sbp_values = datos["sbp_mmHg"].dropna()
    stats.shapiro(sbp_values)

    grupo_a = datos.loc[datos["sex"] == "Male", "sbp_mmHg"].dropna()
    grupo_b = datos.loc[datos["sex"] == "Female", "sbp_mmHg"].dropna()
    stats.ttest_ind(grupo_a, grupo_b, equal_var=False)

    pares = datos[["age", "ldl_mg_dL"]].dropna()
    stats.pearsonr(pares["age"], pares["ldl_mg_dL"])"""

    mo.md(r"""
    ## ¿Cómo se ve `scipy.stats`?

    `scipy.stats` exige preparar de forma explícita los vectores o tablas que necesita cada prueba.

    Eso la hace muy útil para mostrar con claridad qué entra en cada función.
    """)
    mo.ui.code_editor(
        scipy_code,
        language="python",
        disabled=True,
        min_height=260,
    )
    return


@app.cell(hide_code=True)
def _():
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## pingouin → simplicidad y claridad

    `pingouin` es una librería diseñada para facilitar el análisis estadístico aplicado.

    Características principales:

    - Sintaxis más compacta
    - Outputs en formato tabular
    - Incluye métricas adicionales automáticamente (IC, effect size)

    Idea clave:

    > Es una capa de alto nivel sobre pruebas estadísticas comunes
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## ¿Cómo pensar pingouin?

    `pingouin` está pensado para:

    - análisis exploratorio rápido,
    - reportes,
    - y workflows aplicados.

    Ventajas:

    - menos código
    - outputs listos para interpretar

    Trade-off:

    - menos control sobre detalles internos
    """)
    return


@app.cell(hide_code=True)
def _():
    pingouin_code = """import pingouin as pg

    pg.normality(data=datos, dv="sbp_mmHg")

    pg.ttest(
    x=datos.loc[datos["sex"] == "Male", "sbp_mmHg"].dropna(),
    y=datos.loc[datos["sex"] == "Female", "sbp_mmHg"].dropna(),
    )

    pg.corr(data=datos, x="age", y="ldl_mg_dL")"""

    mo.md(r"""
    ## ¿Cómo se ve `pingouin`?

    `pingouin` suele devolver salidas más listas para leer y reportar.

    En general, el código es más compacto y el output suele venir en formato tabular.
    """)
    mo.ui.code_editor(
        pingouin_code,
        language="python",
        disabled=True,
        min_height=230,
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## statsmodels → modelación estadística

    `statsmodels` se enfoca en construir modelos estadísticos explícitos.

    Características principales:

    - modelos lineales y generalizados
    - inferencia estadística completa
    - outputs detallados (coeficientes, IC, tests)

    Idea clave:

    > aquí ya no solo probamos, sino que modelamos relaciones entre variables
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## ¿Cómo pensar statsmodels?

    A diferencia de las otras librerías:

    - defines una variable respuesta (Y)
    - defines variables explicativas (X)
    - ajustas un modelo

    Esto permite:

    - controlar confusión,
    - estimar efectos,
    - y trabajar con múltiples variables al mismo tiempo.

    Trade-off:

    - mayor complejidad conceptual
    """)
    return


@app.cell(hide_code=True)
def _():
    statsmodels_code = """import statsmodels.api as sm

    y = datos["sbp_mmHg"]
    X = sm.add_constant(datos[["age"]])

    modelo = sm.OLS(y, X).fit()
    modelo.summary()"""

    mo.md(r"""
    ## ¿Cómo se ve `statsmodels`?

    `statsmodels` entra cuando ya no solo queremos una prueba puntual, sino una relación formal entre variables.

    Aquí ya aparece con claridad la lógica de modelo:

    - variable respuesta,
    - variable explicativa,
    - constante,
    - ajuste.
    """)
    mo.ui.code_editor(
        statsmodels_code,
        language="python",
        disabled=True,
        min_height=190,
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Comparación rápida

    | Librería        | Enfoque                | Nivel |
    |----------------|-----------------------|------|
    | scipy.stats     | funciones estadísticas | bajo |
    | pingouin        | análisis aplicado     | medio |
    | statsmodels     | modelación            | alto |

    Idea clave de la clase:

    > misma pregunta → distintas formas de resolverla
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Qué debes observar hoy

    Durante la clase, enfócate en:

    - cómo cambia el código entre librerías
    - cómo cambia el output
    - qué tan explícito es el proceso

    No se trata de memorizar funciones.

    Se trata de entender:

    > cómo elegir la herramienta adecuada según la pregunta
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Flujo común que compararemos

    Usaremos la misma secuencia analítica con distintas librerías:

    - normalidad de `sbp_mmHg`,
    - comparación de `sbp_mmHg` entre sexos,
    - correlación entre `age` y `ldl_mg_dL`,
    - y finalmente un modelo lineal simple para `sbp_mmHg ~ age`.

    La pregunta de la clase no es cuál librería es “mejor”.

    La pregunta es:

    **cómo cambia el trabajo analítico y el output según la herramienta que usamos**.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Sección 1: Normalidad

    Empezaremos con la misma pregunta en dos librerías:

    **¿`sbp_mmHg` parece compatible con una distribución aproximadamente normal?**
    """)
    return


@app.cell
def _(datos):
    # Scipy.stats


    col_cont = ["age", "sbp_mmHg", "glucose_mg_dL", "glucose_mg_dL"]

    for _col in col_cont:
        # limpiar
        sbp_value_scipy = datos[_col].dropna()

        # Realizar prueba
        sbp_norm_scipy = stats.shapiro(sbp_value_scipy)

        # Imprimir resultado
        print(_col)
        print(sbp_norm_scipy.statistic, sbp_norm_scipy.pvalue,"\n")
    return


@app.cell(hide_code=True)
def _(datos):
    pigouin_norm = pg.normality(datos.drop(columns="ID"))
    pigouin_norm
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Comparación rápida

    Aquí se ve una diferencia importante:

    - `scipy.stats` devuelve una salida mínima,
    - `pingouin` devuelve una tabla más estructurada.

    La prueba es la misma idea estadística.
    Cambia la forma en que la librería presenta el resultado.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Sección 2: Comparación entre grupos

    Nueva pregunta:

    **¿`sbp_mmHg` difiere entre hombres y mujeres?**

    Repetiremos el flujo con ambas librerías.
    """)
    return


@app.cell
def _(datos):
    # scipy
    sbp_hombres = datos.loc[datos["sex"] == "Male", "sbp_mmHg"].dropna()
    sbp_mujeres = datos.loc[datos["sex"] == "Female", "sbp_mmHg"].dropna()

    scipy_ttest = stats.ttest_ind(sbp_hombres,sbp_mujeres, equal_var = False)
    scipy_ttest.statistic, scipy_ttest.pvalue
    return sbp_hombres, sbp_mujeres


@app.cell
def _(sbp_hombres, sbp_mujeres):
    # pingouin

    pg_ttest = pg.ttest(x = sbp_hombres, y = sbp_mujeres)
    pg_ttest
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Sección 3: Correlación

    Nueva pregunta:

    **¿`age` y `ldl_mg_dL` muestran una asociación lineal?**
    """)
    return


@app.cell
def _(datos):
    # Scipy

    col_a_selec = ["age","ldl_mg_dL"]
    par_age_ldl = datos[col_a_selec].dropna()

    scipy_corr = stats.pearsonr(x = par_age_ldl["age"], y = par_age_ldl["ldl_mg_dL"])
    scipy_corr.statistic ,  scipy_corr.pvalue 
    return


@app.cell
def _(datos):
    # Pingouin 
    ping_corr = pg.pairwise_corr(data=datos.drop(columns="ID"))
    ping_corr
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Sección 4: Modelo lineal simple

    Cerramos con una tarea distinta.

    - Ya no preguntamos solo si existe asociación.

    Ahora preguntamos:

    > **¿cómo cambia `sbp_mmHg` en función de `age` dentro de un modelo lineal simple?**

    Aquí entra `statsmodels`.
    """)
    return


@app.cell
def _(datos):
    # Statsmodels 

    y = datos["sbp_mmHg"]
    X = sm.add_constant(datos["age"])

    SM_linear_model = sm.OLS(y, X).fit()
    SM_linear_model.summary()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Qué cambia en esta última parte

    En este punto ya no estamos frente a una prueba puntual.

    Aquí construimos explícitamente un modelo.

    Esa es la diferencia central entre esta sección y las anteriores:

    - `scipy.stats` y `pingouin` nos ayudaron a resolver preguntas estadísticas específicas,
    - `statsmodels` nos permite formular una relación con una estructura de modelo.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Comparación final de las librerías

    Después de ejecutar los ejemplos, conviene resumir así:

    - `scipy.stats` → más explícita y básica,
    - `pingouin` → más compacta y amigable para interpretación,
    - `statsmodels` → centrada en modelación formal.

    > Recuerda: la elección de herramienta depende del objetivo analítico y del tipo de output que se quiere obtener.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Cierre de la sesión

    La idea principal de esta clase es que el flujo analítico puede mantenerse estable aunque cambie la librería:

    - formular la pregunta,
    - preparar datos,
    - ejecutar una función o ajustar un modelo,
    - interpretar el resultado.

    Lo que cambia entre herramientas es la forma en que se organiza el código y cómo se presenta el output.
    """)
    return


if __name__ == "__main__":
    app.run()
