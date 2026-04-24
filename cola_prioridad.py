"""
================================================================================
MÓDULO: cola_prioridad.py
================================================================================
A diferencia de la cola simple (FIFO), aquí los elementos se organizan
según su NIVEL DE PRIORIDAD, no según su orden de llegada.

- Mayor número = Mayor prioridad (5 = alta prioridad, 1 = baja prioridad)
- El elemento con MAYOR prioridad siempre está al FRENTE
- Los de igual prioridad se ordenan por orden de llegada (FIFO)

================================================================================
"""

from nodo import Nodo
from estudiante import Estudiante

class ColaPrioridad:
    """
    Cola de Prioridad: Los estudiantes se atienden según su nivel de prioridad.
    
    Atributos:
    - frente: Puntero al estudiante con mayor prioridad
    - length: Cantidad de estudiantes en la cola
    
    Diferencia con ColaSimple:
    - ColaSimple: El primero en llegar = primero en salir
    - ColaPrioridad: El de mayor prioridad = primero en salir
    
    Niveles de prioridad:
    - 5 = Alta prioridad
    - 4 = Prioridad media-alta
    - 3 = Prioridad media
    - 2 = Prioridad media-baja
    - 1 = Baja prioridad
    """
    
    def __init__(self):
        self.frente = None
        self.length = 0

    def enqueue(self, valor: Estudiante, prioridad: int, motivo_prioridad: str = None):
        """
        Inserta un estudiante en la posición correcta según su prioridad.

        Proceso:
        1. Crea un nodo con la prioridad del estudiante
        2. Si la cola está vacía o el nuevo tiene mayor prioridad, entonces se inserta al frente
        3. Si no, recorre la cola buscando donde insertar (orden descendente)
        4. Los de mayor prioridad quedan más cerca del frente
        """
        nuevo = Nodo(valor, prioridad, motivo_prioridad)
        
        # Caso 1: Cola vacía o nueva prioridad mayor que el frente
        if self.is_empty() or prioridad > self.frente.prioridad:
            nuevo.siguiente = self.frente
            self.frente = nuevo
        else:
            # Caso 2: Buscar posición correcta (orden descendente)
            actual = self.frente
            # Avanzar mientras siguiente tenga >= prioridad (mantener orden)
            while actual.siguiente and actual.siguiente.prioridad >= prioridad:
                actual = actual.siguiente
            # Insertar el nuevo nodo en la posición encontrada
            nuevo.siguiente = actual.siguiente
            actual.siguiente = nuevo
        
        self.length += 1
        return nuevo

    def dequeue(self):
        """
        Remueve y retorna el estudiante con MAYOR prioridad (del frente).
        
        Nota: Siempre atiende al del frente, que es el de mayor prioridad.
        """
        if self.is_empty():
            return None
        
        estudiante = self.frente.estudiante
        prioridad = self.frente.prioridad
        motivo_prioridad = self.frente.motivo_prioridad
        
        self.frente = self.frente.siguiente
        self.length -= 1
        
        return estudiante, prioridad, motivo_prioridad

    def is_empty(self):
        """Verifica si la cola no tiene elementos."""
        return self.frente is None

    def size(self):
        """Retorna la cantidad de estudiantes en la cola."""
        return self.length

    def __iter__(self):
        """Permite iterar sobre la cola (desde mayor a menor prioridad)."""
        actual = self.frente
        while actual:
            yield actual.id_estudiante, actual.estudiante, actual.prioridad, actual.motivo_prioridad
            actual = actual.siguiente

    def remove_by_ci(self, ci: str):
        """Elimina un estudiante específico por su cédula de identidad."""
        if self.is_empty():
            return None
        
        # Eliminar del frente si es el buscado
        if self.frente.estudiante.ci_estudiante == ci:
            self.frente = self.frente.siguiente
            self.length -= 1
            return True
        
        # Buscar en el resto de la cola
        actual = self.frente
        while actual.siguiente:
            if actual.siguiente.estudiante.ci_estudiante == ci:
                actual.siguiente = actual.siguiente.siguiente
                self.length -= 1
                return True
            actual = actual.siguiente
        
        return False