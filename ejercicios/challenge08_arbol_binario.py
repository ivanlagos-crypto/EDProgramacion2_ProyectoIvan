"""
CHALLENGE 08 - Árbol binario de búsqueda
- Insertar una serie de números e imprimirlos en InOrder, PreOrder y PostOrder por consola.
- Función para verificar si un valor está en el árbol.
- Visualización: se dibuja el árbol en consola y se genera 'arbol_d3.json'
  con el formato que usa la librería react-d3-tree ({name, children}).
"""
import json
from pathlib import Path


class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.left = None
        self.right = None

    def is_leaf(self):
        return self.left is None and self.right is None


class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, valor):
        """Menores a la izquierda, mayores a la derecha. No se permiten repetidos."""
        nuevo = Nodo(valor)
        if self.root is None:
            self.root = nuevo
            return True
        actual = self.root
        while True:
            if valor == actual.valor:
                return False                     # repetido: no se agrega
            if valor < actual.valor:
                if actual.left is None:
                    actual.left = nuevo
                    return True
                actual = actual.left
            else:
                if actual.right is None:
                    actual.right = nuevo
                    return True
                actual = actual.right

    def contains(self, valor):
        actual = self.root
        while actual is not None:
            if valor == actual.valor:
                return True
            actual = actual.left if valor < actual.valor else actual.right
        return False

    # ----- recorridos recursivos -----
    def preorder(self, nodo="inicio"):     # Nodo - Izquierda - Derecha
        if nodo == "inicio":
            nodo = self.root
        if nodo is None:
            return []
        return [nodo.valor] + self.preorder(nodo.left) + self.preorder(nodo.right)

    def inorder(self, nodo="inicio"):      # Izquierda - Nodo - Derecha
        if nodo == "inicio":
            nodo = self.root
        if nodo is None:
            return []
        return self.inorder(nodo.left) + [nodo.valor] + self.inorder(nodo.right)

    def postorder(self, nodo="inicio"):    # Izquierda - Derecha - Nodo
        if nodo == "inicio":
            nodo = self.root
        if nodo is None:
            return []
        return self.postorder(nodo.left) + self.postorder(nodo.right) + [nodo.valor]

    # ----- visualización -----
    def dibujar(self):
        """Dibuja el árbol en consola (la raíz arriba, las ramas hacia abajo)."""
        if self.root is None:
            print("(árbol vacío)")
            return
        print(self.root.valor)
        hijos = [(h, izq) for h, izq in [(self.root.right, False), (self.root.left, True)] if h]
        for i, (hijo, izq) in enumerate(hijos):
            self._dibujar_rama(hijo, "", izq, i == len(hijos) - 1)

    def _dibujar_rama(self, nodo, prefijo, es_izq, ultimo):
        conector = "└── " if ultimo else "├── "
        lado = "(I) " if es_izq else "(D) "
        print(prefijo + conector + lado + str(nodo.valor))
        nuevo_prefijo = prefijo + ("    " if ultimo else "│   ")
        hijos = [(h, izq) for h, izq in [(nodo.right, False), (nodo.left, True)] if h]
        for i, (hijo, izq) in enumerate(hijos):
            self._dibujar_rama(hijo, nuevo_prefijo, izq, i == len(hijos) - 1)

    def to_d3(self, nodo="inicio"):
        """Formato de react-d3-tree: {"name": ..., "children": [...]}"""
        if nodo == "inicio":
            nodo = self.root
        if nodo is None:
            return None
        hijos = [self.to_d3(h) for h in (nodo.left, nodo.right) if h is not None]
        datos = {"name": str(nodo.valor)}
        if hijos:
            datos["children"] = hijos
        return datos


if __name__ == "__main__":
    arbol = BinaryTree()
    numeros = [50, 30, 70, 20, 40, 60, 80, 35, 65]
    for n in numeros:
        arbol.insert(n)

    print("Números insertados:", numeros)
    print("PreOrder  (N-I-D):", arbol.preorder())
    print("InOrder   (I-N-D):", arbol.inorder())
    print("PostOrder (I-D-N):", arbol.postorder())

    print("\nÁrbol (D = derecha, I = izquierda):")
    arbol.dibujar()

    for valor in [40, 65, 99]:
        print(f"¿Está el {valor}? ->", "Sí" if arbol.contains(valor) else "No")

    salida = Path(__file__).parent / "arbol_d3.json"
    salida.write_text(json.dumps(arbol.to_d3(), indent=2), encoding="utf-8")
    print(f"\nEstructura para react-d3-tree guardada en {salida.name}")

    # Modo interactivo para buscar valores
    while True:
        texto = input("\nEscribe un número para buscarlo (o 'salir'): ").strip()
        if texto.lower() == "salir":
            break
        if texto.lstrip("-").isdigit():
            print("Está en el árbol ✅" if arbol.contains(int(texto)) else "No está ❌")
