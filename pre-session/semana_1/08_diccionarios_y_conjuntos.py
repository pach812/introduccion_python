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
# 07 — Estructuras de datos avanzadas: diccionarios y conjuntos

## Propósito de la sección

Además de las secuencias (listas, tuplas y strings), Python ofrece estructuras de datos clave para modelar información en ciencia de datos:

- **Diccionarios (`dict`)**: pares clave–valor, ideales para representar registros, mapeos y parámetros.
- **Conjuntos (`set`)**: colecciones sin orden y sin duplicados, útiles para operaciones de pertenencia, deduplicación y álgebra de conjuntos.

En esta sección se estudian:

- Creación y manipulación de `dict` y `set`
- Acceso seguro a llaves (métodos `get`, `in`)
- Iteración sobre llaves, valores e ítems
- Patrones frecuentes: conteo, agrupación simple y deduplicación
- Buenas prácticas y errores comunes
"""
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
## 1) Diccionarios: concepto y creación

Un diccionario representa un mapeo **clave → valor**.

Propiedades:
- Las llaves son únicas.
- Acceso promedio O(1) para lectura/escritura.
- Las llaves deben ser *hashables* (por ejemplo: `str`, `int`, `tuple` inmutable).

Creación común:
- Literales con llaves `{...}`
- `dict(...)`
"""
    )
    return


@app.cell
def _():
    paciente_d8_1 = {
        "id": "P001",
        "edad": 54,
        "sexo": "F",
        "diagnostico": "HTA",
    }

    print("Registro paciente:", paciente_d8_1)
    print("Edad:", paciente_d8_1["edad"])
    return paciente_d8_1


@app.cell
def _(mo):
    mo.md(
        r"""
### Acceso seguro: `in` y `get`

- `clave in diccionario` permite verificar existencia.
- `diccionario.get(clave, default)` evita `KeyError` y retorna un valor por defecto si no existe.
"""
    )
    return


@app.cell
def _():
    paciente_d8_2 = {"id": "P002", "edad": 61}

    print("¿Tiene 'peso'?:", "peso" in paciente_d8_2)
    print("Peso (get):", paciente_d8_2.get("peso", "No registrado"))

    return paciente_d8_2


@app.cell
def _(mo):
    mo.md(
        r"""
## 2) Actualización y operaciones frecuentes

- Asignación: `d[k] = v`
- Actualización múltiple: `d.update({...})`
- Eliminación: `del d[k]` o `pop(k)`
"""
    )
    return


@app.cell
def _():
    paciente_d8_3 = {"id": "P003", "edad": 48, "sexo": "M"}

    paciente_d8_3["edad"] = 49
    paciente_d8_3["peso_kg"] = 80.2

    paciente_d8_3.update({"diagnostico": "DM2", "fumador": False})

    eliminado_d8_3 = paciente_d8_3.pop("fumador")
    print("Diccionario actualizado:", paciente_d8_3)
    print("Valor eliminado (fumador):", eliminado_d8_3)

    return paciente_d8_3


@app.cell
def _(mo):
    mo.md(
        r"""
## 3) Iteración en diccionarios

Opciones:
- `for k in d`: itera llaves
- `for v in d.values()`: itera valores
- `for k, v in d.items()`: itera pares (llave, valor)

`items()` es la forma estándar cuando se necesitan llaves y valores simultáneamente.
"""
    )
    return


@app.cell
def _():
    parametros_d8_4 = {"alpha": 0.05, "max_iter": 1000, "seed": 2026}

    print("Llaves:")
    for k_d8_4 in parametros_d8_4:
        print("-", k_d8_4)

    print("\nPares (k, v):")
    for k_d8_4b, v_d8_4b in parametros_d8_4.items():
        print(f"- {k_d8_4b} = {v_d8_4b}")

    return parametros_d8_4


@app.cell
def _(mo):
    mo.md(
        r"""
## 4) Patrón: conteo (frecuencias) con diccionarios

Un patrón clásico en análisis exploratorio consiste en contar ocurrencias de categorías.

Ejemplo: contar diagnósticos en una lista de registros.
"""
    )
    return


@app.cell
def _():
    diagnosticos_d8_5 = ["HTA", "DM2", "HTA", "EPOC", "HTA", "DM2"]

    conteo_d8_5 = {}
    for dx_d8_5 in diagnosticos_d8_5:
        conteo_d8_5[dx_d8_5] = conteo_d8_5.get(dx_d8_5, 0) + 1

    print("Conteo:", conteo_d8_5)
    return diagnosticos_d8_5, conteo_d8_5


