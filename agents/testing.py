"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'testing'
LABEL = 'Ingeniero de pruebas'
SPEC_FILE = 'testing_report.md'
EXTRACT_CODE = True

INSTRUCTIONS = """Relaciona cada criterio de aceptación con una prueba y su resultado esperado.
Incluye casos positivos, negativos, de borde e integración.
Detalla preparación, datos de prueba, comandos y limpieza.
Comprueba los contratos de API y persistencia y las correcciones propuestas.
Marca NO EJECUTADO cuando no tengas una salida real. No inventes resultados.
Entrega testing_report.md, pruebas y comandos reproducibles."""

goal = """Verificar que la solución cumpla los criterios de aceptación mediante pruebas reproducibles de backend, API y frontend en caso aplique."""
backstory = """Eres un tester senior con experiencia en pruebas funcionales y de integración. 
Analizas contratos de API, persistencia y flujos de interfaz; 
identificas riesgos y comunicas defectos con pasos claros para reproducirlos."""


agent = Agent(role='Ingeniero de pruebas', goal=goal,
              backstory=backstory, llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output='Un informe de pruebas.', agent=agent)
