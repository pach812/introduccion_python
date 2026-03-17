# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "pandas",
#     "altair",
#     "pytest",
# ]
# ///

import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


with app.setup(hide_code=True):
    import marimo as mo
    import pandas as pd
    import altair as alt
    from pathlib import Path


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
        # Semana 3 · Lección 4
        ## Visualización declarativa con Altair

        **Propósito de la sesión:** introducir la lógica declarativa de Altair para construir visualizaciones clínicas y de salud pública a partir de una idea central:

        **no describimos cada píxel del gráfico; describimos qué variable va en cada canal visual.**

        En esta lección trabajaremos con cuatro piezas del lenguaje declarativo:

        - **datos**: la tabla que queremos visualizar
        - **marca**: la forma geométrica principal (`bar`, `line`, `point`, `rect`)
        - **encodings**: cómo las variables se asignan a posición, color o tooltip
        - **propiedades**: título, tamaño y ajustes de presentación

        ### Pregunta guía de la sesión

        ¿Cómo pasar de una tabla clínica a un gráfico que exprese claramente la intención analítica?
        """
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
        ## 1) Diferencia entre enfoque imperativo y declarativo

        En un enfoque **imperativo**, controlamos muchos detalles del dibujo paso a paso.

        En un enfoque **declarativo**, especificamos:

        - qué datos usaremos,
        - qué marca representa esos datos,
        - y qué variable ocupa cada canal visual.

        Esta lógica es especialmente útil cuando queremos que la estructura del gráfico sea **explícita, legible y fácil de modificar**.

        En términos analíticos, la secuencia suele ser:

        **pregunta clínica → tabla resumida → selección de marca → asignación de variables a canales**
        """
    )
    return


@app.cell(hide_code=True)
def _():
    data_candidates = [
        Path("dataset_clase_semana2_small.csv"),
        Path(__file__).with_name("dataset_clase_semana2_small.csv") if "__file__" in globals() else Path("dataset_clase_semana2_small.csv"),
        Path("/mnt/data/dataset_clase_semana2_small.csv"),
    ]

    data_path = None
    for candidate in data_candidates:
        if candidate.exists():
            data_path = candidate
            break

    if data_path is None:
        raise FileNotFoundError(
            "No se encontró `dataset_clase_semana2_small.csv`. Coloca el archivo en la misma carpeta del notebook o ajusta `data_path`."
        )

    df = pd.read_csv(data_path)
    return data_path, df


@app.cell(hide_code=True)
def _(data_path, df):
    mo.md(
        f"""
        ## 2) Dataset de trabajo

        Usaremos un dataset sintético de salud con **{df.shape[0]} filas** y **{df.shape[1]} columnas**.

        La ruta detectada fue:

        ```python
        {data_path}
        ```

        Algunas variables relevantes para la sesión son:

        - `sex`
        - `age`
        - `hypertension`
        - `Diabetes`
        - `bmi_category`
        - `education_grouped`
        - `sbp_mmHg`
        - `glucose_mg_dL`
        - `ldl_mg_dL`

        Nuestro objetivo no será solo graficar, sino **graficar con intención analítica**.
        """
    )
    return


@app.cell
def _(df):
    df.head(8)
    return


@app.cell(hide_code=True)
def _(df):
    mo.md(
        f"""
        ### Estructura básica de la tabla

        La tabla contiene perfiles demográficos, factores sociales, comorbilidades y biomarcadores.

        Antes de construir gráficos declarativos conviene revisar:

        - cuáles variables son categóricas,
        - cuáles son numéricas,
        - y cuál unidad analítica representa cada fila.

        En este dataset, cada fila representa un **individuo**.

        Columnas disponibles:

        ```python
        {df.columns.tolist()}
        ```
        """
    )
    return


