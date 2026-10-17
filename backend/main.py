"""
BACKEND - Mini SOC (Centro de Operaciones de Seguridad)

API hecha con FastAPI. Cada estructura de datos tiene sus propios endpoints:
    /pila/...    Historial de actividad (Pila - LIFO)
    /cola/...    Tickets de soporte (Cola - FIFO)
    /heap/...    Alertas por severidad (Max-Heap)
    /trie/...    Buscador de equipos con autocompletado (Trie)
    /grafo/...   Topología de la red (Grafo)

Cómo correrlo (desde la carpeta del proyecto):
    python -m uvicorn backend.main:app --reload
Luego abrir en el navegador:
    http://127.0.0.1:8000/docs   -> aquí se prueban todos los endpoints
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from . import db
from .estructuras import Cola, Grafo, MaxHeap, Pila, Trie

app = FastAPI(title="Mini SOC - Estructuras de Datos II", version="1.0")

# ---------------------------------------------------------------
# Estructuras en memoria
# ---------------------------------------------------------------
historial = Pila()
tickets = Cola()
alertas = MaxHeap(prioridad=lambda a: (a["severidad"], -a["id"]))  # más severa primero; si empatan, la más antigua
buscador = Trie()
red = Grafo()


def registrar_accion(texto):
    """Toda acción queda en el historial (Pila) y en la base de datos."""
    fecha = db.ahora()
    id_ = db.ejecutar("INSERT INTO historial (accion, fecha) VALUES (?, ?)", (texto, fecha))
    historial.push({"id": id_, "accion": texto, "fecha": fecha})


def cargar_desde_db():
    """Reconstruye todas las estructuras con lo guardado en SQLite."""
    for e in db.consultar("SELECT * FROM equipos"):
        red.add_node(e["nombre"], {"ip": e["ip"], "tipo": e["tipo"]})
        buscador.insert(e["nombre"])
    for c in db.consultar("SELECT * FROM conexiones"):
        red.add_edge(c["a"], c["b"])
    for t in db.consultar("SELECT * FROM tickets ORDER BY id"):
        tickets.enqueue(t)
    alertas.heapify(db.consultar("SELECT * FROM alertas"))
    for h in db.consultar("SELECT * FROM historial ORDER BY id"):
        historial.push(h)


def datos_de_ejemplo():
    """Si la base está vacía, se llena con datos de prueba (mock data)."""
    if db.consultar("SELECT nombre FROM equipos LIMIT 1"):
        return
    equipos = [
        ("router-core", "10.0.0.1", "router"),
        ("fw-perimetral", "10.0.0.2", "firewall"),
        ("switch-piso1", "10.0.1.1", "switch"),
        ("switch-piso2", "10.0.2.1", "switch"),
        ("srv-web-01", "10.0.1.10", "servidor"),
        ("srv-db-01", "10.0.1.11", "servidor"),
        ("pc-contabilidad", "10.0.2.20", "pc"),
        ("pc-gerencia", "10.0.2.21", "pc"),
        ("cam-entrada", "10.0.2.30", "camara"),
    ]
    for nombre, ip, tipo in equipos:
        crear_equipo(Equipo(nombre=nombre, ip=ip, tipo=tipo))
    for a, b in [
        ("fw-perimetral", "router-core"),
        ("router-core", "switch-piso1"),
        ("router-core", "switch-piso2"),
        ("switch-piso1", "srv-web-01"),
        ("switch-piso1", "srv-db-01"),
        ("switch-piso2", "pc-contabilidad"),
        ("switch-piso2", "pc-gerencia"),
        ("switch-piso2", "cam-entrada"),
    ]:
        conectar_equipos(Conexion(a=a, b=b))
    crear_ticket(Ticket(solicitante="Ana Gómez", descripcion="No imprime la impresora del piso 2"))
    crear_ticket(Ticket(solicitante="Luis Pérez", descripcion="Olvidé mi contraseña del correo"))
    crear_ticket(Ticket(solicitante="Marta Ruiz", descripcion="La cámara de la entrada no graba"))
    crear_alerta(Alerta(descripcion="Múltiples logins fallidos (fuerza bruta SSH)", severidad=9, equipo="srv-web-01"))
    crear_alerta(Alerta(descripcion="Puerto 3389 (RDP) expuesto a internet", severidad=7, equipo="fw-perimetral"))
    crear_alerta(Alerta(descripcion="Antivirus desactualizado", severidad=4, equipo="pc-contabilidad"))
    crear_alerta(Alerta(descripcion="Posible ransomware: cifrado masivo de archivos", severidad=10, equipo="srv-db-01"))
    crear_alerta(Alerta(descripcion="Certificado SSL próximo a vencer", severidad=3, equipo="srv-web-01"))


@app.on_event("startup")
def iniciar():
    db.crear_tablas()
    cargar_desde_db()
    datos_de_ejemplo()


# ---------------------------------------------------------------
# Modelos de entrada (lo que el usuario envía)
# ---------------------------------------------------------------
class Equipo(BaseModel):
    nombre: str = Field(min_length=1, examples=["srv-mail-01"])
    ip: str = Field(default="", examples=["10.0.1.12"])
    tipo: str = Field(default="servidor", examples=["servidor"])


class Conexion(BaseModel):
    a: str = Field(examples=["switch-piso1"])
    b: str = Field(examples=["srv-mail-01"])


class Ticket(BaseModel):
    solicitante: str = Field(min_length=1, examples=["Carlos Díaz"])
    descripcion: str = Field(min_length=1, examples=["El computador no enciende"])


class Alerta(BaseModel):
    descripcion: str = Field(min_length=1, examples=["Escaneo de puertos detectado"])
    severidad: int = Field(ge=1, le=10, examples=[8])
    equipo: str | None = Field(default=None, examples=["router-core"])


# ---------------------------------------------------------------
# INICIO
# ---------------------------------------------------------------
@app.get("/")
def inicio():
    return {"mensaje": "API Mini SOC funcionando. Ve a /docs para probarla."}


# ---------------------------------------------------------------
# PILA - Historial de actividad
# ---------------------------------------------------------------
@app.get("/pila", tags=["Pila - Historial"])
def ver_historial():
    return {"tamano": historial.size(), "elementos": historial.to_list()}


@app.get("/pila/peek", tags=["Pila - Historial"])
def ultima_accion():
    return historial.peek()


@app.delete("/pila/pop", tags=["Pila - Historial"])
def descartar_ultima_accion():
    accion = historial.pop()
    if accion is None:
        raise HTTPException(404, "El historial está vacío")
    db.ejecutar("DELETE FROM historial WHERE id = ?", (accion["id"],))
    return {"descartada": accion}


# ---------------------------------------------------------------
# COLA - Tickets de soporte
# ---------------------------------------------------------------
@app.get("/cola", tags=["Cola - Tickets"])
def ver_tickets():
    return {"tamano": tickets.size(), "elementos": tickets.to_list()}


@app.post("/cola/enqueue", tags=["Cola - Tickets"])
def crear_ticket(t: Ticket):
    creado = db.ahora()
    id_ = db.ejecutar(
        "INSERT INTO tickets (solicitante, descripcion, creado) VALUES (?, ?, ?)",
        (t.solicitante, t.descripcion, creado),
    )
    ticket = {"id": id_, "solicitante": t.solicitante, "descripcion": t.descripcion, "creado": creado}
    tickets.enqueue(ticket)
    registrar_accion(f"Ticket #{id_} creado por {t.solicitante}")
    return ticket


@app.get("/cola/peek", tags=["Cola - Tickets"])
def siguiente_ticket():
    return tickets.peek()


@app.delete("/cola/dequeue", tags=["Cola - Tickets"])
def atender_ticket():
    ticket = tickets.dequeue()
    if ticket is None:
        raise HTTPException(404, "No hay tickets pendientes")
    db.ejecutar("DELETE FROM tickets WHERE id = ?", (ticket["id"],))
    registrar_accion(f"Ticket #{ticket['id']} atendido")
    return {"atendido": ticket}


# ---------------------------------------------------------------
# HEAP - Alertas por severidad
# ---------------------------------------------------------------
@app.get("/heap", tags=["Heap - Alertas"])
def ver_alertas():
    """Todas las alertas ordenadas de la más crítica a la menos crítica."""
    return {"tamano": alertas.size(), "elementos": alertas.top_k(alertas.size()), "arreglo_interno": alertas.to_array()}


@app.post("/heap/push", tags=["Heap - Alertas"])
def crear_alerta(a: Alerta):
    if a.equipo and not red.has_node(a.equipo):
        raise HTTPException(400, f"El equipo '{a.equipo}' no existe en la red")
    creada = db.ahora()
    id_ = db.ejecutar(
        "INSERT INTO alertas (descripcion, severidad, equipo, creada) VALUES (?, ?, ?, ?)",
        (a.descripcion, a.severidad, a.equipo, creada),
    )
    alerta = {"id": id_, "descripcion": a.descripcion, "severidad": a.severidad, "equipo": a.equipo, "creada": creada}
    alertas.push(alerta)
    registrar_accion(f"Alerta #{id_} registrada (severidad {a.severidad})")
    return alerta


@app.get("/heap/peek", tags=["Heap - Alertas"])
def alerta_mas_critica():
    return alertas.peek()


@app.get("/heap/top/{k}", tags=["Heap - Alertas"])
def top_alertas(k: int):
    return alertas.top_k(k)


@app.delete("/heap/pop", tags=["Heap - Alertas"])
def atender_alerta():
    alerta = alertas.pop()
    if alerta is None:
        raise HTTPException(404, "No hay alertas pendientes")
    db.ejecutar("DELETE FROM alertas WHERE id = ?", (alerta["id"],))
    registrar_accion(f"Alerta #{alerta['id']} atendida")
    return {"atendida": alerta}


# ---------------------------------------------------------------
# TRIE - Buscador de equipos
# ---------------------------------------------------------------
@app.get("/trie/autocompletar", tags=["Trie - Buscador"])
def autocompletar(prefijo: str = ""):
    return {"prefijo": prefijo, "sugerencias": buscador.autocompletar(prefijo)}


@app.get("/trie/existe/{nombre}", tags=["Trie - Buscador"])
def existe_equipo(nombre: str):
    return {"nombre": nombre, "existe": buscador.search(nombre)}


# ---------------------------------------------------------------
# GRAFO - Red de equipos
# ---------------------------------------------------------------
@app.get("/grafo", tags=["Grafo - Red"])
def ver_red():
    return red.to_dict()


@app.post("/grafo/equipos", tags=["Grafo - Red"])
def crear_equipo(e: Equipo):
    nombre = e.nombre.strip().lower()
    if red.has_node(nombre):
        raise HTTPException(400, "Ese equipo ya existe")
    db.ejecutar("INSERT INTO equipos (nombre, ip, tipo) VALUES (?, ?, ?)", (nombre, e.ip, e.tipo))
    red.add_node(nombre, {"ip": e.ip, "tipo": e.tipo})
    buscador.insert(nombre)          # el equipo también queda en el buscador (Trie)
    registrar_accion(f"Equipo {nombre} registrado")
    return {"nombre": nombre, "ip": e.ip, "tipo": e.tipo}


@app.post("/grafo/conexiones", tags=["Grafo - Red"])
def conectar_equipos(c: Conexion):
    a, b = c.a.strip().lower(), c.b.strip().lower()
    try:
        red.add_edge(a, b)
    except ValueError as error:
        raise HTTPException(400, str(error))
    db.ejecutar("INSERT OR IGNORE INTO conexiones (a, b) VALUES (?, ?)", tuple(sorted((a, b))))
    registrar_accion(f"Conexión {a} <-> {b} creada")
    return {"a": a, "b": b}


@app.get("/grafo/vecinos/{nombre}", tags=["Grafo - Red"])
def vecinos(nombre: str):
    if not red.has_node(nombre):
        raise HTTPException(404, "Equipo no encontrado")
    return {"equipo": nombre, "vecinos": red.vecinos(nombre)}


@app.get("/grafo/bfs/{inicio}", tags=["Grafo - Red"])
def recorrido_bfs(inicio: str):
    return {"inicio": inicio, "orden": red.bfs(inicio)}


@app.get("/grafo/dfs/{inicio}", tags=["Grafo - Red"])
def recorrido_dfs(inicio: str):
    return {"inicio": inicio, "orden": red.dfs(inicio)}


@app.get("/grafo/ruta", tags=["Grafo - Red"])
def ruta(origen: str, destino: str):
    camino = red.ruta(origen, destino)
    return {"origen": origen, "destino": destino, "ruta": camino, "saltos": max(len(camino) - 1, 0)}
