from nodo import Nodo


class ColaCircular:
    def __init__(self):
        self.frente = None
        self.final = None
        self.length = 0

    def is_empty(self):
        return self.frente is None

    def enqueue(self, valor):
        nuevo = Nodo(valor)
        if self.is_empty():
            self.frente = nuevo
            self.final = nuevo
            self.final.siguiente = self.frente
        else:
            self.final.siguiente = nuevo
            self.final = nuevo
            self.final.siguiente = self.frente
        self.length += 1

    def dequeue(self):
        if self.is_empty():
            return None
        valor = self.frente.estudiante
        if self.frente == self.final:
            self.frente = None
            self.final = None
        else:
            self.frente = self.frente.siguiente
            self.final.siguiente = self.frente
        self.length -= 1
        return valor

    def size(self):
        return self.length
