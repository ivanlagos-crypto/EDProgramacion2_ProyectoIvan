"""
PILA (Stack) - Principio LIFO: Last In, First Out (el último en entrar es el primero en salir).

Uso en el proyecto: HISTORIAL DE ACTIVIDAD del analista.
Cada acción que se hace en la plataforma (registrar equipo, crear ticket, etc.)
se apila encima. La más reciente queda arriba y es la primera que se ve.

Implementación: con NODOS enlazados (como vimos en la clase de listas).
El "tope" de la pila es el primer nodo; cada nodo apunta al que está debajo.
"""


class Nodo:
    def __init__(self, valor):
        self.valor = valor      # el dato que guarda el nodo
        self.siguiente = None   # la "flecha" al nodo que está debajo


class Pila:
    def __init__(self):
        self.tope = None    # nodo de arriba (None = pila vacía)
        self.tamano = 0

    def push(self, valor):
        """Agrega un elemento ENCIMA de la pila."""
        nuevo = Nodo(valor)
        nuevo.siguiente = self.tope   # el nuevo apunta al que era el tope
        self.tope = nuevo             # ahora el nuevo es el tope
        self.tamano += 1

    def pop(self):
        """Saca y devuelve el elemento de ARRIBA. Si está vacía devuelve None."""
        if self.is_empty():
            return None
        nodo = self.tope
        self.tope = nodo.siguiente    # el de abajo pasa a ser el tope
        self.tamano -= 1
        return nodo.valor

    def peek(self):
        """Devuelve el elemento de arriba SIN sacarlo."""
        return None if self.is_empty() else self.tope.valor

    def is_empty(self):
        return self.tope is None

    def size(self):
        return self.tamano

    def to_list(self):
        """Devuelve los elementos desde el tope hacia abajo (del más reciente al más antiguo)."""
        elementos = []
        actual = self.tope
        while actual is not None:
            elementos.append(actual.valor)
            actual = actual.siguiente
        return elementos

    def print(self):
        for valor in self.to_list():
            print(valor)
