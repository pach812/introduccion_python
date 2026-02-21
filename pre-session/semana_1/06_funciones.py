import marimo

app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return mo


@app.cell
def _(mo):
    mo.md(
        r"""
# 06 — Funciones

## Propósito de la sección

Las funciones permiten:

- Encapsular lógica.
- Reutilizar código.
- Separar especificación de implementación.
- Facilitar pruebas y validación.

En programación científica, las funciones constituyen la unidad básica de modularidad.
"""
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
## 1) Definición básica

Sintaxis:

```python
def nombre(parametros):
    cuerpo
    return valor
```

Una función puede:
- Recibir argumentos.
- Realizar cálculos.
- Retornar un valor.
"""
    )
    return


@app.cell
def _():
    def cuadrado_fn1(x_fn1):
        return x_fn1 ** 2

    resultado_fn1 = cuadrado_fn1(5)
    print("Cuadrado:", resultado_fn1)

    return cuadrado_fn1, resultado_fn1


@app.cell
def _(mo):
    mo.md(
        r"""
## 2) Parámetros y argumentos

Los parámetros se definen en la firma.
Los argumentos se pasan al llamar la función.

Se recomienda nombrar parámetros de forma semánticamente clara.
"""
    )
    return


@app.cell
def _():
    def area_rectangulo_fn2(base_fn2, altura_fn2):
        return base_fn2 * altura_fn2

    area_fn2 = area_rectangulo_fn2(10, 3)
    print("Área:", area_fn2)

    return area_rectangulo_fn2, area_fn2


@app.cell
def _(mo):
    mo.md(
        r"""
## 3) Valores por defecto

Se pueden definir valores por defecto en parámetros.
"""
    )
    return


@app.cell
def _():
    def potencia_fn3(base_fn3, exponente_fn3=2):
        return base_fn3 ** exponente_fn3

    print("Potencia por defecto:", potencia_fn3(4))
    print("Potencia personalizada:", potencia_fn3(4, 3))

    return potencia_fn3


@app.cell
def _(mo):
    mo.md(
        r"""
## 4) Retorno múltiple

Una función puede retornar múltiples valores (como tupla).
"""
    )
    return


@app.cell
def _():
    def estadisticas_fn4(x_fn4):
        return min(x_fn4), max(x_fn4)

    minimo_fn4, maximo_fn4 = estadisticas_fn4([3, 7, 1, 9])
    print("Min:", minimo_fn4, "Max:", maximo_fn4)

    return estadisticas_fn4


@app.cell
def _(mo):
    mo.md(
        r"""
## 5) Ámbito (scope)

Las variables definidas dentro de la función no existen fuera de ella.
"""
    )
    return


@app.cell
def _():
    def ejemplo_scope_fn5():
        variable_interna_fn5 = 10
        return variable_interna_fn5

    valor_scope_fn5 = ejemplo_scope_fn5()
    print("Valor interno:", valor_scope_fn5)

    return ejemplo_scope_fn5


@app.cell
def _(mo):
    mo.md(
        r"""
## 6) Documentación (docstrings)

Las funciones deben documentarse formalmente.
"""
    )
    return


@app.cell
def _():
    def promedio_fn6(x_fn6):
        """Calcula el promedio de una secuencia numérica."""
        return sum(x_fn6) / len(x_fn6)

    print(promedio_fn6([1, 2, 3]))
    return promedio_fn6


@app.cell
def _(mo):
    mo.md(
        r"""
---

# Mini-reto (Sección 6)

Construye una función `evaluar_aprobacion(nota)` que:

1. Lance TypeError si la nota no es numérica.
2. Lance ValueError si la nota está fuera del rango 0–5.
3. Retorne "Aprobado" si nota >= 3.
4. Retorne "Reprobado" si nota < 3.
"""
    )
    return


@app.cell
def _():
    def evaluar_aprobacion_fn7(nota_fn7):

        if not isinstance(nota_fn7, (int, float)):
            raise TypeError("La nota debe ser numérica.")

        if not (0 <= nota_fn7 <= 5):
            raise ValueError("La nota debe estar entre 0 y 5.")

        return "Aprobado" if nota_fn7 >= 3 else "Reprobado"

    return evaluar_aprobacion_fn7


@app.cell
def _(evaluar_aprobacion_fn7, mo):

    assert evaluar_aprobacion_fn7(4) == "Aprobado"
    assert evaluar_aprobacion_fn7(2.5) == "Reprobado"

    mo.md("Reto superado.")

    return


if __name__ == "__main__":
    app.run()
