"""
GRAFO - Vértices (nodos) conectados por aristas.

Uso en el proyecto: TOPOLOGÍA DE LA RED.
Cada equipo (router, switch, servidor, PC, cámara) es un vértice y cada
cable/enlace entre dos equipos es una arista. Es un grafo NO DIRIGIDO.

Representación: LISTA DE ADYACENCIA (diccionario):
    { "router-01": {"switch-01"}, "switch-01": {"router-01", "srv-web-01"}, ... }
Además guardamos la información de cada nodo en otro diccionario.
"""
from .cola import Cola


class Grafo:
    def __init__(self):
        self.nodos = {}        # nombre -> datos del equipo (ip, tipo)
        self.adyacencia = {}   # nombre -> conjunto de vecinos

    def add_node(self, nombre, datos=None):
        if nombre not in self.nodos:
            self.nodos[nombre] = datos or {}
            self.adyacencia[nombre] = set()

    def add_edge(self, a, b):
        """Conecta dos equipos (en ambas direcciones porque es no dirigido)."""
        if a not in self.nodos or b not in self.nodos:
            raise ValueError("Ambos equipos deben existir en el grafo")
        if a == b:
            raise ValueError("Un equipo no se puede conectar consigo mismo")
        self.adyacencia[a].add(b)
        self.adyacencia[b].add(a)

    def remove_edge(self, a, b):
        self.adyacencia.get(a, set()).discard(b)
        self.adyacencia.get(b, set()).discard(a)

    def remove_node(self, nombre):
        for vecino in self.adyacencia.get(nombre, set()):
            self.adyacencia[vecino].discard(nombre)
        self.adyacencia.pop(nombre, None)
        self.nodos.pop(nombre, None)

    def has_node(self, nombre):
        return nombre in self.nodos

    def vecinos(self, nombre):
        return sorted(self.adyacencia.get(nombre, set()))

    def bfs(self, inicio):
        """Recorrido por ANCHURA: primero los vecinos directos, luego los vecinos de esos...
        Usa nuestra propia COLA."""
        if inicio not in self.nodos:
            return []
        visitados = {inicio}
        orden = []
        cola = Cola()
        cola.enqueue(inicio)
        while not cola.is_empty():
            actual = cola.dequeue()
            orden.append(actual)
            for vecino in self.vecinos(actual):
                if vecino not in visitados:
                    visitados.add(vecino)
                    cola.enqueue(vecino)
        return orden

    def dfs(self, inicio, visitados=None):
        """Recorrido en PROFUNDIDAD (recursivo): baja por una rama hasta el fondo."""
        if inicio not in self.nodos:
            return []
        if visitados is None:
            visitados = set()
        visitados.add(inicio)
        orden = [inicio]
        for vecino in self.vecinos(inicio):
            if vecino not in visitados:
                orden.extend(self.dfs(vecino, visitados))
        return orden

    def ruta(self, origen, destino):
        """Camino más corto (en saltos) entre dos equipos usando BFS."""
        if origen not in self.nodos or destino not in self.nodos:
            return []
        anterior = {origen: None}
        cola = Cola()
        cola.enqueue(origen)
        while not cola.is_empty():
            actual = cola.dequeue()
            if actual == destino:
                break
            for vecino in self.vecinos(actual):
                if vecino not in anterior:
                    anterior[vecino] = actual
                    cola.enqueue(vecino)
        if destino not in anterior:
            return []        # no hay conexión
        camino = []
        paso = destino
        while paso is not None:
            camino.insert(0, paso)
            paso = anterior[paso]
        return camino

    def to_dict(self):
        return {
            "nodos": [{"nombre": n, **d} for n, d in self.nodos.items()],
            "aristas": sorted({tuple(sorted((a, b))) for a in self.adyacencia for b in self.adyacencia[a]}),
        }
