import marimo

__generated_with = "0.20.1"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return mo

@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
# 08 — Comprensiones: listas, diccionarios y conjuntos

## Propósito de la sección

Las comprensiones (*comprehensions*) son una notación compacta y expresiva para construir colecciones a partir de iteraciones, usualmente con filtros.

Se estudian:

- List comprehensions
- Dict comprehensions
- Set comprehensions
- Uso de condiciones (`if`) dentro de la comprensión
- Buenas prácticas: claridad, legibilidad y límites de complejidad
- Comparación con bucles explícitos

El objetivo es usar comprensiones con criterio: cuando aportan claridad y cuando conviene evitarlas.
"""
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
## 1) List comprehensions

Forma general:

```python
[expresion for elemento in iterable]
```

Con filtro:

```python
[expresion for elemento in iterable if condicion]
```

Ejemplo: cuadrados de números.
"""
    )
    return


@app.cell
def _():
    numeros_c9_1 = [1, 2, 3, 4, 5]
    cuadrados_c9_1 = [n_c9_1 ** 2 for n_c9_1 in numeros_c9_1]

    print("Números:", numeros_c9_1)
    print("Cuadrados:", cuadrados_c9_1)

    return numeros_c9_1, cuadrados_c9_1


@app.cell
def _(mo):
    mo.md(
        r"""
### Comprensión con filtro

Ejemplo: seleccionar pares y elevar al cubo.
"""
    )
    return


@app.cell(hide_code=True)
def _():
    numeros_c9_2 = list(range(1, 11))
    cubos_pares_c9_2 = [n_c9_2 ** 3 for n_c9_2 in numeros_c9_2 if n_c9_2 % 2 == 0]

    print("Cubos de pares:", cubos_pares_c9_2)
    return numeros_c9_2, cubos_pares_c9_2


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
## 2) Dict comprehensions

Forma general:

```python
{llave: valor for elemento in iterable}
```

Ejemplo: mapear número → cuadrado.
"""
    )
    return


@app.cell(hide_code=True)
def _():
    numeros_c9_3 = [1, 2, 3, 4]
    mapa_cuadrados_c9_3 = {n_c9_3: n_c9_3 ** 2 for n_c9_3 in numeros_c9_3}

    print("Mapa:", mapa_cuadrados_c9_3)
    return numeros_c9_3, mapa_cuadrados_c9_3


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
## 3) Set comprehensions

Forma general:

```python
{expresion for elemento in iterable}
```

Ejemplo: deduplicar y transformar.
"""
    )
    return


@app.cell
def _():
    datos_c9_4 = [1, 1, 2, 2, 3, 4]
    dobles_unicos_c9_4 = {x_c9_4 * 2 for x_c9_4 in datos_c9_4}

    print("Dobles únicos:", dobles_unicos_c9_4)
    return datos_c9_4, dobles_unicos_c9_4


@app.cell
def _(mo):
    mo.md(
        r"""
## 4) Comprensiones anidadas: uso con criterio

Es posible anidar comprensiones, pero esto puede reducir legibilidad.

Ejemplo: producto cartesiano simple (pares).
"""
    )
    return


@app.cell
def _():
    A_c9_5 = [1, 2]
    B_c9_5 = ["a", "b", "c"]

    pares_c9_5 = [(a_c9_5, b_c9_5) for a_c9_5 in A_c9_5 for b_c9_5 in B_c9_5]
    print("Pares:", pares_c9_5)

    return A_c9_5, B_c9_5, pares_c9_5


@app.cell
def _(mo):
    mo.md(
        r"""
## 5) Buenas prácticas

Recomendaciones operativas:

- Si la comprensión no cabe razonablemente en una línea o requiere múltiples condiciones complejas, considerar un bucle explícito.
- Preferir nombres claros en el iterador.
- Evitar comprensiones con efectos colaterales (por ejemplo, que llamen funciones que mutan estado global).
- Usar comprensiones cuando aporten claridad y reduzcan ruido sintáctico, no por “estilo”.

En análisis de datos, las comprensiones pueden ser útiles para:
- transformaciones simples,
- filtrados directos,
- construcción rápida de diccionarios de mapeo.
"""
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
---

# Mini-reto (Sección 9): comprensiones

## Enunciado

Dada una lista de enteros `x`, implementa una función `pipeline_simple(x)` que:

1. Verifique que `x` sea lista o tupla.
2. Verifique que todos los elementos sean enteros.
3. Construya y retorne un diccionario con:
   - `pares`: lista con los números pares de `x`
   - `cuadrados_impares`: lista con el cuadrado de los impares de `x`
   - `mapa_paridad`: diccionario que mapee cada número a "par" o "impar"

Restricción:
- Debes usar al menos **una list comprehension** y **una dict comprehension**.

Completa la siguiente celda y ejecuta los tests.
"""
    )
    return


@app.cell
def _():
    def pipeline_simple_c9_r(x_c9_r):

        if not isinstance(x_c9_r, (list, tuple)):
            raise TypeError("x debe ser lista o tupla.")

        for i_c9_r, v_c9_r in enumerate(x_c9_r):
            if not isinstance(v_c9_r, int):
                raise TypeError(
                    f"Elemento no entero en posición {i_c9_r}: {v_c9_r!r} (tipo {type(v_c9_r).__name__})"
                )

        pares_c9_r = [v_c9_r for v_c9_r in x_c9_r if v_c9_r % 2 == 0]
        cuadrados_impares_c9_r = [v_c9_r ** 2 for v_c9_r in x_c9_r if v_c9_r % 2 != 0]
        mapa_paridad_c9_r = {v_c9_r: ("par" if v_c9_r % 2 == 0 else "impar") for v_c9_r in x_c9_r}

        return {
            "pares": pares_c9_r,
            "cuadrados_impares": cuadrados_impares_c9_r,
            "mapa_paridad": mapa_paridad_c9_r,
        }

    return pipeline_simple_c9_r


@app.cell
def _(pipeline_simple_c9_r, mo):

    out_c9_t = pipeline_simple_c9_r([1, 2, 3, 4, 5])

    assert out_c9_t["pares"] == [2, 4]
    assert out_c9_t["cuadrados_impares"] == [1, 9, 25]
    assert out_c9_t["mapa_paridad"][1] == "impar"
    assert out_c9_t["mapa_paridad"][2] == "par"
    assert out_c9_t["mapa_paridad"][5] == "impar"

    mo.md("✅ Reto superado.")
    return out_c9_t


if __name__ == "__main__":
    app.run()
