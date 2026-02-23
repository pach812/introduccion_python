# /// script
# dependencies = [
#     "marimo",
#     "pyyaml==6.0.3",
# ]
# requires-python = ">=3.14"
# ///

import marimo

__generated_with = "0.19.11"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Editor de presets (YAML) para notebooks educativos en marimo

    Este notebook te permite:
    - Cargar tu YAML base (o iniciar vacío si no existe el archivo)
    - Elegir un preset base
    - Editar parámetros por clase (tema, objetivos, plan de secciones, lenguaje, etc.)
    - Editar parámetros avanzados (complejidad, interactividad, etc.)
    - Generar un preset nuevo con nombre `nombre_clase_preset`
    - Previsualizar el YAML final
    - Guardar el preset final como YAML (snippet) y/o actualizar el YAML maestro
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Dependencias y utilidades internas

    Incluye:
    - Carga/guardado YAML
    - Utilidades de parsing
    - Merge profundo (para aplicar overrides avanzados)
    - Upsert seguro en YAML maestro (sin redefinir variables globales)
    """)
    return


@app.cell
def _():
    from copy import deepcopy
    from pathlib import Path
    from datetime import datetime, timezone
    import re
    import yaml

    def slugify(value: str) -> str:
        # English comments by request.
        value = value.strip().lower()
        value = re.sub(r"\s+", "_", value)
        value = re.sub(r"[^a-z0-9_]+", "", value)
        value = re.sub(r"_+", "_", value).strip("_")
        return value or "clase"

    def parse_lines_list(text: str) -> list[str]:
        return [line.strip() for line in (text or "").splitlines() if line.strip()]

    def parse_section_plan(text: str) -> list[dict]:
        sections = []
        for line in (text or "").splitlines():
            line = line.strip()
            if not line:
                continue

            if "|" in line:
                name, cells = line.split("|", 1)
                name = name.strip()
                try:
                    approx = int(cells.strip())
                except ValueError:
                    approx = 2
                if name:
                    sections.append({"name": name, "approx_cells": approx})
            else:
                sections.append({"name": line, "approx_cells": 2})

        return sections

    def deep_merge(base: dict, patch: dict) -> dict:
        """Deep-merge patch into base (returns a new dict)."""
        out = deepcopy(base)
        stack = [(out, patch)]
        while stack:
            target, src = stack.pop()
            for k, v in src.items():
                if isinstance(v, dict) and isinstance(target.get(k), dict):
                    stack.append((target[k], v))
                else:
                    target[k] = v
        return out

    def upsert_preset_in_master(master_data: dict, preset_name: str, preset_value: dict) -> dict:
        """Insert or update a preset under agent_contract.presets (returns a new dict)."""
        updated_master = deepcopy(master_data)

        agent = updated_master.setdefault("agent_contract", {})
        master_presets = agent.setdefault("presets", {})
        master_presets[preset_name] = preset_value

        return updated_master

    def build_resolved_spec(master_data: dict, preset_name: str, preset_value: dict) -> dict:
        """
        Build a self-contained spec that includes agent_contract + exactly one preset.
        This is what you can feed to the notebook-generation agent.
        """
        updated_master = deepcopy(master_data)

        agent = updated_master.setdefault("agent_contract", {})
        agent_presets = agent.setdefault("presets", {})
        agent_presets[preset_name] = preset_value

        # Optional: mark which preset to use
        agent["active_preset"] = preset_name

        # Optional: keep only the active preset to avoid bloating the file
        agent["presets"] = {preset_name: agent_presets[preset_name]}

        return updated_master

    return (
        Path,
        build_resolved_spec,
        datetime,
        deep_merge,
        deepcopy,
        parse_lines_list,
        parse_section_plan,
        slugify,
        timezone,
        upsert_preset_in_master,
        yaml,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## YAML Maestro

    Si existe el archivo indicado, se carga automáticamente.
    Si no existe, se inicializa una estructura mínima y se crea al guardar.
    """)
    return


@app.cell
def _(mo):
    spec_path = mo.ui.text(
        value="education/notebook_spec.yml",
        label="Ruta del YAML maestro (se crea si no existe)",
        full_width=True,
    )

    output_dir = mo.ui.text(
        value="generated_presets",
        label="Directorio de salida (snippets)",
        full_width=True,
    )

    mo.vstack([spec_path, output_dir])
    return output_dir, spec_path