@app.cell
def _(df):
    summary_types = pd.DataFrame(
        {
            "column": df.columns,
            "dtype": df.dtypes.astype(str).values,
        }
    )
    summary_types
    return (summary_types,)


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
        ## 3) Primera gramática declarativa: barras para proporciones

        Cuando queremos comparar **frecuencias o proporciones entre grupos**, una barra suele ser una elección natural.

        Aquí construiremos un resumen de prevalencia observada de hipertensión por sexo.

        La lógica será:

        1. transformar una respuesta categórica en una bandera booleana,
        2. resumir con `groupby`,
        3. y luego declarar el gráfico con Altair.
        """
    )
    return


@app.cell
def _(df, pd):
    hypertension_by_sex = (
        df.assign(hypertension_flag=lambda d: d["hypertension"].eq("Yes"))
        .groupby("sex", as_index=False)
        .agg(
            n_people=("ID", "count"),
            prop_hypertension=("hypertension_flag", "mean"),
        )
    )

    hypertension_by_sex["prop_hypertension_pct"] = (
        hypertension_by_sex["prop_hypertension"] * 100
    ).round(1)

    hypertension_by_sex
    return (hypertension_by_sex,)


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
        ### Lectura conceptual

        En esta tabla ya está resuelta la parte analítica.

        Ahora Altair recibe una tabla pequeña y clara, y nosotros declaramos:

        - `x`: el grupo (`sex`)
        - `y`: la proporción (`prop_hypertension_pct`)
        - `color`: también `sex`, para reforzar separación visual

        Altair se encarga del resto de la construcción.
        """
    )
    return


@app.cell
def _(alt, hypertension_by_sex):
    chart_hypertension_by_sex = (
        alt.Chart(hypertension_by_sex)
        .mark_bar()
        .encode(
            x=alt.X("sex:N", title="Sexo"),
            y=alt.Y(
                "prop_hypertension_pct:Q",
                title="Hipertensión (%)",
                scale=alt.Scale(domain=[0, 100]),
            ),
            color=alt.Color("sex:N", title="Sexo"),
            tooltip=[
                alt.Tooltip("sex:N", title="Sexo"),
                alt.Tooltip("n_people:Q", title="N", format=",.0f"),
                alt.Tooltip(
                    "prop_hypertension_pct:Q",
                    title="Hipertensión (%)",
                    format=".1f",
                ),
            ],
        )
        .properties(
            title="Proporción de hipertensión por sexo",
            width=420,
            height=320,
        )
    )

    chart_hypertension_by_sex
    return (chart_hypertension_by_sex,)


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
        ## Mini-reto 1

        Construye un gráfico declarativo llamado `chart_diabetes_by_sex`.

        ### Objetivo analítico

        Comparar el **porcentaje de diabetes** entre categorías de sexo.

        ### Requisitos

        1. crea antes una tabla llamada `diabetes_by_sex`,
        2. usa una barra (`mark_bar()`),
        3. coloca `sex` en el eje x,
        4. coloca el porcentaje en el eje y,
        5. incluye `tooltip`,
        6. asigna el resultado final a `chart_diabetes_by_sex`.
        """
    )
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    diabetes_by_sex = None
    chart_diabetes_by_sex = None
    return chart_diabetes_by_sex, diabetes_by_sex


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
        <details>
        <summary><strong>Tips · Mini-reto 1</strong></summary>

        <p><strong>Tip 1.</strong> Convierte la variable <code>Diabetes</code> en una bandera booleana con <code>.eq("Yes")</code>.</p>
        <p><strong>Tip 2.</strong> El promedio de una columna booleana puede interpretarse como proporción.</p>
        <p><strong>Tip 3.</strong> Para mostrar porcentaje, multiplica por 100 antes de graficar.</p>
        <p><strong>Tip 4.</strong> Usa una tabla intermedia; eso hace más clara la intención del gráfico.</p>

        <p><strong>Solución esperada</strong></p>

        ```python
        diabetes_by_sex = (
            df.assign(diabetes_flag=lambda d: d["Diabetes"].eq("Yes"))
            .groupby("sex", as_index=False)
            .agg(
                n_people=("ID", "count"),
                prop_diabetes=("diabetes_flag", "mean"),
            )
        )

        diabetes_by_sex["prop_diabetes_pct"] = (
            diabetes_by_sex["prop_diabetes"] * 100
        ).round(1)

        chart_diabetes_by_sex = (
            alt.Chart(diabetes_by_sex)
            .mark_bar()
            .encode(
                x=alt.X("sex:N", title="Sexo"),
                y=alt.Y("prop_diabetes_pct:Q", title="Diabetes (%)"),
                color=alt.Color("sex:N", title="Sexo"),
                tooltip=["sex:N", "n_people:Q", "prop_diabetes_pct:Q"],
            )
            .properties(title="Proporción de diabetes por sexo", width=420, height=320)
        )
        ```
        </details>
        """
    )
    return


