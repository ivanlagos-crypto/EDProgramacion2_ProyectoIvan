"""
CHALLENGE 04 - Pila de libros
Cada libro tiene: nombre, ISBN, autor y editorial.
Se llena con datos de prueba, hay un "formulario" para agregar libros
y se imprime la pila en pantalla (el de arriba primero).
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from backend.estructuras.pila import Pila  # noqa: E402  (reutilizamos la Pila del proyecto)


def mostrar(pila):
    print("\n📚 PILA DE LIBROS (arriba = último agregado)")
    if pila.is_empty():
        print("   (vacía)")
    for i, libro in enumerate(pila.to_list()):
        marca = "⬆ TOPE" if i == 0 else ""
        print(f"   | {libro['nombre']} — {libro['autor']} ({libro['editorial']}) ISBN {libro['isbn']} {marca}")
    print(f"   Total: {pila.size()} libros")


def main():
    libros = Pila()
    datos_prueba = [
        {"nombre": "Cien años de soledad", "isbn": "978-0307474728", "autor": "Gabriel García Márquez", "editorial": "Sudamericana"},
        {"nombre": "Clean Code", "isbn": "978-0132350884", "autor": "Robert C. Martin", "editorial": "Prentice Hall"},
        {"nombre": "Estructuras de datos en Python", "isbn": "978-1118290279", "autor": "Michael Goodrich", "editorial": "Wiley"},
        {"nombre": "El principito", "isbn": "978-0156012195", "autor": "Antoine de Saint-Exupéry", "editorial": "Reynal & Hitchcock"},
    ]
    for libro in datos_prueba:
        libros.push(libro)

    while True:
        mostrar(libros)
        print("\n[1] Agregar libro (push)  [2] Sacar libro de arriba (pop)  [3] Ver libro de arriba (peek)  [0] Salir")
        op = input("> ").strip()
        if op == "1":
            print("--- Formulario nuevo libro ---")
            libro = {
                "nombre": input("Nombre: "),
                "isbn": input("ISBN: "),
                "autor": input("Autor: "),
                "editorial": input("Editorial: "),
            }
            libros.push(libro)
            print("✅ Libro agregado encima de la pila")
        elif op == "2":
            libro = libros.pop()
            print("Sacado:", libro["nombre"] if libro else "la pila está vacía")
        elif op == "3":
            libro = libros.peek()
            print("Arriba está:", libro["nombre"] if libro else "nada")
        elif op == "0":
            break


if __name__ == "__main__":
    main()
