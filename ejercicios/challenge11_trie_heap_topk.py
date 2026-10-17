"""
CHALLENGE 11 - Buscador inteligente + Top resultados
- Los productos se guardan en un TRIE (búsqueda por prefijo).
- Un HEAP devuelve los K productos más populares que coinciden con el prefijo.
Cada producto: {"name": "air max", "popularity": 95}
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from backend.estructuras.heap import MaxHeap  # noqa: E402


class NodoTrie:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.popularity = 0


class BuscadorProductos:
    def __init__(self):
        self.root = NodoTrie()

    def insert(self, name, popularity):
        actual = self.root
        for letra in name.lower():
            if letra not in actual.children:
                actual.children[letra] = NodoTrie()
            actual = actual.children[letra]
        actual.is_end_of_word = True
        actual.popularity = popularity

    def search(self, name):
        nodo = self._nodo(name)
        return nodo is not None and nodo.is_end_of_word

    def _nodo(self, texto):
        actual = self.root
        for letra in texto.lower():
            if letra not in actual.children:
                return None
            actual = actual.children[letra]
        return actual

    def _por_prefijo(self, prefijo):
        """Todos los productos que empiezan con el prefijo (DFS desde ese nodo)."""
        inicio = self._nodo(prefijo)
        encontrados = []
        if inicio is None:
            return encontrados
        pila = [(inicio, prefijo.lower())]
        while pila:
            nodo, palabra = pila.pop()
            if nodo.is_end_of_word:
                encontrados.append({"name": palabra, "popularity": nodo.popularity})
            for letra, hijo in nodo.children.items():
                pila.append((hijo, palabra + letra))
        return encontrados

    def search_top_k(self, prefijo, k):
        heap = MaxHeap(prioridad=lambda p: p["popularity"])
        heap.heapify(self._por_prefijo(prefijo))
        return [heap.pop() for _ in range(min(k, heap.size()))]


if __name__ == "__main__":
    tienda = BuscadorProductos()
    tienda.insert("air max", 90)
    tienda.insert("air force", 95)
    tienda.insert("air jordan", 85)
    tienda.insert("adidas boost", 80)
    tienda.insert("adidas samba", 88)
    tienda.insert("asics gel", 70)

    print('searchTopK("air", 2):')
    print(tienda.search_top_k("air", 2))   # -> air force (95), air max (90)

    while True:
        texto = input("\nBuscar (prefijo) o 'salir': ")
        if texto.strip().lower() == "salir":
            break
        try:
            k = int(input("¿Cuántos resultados (K)? "))
        except ValueError:
            k = 3
        resultados = tienda.search_top_k(texto, k)
        if not resultados:
            print("Sin resultados")
        for i, p in enumerate(resultados, start=1):
            print(f"  {i}. {p['name']} ⭐ {p['popularity']}")