@app.cell
def _(mo):
    mo.md(
        r"""
## 5) Conjuntos (`set`): concepto y creación

Un conjunto es una colección:
- Sin orden (no indexable)
- Sin duplicados
- Con operaciones eficientes de pertenencia (`in`)

Es útil para:
- Deduplicación
- Operaciones como unión, intersección, diferencia
"""
    )
    return


@app.cell
def _():
    valores_d8_6 = [1, 2, 2, 3, 3, 3, 4]
    conjunto_d8_6 = set(valores_d8_6)

    print("Lista original:", valores_d8_6)
    print("Conjunto (deduplicado):", conjunto_d8_6)
    print("¿Está 3?:", 3 in conjunto_d8_6)

    return valores_d8_6, conjunto_d8_6


@app.cell
def _(mo):
    mo.md(
        r"""
## 6) Operaciones de conjuntos

- Unión: `A | B`
- Intersección: `A & B`
- Diferencia: `A - B`
- Diferencia simétrica: `A ^ B`
"""
    )
    return


@app.cell
def _():
    A_d8_7 = {1, 2, 3}
    B_d8_7 = {3, 4, 5}

    print("A | B:", A_d8_7 | B_d8_7)
    print("A & B:", A_d8_7 & B_d8_7)
    print("A - B:", A_d8_7 - B_d8_7)
    print("A ^ B:", A_d8_7 ^ B_d8_7)

    return A_d8_7, B_d8_7


@app.cell
def _(mo):
    mo.md(
        r"""
## 7) Buenas prácticas y errores comunes

- Preferir `get()` para llaves opcionales en registros (evita `KeyError`).
- Documentar la estructura esperada del diccionario (llaves requeridas vs opcionales).
- No usar `set` cuando se requiere mantener orden o duplicados (para eso están `list` y `collections.Counter`).
- Si se necesita orden en un conjunto, ordenar al final: `sorted(mi_set)`.

A continuación, se propone un mini-reto que combina `dict` y `set` con validaciones.
"""
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
---

# Mini-reto (Sección 8): diccionarios y conjuntos

## Enunciado

Implementa una función `resumen_categorico(lista_etiquetas)` que:

1. Verifique que `lista_etiquetas` sea una lista o tupla.
2. Verifique que todos los elementos sean strings.
3. Retorne un diccionario con:
   - `unicos`: un `set` con las etiquetas únicas
   - `conteo`: un `dict` con frecuencias por etiqueta (conteo)
4. Lance TypeError si el tipo de entrada es inválido, o si algún elemento no es string.
5. Lance ValueError si la secuencia está vacía.

Completa la siguiente celda y ejecuta los tests.
"""
    )
    return


@app.cell
def _():
    def resumen_categorico_d8_r(lista_etiquetas_d8_r):

        if not isinstance(lista_etiquetas_d8_r, (list, tuple)):
            raise TypeError("La entrada debe ser una lista o tupla.")

        if len(lista_etiquetas_d8_r) == 0:
            raise ValueError("La secuencia no puede estar vacía.")

        for i_d8_r, v_d8_r in enumerate(lista_etiquetas_d8_r):
            if not isinstance(v_d8_r, str):
                raise TypeError(
                    f"Elemento no string en posición {i_d8_r}: {v_d8_r!r} (tipo {type(v_d8_r).__name__})"
                )

        unicos_d8_r = set(lista_etiquetas_d8_r)

        conteo_d8_r = {}
        for etiqueta_d8_r in lista_etiquetas_d8_r:
            conteo_d8_r[etiqueta_d8_r] = conteo_d8_r.get(etiqueta_d8_r, 0) + 1

        return {"unicos": unicos_d8_r, "conteo": conteo_d8_r}

    return resumen_categorico_d8_r


@app.cell
def _(resumen_categorico_d8_r, mo):

    salida_d8_t = resumen_categorico_d8_r(["a", "b", "a", "c", "b", "a"])

    assert isinstance(salida_d8_t, dict)
    assert set(salida_d8_t.keys()) == {"unicos", "conteo"}
    assert salida_d8_t["unicos"] == {"a", "b", "c"}
    assert salida_d8_t["conteo"]["a"] == 3
    assert salida_d8_t["conteo"]["b"] == 2
    assert salida_d8_t["conteo"]["c"] == 1

    mo.md("✅ Reto superado.")
    return salida_d8_t


if __name__ == "__main__":
    app.run()
