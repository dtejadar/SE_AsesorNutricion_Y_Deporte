from fastapi import FastAPI, Request
import clips  # Asegúrate de tener instalada esta librería

app = FastAPI()

# Configurar el entorno de CLIPS
env = clips.Environment()

# Ruta para manejar solicitudes de recomendación
@app.post("/recomendaciones")
async def obtener_recomendaciones(request: Request):
    data = await request.json()
    objetivo = data.get("objetivo", "")
    actividad_fisica = data.get("actividad_fisica", "")
    restriccion_alimentaria = data.get("restriccion_alimentaria", "")
    tiempo_entrenamiento = data.get("tiempo_entrenamiento", "")
    edad = data.get("edad", "")

    # Restablecer el entorno para evitar acumulación de hechos anteriores
    env.clear()

    #Definición de reglas
    #Regla 1 - para sugerir rutiana de ejercicio - Ganar masa muscular con un nivel alto
    env.build('''
    (defrule sugerir-rutina-ganar-masa
        (objetivo ganar_masa_muscular)
        (actividad_fisica nivel_alto)
        (tiempo_entrenamiento ?tiempo&:(>= ?tiempo 30))
        (edad ?edad&:(< ?edad 40))
        =>
        (assert (Recomendacion ejercicio: "Rutina de fuerza con pesas 5 veces por semana"))
    )
    ''')

    #Regla 2 - para sugerir rutiana de ejercicio - Perder grasa con un nivel bajo
    env.build('''
    (defrule sugerir-rutina-perder-grasa
        (objetivo perder_grasa)
        (actividad_fisica nivel_bajo)
        (tiempo_entrenamiento ?tiempo&:(>= ?tiempo 30))
        =>
        (assert (Recomendacion ejercicio: "Rutina de fuerza con pesas y cardio 3 veces por semana"))
    )
    ''')

    #Regla 3 - para sugerir plan de alimentacion con restriccion
    env.build('''
    (defrule sugerir-alimentacion-restriccion
        (restriccion_alimentaria vegetariano)
        =>
        (assert (Recomendacion alimentacion: "Dieta baja en carbohidratos con proteínas vegetales"))
    )
    ''')

    #Regla 4 - para sugerir plan de alimentacion en perdida de grasa
    env.build('''
    (defrule sugerir-alimentacion-perder-grasa
        (objetivo perder_grasa)
        (actividad_fisica nivel_bajo)
        (restriccion_alimentaria ninguna)
        =>
        (assert (Recomendacion alimentacion: "Dieta baja en carbohidratos y azúcares con fuentes de proteína y fibra"))
    )
    ''')

    #Regla 5 - para ajustar rutina segun tiempo disponible
    env.build('''
    (defrule ajustar-rutina
        (tiempo_entrenamiento ?tiempo&:(< ?tiempo 30))
        =>
        (assert (Recomendacion ejercicio: "Rutina de alta intensidad 20 minutos diarios"))
    )
    ''')

    #Regla 6 - para ajustar recomendacion segun edad
    env.build('''
    (defrule ajustar-segun-edad
        (edad ?edad&:(> ?edad 40))
        (objetivo ganar_masa_muscular)
        =>
        (assert (Recomendacion ejercicio "Enfoque en resistencia, con pesos moderados y repeticiones altas"))
    )
    ''')

    #Regla 7 - para sugerir plan de alimentacion en ganancia muscular
    env.build('''
    (defrule sugerir-alimentacion-ganar-masa
        (objetivo ganar_masa_muscular)
        (restriccion_alimentaria ninguna)
        =>
        (assert (Recomendacion alimentacion: "Dieta alta en proteína, fibra y grasas saludables"))
    )
    ''')

    # Insertar los hechos en el entorno CLIPS
    if objetivo:
        env.assert_string(f"(objetivo {objetivo})")
    if actividad_fisica:
        env.assert_string(f"(actividad_fisica {actividad_fisica})")
    if restriccion_alimentaria:
        env.assert_string(f"(restriccion_alimentaria {restriccion_alimentaria})")
    if tiempo_entrenamiento:
        env.assert_string(f"(tiempo_entrenamiento {tiempo_entrenamiento})")
    if edad:
        env.assert_string(f"(edad {edad})")

    # Lista de reglas activadas
    reglas_activadas = []
    for activation in env.activations():
        print("Activation: ", activation)
        reglas_activadas.append(activation.name)

 

    # Ejecutar el motor de inferencia de CLIPS
    env.run()

    # Recopilar recomendaciones generadas
    recomendaciones = []
    facts = []
    for fact in env.facts():
        #print("fact: ", fact.template.name, " - ", fact[0])
        if fact.template.name == "Recomendacion":
            recomendaciones.append(fact[1])
        else:
            facts.append(f"{fact.template.name}  -  {fact[0]}")
    
    print("facts", facts)

    return {
        "recomendaciones": recomendaciones,
        "facts": facts, 
        "reglas_activadas": reglas_activadas
    }
