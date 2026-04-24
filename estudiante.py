"""
================================================================================
MÓDULO: estudiante.py
================================================================================

Clase estudiante que define las características básicas de un estudiante
que se registrará en el sistema de inscripciones.

CARACTERÍSTICAS:
- Nombre del estudiante
- Cédula de identidad (identificador único)

Atributo especial:
- has_prioridad: Indica si el estudiante tiene alguna prioridad para atención

================================================================================
"""

from dataclasses import dataclass

@dataclass
class Estudiante:
    nombre: str
    ci_estudiante: str
    has_prioridad: bool = False
