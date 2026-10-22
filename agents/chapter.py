"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'chapter'
LABEL = 'Chapter'
SPEC_FILE = 'chapter_review.md'
EXTRACT_CODE = False

INSTRUCTIONS = """Contrasta cada criterio de aceptación con arquitectura, persistencia, implementación, pruebas y seguridad.
Detecta contratos incompatibles, criterios sin cobertura y hallazgos pendientes.
Para cada observación indica responsable, cambio requerido y cómo verificarlo.
Justifica el veredicto con evidencia y señala las pruebas pendientes.
Conserva las aprobaciones humanas; tu informe no las sustituye.
Entrega chapter_review.md con VEREDICTO: APROBADO o RECHAZADO, motivos y correcciones."""
agent = Agent(role='Chapter', goal="""Evaluar la solución frente a cada criterio de aceptación y emitir un
    veredicto sustentado en evidencia, con hallazgos y correcciones verificables.""",
              backstory="""Eres el revisor técnico final del equipo. Tienes experiencia en análisis
    de requisitos, arquitectura, persistencia, desarrollo, pruebas y seguridad.
    Evalúas cada criterio de aceptación con base en los artefactos y resultados
    disponibles; identificas contradicciones, cobertura faltante y hallazgos
    pendientes. Distingues claramente la evidencia ejecutada de las propuestas
    o verificaciones no realizadas, y no afirmas cumplimiento sin respaldo.
    Tus observaciones son accionables: indican responsable, corrección y forma
    de comprobarla. Tu informe justifica el veredicto, pero no sustituye las aprobaciones humanas.""", llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output='Un informe con VEREDICTO: APROBADO o RECHAZADO.', agent=agent)
