"""
COLA (Queue) - Principio FIFO: First In, First Out (el primero en entrar es el primero en salir).

Uso en el proyecto: TICKETS DE SOPORTE.
Los tickets se atienden en orden de llegada, como la fila de un banco.

Implementación: con NODOS enlazados.
- "frente" (head): el primero de la fila, el próximo en ser atendido.
- "final" (tail): el último que llegó. Los nuevos se agregan detrás de él.
"""


class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None


class Cola:
    def __init__(self):
        self.frente = None
        self.final = None
        self.tamano = 0

    def enqueue(self, valor):
        """Agrega un elemento AL FINAL de la cola."""
        nuevo = Nodo(valor)
        if self.is_empty():
            self.frente = nuevo
            self.final = nuevo
        else:
            self.final.siguiente = nuevo   # el último apunta al nuevo
            self.final = nuevo             # el nuevo pasa a ser el último
        self.tamano += 1

    def dequeue(self):
        """Saca y devuelve el PRIMER elemento. Si está vacía devuelve None."""
        if self.is_empty():
            return None
        nodo = self.frente
        self.frente = nodo.siguiente
        if self.frente is None:      # si quedó vacía, el final también se borra
            self.final = None
        self.tamano -= 1
        return nodo.valor

    def peek(self):
        """Devuelve el primer elemento SIN sacarlo."""
        return None if self.is_empty() else self.frente.valor

    def is_empty(self):
        return self.frente is None

    def size(self):
        return self.tamano

    def to_list(self):
        """Elementos en orden de atención (del primero al último)."""
        elementos = []
        actual = self.frente
        while actual is not None:
            elementos.append(actual.valor)
            actual = actual.siguiente
        return elementos

    def print(self):
        for valor in self.to_list():
            print(valor)
