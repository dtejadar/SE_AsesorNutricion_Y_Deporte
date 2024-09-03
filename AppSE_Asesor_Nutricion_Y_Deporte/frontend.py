from reactpy import component, html, use_state
import httpx  # Cliente HTTP para python

@component
def RecomendacionForm():
    objetivo, set_objetivo = use_state("")
    actividad_fisica, set_actividad_fisica = use_state("")
    restriccion_alimentaria, set_restriccion_alimentaria = use_state("")
    tiempo_entrenamiento, set_tiempo_entrenamiento = use_state(0)
    edad, set_edad = use_state(0)
    recomendaciones, set_recomendaciones = use_state([])
    reglas_activadas, set_reglas_activadas = use_state([])
    facts, set_facts = use_state([])

    def handle_change(set_value):
        def _handle_change(event):
            value = event['target'].get('value', '')
            set_value(value)
        return _handle_change

    async def handle_submit(event):
        # Enviar el objetivo seleccionado al backend para obtener recomendaciones
        if objetivo and actividad_fisica and restriccion_alimentaria and tiempo_entrenamiento and edad:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "http://127.0.0.1:8000/api/recomendaciones", 
                    json={
                        "objetivo": objetivo,
                        "actividad_fisica": actividad_fisica,
                        "restriccion_alimentaria": restriccion_alimentaria,
                        "tiempo_entrenamiento": tiempo_entrenamiento,
                        "edad": edad 
                    }
                )
                if response.status_code == 200:
                    data = response.json()
                    set_recomendaciones(data["recomendaciones"])
                    set_reglas_activadas(data["reglas_activadas"])
                    set_facts(data["facts"])
                else:
                    set_recomendaciones(["Error al obtener los datos."])
        else:
            set_recomendaciones(["Faltan campos por digitar."])

    return html.div(
        html.div(
            {
                "class": "col-lg-12 col-md-12 mt-2",
                "style": "display: flex; justify-content: center;"
            },
            html.h2({"class": "title"},"Asesor en Nutrición y Ejercicio")
        ),
        html.div(
            {"style": "display:flex; justify-content: space-around;"},
            html.div(
                {"class": "offset-lg-4 offset-md-4 col-lg-4 col-md-4 mt-4"},
                html.div(
                    {"class": "form-group"},
                    html.label({"class": "label-title"},"Objetivo: "),
                    html.select(
                        {
                            "class": "form-control",
                            "value": objetivo,
                            "onchange": handle_change(set_objetivo)
                        },
                        html.option({"value": ""}, "Seleccione un objetivo"),
                        html.option({"value": "ganar_masa_muscular"}, "Ganar Masa Muscular"),
                        html.option({"value": "perder_grasa"}, "Perder grasa")
                    )
                ),
                html.div(
                    {"class": "form-group"},
                    html.label({"class": "label-title"},"Nivel de entrenamiento: "),
                    html.select(
                        {
                            "class": "form-control",
                            "value": actividad_fisica,
                            "onchange": handle_change(set_actividad_fisica)
                        },
                        html.option({"value": ""}, "Seleccione su nivel de entrenamiento"),
                        html.option({"value": "nivel_alto"}, "Nivel alto"),
                        html.option({"value": "nivel_medio"}, "Nivel medio"),
                        html.option({"value": "nivel_bajo"}, "Nivel bajo")
                    )
                ),
                html.div(
                    {"class": "form-group"},
                    html.label({"class": "label-title"},"Restricción alimentaria: "),
                    html.select(
                        {
                            "class": "form-control",
                            "value": restriccion_alimentaria,
                            "onchange": handle_change(set_restriccion_alimentaria)
                        },
                        html.option({"value": ""}, "Seleccione restricción alimentaria"),
                        html.option({"value": "ninguna"}, "Ninguna"),
                        html.option({"value": "vegetariano"}, "Vegetariano")
                    )
                ),
                html.div(
                    {"class": "form-group"},
                    html.label({"for": "time-workout","class": "label-title"}, "Tiempo de entrenamiento: "),
                    html.input(
                        {
                            "type": "number",
                            "class": "form-control",
                            "id": "time-workout",
                            "name": "time-workout",
                            "min": "0",
                            "max": "300",
                            "step": "1",
                            "placeholder": "0",
                            "value": tiempo_entrenamiento,
                            "oninput": handle_change(set_tiempo_entrenamiento)
                        }
                    )
                ),
                html.div(
                    {"class": "form-group"},
                    html.label({"for": "age", "class": "label-title"}, "Edad: "),
                    html.input(
                        {
                            "type": "number",
                            "class": "form-control",
                            "id": "age",
                            "name": "age",
                            "min": "0",
                            "max": "150",
                            "step": "1",
                            "placeholder": "0",
                            "value": edad,
                            "oninput": handle_change(set_edad)
                        }
                    )
                ),
                html.button(
                    {"type": "button", "class": "btn btn-primary", "onclick": handle_submit}, 
                    "Obtener Recomendaciones"
                ),
                html.div(
                    {"class": "mt-4"},
                    html.h3("Recomendaciones:"),
                    html.ul({"class": "list-group"}, 
                        [html.li({"class": "list-group-item"}, rec) for rec in recomendaciones] 
                        if recomendaciones else 
                        [html.li({"class": "list-group-item"}, "No hay recomendaciones disponibles")]
                    )
                ),
                html.br()       
            ),
            html.div(
                {
                    "class": "col-lg-4 col-md-4 mt-4",
                    "style": "display: flex; justify-content: center;"
                },
                html.div(
                    {"class": "technical-information"},
                    html.h4("Información técnica"),
                    html.br(),
                    html.p({"class": "label-title"},"Reglas activadas:"),
                    html.ul({"class": "list-group"}, 
                        [html.li({"class": "list-group-item"}, regla) for regla in reglas_activadas] 
                        if reglas_activadas else 
                        [html.li({"class": "list-group-item"}, "No hay reglas activas")]
                    ),
                    html.br(),                          
                    html.p({"class": "label-title"},"Hechos registrados:"),
                    html.ul({"class": "list-group"}, 
                        [html.li({"class": "list-group-item"}, fact) for fact in facts] 
                        if reglas_activadas else 
                        [html.li({"class": "list-group-item"}, "No hay hechos registrados")]
                    )
                )
            )
        )
    )