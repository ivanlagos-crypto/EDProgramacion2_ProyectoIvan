"""
TRIE (Árbol de prefijos) - La información está en el CAMINO, no en los nodos.

Uso en el proyecto: BUSCADOR CON AUTOCOMPLETADO DE EQUIPOS.
Al escribir "srv" se sugieren "srv-web-01", "srv-db-01", etc.

Cada nodo tiene:
- hijos: diccionario {letra: NodoTrie}
- fin_de_palabra: True si en ese nodo termina una palabra guardada
La raíz es un nodo vacío (no representa ninguna letra).
"""


class NodoTrie:
    def __init__(self):
        self.hijos = {}
        self.fin_de_palabra = False


class Trie:
    def __init__(self):
        self.raiz = NodoTrie()

    def insert(self, palabra):
        """Recorre letra por letra; si la letra no existe, crea el nodo."""
        actual = self.raiz
        for letra in palabra.lower():
            if letra not in actual.hijos:
                actual.hijos[letra] = NodoTrie()
            actual = actual.hijos[letra]
        actual.fin_de_palabra = True     # marcamos que aquí termina una palabra

    def _buscar_nodo(self, texto):
        """Devuelve el nodo donde termina 'texto', o None si el camino no existe."""
        actual = self.raiz
        for letra in texto.lower():
            if letra not in actual.hijos:
                return None
            actual = actual.hijos[letra]
        return actual

    def search(self, palabra):
        """True si la palabra COMPLETA está guardada."""
        nodo = self._buscar_nodo(palabra)
        return nodo is not None and nodo.fin_de_palabra

    def starts_with(self, prefijo):
        """True si alguna palabra empieza con ese prefijo."""
        return self._buscar_nodo(prefijo) is not None

    def autocompletar(self, prefijo):
        """Devuelve TODAS las palabras que empiezan con el prefijo (recorrido DFS)."""
        nodo = self._buscar_nodo(prefijo)
        resultados = []
        if nodo is None:
            return resultados

        def dfs(nodo_actual, camino):
            if nodo_actual.fin_de_palabra:
                resultados.append(camino)
            for letra in sorted(nodo_actual.hijos):
                dfs(nodo_actual.hijos[letra], camino + letra)

        dfs(nodo, prefijo.lower())
        return resultados

    def delete(self, palabra):
        """Quita la marca de fin de palabra (la palabra deja de existir)."""
        nodo = self._buscar_nodo(palabra)
        if nodo is not None and nodo.fin_de_palabra:
            nodo.fin_de_palabra = False
            return True
        return False
