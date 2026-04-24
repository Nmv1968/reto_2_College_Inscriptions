"""
================================================================================
MÓDULO: cola_circular.py
================================================================================
Cola donde el ÚLTIMO elemento se conecta de vuelta al PRIMERO,
formando un círculo lógico (no físico).

La diferencia principal con la cola simple:
- Cola Simple: El final NO apunta a nada (termina en None)
- Cola Circular: El final APUNTA al frente, formando un ciclo cerrado
================================================================================
"""

from nodo import Nodo
from estudiante import Estudiante

class ColaCircular:
    """
    Cola Circular: Los nodos forman un ciclo donde el final apunta al frente.
    
    Atributos:
    - frente: Puntero al primer elemento
    - final: Puntero al último elemento
    - length: Cantidad de estudiantes
    
    Diferencia con ColaSimple:
    - ColaSimple: final.siguiente = None (termina la cadena)
    - ColaCircular: final.siguiente = frente (forma un ciclo)
    
    Nota: El comportamiento externo es similar a FIFO, pero internamente
    mantiene una referencia circular que permite iteración infinita.
    """
    
    def __init__(self):
        self.frente = None
        self.final = None
        self.length = 0

    def is_empty(self):
        """Verifica si la cola no tiene elementos."""
        return self.frente is None

    def enqueue(self, estudiante: Estudiante):
        """
        Agrega un estudiante al final de la cola circular.
        
        Proceso:
        1. Crea un nuevo nodo
        2. Si está vacía: frente y final apuntan al nuevo, que se apunta a sí mismo
        3. Si no está vacía: el actual final apunta al nuevo, y el nuevo apunta al frente
        """
        nuevo = Nodo(estudiante)
        
        if self.is_empty():
            # Primer elemento: se apunta a sí mismo formando el ciclo
            self.frente = nuevo
            self.final = nuevo
            self.final.siguiente = self.frente  # Ciclo cerrado
        else:
            # El actual final apunta al nuevo nodo
            self.final.siguiente = nuevo
            # El nuevo nodo se convierte en el final
            self.final = nuevo
            # El nuevo final apunta al frente (cerrando el ciclo)
            self.final.siguiente = self.frente
        
        self.length += 1

    def dequeue(self):
        """
        Remueve y retorna el estudiante del frente de la cola.
        
        Proceso similar a ColaSimple, pero mantiene el ciclo:
        - Si era el único elemento: limpia todo (frente y final = None)
        - Si había más: mueve frente al siguiente y actualiza el ciclo
        """
        if self.is_empty():
            return None
        
        estudiante = self.frente.estudiante
        
        if self.frente == self.final:
            # Era el único elemento: romper el ciclo
            self.frente = None
            self.final = None
        else:
            # Mover frente al siguiente y mantener el ciclo
            self.frente = self.frente.siguiente
            self.final.siguiente = self.frente  # Mantener ciclo actualizado
        
        self.length -= 1
        return estudiante

    def size(self):
        """Retorna la cantidad de estudiantes en la cola."""
        return self.length
    
    def __iter__(self):
        """
        Itera sobre la cola de forma circular.
        
        IMPORTANTE: Usa un ciclo while True con condición de parada
        para evitar bucle infinito. Se detiene cuando vuelve al frente.
        """
        if self.is_empty():
            return
        
        actual = self.frente
        while True:
            yield actual.id_estudiante, actual.estudiante
            actual = actual.siguiente
            # Detenerse cuando llegamos de vuelta al frente
            if actual == self.frente:
                break
        
