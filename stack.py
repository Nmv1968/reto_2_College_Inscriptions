"""
================================================================================
MÓDULO: stack.py
================================================================================
Este módulo implementa una PILA (STACK) y la clase Accion para el sistema de
deshacer acciones (undo).

Estructura de datos LIFO (Last In, First Out) - "Último en entrar,
primero en salir".

Funcionamiento:
- Cada acción que se hace se "empuja" a la pila
- Para deshacer, se remueve la última acción (la más reciente)

LÓGICA: "El último en entrar, primero en salir"
================================================================================
"""

from datetime import datetime
from nodo import Nodo


class Accion:
    """
    Representa una acción ejecutada que puede ser deshecha.
    
    Esta clase almacena toda la información necesaria para revertir
    una operación del sistema de inscripciones.
    
    Atributos:
    - tipo: Tipo de acción realizada
      * "configurar_curso" - Crear un nuevo curso
      * "enqueue_normal" - Inscribir en cola normal
      * "enqueue_prioridad" - Inscribir con prioridad
      * "atender" - Atender un estudiante
      * "liberar_cupo" - Liberar un estudiante del curso
    - datos: Diccionario con datos necesarios para deshacer
    - descripcion: Texto legible describiendo la acción
    - fecha_hora: Timestamp automático de cuándo se ejecutó
    """
    
    def __init__(self, tipo: str, datos: dict, descripcion: str):
        self.tipo = tipo
        self.datos = datos          # Datos para revertir la acción
        self.descripcion = descripcion  # Descripción legible
        self.fecha_hora = datetime.now()  # Timestamp automático

    def __repr__(self):
        """Representación legible para debugging."""
        hora_str = self.fecha_hora.strftime("%H:%M:%S")
        return f"[{hora_str}] {self.tipo}: {self.descripcion}"


class Stack:
    """
    Atributos:
    - top: Puntero al nodo en la cima de la pila (último elemento agregado)
    - _size: Cantidad de acciones en el historial
    
    Métodos principales:
    - push(): Agrega una acción al historial
    - pop(): Remueve y retorna la última acción (para deshacer)
    - peek(): Ve la última acción sin removerla
    - is_empty(): Verifica si hay acciones para deshacer
    
    Relación con el reto:
    - Cada operación del menú se registra como una "Accion"
    - Al elegir "Deshacer", se ejecuta pop() para obtener la última acción
    - Los datos de la acción permiten revertirla correctamente
    """
    
    def __init__(self):
        # Top = cima de la pila (último elemento agregado)
        self.top = None
        # Contador de elementos
        self._size = 0

    def push(self, value):
        """
        Agrega una nueva acción a la cima de la pila.
        
        Proceso:
        1. Crea un nuevo nodo con la acción
        2. El nuevo nodo apunta al anterior top
        3. Actualiza el top para que apunte al nuevo nodo
        4. Incrementa el tamaño
        
        Nota: El orden de inserción importa - el último push será el primero en pop.
        """
        nodo = Nodo(value, None, None)
        nodo.valor = value
        nodo.siguiente = self.top  # El nuevo apunta al anterior top
        self.top = nodo            # El nuevo se convierte en el top
        self._size += 1

    def pop(self):
        """
        Remueve y retorna la acción de la cima (la más reciente).
        
        Este es el método usado para "Deshacer" - obtiene la última
        acción para poder revertirla.
        
        Proceso:
        1. Verifica si la pila está vacía
        2. Obtiene el valor del top
        3. Mueve el top al siguiente nodo
        4. Decrementa el tamaño
        5. Retorna la acción extraída
        """
        if self.is_empty():
            return None
        
        extracted_value = self.top.valor
        self.top = self.top.siguiente
        self._size -= 1
        return extracted_value

    def is_empty(self):
        """Verifica si no hay acciones para deshacer."""
        return self.top is None

    def peek(self):
        """
        Ve la acción de la cima SIN removerla.
        
        Útil para mostrar qué acción se deshará next sin ejecutarla.
        """
        if self.is_empty():
            return None
        return self.top.valor

    def size(self):
        """Retorna la cantidad de acciones en el historial."""
        return self._size

    def __iter__(self):
        """
        Itera sobre las acciones desde la más reciente hasta la más antigua.
        
        Útil para mostrar el historial de acciones al usuario.
        """
        current_node = self.top
        while current_node is not None:
            yield current_node.valor
            current_node = current_node.siguiente