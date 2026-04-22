from nodo import Nodo


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
    def enqueue(self, valor: str):
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
            yield actual.estudiante
            actual = actual.siguiente

