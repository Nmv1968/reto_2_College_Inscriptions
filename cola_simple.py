"""
================================================================================
MÓDULO: cola_simple.py
================================================================================
COLA SIMPLE (FIFO - First In, First Out).

Es como una fila real en un banco o supermercado:
- El PRIMERO que llega es el PRIMERO en ser atendido
- Los nuevos elementos se agregan al FINAL de la cola
- Los elementos se removen desde el FRENTE de la cola
- Primero en entrar, primero en salir
================================================================================
"""

from nodo import Nodo
from estudiante import Estudiante

class ColaSimple:
    """
    Cola Simple (FIFO): Implementa el comportamiento de una cola real.
    
    Atributos:
    - frente: Puntero al primer elemento (el que será atendido primero)
    - final: Puntero al último elemento (donde se agregan nuevos elementos)
    - length: Cantidad de estudiantes en la cola
    
    Comportamiento:
    - enqueue(): Agrega al final
    - dequeue(): Remueve del frente
    """
    
    def __init__(self):
        # Frente = primer elemento en ser atendido (None si cola vacía)
        self.frente = None
        # Final = último elemento agregado (None si cola vacía)
        self.final = None
        # Contador de elementos
        self.length = 0

    def is_empty(self):
        """Verifica si la cola no tiene elementos."""
        return self.frente is None

    def enqueue(self, valor: Estudiante):
        """
        Agrega un estudiante al FINAL de la cola.
        
        Proceso:
        1. Crea un nuevo nodo con el estudiante
        2. Si la cola está vacía, frente y final apuntan al nuevo nodo
        3. Si ya hay elementos, el actual 'final' apunta al nuevo nodo
        4. Actualiza 'final' para que apunte al nuevo nodo
        """
        nuevo = Nodo(valor)
        if self.final:
            self.final.siguiente = nuevo
        self.final = nuevo
        if self.frente is None:
            self.frente = nuevo
        self.length += 1
        return valor

    def dequeue(self):
        """
        Remueve y retorna el estudiante del FRENTE de la cola.
        
        Proceso:
        1. Verifica si la cola está vacía
        2. Obtiene el estudiante del frente
        3. Si solo había un elemento, limpia frente y final
        4. Si había más, mueve frente al siguiente elemento
        5. Retorna el estudiante atendido
        """
        if self.is_empty():
            return None
        valor = self.frente.estudiante
        self.frente = self.frente.siguiente
        # Si la cola queda vacía, el puntero final también debe ser None.
        if self.frente is None:
            self.final = None
        self.length -= 1
        return valor

    def front(self):
        """Retorna el valor al frente de la cola sin removerlo."""
        return None if self.is_empty() else self.frente.estudiante

    def size(self):
        """Retorna la cantidad de estudiantes en la cola."""
        return self.length

    def __iter__(self):
        """Permite iterar sobre la cola desde el frente hacia el final."""
        actual = self.frente
        while actual:
            yield actual.id_estudiante, actual.estudiante
            actual = actual.siguiente

    # Elimina un estudiante de la cola por su cédula de identidad.
    def remove_by_ci(self, ci: str):
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
