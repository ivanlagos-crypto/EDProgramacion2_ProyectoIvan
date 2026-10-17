"""
CHALLENGE 03 - Listas enlazadas
1. Lista enlazada SIMPLE para reproducir canciones en orden (datos de prueba).
2. Lista DOBLEMENTE enlazada para navegar atrás/adelante entre páginas visitadas.
Se navega con un menú de "botones" (opciones) en la consola.
"""


# ------------------------------------------------------------
# LISTA ENLAZADA SIMPLE
# ------------------------------------------------------------
class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def append(self, valor):
        """Agrega al final."""
        nuevo = Nodo(valor)
        if self.head is None:
            self.head = nuevo
            self.tail = nuevo
        else:
            self.tail.next = nuevo
            self.tail = nuevo
        self.length += 1

    def peek(self, indice):
        """Devuelve el valor en una posición (0 = primero)."""
        if indice < 0 or indice >= self.length:
            return None
        actual = self.head
        for _ in range(indice):
            actual = actual.next
        return actual.valor

    def size(self):
        return self.length

    def remove(self, indice):
        """Elimina el nodo en esa posición y une el anterior con el siguiente."""
        if indice < 0 or indice >= self.length:
            return None
        if indice == 0:
            eliminado = self.head
            self.head = eliminado.next
            if self.head is None:
                self.tail = None
        else:
            anterior = self.head
            for _ in range(indice - 1):
                anterior = anterior.next
            eliminado = anterior.next
            anterior.next = eliminado.next
            if eliminado is self.tail:
                self.tail = anterior
        self.length -= 1
        return eliminado.valor

    def print(self):
        actual = self.head
        partes = []
        while actual is not None:
            partes.append(str(actual.valor))
            actual = actual.next
        print(" -> ".join(partes) + " -> None")


# ------------------------------------------------------------
# LISTA DOBLEMENTE ENLAZADA
# ------------------------------------------------------------
class NodoDoble:
    def __init__(self, valor):
        self.valor = valor
        self.next = None
        self.prev = None     # la novedad: también apunta al anterior


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def append(self, valor):
        nuevo = NodoDoble(valor)
        if self.head is None:
            self.head = nuevo
            self.tail = nuevo
        else:
            nuevo.prev = self.tail
            self.tail.next = nuevo
            self.tail = nuevo
        self.length += 1
        return nuevo

    def remove_after(self, nodo):
        """Borra todo lo que hay después de 'nodo' (como hace un navegador
        cuando vas atrás y luego visitas una página nueva)."""
        actual = nodo.next
        while actual is not None:
            self.length -= 1
            actual = actual.next
        nodo.next = None
        self.tail = nodo

    def print(self):
        actual = self.head
        partes = []
        while actual is not None:
            partes.append(str(actual.valor))
            actual = actual.next
        print("None <- " + " <-> ".join(partes) + " -> None")


# ------------------------------------------------------------
# REPRODUCTOR DE CANCIONES (lista simple)
# ------------------------------------------------------------
def reproductor():
    playlist = LinkedList()
    for cancion in ["Bohemian Rhapsody - Queen", "La Bicicleta - Shakira", "Hotel California - Eagles",
                    "Ojitos Lindos - Bad Bunny", "Thunderstruck - AC/DC"]:
        playlist.append(cancion)

    actual = playlist.head
    while True:
        print("\n🎵 Sonando:", actual.valor if actual else "(fin de la lista)")
        print("[1] Siguiente  [2] Agregar canción  [3] Eliminar canción  [4] Ver lista  [0] Volver")
        op = input("> ").strip()
        if op == "1":
            actual = actual.next if actual else playlist.head
            if actual is None:
                print("Se acabó la lista. Vuelve a dar siguiente para empezar de nuevo.")
        elif op == "2":
            playlist.append(input("Nombre de la canción: "))
            if actual is None:
                actual = playlist.tail
        elif op == "3":
            playlist.print()
            try:
                pos = int(input("Posición a eliminar (empieza en 1): ")) - 1
            except ValueError:
                continue
            if actual is not None and playlist.peek(pos) == actual.valor:
                actual = actual.next
            print("Eliminada:", playlist.remove(pos))
        elif op == "4":
            print(f"Total: {playlist.size()} canciones")
            playlist.print()
        elif op == "0":
            break


# ------------------------------------------------------------
# NAVEGADOR (lista doble)
# ------------------------------------------------------------
def navegador():
    historial = DoublyLinkedList()
    actual = None
    for pagina in ["google.com", "uao.edu.co", "github.com", "stackoverflow.com"]:
        actual = historial.append(pagina)

    while True:
        print("\n🌐 Página actual:", actual.valor)
        print("[1] ◀ Atrás  [2] Adelante ▶  [3] Visitar página nueva  [4] Ver historial  [0] Volver")
        op = input("> ").strip()
        if op == "1":
            if actual.prev:
                actual = actual.prev
            else:
                print("No hay páginas anteriores")
        elif op == "2":
            if actual.next:
                actual = actual.next
            else:
                print("No hay páginas siguientes")
        elif op == "3":
            historial.remove_after(actual)
            actual = historial.append(input("URL: "))
        elif op == "4":
            historial.print()
        elif op == "0":
            break


if __name__ == "__main__":
    while True:
        print("\n=== CHALLENGE 03 ===")
        print("[1] Reproductor de canciones (lista simple)")
        print("[2] Navegador web (lista doble)")
        print("[0] Salir")
        opcion = input("> ").strip()
        if opcion == "1":
            reproductor()
        elif opcion == "2":
            navegador()
        elif opcion == "0":
            break
