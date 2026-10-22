"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'backend'
LABEL = 'Desarrollador backend'
SPEC_FILE = 'backend_spec.md'
EXTRACT_CODE = True

INSTRUCTIONS = """Recibe el Issue, sus criterios de aceptación, el contrato de API aprobado por Arquitectura,
el código existente del producto y, si está activo el rol Datos, su modelo y migración aprobados.
Implementa los endpoints, servicios, validaciones y acceso a datos necesarios para cumplir los criterios.
No inventes ni cambies rutas, campos, formatos, códigos de error ni reglas del contrato: señala como
PENDIENTE DE CONFIRMAR cualquier contradicción o decisión que falte y solicita alinearla con Arquitectura.
Con Datos activo, respeta su modelo y migración sin rediseñar tablas ni regenerar SQL. En equipos de seis,
define la persistencia que requiera la funcionalidad y entrega su esquema o migración cuando corresponda.
En backend_spec.md relaciona cada criterio con la implementación, describe los endpoints, validaciones,
errores y acceso a datos, y traza un caso válido y uno de error desde la petición hasta la persistencia.
Incluye comprobaciones reproducibles y comandos; marca NO EJECUTADO toda prueba que no hayas ejecutado
y no afirmes resultados sin evidencia. Después entrega cada archivo Java en su propio bloque de código,
con // Nombre.java como primera línea y el package correspondiente a su ubicación de extracción."""
agent = Agent(role='Desarrollador backend', goal="Implementar la funcionalidad backend conforme a los criterios de aceptación y contratos aprobados.",
              backstory="Eres responsable de convertir los contratos aprobados en endpoints y servicios Java verificables, coordinando las dudas de API con Arquitectura y respetando el modelo de Datos cuando esté activo.", llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output=(
                    'Primero backend_spec.md con el mapeo de criterios, contrato implementado, validaciones, '
                    'errores, acceso a datos, trazas de un caso válido y uno de error, y comandos de comprobación. '
                    'Marca NO EJECUTADO las pruebas no ejecutadas y señala pendientes de contrato. Después, '
                    'un bloque markdown por archivo Java; su primera línea debe ser // Nombre.java, seguido '
                    'del package correspondiente a su ubicación (service, resource, repository, dto o model).'
                ), agent=agent)


