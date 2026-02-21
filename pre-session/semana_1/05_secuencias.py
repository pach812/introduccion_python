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
# 05 — Estructuras incorporadas: secuencias

## Propósito de la sección

Las secuencias constituyen uno de los pilares del lenguaje Python y de la programación para análisis de datos.

En esta sección se estudian:

- list
- tuple
- str
- Indexación y slicing
- Mutabilidad
- Métodos relevantes
- Buenas prácticas en manipulación de datos secuenciales

El objetivo es comprender cómo se almacenan, acceden y transforman datos ordenados.
"""
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
## 1) Listas (list)

Una lista es una secuencia ordenada y mutable.

Características:
- Permite elementos heterogéneos.
- Permite modificación interna.
- Permite indexación.
"""
    )
    return


@app.cell
def _():
    lista_seq1 = [10, 20, 30, 40]
    print("Lista original:", lista_seq1)

    lista_seq1.append(50)
    print("Después de append:", lista_seq1)

    lista_seq1[0] = 5
    print("Después de modificar índice 0:", lista_seq1)

    return lista_seq1


@app.cell
def _(mo):
    mo.md(
        r"""
## 2) Tuplas (tuple)

Una tupla es una secuencia ordenada e inmutable.

Se utiliza cuando:
- No se desea modificación.
- Se requiere estructura fija.
"""
    )
    return


@app.cell
def _():
    tupla_seq2 = (1, 2, 3)
    print("Tupla:", tupla_seq2)
    print("Elemento en índice 1:", tupla_seq2[1])
    return tupla_seq2


@app.cell
def _(mo):
    mo.md(
        r"""
## 3) Cadenas de texto (str)

Las cadenas son secuencias inmutables de caracteres.

Permiten indexación, slicing y múltiples métodos.
"""
    )
    return


@app.cell
def _():
    texto_seq3 = "Python"
    print("Texto:", texto_seq3)
    print("Primer carácter:", texto_seq3[0])
    print("Últimos tres caracteres:", texto_seq3[-3:])
    return texto_seq3


@app.cell
def _(mo):
    mo.md(
        r"""
## 4) Indexación y slicing

Indexación:
- Positiva (desde 0)
- Negativa (desde -1)

Slicing:
secuencia[inicio:fin:paso]
"""
    )
    return


@app.cell
def _():
    datos_seq4 = [0, 1, 2, 3, 4, 5, 6]

    print("datos_seq4[2]:", datos_seq4[2])
    print("datos_seq4[-1]:", datos_seq4[-1])
    print("datos_seq4[1:5]:", datos_seq4[1:5])
    print("datos_seq4[::2]:", datos_seq4[::2])

    return datos_seq4


@app.cell
def _(mo):
    mo.md(
        r"""
## 5) Métodos relevantes en listas

Algunos métodos importantes:

- append()
- extend()
- insert()
- remove()
- pop()
- sort()
"""
    )
    return


@app.cell
def _():
    lista_seq5 = [3, 1, 4]

    lista_seq5.append(2)
    print("append:", lista_seq5)

    lista_seq5.sort()
    print("sort:", lista_seq5)

    elemento_eliminado_seq5 = lista_seq5.pop()
    print("pop:", lista_seq5, "| eliminado:", elemento_eliminado_seq5)

    return lista_seq5


@app.cell
def _(mo):
    mo.md(
        r"""
## 6) Mutabilidad comparativa

- list → mutable
- tuple → inmutable
- str → inmutable

La mutabilidad afecta cómo se comportan las referencias.
"""
    )
    return


@app.cell
def _():
    lista_seq6 = [1, 2, 3]
    copia_lista_seq6 = lista_seq6
    copia_lista_seq6.append(4)

    print("Lista original:", lista_seq6)
    print("Referencia compartida:", copia_lista_seq6)

    return lista_seq6


@app.cell
def _(mo):
    mo.md(
        r"""
---

# Mini-reto (Sección 5)

Construye una función `analizar_secuencia(seq)` que:

1. Verifique que seq sea una lista o tupla.
2. Retorne un diccionario con:
   - longitud
   - primer_elemento
   - ultimo_elemento
   - invertida (usando slicing)
3. Lance TypeError si no es list o tuple.
"""
    )
    return


@app.cell
def _():
    def analizar_secuencia(seq_input):

        if not isinstance(seq_input, (list, tuple)):
            raise TypeError("La entrada debe ser lista o tupla.")

        if len(seq_input) == 0:
            raise ValueError("La secuencia no puede estar vacía.")

        return {
            "longitud": len(seq_input),
            "primer_elemento": seq_input[0],
            "ultimo_elemento": seq_input[-1],
            "invertida": seq_input[::-1],
        }

    return analizar_secuencia


@app.cell
def _(analizar_secuencia, mo):

    test_seq = [10, 20, 30]

    resultado_test = analizar_secuencia(test_seq)

    assert resultado_test["longitud"] == 3
    assert resultado_test["primer_elemento"] == 10
    assert resultado_test["ultimo_elemento"] == 30
    assert resultado_test["invertida"] == [30, 20, 10]

    mo.md(
        r"""
Reto superado.

Has aplicado correctamente indexación, slicing y validación de tipos en secuencias.
"""
    )

    return resultado_test


if __name__ == "__main__":
    app.run()