@app.cell
def _(Path, mo, spec_path, yaml):
    p = Path(spec_path.value).expanduser()

    if p.exists():
        raw = p.read_text(encoding="utf-8")
        data = yaml.safe_load(raw) or {}
        source_msg = f"YAML cargado desde: `{p}`"
    else:
        data = {"agent_contract": {"presets": {}}}
        source_msg = f"No existe `{p}`. Se inicializa estructura mínima (se creará al guardar)."

    presets = data.get("agent_contract", {}).get("presets", {})
    if not isinstance(presets, dict):
        presets = {}

    preset_selector = mo.ui.dropdown(
        options=sorted(list(presets.keys())) if presets else [],
        label="Preset base",
    )

    mo.vstack(
        [
            mo.md(source_msg),
            preset_selector,
            mo.md(f"Presets disponibles: **{len(presets)}**"),
        ],
        gap=1,
    )
    return data, preset_selector, presets


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Configuración de la clase

    Estos campos se aplican al preset generado (independientemente de los ajustes avanzados).
    """)
    return


@app.cell
def _(mo):
    class_name = mo.ui.text(
        value="clase_01_introduccion_python",
        label="Nombre de la clase (para el nombre del preset)",
        full_width=True,
    )

    topic_title = mo.ui.text(
        value="Introducción a Python",
        label="Título del notebook",
        full_width=True,
    )

    topic_scope = mo.ui.text_area(
        value="Describe qué incluye y qué excluye el notebook.",
        label="Scope (qué incluye / qué excluye)",
        full_width=True,
        rows=4,
    )

    language = mo.ui.dropdown(
        options=["es", "en"],
        value="es",
        label="Lenguaje de salida (afecta todo el notebook)",
    )

    mo.vstack([class_name, topic_title, topic_scope, language], gap=1)
    return class_name, language, topic_scope, topic_title


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Objetivos y restricciones
    """)
    return


@app.cell
def _(mo):
    learning_objectives = mo.ui.text_area(
        value="\n".join(
            [
                "Definir qué es Python y para qué se usa",
                "Entender el concepto de variable",
                "Identificar y crear tipos de datos básicos",
            ]
        ),
        label="Learning objectives (uno por línea)",
        full_width=True,
        rows=6,
    )

    constraints = mo.ui.text_area(
        value="\n".join(
            [
                "No clases",
                "No type hints",
                "No resultados simulados",
                "No imports fuera de marimo y stdlib (preferir built-ins)",
            ]
        ),
        label="Constraints (uno por línea)",
        full_width=True,
        rows=6,
    )

    mo.vstack([learning_objectives, constraints], gap=1)
    return constraints, learning_objectives


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Plan de secciones

    Formato (una por línea):

    `Nombre sección | número_aprox_celdas`
    """)
    return


@app.cell
def _(mo):
    section_plan_input = mo.ui.text_area(
        value="\n".join(
            [
                "Título y objetivos | 2",
                "¿Qué es Python? ¿Qué es programar? | 3",
                "Variables y asignación | 2",
                "Tipos de datos básicos | 6",
                "Ejercicios integradores | 3",
                "Resumen | 2",
            ]
        ),
        label="Section plan",
        full_width=True,
        rows=8,
    )

    glossary_enabled = mo.ui.checkbox(value=True, label="Incluir glosario")
    glossary_min = mo.ui.number(value=8, label="Glosario min_terms", step=1)
    glossary_max = mo.ui.number(value=15, label="Glosario max_terms", step=1)

    mo.vstack(
        [
            section_plan_input,
            mo.hstack([glossary_enabled, glossary_min, glossary_max], gap=2),
        ],
        gap=1,
    )
    return glossary_enabled, glossary_max, glossary_min, section_plan_input


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Preset seleccionado: resumen + edición avanzada

    - La tabla resume el preset base actual.
    - En el accordion puedes ajustar parámetros avanzados.
    - Esos cambios se aplican como `overrides` (merge profundo) al preset final.

    Nota: Si no hay preset seleccionado, los valores avanzados funcionan como defaults.
    """)
    return