@app.cell(hide_code=True)
def _(chart_diabetes_by_sex, diabetes_by_sex):
    mo.md(
        rf"""
        <details>
        <summary><strong>Test · Mini-reto 1</strong></summary>

        ```python
        assert diabetes_by_sex is not None, "Debes definir `diabetes_by_sex`."
        assert chart_diabetes_by_sex is not None, "Debes definir `chart_diabetes_by_sex`."
        assert list(diabetes_by_sex.columns) == [
            "sex",
            "n_people",
            "prop_diabetes",
            "prop_diabetes_pct",
        ], "Revisa los nombres de las columnas de `diabetes_by_sex`."
        assert hasattr(chart_diabetes_by_sex, "to_dict"), "El gráfico debe ser un objeto de Altair."
        spec = chart_diabetes_by_sex.to_dict()
        assert spec["mark"]["type"] == "bar", "El mini-reto pide una barra."
        assert spec["encoding"]["x"]["field"] == "sex", "`sex` debe ir en el eje x."
        assert spec["encoding"]["y"]["field"] == "prop_diabetes_pct", "El porcentaje debe ir en el eje y."
        print("Mini-reto 1 resuelto correctamente.")
        ```
        </details>
        """
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
        ## 4) Segunda gramática declarativa: mapas de calor con `mark_rect`

        Cuando queremos comparar un valor resumen en una matriz de categorías, un **heatmap** puede expresar el patrón con claridad.

        Aquí resumiremos la presión arterial sistólica promedio según:

        - categoría de IMC,
        - y estado de diabetes.

        En términos declarativos:

        - filas: `bmi_category`
        - columnas: `Diabetes`
        - color: `mean_sbp`
        """
    )
    return


@app.cell
def _(df, pd):
    heatmap_table = (
        df.groupby(["bmi_category", "Diabetes"], as_index=False)
        .agg(mean_sbp=("sbp_mmHg", "mean"))
        .round({"mean_sbp": 1})
    )
    heatmap_table
    return (heatmap_table,)


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
        ### ¿Por qué `mark_rect`?

        En Altair, el heatmap no es una función especial independiente.

        Se construye declarando:

        - una **marca rectangular**,
        - dos ejes categóricos,
        - y una variable cuantitativa asignada a color.

        Esto refleja muy bien la lógica declarativa: el gráfico emerge de la combinación entre marca y encodings.
        """
    )
    return


@app.cell
def _(alt, heatmap_table):
    chart_heatmap_sbp = (
        alt.Chart(heatmap_table)
        .mark_rect()
        .encode(
            x=alt.X("Diabetes:N", title="Diabetes"),
            y=alt.Y("bmi_category:N", title="Categoría de IMC"),
            color=alt.Color("mean_sbp:Q", title="PAS media (mmHg)"),
            tooltip=[
                alt.Tooltip("bmi_category:N", title="IMC"),
                alt.Tooltip("Diabetes:N", title="Diabetes"),
                alt.Tooltip("mean_sbp:Q", title="PAS media", format=".1f"),
            ],
        )
        .properties(
            title="Presión arterial sistólica media por IMC y diabetes",
            width=360,
            height=240,
        )
    )

    chart_heatmap_sbp
    return (chart_heatmap_sbp,)


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
        ## Mini-reto 2

        Construye un heatmap llamado `chart_heatmap_ldl`.

        ### Objetivo analítico

        Visualizar el **LDL promedio** según:

        - `education_grouped`
        - `high_cholesterol`

        ### Requisitos

        1. crea primero una tabla llamada `heatmap_ldl_table`,
        2. usa `mark_rect()`,
        3. coloca `high_cholesterol` en x,
        4. coloca `education_grouped` en y,
        5. coloca el LDL promedio en color,
        6. agrega `tooltip`,
        7. asigna el resultado a `chart_heatmap_ldl`.
        """
    )
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    heatmap_ldl_table = None
    chart_heatmap_ldl = None
    return chart_heatmap_ldl, heatmap_ldl_table


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
        <details>
        <summary><strong>Tips · Mini-reto 2</strong></summary>

        <p><strong>Tip 1.</strong> El resumen debe hacerse antes del gráfico, usando <code>groupby</code> y <code>agg</code>.</p>
        <p><strong>Tip 2.</strong> La variable cuantitativa en este reto es <code>ldl_mg_dL</code>.</p>
        <p><strong>Tip 3.</strong> Un heatmap en Altair se construye con <code>mark_rect()</code>, no con barras.</p>
        <p><strong>Tip 4.</strong> Redondear la tabla ayuda a revisar si los valores tienen sentido antes de graficar.</p>

        <p><strong>Solución esperada</strong></p>

        ```python
        heatmap_ldl_table = (
            df.groupby(["education_grouped", "high_cholesterol"], as_index=False)
            .agg(mean_ldl=("ldl_mg_dL", "mean"))
            .round({"mean_ldl": 1})
        )

        chart_heatmap_ldl = (
            alt.Chart(heatmap_ldl_table)
            .mark_rect()
            .encode(
                x=alt.X("high_cholesterol:N", title="Colesterol alto"),
                y=alt.Y("education_grouped:N", title="Educación"),
                color=alt.Color("mean_ldl:Q", title="LDL medio (mg/dL)"),
                tooltip=["education_grouped:N", "high_cholesterol:N", "mean_ldl:Q"],
            )
            .properties(title="LDL medio por educación y colesterol alto", width=420, height=260)
        )
        ```
        </details>
        """
    )
    return


