import marimo

__generated_with = "0.20.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return mo


@app.cell
def _(mo):
    mo.md(
        r"""
# 06 — Iteraciones

## Propósito de la sección

Las iteraciones permiten ejecutar bloques de código múltiples veces de forma controlada.

En programación científica y análisis de datos, los bucles permiten:

- Recorrer estructuras de datos.
- Aplicar transformaciones repetitivas.
- Construir algoritmos paso a paso.

Se estudian:

- for
- while
- range
- break y continue
- Patrones iterativos comunes
"""
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
## 1) Bucle for

El bucle `for` itera sobre una secuencia.
"""
    )
    return


@app.cell
def _():
    numeros_it1 = [1, 2, 3, 4]

    for numero_it1 in numeros_it1:
        print("Número:", numero_it1)

    return numeros_it1


@app.cell
def _(mo):
    mo.md(
        r"""
## 2) range()

`range(inicio, fin, paso)` genera secuencias numéricas.
"""
    )
    return


@app.cell
def _():
    for valor_it2 in range(0, 5):
        print("Valor:", valor_it2)

    return


@app.cell
def _(mo):
    mo.md(
        r"""
## 3) Bucle while

El bucle `while` ejecuta mientras la condición sea verdadera.
"""
    )
    return


@app.cell
def _():
    contador_it3 = 0

    while contador_it3 < 3:
        print("Contador:", contador_it3)
        contador_it3 += 1

    return contador_it3


@app.cell
def _(mo):
    mo.md(
        r"""
## 4) break y continue

- `break` termina el bucle.
- `continue` salta a la siguiente iteración.
"""
    )
    return


@app.cell
def _():
    for valor_it4 in range(5):

        if valor_it4 == 3:
            break

        print("Break ejemplo:", valor_it4)

    for valor_it4b in range(5):

        if valor_it4b == 2:
            continue

        print("Continue ejemplo:", valor_it4b)

    return


@app.cell
def _(mo):
    mo.md(
        r"""
## 5) Patrón acumulador

Un patrón común en análisis numérico es acumular resultados.
"""
    )
    return


@app.cell
def _():
    datos_it5 = [2, 4, 6, 8]

    suma_it5 = 0
    for valor_it5 in datos_it5:
        suma_it5 += valor_it5

    print("Suma acumulada:", suma_it5)

    return suma_it5


@app.cell
def _(mo):
    mo.md(
        r"""
---

# Mini-reto (Sección 7)

Construye una función `factorial(n)` que:

1. Lance TypeError si n no es entero.
2. Lance ValueError si n es negativo.
3. Calcule el factorial usando un bucle (no recursión).
"""
    )
    return


@app.cell
def _():
    def factorial_it6(n_it6):

        if not isinstance(n_it6, int):
            raise TypeError("n debe ser entero.")

        if n_it6 < 0:
            raise ValueError("n debe ser no negativo.")

        resultado_it6 = 1
        for i_it6 in range(1, n_it6 + 1):
            resultado_it6 *= i_it6

        return resultado_it6

    return factorial_it6


@app.cell
def _(factorial_it6, mo):

    assert factorial_it6(0) == 1
    assert factorial_it6(5) == 120

    mo.md("Reto superado.")

    return


if __name__ == "__main__":
    app.run()
