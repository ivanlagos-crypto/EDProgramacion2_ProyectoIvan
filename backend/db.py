"""
Base de datos SQLite (viene incluida en Python, no hay que instalar nada).

Las estructuras de datos viven en memoria mientras el servidor corre.
Cada cambio también se guarda (transacción) en la base de datos, y al
arrancar el servidor las estructuras se reconstruyen desde aquí.
Así la información NO se pierde al cerrar el programa.
"""
import sqlite3
from datetime import datetime
from pathlib import Path

RUTA_DB = Path(__file__).parent / "soc.db"


def conectar():
    conexion = sqlite3.connect(RUTA_DB)
    conexion.row_factory = sqlite3.Row   # para leer filas como diccionarios
    return conexion


def ahora():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def crear_tablas():
    with conectar() as c:
        c.executescript(
            """
            CREATE TABLE IF NOT EXISTS equipos (
                nombre TEXT PRIMARY KEY,
                ip     TEXT,
                tipo   TEXT
            );
            CREATE TABLE IF NOT EXISTS conexiones (
                a TEXT NOT NULL,
                b TEXT NOT NULL,
                PRIMARY KEY (a, b),
                FOREIGN KEY (a) REFERENCES equipos(nombre),
                FOREIGN KEY (b) REFERENCES equipos(nombre)
            );
            CREATE TABLE IF NOT EXISTS tickets (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                solicitante TEXT NOT NULL,
                descripcion TEXT NOT NULL,
                creado      TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS alertas (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                descripcion TEXT NOT NULL,
                severidad   INTEGER NOT NULL,
                equipo      TEXT,
                creada      TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS historial (
                id     INTEGER PRIMARY KEY AUTOINCREMENT,
                accion TEXT NOT NULL,
                fecha  TEXT NOT NULL
            );
            """
        )


def ejecutar(sql, parametros=()):
    """Ejecuta un INSERT/DELETE dentro de una transacción y devuelve el id insertado."""
    with conectar() as c:          # 'with' hace COMMIT si todo sale bien o ROLLBACK si falla
        cursor = c.execute(sql, parametros)
        return cursor.lastrowid


def consultar(sql, parametros=()):
    with conectar() as c:
        return [dict(fila) for fila in c.execute(sql, parametros).fetchall()]