@app.cell(hide_code=True)
def _(chart_heatmap_ldl, heatmap_ldl_table):
    mo.md(
        rf"""
        <details>
        <summary><strong>Test · Mini-reto 2</strong></summary>

        ```python
        assert heatmap_ldl_table is not None, "Debes definir `heatmap_ldl_table`."
        assert chart_heatmap_ldl is not None, "Debes definir `chart_heatmap_ldl`."
        assert list(heatmap_ldl_table.columns) == [
            "education_grouped",
            "high_cholesterol",
            "mean_ldl",
        ], "Revisa las columnas de `heatmap_ldl_table`."
        assert hasattr(chart_heatmap_ldl, "to_dict"), "El gráfico debe ser un objeto de Altair."
        spec = chart_heatmap_ldl.to_dict()
        assert spec["mark"]["type"] == "rect", "El mini-reto pide `mark_rect()`."
        assert spec["encoding"]["x"]["field"] == "high_cholesterol", "`high_cholesterol` debe ir en x."
        assert spec["encoding"]["y"]["field"] == "education_grouped", "`education_grouped` debe ir en y."
        assert spec["encoding"]["color"]["field"] == "mean_ldl", "El color debe codificar `mean_ldl`."
        print("Mini-reto 2 resuelto correctamente.")
        ```
        </details>
        """
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
        ## 5) Tercera gramática declarativa: dispersión e interacción

        Un gráfico de dispersión es útil cuando queremos estudiar la relación entre dos variables numéricas.

        En salud, esta estructura sirve para explorar asociaciones entre biomarcadores o entre edad y medidas clínicas.

        En Altair, esta lógica se expresa con:

        - `mark_point()` para observaciones individuales,
        - dos variables cuantitativas en posición,
        - una categoría en color,
        - y `tooltip` para recuperar contexto por punto.

        Además, podemos hacer el gráfico **interactivo** sin redibujarlo manualmente.
        """
    )
    return


@app.cell
def _(alt, df):
    chart_scatter_biomarkers = (
        alt.Chart(df)
        .mark_point(size=65, opacity=0.55)
        .encode(
            x=alt.X("glucose_mg_dL:Q", title="Glucosa (mg/dL)"),
            y=alt.Y("ldl_mg_dL:Q", title="LDL (mg/dL)"),
            color=alt.Color("Diabetes:N", title="Diabetes"),
            tooltip=[
                alt.Tooltip("ID:Q", title="ID"),
                alt.Tooltip("age:Q", title="Edad"),
                alt.Tooltip("sex:N", title="Sexo"),
                alt.Tooltip("glucose_mg_dL:Q", title="Glucosa", format=".1f"),
                alt.Tooltip("ldl_mg_dL:Q", title="LDL", format=".1f"),
                alt.Tooltip("Diabetes:N", title="Diabetes"),
            ],
        )
        .properties(
            title="Relación entre glucosa y LDL",
            width=430,
            height=320,
        )
        .interactive()
    )

    chart_scatter_biomarkers
    return (chart_scatter_biomarkers,)


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
        ### Interpretación analítica

        Este gráfico no prueba causalidad ni ajuste estadístico.

        Su función aquí es **exploratoria y descriptiva**: permite detectar patrones visuales, posibles agrupamientos y valores extremos, manteniendo una sintaxis declarativa compacta.

        En Altair, la interactividad se agrega como una propiedad adicional del gráfico, no como una reconstrucción completa del objeto.
        """
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
        ## Mini-reto 3 · Final

        Construye un gráfico declarativo llamado `chart_age_sbp`.

        ### Objetivo analítico

        Visualizar la relación entre **edad** y **presión arterial sistólica**.

        ### Requisitos

        1. usa la tabla original `df`,
        2. emplea `mark_point()`,
        3. coloca `age` en x,
        4. coloca `sbp_mmHg` en y,
        5. colorea por `hypertension`,
        6. agrega `tooltip`,
        7. vuelve el gráfico interactivo,
        8. asigna el resultado a `chart_age_sbp`.

        Este mini-reto final integra los elementos centrales vistos en la sesión:

        - elección de marca,
        - encodings,
        - tooltip,
        - y propiedades declarativas.
        """
    )
    return


@app.cell
def _():
    # === TU TURNO (EDITA ESTA CELDA) ===
    chart_age_sbp = None
    return (chart_age_sbp,)


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
        <details>
        <summary><strong>Tips · Mini-reto 3</strong></summary>

        <p><strong>Tip 1.</strong> En este reto no necesitas resumir la tabla: cada punto representa una observación individual.</p>
        <p><strong>Tip 2.</strong> La marca correcta es <code>mark_point()</code>.</p>
        <p><strong>Tip 3.</strong> Piensa la declaración mínima: datos + marca + <code>x</code> + <code>y</code> + color + tooltip.</p>
        <p><strong>Tip 4.</strong> La interactividad se añade al final con <code>.interactive()</code>.</p>

        <p><strong>Solución esperada</strong></p>

        ```python
        chart_age_sbp = (
            alt.Chart(df)
            .mark_point(size=65, opacity=0.55)
            .encode(
                x=alt.X("age:Q", title="Edad"),
                y=alt.Y("sbp_mmHg:Q", title="PAS (mmHg)"),
                color=alt.Color("hypertension:N", title="Hipertensión"),
                tooltip=[
                    alt.Tooltip("ID:Q", title="ID"),
                    alt.Tooltip("age:Q", title="Edad"),
                    alt.Tooltip("sbp_mmHg:Q", title="PAS", format=".1f"),
                    alt.Tooltip("hypertension:N", title="Hipertensión"),
                ],
            )
            .properties(title="Edad y presión arterial sistólica", width=430, height=320)
            .interactive()
        )
        ```
        </details>
        """
    )
    return


