"""
================================================================================
MÓDULO: lista_enlazada.py
================================================================================
Este módulo implementa una LISTA ENLAZADA SIMPLE.
Estructura de datos lineal donde cada elemento (nodo) contiene:
- Un dato (estudiante)
- Un puntero al siguiente nodo

A diferencia de las colas, la lista enlazada permite:
- Insertar al inicio o al final
- Eliminar desde cualquier posición
- Recorrer en ambas direcciones (con doble enlace, pero aquí es simple)

En este reto, se usa para representar los ESTUDIANTES INSCRITOS
en un curso específico (la lista de inscritos).
================================================================================
"""

from nodo import Nodo
from estudiante import Estudiante


class ListaEnlazada:
    """
    Lista Enlazada Simple: Almacena los estudiantes inscritos en un curso.
    
    Atributos:
    - head: Puntero al primer nodo de la lista (cabeza)
    - _max_size: Cupo máximo del curso (0 = sin límite)
    - _length: Cantidad actual de estudiantes inscritos
    - _list_name: Nombre del curso/Lista
    
    Uso en el reto:
    - Representa la lista de estudiantes ya inscritos en un curso
    - Controla que no se exceda el cupo máximo
    """
    
    def __init__(self):
        self.head = None           # Primer nodo (None si lista vacía)
        self._max_size = 0         # Cupo máximo del curso
        self._length = 0           # Cantidad actual de inscritos
        self._list_name = None     # Nombre del curso

    # ==================== PROPIEDADES (Getters/Setters) ====================
    
    @property
    def list_name(self):
        """Retorna el nombre del curso."""
        return self._list_name

    @list_name.setter
    def list_name(self, value):
        """Establece el nombre del curso."""
        self._list_name = value

    @property
    def max_size(self):
        """Retorna el cupo máximo del curso."""
        return self._max_size

    @max_size.setter
    def max_size(self, value: int):
        """Establece el cupo máximo del curso."""
        self._max_size = value

    @property
    def is_course_configurated(self):
        """Verifica si el curso está configurado (nombre y cupo definidos)."""
        return self._list_name is not None and self._max_size > 0

    # ==================== MÉTODOS PRINCIPALES ====================
    
    def append(self, estudiante: Estudiante, prioridad: int = None, motivo_prioridad: str = None):
        """
        Agrega un estudiante al FINAL de la lista de inscritos.
        
        Proceso:
        1. Verifica si hay cupos disponibles
        2. Crea un nuevo nodo con los datos del estudiante
        3. Si la lista está vacía, el nuevo nodo es la cabeza
        4. Si no, recorre hasta el final y enlaza el nuevo nodo
        """
        # Verificar límite de cupos
        if self._max_size > 0 and self._length >= self._max_size:
            return False  # Cupo lleno
        
        nuevo = Nodo(estudiante, prioridad, motivo_prioridad)
        
        if self.head is None:
            # Lista vacía: el nuevo nodo es la cabeza
            self.head = nuevo
        else:
            # Recorrer hasta el final de la lista
            actual = self.head
            while actual.siguiente:
                actual = actual.siguiente
            # Enlazar el nuevo nodo al final
            actual.siguiente = nuevo
        
        self._length += 1
        return True

    def remove(self, id: str):
        """
        Elimina un estudiante de la lista por su ID.
        
        Proceso:
        1. Si la lista está vacía, retorna False
        2. Recorre la lista buscando el nodo con el ID
        3. Mantiene referencia al nodo anterior para reenlazar
        4. Si es el primero (head), mueve head al siguiente
        5. Si está en medio/fin, reenlaza anterior con siguiente
        """
        if self.is_empty():
            return False
        
        actual = self.head
        anterior = None
        
        # Buscar el nodo a eliminar
        while actual and actual.id_estudiante != id:
            anterior = actual
            actual = actual.siguiente
        
        # No se encontró el estudiante
        if actual is None:
            return False
        
        self._length -= 1
        
        # Eliminar: reenlazar la cadena
        if anterior is None:
            # Era el primer elemento: mover head
            self.head = actual.siguiente
        else:
            # Era un elemento del medio/final: saltar el nodo
            anterior.siguiente = actual.siguiente
        
        return True

    def is_empty(self):
        """Verifica si la lista no tiene estudiantes inscritos."""
        return self.head is None

    def size(self):
        """Retorna la cantidad de estudiantes inscritos."""
        return self._length
    
    def get_head(self):
        """Retorna la cabeza de la lista (para iteración)."""
        return self.head

    def __iter__(self):
        """Permite iterar sobre los estudiantes inscritos."""
        actual = self.head
        while actual:
            yield actual.id_estudiante, actual.estudiante
            actual = actual.siguiente

    def is_empty(self):
        return self.head is None

    def size(self):
        return self._length
    
    def get_head(self):
        return self.head

    # Permite recorrer los valores de la lista de forma iterativa (ej: en un for).
    def __iter__(self):
        actual = self.head
        while actual:
            yield actual.id_estudiante, actual.estudiante
            actual = actual.siguiente
