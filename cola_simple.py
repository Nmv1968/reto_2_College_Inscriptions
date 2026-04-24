from nodo import Nodo
from estudiante import Estudiante


# =============================================================================
# Clase ColaSimple: Implementa una estructura FIFO (First-In, First-Out).
# =============================================================================
class ColaSimple:
    # Inicializa una cola vacía con referencias al frente, final y contador.
    def __init__(self):
        self.frente = None
        self.final = None
        self.length = 0

    # Verifica si la cola no tiene elementos (frente es None).
    def is_empty(self):
        return self.frente is None

    # Lógica Enqueue Simple:
    # Inserta el nuevo elemento siempre al final de la cola (tail).
    # No considera prioridades, solo el orden cronológico de llegada.
    def enqueue(self, valor: Estudiante):
        nuevo = Nodo(valor)
        if self.final:
            self.final.siguiente = nuevo
        self.final = nuevo
        if self.frente is None:
            self.frente = nuevo
        self.length += 1
        return valor

    # Remueve y retorna el elemento que está al frente de la cola.
    # Sigue el principio FIFO permitiendo avanzar al siguiente nodo.
    def dequeue(self):
        # Verifica si la cola está vacía antes de remover un elemento.
        if self.is_empty():
            print("⚠️ Underflow: cola vacía.")
            return None
        valor = self.frente.estudiante
        self.frente = self.frente.siguiente
        # Si la cola queda vacía, el puntero final también debe ser None.
        if self.frente is None:
            self.final = None
        self.length -= 1
        return valor

    # Retorna el valor al frente de la cola sin removerlo.
    def front(self):
        return None if self.is_empty() else self.frente.estudiante

    # Retorna la cantidad total de elementos actualmente en la cola.
    def size(self):
        return self.length

    # Permite recorrer los valores de la cola de forma iterativa (ej: en un for).
    def __iter__(self):
        actual = self.frente
        while actual:
            yield actual.id_estudiante, actual.estudiante
            actual = actual.siguiente

    # Elimina un estudiante de la cola por su cédula de identidad.
    def eliminar_por_ci(self, ci: str):
        if self.is_empty():
            return None
        
        # Si el estudiante a eliminar está al frente
        if self.frente.estudiante.ci_estudiante == ci:
            self.frente = self.frente.siguiente
            if self.frente is None:
                self.final = None
            self.length -= 1
            return True
        
        # Buscar el estudiante en el resto de la cola
        actual = self.frente
        while actual.siguiente:
            if actual.siguiente.estudiante.ci_estudiante == ci:
                actual.siguiente = actual.siguiente.siguiente
                # Si se eliminó el último nodo, actualizar final
                if actual.siguiente is None:
                    self.final = actual
                self.length -= 1
                return True
            actual = actual.siguiente
        return False