@app.cell(hide_code=True)
def _(chart_age_sbp):
    mo.md(
        rf"""
        <details>
        <summary><strong>Test · Mini-reto 3</strong></summary>

        ```python
        assert chart_age_sbp is not None, "Debes definir `chart_age_sbp`."
        assert hasattr(chart_age_sbp, "to_dict"), "El resultado debe ser un objeto de Altair."
        spec = chart_age_sbp.to_dict()
        assert spec["mark"]["type"] == "point", "El mini-reto final pide `mark_point()`."
        assert spec["encoding"]["x"]["field"] == "age", "`age` debe ir en el eje x."
        assert spec["encoding"]["y"]["field"] == "sbp_mmHg", "`sbp_mmHg` debe ir en el eje y."
        assert spec["encoding"]["color"]["field"] == "hypertension", "El color debe codificar `hypertension`."
        print("Mini-reto 3 resuelto correctamente.")
        ```
        </details>
        """
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
        ## 6) Cierre conceptual

        En esta sesión, Altair nos permitió expresar gráficos como una **declaración estructurada**:

        - una tabla,
        - una marca,
        - una asignación explícita de variables a canales,
        - y propiedades de presentación.

        ### Ideas que deben quedar firmes

        1. **La tabla correcta antecede al gráfico correcto.**
        2. **La marca debe responder a la pregunta analítica.**
        3. **Los encodings expresan intención, no solo decoración.**
        4. **Tooltip e interactividad amplían la lectura sin sobrecargar el gráfico.**

        En la siguiente etapa del curso, estas visualizaciones se integrarán progresivamente en flujos analíticos más estructurados.
        """
    )
    return


if __name__ == "__main__":
    app.run()
