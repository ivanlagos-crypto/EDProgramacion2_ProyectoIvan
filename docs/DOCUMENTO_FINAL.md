# Documento Final — Mini SOC
**Asignatura:** Estructuras de Datos II
**Estudiante:** Ivan Lagos (trabajo individual)
**Fecha:** 16 de octubre de 2026

---

## 1. Descripción y alcance del sistema

**Mini SOC** es una plataforma para el monitoreo básico de la seguridad de una red pequeña, inspirada en un *Security Operations Center*. Permite:

1. **Registrar equipos de la red** (routers, switches, servidores, PCs, cámaras) y las conexiones entre ellos.
2. **Buscar equipos** escribiendo solo el inicio de su nombre (autocompletado).
3. **Registrar alertas de seguridad** con una severidad del 1 al 10 y atenderlas siempre empezando por la más crítica.
4. **Gestionar tickets de soporte** que se atienden en orden de llegada.
5. **Consultar la red**: vecinos de un equipo, la ruta más corta entre dos equipos y recorridos BFS/DFS.
6. **Ver el historial de actividad**, con la acción más reciente primero.

Toda la información se guarda en una base de datos SQLite, así que no se pierde al cerrar el programa.

### Fuera del alcance
- Autenticación de usuarios y roles.
- Monitoreo automático real de la red (los datos se registran manualmente o vienen de datos de prueba).
- Interfaz gráfica propia: el sistema se usa desde la documentación interactiva de FastAPI (`/docs`).
- Despliegue en un servidor público: el sistema se ejecuta en local.

---

## 2. Tecnologías utilizadas

| Capa | Tecnología | Motivo |
|---|---|---|
| Lenguaje | Python 3 | Lenguaje aceptado por el docente y fácil de leer. |
| Backend / API | FastAPI + Uvicorn | Permite exponer cada estructura como endpoints REST y genera documentación interactiva automática (`/docs`). |
| Base de datos | SQLite | Viene incluida en Python, no requiere servidor y guarda los datos en un archivo. |
| Control de versiones | Git + GitHub | Una rama por estructura, mezcladas en `main`. |

### Arquitectura

```
Navegador (/docs de FastAPI)
        │  peticiones HTTP (JSON)
        ▼
FastAPI (backend/main.py) ──► Estructuras en memoria (Pila, Cola, Heap, Trie, Grafo)
        │
        ▼
SQLite (backend/soc.db)  ◄── cada cambio se guarda en una transacción
```

Al iniciar, el servidor lee la base de datos y **reconstruye** todas las estructuras. Cada operación (crear, atender, conectar…) modifica la estructura en memoria y **en la misma petición** guarda el cambio en SQLite (`INSERT` o `DELETE` dentro de una transacción con `COMMIT` o `ROLLBACK`).

---

## 3. Estructuras de datos y por qué se usaron

### 3.1 Pila (Stack) — Historial de actividad
- **Principio:** LIFO (el último en entrar es el primero en salir).
- **Implementación:** nodos enlazados; el `tope` apunta al último elemento y cada nodo apunta al de abajo.
- **Métodos:** `push`, `pop`, `peek`, `is_empty`, `size`, `to_list`, `print`.
- **¿Por qué?** En un historial lo más útil es ver primero lo **más reciente**, igual que el historial de un navegador. La pila deja la última acción siempre arriba, y `push`/`pop` son O(1).

### 3.2 Cola (Queue) — Tickets de soporte
- **Principio:** FIFO (el primero en entrar es el primero en salir).
- **Implementación:** nodos enlazados con `frente` y `final`.
- **Métodos:** `enqueue`, `dequeue`, `peek`, `is_empty`, `size`, `to_list`, `print`.
- **¿Por qué?** Los tickets de soporte deben atenderse **en orden de llegada**, para que sea justo: nadie que llegó después pasa adelante. Agregar al final y sacar del frente son O(1).
- **Uso extra:** la misma cola se reutiliza en el grafo para los recorridos **BFS**.

