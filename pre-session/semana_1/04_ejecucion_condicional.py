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
# 04 — Ejecución condicional (control de flujo)

## Propósito de la sección

El control de flujo permite que un programa tome decisiones en función de condiciones lógicas.
En esta sección se estudia formalmente:

- Estructura `if / elif / else`
- Evaluación booleana
- Anidamiento de condiciones
- Condicionales compuestos
- Expresiones condicionales en una línea
- Buenas prácticas en diseño de decisiones

El objetivo es escribir lógica condicional clara, verificable y estructurada.
"""
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
## 1) Estructura básica: if / else

Sintaxis:

```python
if condicion:
    bloque_1
else:
    bloque_2
```

La condición debe evaluar a un valor booleano.
"""
    )
    return


@app.cell
def _():
    edad_cf1 = 20

    if edad_cf1 >= 18:
        resultado_cf1 = "Mayor de edad"
    else:
        resultado_cf1 = "Menor de edad"

    print(resultado_cf1)
    return edad_cf1, resultado_cf1


@app.cell
def _(mo):
    mo.md(
        r"""
## 2) Uso de elif (múltiples ramas)

Cuando existen más de dos posibles escenarios, se utiliza `elif`.

```python
if condicion_1:
    ...
elif condicion_2:
    ...
else:
    ...
```
"""
    )
    return


@app.cell
def _():
    nota_cf2 = 3.7

    if nota_cf2 >= 4.5:
        categoria_cf2 = "Excelente"
    elif nota_cf2 >= 3.5:
        categoria_cf2 = "Aprobado"
    else:
        categoria_cf2 = "Reprobado"

    print("Categoría:", categoria_cf2)
    return nota_cf2, categoria_cf2


@app.cell
def _(mo):
    mo.md(
        r"""
## 3) Condiciones compuestas

Las condiciones pueden combinarse usando operadores lógicos:

- `and`
- `or`
- `not`
"""
    )
    return


@app.cell
def _():
    edad_cf3 = 25
    permiso_cf3 = True

    acceso_cf3 = (edad_cf3 >= 18) and permiso_cf3
    print("Acceso permitido:", acceso_cf3)

    return edad_cf3, permiso_cf3, acceso_cf3


@app.cell
def _(mo):
    mo.md(
        r"""
## 4) Anidamiento de condicionales

Es posible colocar un `if` dentro de otro, aunque se recomienda evitar estructuras demasiado profundas.
"""
    )
    return


@app.cell
def _():
    ingreso_cf4 = 2500
    deuda_cf4 = 500

    if ingreso_cf4 > 2000:
        if deuda_cf4 < 1000:
            decision_cf4 = "Crédito aprobado"
        else:
            decision_cf4 = "Revisión manual"
    else:
        decision_cf4 = "Crédito rechazado"

    print(decision_cf4)
    return ingreso_cf4, deuda_cf4, decision_cf4


@app.cell
def _(mo):
    mo.md(
        r"""
## 5) Expresión condicional en una línea (ternaria)

Forma compacta:

```python
valor_si_true if condicion else valor_si_false
```
"""
    )
    return


@app.cell
def _():
    edad_cf5 = 16
    mensaje_cf5 = "Mayor" if edad_cf5 >= 18 else "Menor"

    print(mensaje_cf5)
    return edad_cf5, mensaje_cf5


@app.cell
def _(mo):
    mo.md(
        r"""
## 6) Buenas prácticas

- Mantener condiciones simples.
- Evitar lógica redundante.
- Preferir claridad sobre compactación excesiva.
- Documentar reglas de decisión cuando representen criterios académicos o clínicos.
"""
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
---

# Mini-reto (Sección 4)

Construye una función `clasificar_imc(peso_kg, altura_m)` que:

1. Calcule IMC = peso / (altura^2)
2. Clasifique según:
   - IMC < 18.5 → "Bajo peso"
   - 18.5 ≤ IMC < 25 → "Normal"
   - 25 ≤ IMC < 30 → "Sobrepeso"
   - IMC ≥ 30 → "Obesidad"
3. Lance ValueError si altura ≤ 0
4. Lance TypeError si entradas no son numéricas
"""
    )
    return


@app.function
# === TU TURNO (EDITA ESTA CELDA) ===

def clasificar_imc(peso_kg, altura_m):

    # 1) Validar que ambas entradas sean numéricas
    # TODO:
    pass

    # 2) Validar que altura sea > 0
    # TODO:
    pass

    # 3) Calcular IMC
    # TODO:
    imc = None

    # 4) Clasificar según rangos definidos
    # TODO:
    if False:
        return None
    elif False:
        return None
    elif False:
        return None
    else:
        return None


@app.cell(hide_code=True)
def _(mo):
    tip_content = mo.md(
        """
    ### Tip

    Para estructurar `clasificar_imc(peso_kg, altura_m)` con rigor:

    1. Valida tipos primero:
       - `isinstance(peso_kg, (int, float))`
       - `isinstance(altura_m, (int, float))`

    2. Valida dominio:
       - `altura_m` debe ser estrictamente mayor que 0.

    3. Calcula:
       - `imc = peso_kg / (altura_m ** 2)`

    4. Usa condicionales en orden creciente:
       - primero `< 18.5`
       - luego `< 25`
       - luego `< 30`
       - finalmente el caso restante

    Ordenar correctamente los umbrales evita errores lógicos.
    """
    )

    solution_content = mo.md(
        """
    ### Solución (referencia)

    ```python
    def clasificar_imc(peso_kg, altura_m):

        if not isinstance(peso_kg, (int, float)) or not isinstance(altura_m, (int, float)):
            raise TypeError("Peso y altura deben ser numéricos.")

        if altura_m <= 0:
            raise ValueError("La altura debe ser mayor que 0.")

        imc = peso_kg / (altura_m ** 2)

        if imc < 18.5:
            return "Bajo peso"
        elif imc < 25:
            return "Normal"
        elif imc < 30:
            return "Sobrepeso"
        else:
            return "Obesidad"
    ```

    Notas:
    - La validación ocurre antes del cálculo.
    - Los elif se estructuran en orden ascendente.
    - El else captura el caso IMC ≥ 30.
    """
    )
    mo.accordion(
        {
            "Tip (estructura lógica)": tip_content,
            "Solución (referencia)": solution_content,
        }
    )
    return


@app.cell
def _(clasificar_imc, mo):

    assert clasificar_imc(50, 1.70) == "Bajo peso"
    assert clasificar_imc(65, 1.70) == "Normal"
    assert clasificar_imc(80, 1.70) == "Sobrepeso"
    assert clasificar_imc(95, 1.70) == "Obesidad"

    mo.md(
        r"""
✅ Reto superado.

Has aplicado correctamente estructuras condicionales, validación de tipos y lógica compuesta.
"""
    )
    return


if __name__ == "__main__":
    app.run()
