"""
HEAP (Montículo) - Árbol binario completo guardado en un ARREGLO (lista de Python).

Uso en el proyecto: ALERTAS DE SEGURIDAD POR SEVERIDAD.
Es un MAX-HEAP: el padre siempre tiene mayor prioridad que sus hijos,
así que la alerta MÁS CRÍTICA siempre está en la posición 0 (la raíz).

Fórmulas para moverse en el arreglo (vistas en clase):
    hijo izquierdo = 2 * i + 1
    hijo derecho   = 2 * i + 2
    padre          = (i - 1) // 2      (// es división entera)

La "prioridad" se calcula con una función que se recibe al crear el heap.
Así el mismo heap sirve para alertas (por severidad) o productos (por popularidad).
"""


class MaxHeap:
    def __init__(self, prioridad=None):
        self.datos = []
        # Si no nos dan función de prioridad, se compara el valor directamente
        self.prioridad = prioridad if prioridad is not None else (lambda x: x)

    # ---------- helpers ----------
    def _padre(self, i):
        return (i - 1) // 2

    def _izq(self, i):
        return 2 * i + 1

    def _der(self, i):
        return 2 * i + 2

    def _mayor(self, i, j):
        """True si el elemento en i tiene MÁS prioridad que el de j."""
        return self.prioridad(self.datos[i]) > self.prioridad(self.datos[j])

    def _swap(self, i, j):
        self.datos[i], self.datos[j] = self.datos[j], self.datos[i]

    # ---------- reordenar ----------
    def _percolate_up(self, i):
        """Sube el elemento mientras sea más importante que su padre."""
        while i > 0 and self._mayor(i, self._padre(i)):
            self._swap(i, self._padre(i))
            i = self._padre(i)

    def _percolate_down(self, i):
        """Baja el elemento mientras alguno de sus hijos sea más importante."""
        n = len(self.datos)
        while True:
            mayor = i
            izq, der = self._izq(i), self._der(i)
            if izq < n and self._mayor(izq, mayor):
                mayor = izq
            if der < n and self._mayor(der, mayor):
                mayor = der
            if mayor == i:      # ya está en su lugar
                break
            self._swap(i, mayor)
            i = mayor

    # ---------- métodos públicos ----------
    def push(self, valor):
        """Inserta al final y lo sube a su lugar."""
        self.datos.append(valor)
        self._percolate_up(len(self.datos) - 1)

    def pop(self):
        """Saca el de MAYOR prioridad (la raíz) y reordena."""
        if self.is_empty():
            return None
        self._swap(0, len(self.datos) - 1)   # el último pasa a la raíz
        maximo = self.datos.pop()            # sacamos el que era la raíz
        if not self.is_empty():
            self._percolate_down(0)
        return maximo

    def peek(self):
        return None if self.is_empty() else self.datos[0]

    def heapify(self, lista):
        """Convierte una lista cualquiera en heap."""
        self.datos = list(lista)
        for i in range(len(self.datos) // 2 - 1, -1, -1):
            self._percolate_down(i)

    def top_k(self, k):
        """Devuelve los k de mayor prioridad SIN modificar el heap original."""
        copia = MaxHeap(self.prioridad)
        copia.datos = list(self.datos)
        resultado = []
        while len(resultado) < k and not copia.is_empty():
            resultado.append(copia.pop())
        return resultado

    def is_empty(self):
        return len(self.datos) == 0

    def size(self):
        return len(self.datos)

    def to_array(self):
        return list(self.datos)
