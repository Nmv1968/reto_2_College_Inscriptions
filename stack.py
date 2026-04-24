from nodo import Nodo


# =============================================================================
# Clase Accion: Representa una acción ejecutada que puede ser deshecha.
# Contiene el tipo de acción, los datos relevantes y la descripción.
# =============================================================================
class Accion:
    def __init__(self, tipo: str, datos: dict, descripcion: str):
        self.tipo = tipo  # Tipos: "configurar_curso", "enqueue_normal", "enqueue_prioridad", "atender", "liberar_cupo"
        self.datos = datos  # Datos necesarios para deshacer la acción
        self.descripcion = descripcion  # Descripción legible de la acción

    def __repr__(self):
        return f"Accion({self.tipo}: {self.descripcion})"


# =============================================================================
# Clase Stack: Implementa una pila dinámica usando una lista enlazada.
# La pila tiene un tope (top) que apunta al último elemento agregado.
# =============================================================================
class Stack:
    # Constructor de la clase Stack, inicializa la pila con tope None y tamaño 0
    def __init__(self):
        # Inicializa el tope de la pila
        self.top = None
        # Inicializa el tamaño de la pila
        self._size = 0

    # Método push: Agrega un nuevo elemento a la pila.
    # Crea un nuevo nodo con el valor dado, enlaza su 'next' al tope actual,
    # y actualiza el tope para que apunte al nuevo nodo, manteniendo la cadena enlazada.
    def push(self, value):
        # Crea un nuevo nodo con el valor y el tope actual como siguiente
        nodo = Nodo(value, None, None)  # Usamos el Nodo genérico con valor directo
        nodo.valor = value  # Asignamos el valor directamente
        nodo.siguiente = self.top
        # Actualiza el tope para que apunte al nuevo nodo
        self.top = nodo
        # Incrementa el tamaño de la pila
        self._size += 1

    # Método pop: Remueve y devuelve el elemento del tope de la pila.
    def pop(self):
        # Verifica si la pila está vacía
        if self.is_empty():
            # Si está vacía, retorna None
            return None
        # Obtiene el valor del tope
        extracted_value = self.top.valor
        # Actualiza el tope al siguiente nodo
        self.top = self.top.siguiente
        # Decrementa el tamaño de la pila
        self._size -= 1
        # Retorna el valor extraído
        return extracted_value

    # Método is_empty: Verifica si la pila está vacía.
    def is_empty(self):
        # Retorna True si el tope es None, indicando pila vacía
        return self.top is None

    # Método peek: Devuelve el valor del tope sin removerlo.
    def peek(self):
        # Verifica si la pila está vacía
        if self.is_empty():
            # Si está vacía, retorna None
            return None
        # Retorna el valor del tope sin removerlo
        return self.top.valor

    # Método size: Devuelve el número de elementos en la pila.
    def size(self):
        # Retorna el tamaño actual de la pila
        return self._size

    # __iter__: Permite iterar sobre los elementos de la pila desde el tope hacia abajo.
    def __iter__(self):
        # Comenzamos el recorrido desde el nodo que está en el tope (cima)
        current_node = self.top
        # Mientras el nodo actual no sea None (es decir, queden elementos)
        while current_node is not None:
            # 'yield' entrega el valor actual al ciclo 'for' sin detener la función
            yield current_node.valor
            # Movemos el puntero al siguiente nodo de la lista enlazada
            current_node = current_node.siguiente