@app.cell
def _(deepcopy, mo, preset_selector, presets):
    def _get(dct, path, default=None):
        """Safe getter for nested dict keys using dot-separated paths."""
        cur = dct
        for key in path.split("."):
            if not isinstance(cur, dict) or key not in cur:
                return default
            cur = cur[key]
        return cur

    selected_key = preset_selector.value
    current_preset = deepcopy(presets.get(selected_key, {}))

    # Summary table
    level = _get(current_preset, "audience.level", "NA")
    prereq = ", ".join(_get(current_preset, "audience.prerequisites", []) or [])

    math_depth = _get(current_preset, "math_depth", "NA")
    code_depth = _get(current_preset, "code_depth", "NA")

    cells_min = _get(current_preset, "estimated_cells.min", "NA")
    cells_max = _get(current_preset, "estimated_cells.max", "NA")

    mode = _get(current_preset, "interactivity.mode", "NA")
    widgets = ", ".join(_get(current_preset, "interactivity.allowed_widgets", []) or [])
    widgets_min = _get(current_preset, "interactivity.min_widgets_total", "NA")
    widgets_max = _get(current_preset, "interactivity.max_widgets_total", "NA")

    ex_freq = _get(current_preset, "exercises.frequency", "NA")
    ex_count = _get(current_preset, "exercises.count_target", "NA")
    hints = _get(current_preset, "exercises.include_hints", "NA")
    solutions = _get(current_preset, "exercises.include_solutions", "NA")

    gl_enabled = _get(current_preset, "glossary.enabled", "NA")
    gl_min = _get(current_preset, "glossary.min_terms", "NA")
    gl_max = _get(current_preset, "glossary.max_terms", "NA")

    table_md = f"""
    ### Preset base actual: `{selected_key or "None"}`

    | Categoría        | Parámetro              | Valor |
    |:-----------------|:-----------------------|:------|
    | Audience         | level                  | `{level}` |
    | Audience         | prerequisites          | `{prereq}` |
    | Depth            | math_depth             | `{math_depth}` |
    | Depth            | code_depth             | `{code_depth}` |
    | Length           | estimated_cells        | `{cells_min}`–`{cells_max}` |
    | Interactivity    | mode                   | `{mode}` |
    | Interactivity    | allowed_widgets        | `{widgets}` |
    | Interactivity    | widgets_total          | min `{widgets_min}`, max `{widgets_max}` |
    | Exercises        | frequency              | `{ex_freq}` |
    | Exercises        | count_target           | `{ex_count}` |
    | Exercises        | include_hints          | `{hints}` |
    | Exercises        | include_solutions      | `{solutions}` |
    | Glossary         | enabled                | `{gl_enabled}` |
    | Glossary         | terms                  | `{gl_min}`–`{gl_max}` |
    """
    common_summary = mo.md(table_md)

    # Advanced editors (defaults if missing)
    adv_math_depth = mo.ui.dropdown(
        options=["none", "light", "moderate", "heavy"],
        value=_get(current_preset, "math_depth", "none"),
        label="math_depth",
    )

    adv_code_depth = mo.ui.dropdown(
        options=["toy", "practical", "productionish"],
        value=_get(current_preset, "code_depth", "toy"),
        label="code_depth",
    )

    adv_cells_min = mo.ui.number(
        value=int(_get(current_preset, "estimated_cells.min", 18) or 18),
        label="estimated_cells.min",
        step=1,
    )

    adv_cells_max = mo.ui.number(
        value=int(_get(current_preset, "estimated_cells.max", 30) or 30),
        label="estimated_cells.max",
        step=1,
    )

    adv_interactivity_mode = mo.ui.dropdown(
        options=["none", "light", "standard", "heavy"],
        value=_get(current_preset, "interactivity.mode", "light"),
        label="interactivity.mode",
    )

    adv_widgets_allowed = mo.ui.multiselect(
        options=["slider", "dropdown", "checkbox", "text", "table"],
        value=_get(current_preset, "interactivity.allowed_widgets", []) or [],
        label="interactivity.allowed_widgets",
    )

    adv_widgets_min = mo.ui.number(
        value=int(_get(current_preset, "interactivity.min_widgets_total", 0) or 0),
        label="interactivity.min_widgets_total",
        step=1,
    )

    adv_widgets_max = mo.ui.number(
        value=int(_get(current_preset, "interactivity.max_widgets_total", 3) or 3),
        label="interactivity.max_widgets_total",
        step=1,
    )

    adv_ex_freq = mo.ui.dropdown(
        options=["end_only", "per_section", "mixed"],
        value=_get(current_preset, "exercises.frequency", "per_section"),
        label="exercises.frequency",
    )

    adv_ex_count = mo.ui.number(
        value=int(_get(current_preset, "exercises.count_target", 6) or 6),
        label="exercises.count_target",
        step=1,
    )

    adv_hints = mo.ui.checkbox(
        value=bool(_get(current_preset, "exercises.include_hints", True)),
        label="exercises.include_hints",
    )

    adv_solutions = mo.ui.checkbox(
        value=bool(_get(current_preset, "exercises.include_solutions", False)),
        label="exercises.include_solutions",
    )

    adv_glossary_enabled = mo.ui.checkbox(
        value=bool(_get(current_preset, "glossary.enabled", True)),
        label="glossary.enabled",
    )

    adv_gloss_min = mo.ui.number(
        value=int(_get(current_preset, "glossary.min_terms", 8) or 8),
        label="glossary.min_terms",
        step=1,
    )

    adv_gloss_max = mo.ui.number(
        value=int(_get(current_preset, "glossary.max_terms", 15) or 15),
        label="glossary.max_terms",
        step=1,
    )

    advanced_panel = mo.accordion(
        {
            "Depth / Complexity": mo.vstack([adv_math_depth, adv_code_depth], gap=1),
            "Length": mo.hstack([adv_cells_min, adv_cells_max], gap=2),
            "Interactivity": mo.vstack(
                [
                    adv_interactivity_mode,
                    adv_widgets_allowed,
                    mo.hstack([adv_widgets_min, adv_widgets_max], gap=2),
                ],
                gap=1,
            ),
            "Exercises": mo.vstack(
                [
                    adv_ex_freq,
                    adv_ex_count,
                    mo.hstack([adv_hints, adv_solutions], gap=2),
                ],
                gap=1,
            ),
            "Glossary": mo.vstack(
                [
                    adv_glossary_enabled,
                    mo.hstack([adv_gloss_min, adv_gloss_max], gap=2),
                ],
                gap=1,
            ),
        },
        multiple=True,
    )

    mo.vstack([common_summary, advanced_panel], gap=2)
    return (
        adv_cells_max,
        adv_cells_min,
        adv_code_depth,
        adv_ex_count,
        adv_ex_freq,
        adv_gloss_max,
        adv_gloss_min,
        adv_glossary_enabled,
        adv_hints,
        adv_interactivity_mode,
        adv_math_depth,
        adv_solutions,
        adv_widgets_allowed,
        adv_widgets_max,
        adv_widgets_min,
    )


