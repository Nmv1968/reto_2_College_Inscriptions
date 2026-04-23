from nodo import Nodo
from estudiante import Estudiante


# =============================================================================
# Clase ColaPrioridad: Estructura donde los elementos se organizan de
# mayor a menor prioridad antes de ser atendidos.
# =============================================================================
class ColaPrioridad:
    # Inicializa la cola de prioridad con el frente nulo y longitud cero.
    def __init__(self):
        self.frente = None
        self.length = 0

    # Lógica Enqueue de Prioridad:
    # Convención: mayor número = mayor prioridad (5 = crítico, 1 = bajo)
    # No inserta al final. Recorre la lista buscando el lugar adecuado
    # según el valor de 'prioridad'. Los elementos con mayor prioridad
    # se desplazan hacia el frente de la cola.
    def enqueue(self, valor: Estudiante, prioridad: int, motivo_prioridad: str = None):
        nuevo = Nodo(valor, prioridad, motivo_prioridad)
        # Si la cola está vacía o el nuevo nodo tiene mayor prioridad que el frente entonces se inserta al frente
        if self.is_empty() or prioridad > self.frente.prioridad:
            nuevo.siguiente = self.frente
            self.frente = nuevo
        else:
            # Recorrido para insertar en la posición correcta (orden descendente)
            actual = self.frente
            while actual.siguiente and actual.siguiente.prioridad >= prioridad:
                actual = actual.siguiente
            nuevo.siguiente = actual.siguiente
            actual.siguiente = nuevo
        self.length += 1
        return nuevo

    # Remueve el elemento que quedó con mayor prioridad (en el frente).
    def dequeue(self):
        if self.is_empty():
            print("⚠️ Underflow: cola prioritaria vacía.")
            return None
        valor = self.frente.estudiante
        prioridad = self.frente.prioridad
        motivo_prioridad = self.frente.motivo_prioridad
        self.frente = self.frente.siguiente
        self.length -= 1
        return valor, prioridad, motivo_prioridad

    # Comprueba si existen elementos en la cola.
    def is_empty(self):
        return self.frente is None

    # Indica el número de elementos que esperan en la cola de prioridad.
    def size(self):
        return self.length

    # Genera una representación de los valores y sus prioridades para su iteración.
    def __iter__(self):
        actual = self.frente
        while actual:
            yield actual.estudiante, actual.prioridad, actual.motivo_prioridad
            actual = actual.siguiente
