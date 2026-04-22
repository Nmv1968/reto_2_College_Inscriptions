import uuid
from estudiante import Estudiante

# =============================================================================
# Clase Nodo: Representa la unidad básica de la estructura.
# Contiene el valor almacenado, una prioridad opcional y el puntero al siguiente nodo.
# =============================================================================
class Nodo:
    def __init__(self, estudiante: Estudiante, prioridad: int = None):
        self.id_estudiante = str(uuid.uuid4())
        self.estudiante = estudiante
        self.prioridad = prioridad
        self.siguiente = None