@app.cell
def _(
    adv_cells_max,
    adv_cells_min,
    adv_code_depth,
    adv_ex_count,
    adv_ex_freq,
    adv_gloss_max,
    adv_gloss_min,
    adv_glossary_enabled,
    adv_hints,
    adv_interactivity_mode,
    adv_math_depth,
    adv_solutions,
    adv_widgets_allowed,
    adv_widgets_max,
    adv_widgets_min,
):
    overrides = {
        "math_depth": adv_math_depth.value,
        "code_depth": adv_code_depth.value,
        "estimated_cells": {
            "min": int(adv_cells_min.value),
            "max": int(adv_cells_max.value),
        },
        "interactivity": {
            "mode": adv_interactivity_mode.value,
            "allowed_widgets": list(adv_widgets_allowed.value),
            "min_widgets_total": int(adv_widgets_min.value),
            "max_widgets_total": int(adv_widgets_max.value),
        },
        "exercises": {
            "frequency": adv_ex_freq.value,
            "count_target": int(adv_ex_count.value),
            "include_hints": bool(adv_hints.value),
            "include_solutions": bool(adv_solutions.value),
        },
        "glossary": {
            "enabled": bool(adv_glossary_enabled.value),
            "min_terms": int(adv_gloss_min.value),
            "max_terms": int(adv_gloss_max.value),
        },
    }
    return (overrides,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Preset generado (base + overrides) y previsualización

    Se construye:
    - `base_preset`: preset base + campos de la clase
    - `final_preset`: merge profundo de `base_preset` con `overrides` (overrides gana)

    Luego se muestra el YAML final que se guardará.
    """)
    return


@app.cell
def _(
    class_name,
    constraints,
    deep_merge,
    deepcopy,
    glossary_enabled,
    glossary_max,
    glossary_min,
    language,
    learning_objectives,
    mo,
    overrides,
    parse_lines_list,
    parse_section_plan,
    preset_selector,
    presets,
    section_plan_input,
    slugify,
    topic_scope,
    topic_title,
    yaml,
):
    if preset_selector.value:
        base_preset = deepcopy(presets[preset_selector.value])
    else:
        base_preset = {}

    new_name = f"{slugify(class_name.value)}_preset"

    base_preset["topic"] = {
        "title": topic_title.value.strip(),
        "scope": topic_scope.value.strip(),
    }

    base_preset["learning_objectives"] = parse_lines_list(learning_objectives.value)

    base_preset.setdefault("style", {})
    base_preset["style"]["language"] = language.value

    base_preset["constraints"] = parse_lines_list(constraints.value)

    base_preset["section_plan"] = {
        "required": True,
        "sections": parse_section_plan(section_plan_input.value),
    }

    base_preset["glossary"] = {
        "enabled": bool(glossary_enabled.value),
        "min_terms": int(glossary_min.value),
        "max_terms": int(glossary_max.value),
    }

    final_preset = deep_merge(base_preset, overrides)

    preview_yaml = yaml.safe_dump(
        {new_name: final_preset},
        sort_keys=False,
        allow_unicode=True,
    )

    mo.md(f"### Preset final: `{new_name}` (listo para exportar)")
    mo.ui.text_area(
        value=preview_yaml,
        label="Preview YAML (final)",
        full_width=True,
        rows=18,
    )
    return final_preset, new_name


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exportación

    - Guardar snippet YAML del preset final
    - Actualizar YAML maestro insertando el preset final en `agent_contract.presets`
    """)
    return


