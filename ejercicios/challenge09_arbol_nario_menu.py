"""
CHALLENGE 09 - Árbol N-ario de menús
Cada ítem del menú tiene: título, link y componente.
Se llena el árbol con menús y submenús y se "pinta" un menú lateral (sidebar)
recorriendo el árbol. También se muestran los recorridos DFS y BFS.
"""
from collections import deque


class NodoMenu:
    def __init__(self, titulo, link="", componente=""):
        self.titulo = titulo
        self.link = link
        self.componente = componente
        self.children = []

    def add_child(self, hijo):
        self.children.append(hijo)
        return hijo


def construir_menu():
    raiz = NodoMenu("Mi Aplicación", "/", "App")

    inicio = raiz.add_child(NodoMenu("Inicio", "/inicio", "Inicio"))
    inicio.add_child(NodoMenu("Resumen", "/inicio/resumen", "Resumen"))

    seguridad = raiz.add_child(NodoMenu("Seguridad", "/seguridad", "Seguridad"))
    alertas = seguridad.add_child(NodoMenu("Alertas", "/seguridad/alertas", "Alertas"))
    alertas.add_child(NodoMenu("Críticas", "/seguridad/alertas/criticas", "AlertasCriticas"))
    alertas.add_child(NodoMenu("Historial", "/seguridad/alertas/historial", "HistorialAlertas"))
    seguridad.add_child(NodoMenu("Firewall", "/seguridad/firewall", "Firewall"))

    red = raiz.add_child(NodoMenu("Red", "/red", "Red"))
    red.add_child(NodoMenu("Equipos", "/red/equipos", "Equipos"))
    red.add_child(NodoMenu("Topología", "/red/topologia", "Topologia"))

    config = raiz.add_child(NodoMenu("Configuración", "/config", "Configuracion"))
    config.add_child(NodoMenu("Usuarios", "/config/usuarios", "Usuarios"))
    config.add_child(NodoMenu("Perfil", "/config/perfil", "Perfil"))
    return raiz


def imprimir_sidebar(nodo, nivel=0):
    """Pinta el menú lateral con sangría según el nivel (esto es un recorrido DFS)."""
    icono = "📁" if nodo.children else "📄"
    print("│ " + "    " * nivel + f"{icono} {nodo.titulo:<20} {nodo.link:<32} <{nodo.componente} />")
    for hijo in nodo.children:
        imprimir_sidebar(hijo, nivel + 1)


def dfs(nodo):
    """Depth-First Search: baja lo más profundo posible por cada rama."""
    resultado = [nodo.titulo]
    for hijo in nodo.children:
        resultado.extend(dfs(hijo))
    return resultado


def bfs(raiz):
    """Breadth-First Search: nivel por nivel, de izquierda a derecha."""
    resultado = []
    cola = deque([raiz])
    while cola:
        actual = cola.popleft()
        resultado.append(actual.titulo)
        cola.extend(actual.children)
    return resultado


def buscar(nodo, titulo):
    if nodo.titulo.lower() == titulo.lower():
        return nodo
    for hijo in nodo.children:
        encontrado = buscar(hijo, titulo)
        if encontrado:
            return encontrado
    return None


if __name__ == "__main__":
    menu = construir_menu()
    print("┌" + "─" * 80)
    print("│ SIDEBAR")
    print("├" + "─" * 80)
    imprimir_sidebar(menu)
    print("└" + "─" * 80)

    print("\nDFS:", " → ".join(dfs(menu)))
    print("BFS:", " → ".join(bfs(menu)))

    while True:
        texto = input("\nBusca un menú por título para 'navegar' (o 'salir'): ").strip()
        if texto.lower() == "salir":
            break
        item = buscar(menu, texto)
        if item:
            print(f"Navegando a {item.link} → renderiza el componente <{item.componente} />")
            if item.children:
                print("Submenús:", ", ".join(h.titulo for h in item.children))
        else:
            print("No existe ese menú")
