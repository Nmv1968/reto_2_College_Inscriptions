from nodo import Nodo
from estudiante import Estudiante

class ListaEnlazada:
    def __init__(self):
        self.head = None
        self.__max_size = None
        self.length = 0
        self.__list_name = None

    def insertar_final(self, estudiante: Estudiante, prioridad: int = None, motivo_prioridad: str = None):
        if self.__max_size is not None and self.length >= self.__max_size:
            print("⚠️ Lista llena")
            return
        nuevo = Nodo(estudiante, prioridad, motivo_prioridad)
        if self.head is None:
            self.head = nuevo
        else:
            actual = self.head
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo
        self.length += 1
        print(f"✅ Insertado {estudiante.nombre} al final")

    def eliminar(self, id: str):
        if self.is_empty():
            print("⚠️ Lista vacía")
            return
        actual = self.head
        anterior = None
        while actual and actual.id_estudiante != id:
            anterior = actual
            actual = actual.siguiente
        if actual is None:
            print(f"⚠️ Estudiante con ID {id} no encontrado")
            return
        self.length -= 1
        if anterior is None:
            self.head = actual.siguiente
        else:
            anterior.siguiente = actual.siguiente
        print(f"🗑️ Eliminado {actual.estudiante.nombre}")

    def is_empty(self):
        return self.head is None

    def size(self):
        return self.length
    
    def get_head(self):
        return self.head

    def set_list_name(self, name):
        self.__list_name = name

    def set_max_size(self, max_size: int):
        self.__max_size = max_size

    def get_list_max_size(self) -> int:
        return self.__max_size or 0

    def get_list_name(self):
        return self.__list_name

    # Permite recorrer los valores de la cola de forma iterativa (ej: en un for).
    def __iter__(self):
        actual = self.head
        while actual:
            yield actual.id_estudiante, actual.estudiante
            actual = actual.siguiente