@app.cell
def _(mo):
    save_btn = mo.ui.run_button(label="Guardar preset final como snippet YAML")
    update_btn = mo.ui.run_button(label="Actualizar YAML maestro con preset final")
    mo.hstack([save_btn, update_btn], justify="start")
    return save_btn, update_btn


@app.cell
def _(
    Path,
    build_resolved_spec,
    data,
    datetime,
    final_preset,
    mo,
    new_name,
    output_dir,
    save_btn,
    spec_path,
    timezone,
    update_btn,
    upsert_preset_in_master,
    yaml,
):
    mo.stop(not (save_btn.value or update_btn.value))

    messages = []

    if save_btn.value:
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        out_dir = Path(output_dir.value).expanduser()
        out_dir.mkdir(parents=True, exist_ok=True)

        # (a) snippet del preset (como hoy)
        snippet_file = out_dir / f"{new_name}__{ts}.yaml"
        snippet_yaml = yaml.safe_dump({new_name: final_preset}, sort_keys=False, allow_unicode=True)
        snippet_file.write_text(snippet_yaml, encoding="utf-8")

        # (b) resolved spec (completo, listo para el agente)
        resolved = build_resolved_spec(master_data=data, preset_name=new_name, preset_value=final_preset)
        resolved_file = out_dir / f"{new_name}__{ts}__resolved.yml"
        resolved_yaml = yaml.safe_dump(resolved, sort_keys=False, allow_unicode=True)
        resolved_file.write_text(resolved_yaml, encoding="utf-8")

        messages.append(f"Snippet guardado: `{snippet_file}`")
        messages.append(f"Resolved spec guardado: `{resolved_file}`")

    if update_btn.value:
        updated_master = upsert_preset_in_master(
            master_data=data,
            preset_name=new_name,
            preset_value=final_preset,
        )

        master_file = Path(spec_path.value).expanduser()
        master_file.parent.mkdir(parents=True, exist_ok=True)

        master_yaml = yaml.safe_dump(
            updated_master,
            sort_keys=False,
            allow_unicode=True,
        )
        master_file.write_text(master_yaml, encoding="utf-8")
        messages.append(f"YAML maestro actualizado: `{master_file}`")

    mo.md("\n".join(f"- {m}" for m in messages) if messages else "Acción completada.")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
