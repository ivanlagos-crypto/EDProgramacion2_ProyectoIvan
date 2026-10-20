# 🛡️ Mini SOC — Proyecto Final Estructuras de Datos II

Proyecto sencillo de monitoreo de red (mini SOC) con **5 estructuras de datos** hechas en Python, una **API con FastAPI** y los datos guardados en **SQLite**.

## 👤 Integrante
- **Ivan Lagos** — trabajo individual

## 🧱 Estructuras implementadas

| Grupo de la rúbrica | Estructura | Uso en el sistema | Archivo |
|---|---|---|---|
| Listas, Pilas o Colas | **Pila** (LIFO) | Historial de actividad del analista | `backend/estructuras/pila.py` |
| Listas, Pilas o Colas | **Cola** (FIFO) | Tickets de soporte en orden de llegada | `backend/estructuras/cola.py` |
| Árboles, Tries o Heaps | **Max-Heap** | Alertas de seguridad por severidad | `backend/estructuras/heap.py` |
| Árboles, Tries o Heaps | **Trie** | Buscador de equipos con autocompletado | `backend/estructuras/trie.py` |
| Grafos | **Grafo** no dirigido | Red de equipos (vecinos, ruta, BFS/DFS) | `backend/estructuras/grafo.py` |

## 🛠️ Tecnologías
- Python 3.12+
- FastAPI + Uvicorn (backend / API)
- SQLite (base de datos, incluida en Python)
- Render (despliegue en servidor público)

## ▶️ Cómo ejecutarlo
```bash
python -m pip install -r requirements.txt
python -m uvicorn backend.main:app --reload
```
Luego abrir http://127.0.0.1:8000/docs para probar los endpoints.

La primera vez se crea `backend/soc.db` con datos de prueba.

## 📂 Estructura del repositorio
```
backend/
  estructuras/   Pila, Cola, MaxHeap, Trie, Grafo (implementación propia)
  db.py          Conexión y tablas SQLite
  main.py        Endpoints de la API
ejercicios/      Challenges 03, 04, 05, 08, 09, 10 y 11
docs/
  DOCUMENTO_FINAL.md
```

## 📝 Ejercicios (challenges)
Se ejecutan desde la raíz del proyecto, por ejemplo: `python ejercicios/challenge04_pila_libros.py`

| Challenge | Tema | Archivo |
|---|---|---|
| 03 | Lista enlazada (canciones) y doble (navegador) | `ejercicios/challenge03_listas.py` |
| 04 | Pila de libros | `ejercicios/challenge04_pila_libros.py` |
| 05 | Cola del cajero | `ejercicios/challenge05_cola_cajero.py` |
| 08 | Árbol binario (recorridos y búsqueda) | `ejercicios/challenge08_arbol_binario.py` |
| 09 | Árbol N-ario (menú lateral) | `ejercicios/challenge09_arbol_nario_menu.py` |
| 10 | Grafo de personas y ciudades | `ejercicios/challenge10_grafo_personas_ciudades.py` |
| 11 | Trie + Heap (Top-K productos) | `ejercicios/challenge11_trie_heap_topk.py` |

## 🌿 Ramas
Cada estructura se desarrolló en su propia rama (`feature/pila`, `feature/cola`, `feature/heap`, `feature/trie`, `feature/grafo`, `feature/backend`, `feature/ejercicios`, `feature/documentacion`) y todas se mezclaron en `main`.

## 🌐 Despliegue
Publicado en **Render** (plan gratuito) con el archivo `render.yaml`:
- API: https://ed2-proyecto-ivan.onrender.com
- Documentación interactiva (para probar los endpoints): https://ed2-proyecto-ivan.onrender.com/docs

> En el plan gratuito el servidor se "duerme" si nadie lo usa; la primera visita puede tardar unos 50 segundos en cargar.
