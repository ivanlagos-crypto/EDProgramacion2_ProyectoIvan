"""
CHALLENGE 05 - Cola de personas en un cajero (ATM)
Cada persona tiene: nombre, monto a retirar y una fecha de llegada aleatoria
asignada por el sistema. La cola se imprime según la fecha de llegada.

Para que la cola respete la fecha de llegada, cada persona nueva se ubica
en la posición que le corresponde (inserción ordenada por llegada).
"""
import random
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from backend.estructuras.cola import Cola  # noqa: E402


def fecha_aleatoria():
    """Fecha de llegada aleatoria dentro de la última hora."""
    return datetime.now() - timedelta(minutes=random.randint(0, 60), seconds=random.randint(0, 59))


def encolar_por_llegada(cola, persona):
    """Reconstruye la cola dejando a la persona en su lugar según la hora de llegada.
    Se usan solo operaciones de cola: dequeue y enqueue."""
    temporal = Cola()
    insertada = False
    while not cola.is_empty():
        actual = cola.dequeue()
        if not insertada and persona["llegada"] < actual["llegada"]:
            temporal.enqueue(persona)
            insertada = True
        temporal.enqueue(actual)
    if not insertada:
        temporal.enqueue(persona)
    while not temporal.is_empty():
        cola.enqueue(temporal.dequeue())


def mostrar(cola):
    print("\n🏧 COLA DEL CAJERO (primero en llegar = primero en ser atendido)")
    if cola.is_empty():
        print("   (nadie en la fila)")
    for i, p in enumerate(cola.to_list(), start=1):
        print(f"   {i}. {p['nombre']:<18} retira ${p['monto']:>10,.0f}   llegó {p['llegada'].strftime('%H:%M:%S')}")


def main():
    cajero = Cola()
    for nombre, monto in [("Ana", 200000), ("Carlos", 50000), ("Lucía", 1000000), ("Pedro", 300000), ("Sofía", 80000)]:
        encolar_por_llegada(cajero, {"nombre": nombre, "monto": monto, "llegada": fecha_aleatoria()})

    while True:
        mostrar(cajero)
        print("\n[1] Agregar persona (enqueue)  [2] Atender siguiente (dequeue)  [3] Ver siguiente (peek)  [0] Salir")
        op = input("> ").strip()
        if op == "1":
            print("--- Formulario nueva persona ---")
            nombre = input("Nombre: ")
            try:
                monto = float(input("Monto a retirar: "))
            except ValueError:
                print("Monto inválido")
                continue
            persona = {"nombre": nombre, "monto": monto, "llegada": fecha_aleatoria()}
            encolar_por_llegada(cajero, persona)
            print(f"✅ {nombre} llegó a las {persona['llegada'].strftime('%H:%M:%S')} (asignado por el sistema)")
        elif op == "2":
            p = cajero.dequeue()
            print("Atendido:", f"{p['nombre']} retiró ${p['monto']:,.0f}" if p else "no hay nadie")
        elif op == "3":
            p = cajero.peek()
            print("Sigue:", p["nombre"] if p else "nadie")
        elif op == "0":
            break


if __name__ == "__main__":
    main()