### 3.3 Max-Heap — Alertas por severidad
- **Propiedades:** árbol binario completo guardado en un arreglo; cada padre tiene **mayor** prioridad que sus hijos.
- **Fórmulas:** hijo izquierdo `2i + 1`, hijo derecho `2i + 2`, padre `(i − 1) // 2`.
- **Métodos:** `push` (con *percolate up*), `pop` (con *percolate down*), `peek`, `heapify`, `top_k`, `swap`, `size`, `to_array`.
- **Prioridad:** se ordena por `(severidad, −id)`. Gana la de mayor severidad y, si empatan, la más antigua.
- **¿Por qué?** En seguridad **no** se atiende por orden de llegada sino por **gravedad**: un ransomware (10) va antes que un antivirus desactualizado (4). El heap entrega siempre la alerta más crítica en O(log n), sin tener que ordenar toda la lista.

### 3.4 Trie — Buscador de equipos
- **Concepto:** árbol de caracteres; la información está en el **camino** desde la raíz. La raíz es un nodo vacío.
- **Nodo:** diccionario de hijos `{letra: nodo}` y la bandera `fin_de_palabra`.
- **Métodos:** `insert`, `search`, `starts_with`, `autocompletar` (DFS desde el nodo del prefijo), `delete`.
- **¿Por qué?** Para **autocompletar** nombres de equipos (`srv` → `srv-db-01`, `srv-web-01`). El costo de buscar depende del largo del prefijo y no de la cantidad de equipos registrados.

### 3.5 Grafo — Topología de la red
- **Tipo:** no dirigido, porque un enlace de red conecta a los dos equipos en ambos sentidos.
- **Representación:** lista de adyacencia `{equipo: {vecinos}}` más un diccionario con los datos de cada nodo (IP y tipo).
- **Métodos:** `add_node`, `add_edge`, `remove_node`, `remove_edge`, `vecinos`, `bfs`, `dfs`, `ruta` (camino más corto con BFS).
- **¿Por qué?** Una red de computadores **es** un grafo: equipos conectados entre sí sin una jerarquía estricta (puede haber ciclos). Con el grafo se responden preguntas reales de un SOC:
  - ¿Por dónde viaja el tráfico entre dos equipos? → `ruta`

---

## 4. Endpoints principales (API)

| Estructura | Método | Ruta | Acción |
|---|---|---|---|
| Pila | GET | `/pila` | Ver historial |
| Pila | DELETE | `/pila/pop` | Descartar la última entrada |
| Cola | POST | `/cola/enqueue` | Crear ticket |
| Cola | DELETE | `/cola/dequeue` | Atender el siguiente ticket |
| Heap | POST | `/heap/push` | Registrar alerta |
| Heap | DELETE | `/heap/pop` | Atender la alerta más crítica |
| Heap | GET | `/heap/top/{k}` | Las k alertas más críticas |
| Trie | GET | `/trie/autocompletar?prefijo=` | Sugerencias de equipos |
| Grafo | POST | `/grafo/equipos` | Registrar equipo |
| Grafo | POST | `/grafo/conexiones` | Conectar dos equipos |
| Grafo | GET | `/grafo/ruta?origen=&destino=` | Ruta más corta |
| Grafo | GET | `/grafo/bfs/{inicio}` y `/grafo/dfs/{inicio}` | Recorridos |

La documentación completa e interactiva está en `http://127.0.0.1:8000/docs`.

---

## 5. Base de datos

Tablas: `equipos`, `conexiones`, `tickets`, `alertas` e `historial`. Cada operación de la API corresponde a una transacción:

- Crear un ticket → `INSERT INTO tickets` y `enqueue` en la cola.
- Atender un ticket → `DELETE FROM tickets` y `dequeue` en la cola.
- Atender una alerta → `DELETE FROM alertas` y `pop` en el heap.

---

## 6. Ejercicios del curso (challenges)

En la carpeta `ejercicios/` están los challenges 03, 04, 05, 08, 09, 10 y 11 en Python. Las visualizaciones que en clase se planteaban con React se resolvieron en consola. Además, los challenges 08 y 10 generan un archivo JSON con el formato que usan `react-d3-tree` y `react-d3-graph`.

---

## 7. Conclusiones
- Cada estructura se eligió según **cómo se necesita sacar la información**: por recencia (pila), por llegada (cola), por prioridad (heap), por prefijo (trie) y por relaciones (grafo).
- Las estructuras se reutilizan entre sí: el grafo usa la cola para BFS, y el heap sirve tanto para alertas como para el Top-K de productos (challenge 11).

## 8. Uso de herramientas
En el desarrollo de este proyecto se usó un asistente de IA (Claude) como apoyo para el aprendizaje de Python y para la generación y revisión del código.
