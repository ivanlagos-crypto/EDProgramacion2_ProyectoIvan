"""
CHALLENGE 10 - Grafo de amigos y ciudades
- Cada persona es un nodo (nombre y edad) y cada ciudad también (nombre).
- Cada persona está conectada a UNA ciudad (donde vive) y puede tener amigos.
- Se imprime la lista de personas que viven en una ciudad.
- Visualización: dibujo en consola + 'grafo_d3.json' con el formato de
  react-d3-graph ({"nodes": [{"id"}], "links": [{"source", "target"}]}).
"""
import json
from pathlib import Path


class Grafo:
    def __init__(self):
        self.nodos = {}        # id -> datos
        self.adyacencia = {}   # id -> lista de (vecino, tipo de relación)

    def add_node(self, id_, **datos):
        self.nodos[id_] = datos
        self.adyacencia.setdefault(id_, [])

    def add_edge(self, a, b, tipo):
        self.adyacencia[a].append((b, tipo))
        self.adyacencia[b].append((a, tipo))

    def buscar_nodo(self, id_):
        return self.nodos.get(id_)

    def vecinos(self, id_, tipo=None):
        return [v for v, t in self.adyacencia.get(id_, []) if tipo is None or t == tipo]

    def to_d3(self):
        nodes = [{"id": i, "color": "orange" if d["tipo"] == "ciudad" else "lightblue"} for i, d in self.nodos.items()]
        vistos, links = set(), []
        for a, lista in self.adyacencia.items():
            for b, t in lista:
                clave = tuple(sorted((a, b)))
                if clave not in vistos:
                    vistos.add(clave)
                    links.append({"source": a, "target": b, "label": t})
        return {"nodes": nodes, "links": links}


class RedSocial:
    def __init__(self):
        self.grafo = Grafo()

    def agregar_ciudad(self, nombre):
        self.grafo.add_node(nombre, tipo="ciudad")

    def agregar_persona(self, nombre, edad, ciudad):
        if self.grafo.buscar_nodo(ciudad) is None:
            self.agregar_ciudad(ciudad)
        self.grafo.add_node(nombre, tipo="persona", edad=edad)
        self.grafo.add_edge(nombre, ciudad, "vive_en")

    def hacer_amigos(self, a, b):
        self.grafo.add_edge(a, b, "amigo")

    def personas_en(self, ciudad):
        return [(p, self.grafo.nodos[p]["edad"]) for p in self.grafo.vecinos(ciudad, "vive_en")]

    def amigos_de(self, persona):
        return self.grafo.vecinos(persona, "amigo")

    def imprimir(self):
        print("\n🗺️  GRAFO (ciudades y sus habitantes)")
        for id_, datos in self.grafo.nodos.items():
            if datos["tipo"] == "ciudad":
                print(f"  [{id_}]")
                for p, edad in self.personas_en(id_):
                    amigos = ", ".join(self.amigos_de(p)) or "sin amigos"
                    print(f"     ├── {p} ({edad} años)  ~ amigos: {amigos}")


if __name__ == "__main__":
    red = RedSocial()
    for ciudad in ["Cali", "Bogotá", "Medellín"]:
        red.agregar_ciudad(ciudad)
    for nombre, edad, ciudad in [
        ("Daniel", 25, "Cali"), ("Laura", 23, "Cali"), ("Andrés", 30, "Bogotá"),
        ("Camila", 27, "Medellín"), ("Juan", 22, "Cali"), ("Valentina", 29, "Bogotá"),
    ]:
        red.agregar_persona(nombre, edad, ciudad)
    for a, b in [("Daniel", "Laura"), ("Daniel", "Andrés"), ("Laura", "Camila"), ("Juan", "Valentina"), ("Andrés", "Valentina")]:
        red.hacer_amigos(a, b)

    red.imprimir()

    salida = Path(__file__).parent / "grafo_d3.json"
    salida.write_text(json.dumps(red.grafo.to_d3(), indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nEstructura para react-d3-graph guardada en {salida.name}")

    while True:
        print("\n[1] Personas que viven en una ciudad  [2] Agregar persona  [3] Hacer amigos  [4] Ver grafo  [0] Salir")
        op = input("> ").strip()
        if op == "1":
            ciudad = input("Ciudad: ").strip()
            if red.grafo.buscar_nodo(ciudad) is None:
                print("Esa ciudad no está en el grafo")
                continue
            personas = red.personas_en(ciudad)
            print(f"En {ciudad} viven {len(personas)} personas:")
            for p, edad in personas:
                print(f"  - {p} ({edad} años)")
        elif op == "2":
            nombre = input("Nombre: ").strip()
            try:
                edad = int(input("Edad: "))
            except ValueError:
                print("Edad inválida")
                continue
            red.agregar_persona(nombre, edad, input("Ciudad donde vive: ").strip())
            print("✅ Persona agregada")
        elif op == "3":
            a, b = input("Persona 1: ").strip(), input("Persona 2: ").strip()
            if red.grafo.buscar_nodo(a) and red.grafo.buscar_nodo(b):
                red.hacer_amigos(a, b)
                print("✅ Ahora son amigos")
            else:
                print("Alguna de las personas no existe")
        elif op == "4":
            red.imprimir()
        elif op == "0":
            break
