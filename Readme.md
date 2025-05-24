# GMAN: Graph Management API for Directed Acyclic Graphs (DAG)

**GMAN** is internship project. A FastAPI-based service for managing **DAGs** using PostgreSQL as the DB backend.<br>
It provides endpoints for creating, reading, and modifying graphs with built-in validation rules:
- Node names must be **Latin letters only** (no numbers/symbols).
- **No cycles** allowed in graphs.
- **Unique node names** per graph.
- **Cascading deletion** of edges when nodes are removed.

---

## Key Features
- **Cycle Detection**: Uses DFS to prevent cyclic graphs during creation.
- **Adjacency List**: Generates standard and transposed adjacency lists for graph analysis.
- **Node Deletion**: Automatically removes related edges via cascade rules.
- **Validation**: Ensures data integrity with Pydantic models and PostgreSQL constraints.
- **Test Coverage**: Postman

---

##  Requirements
- Python 3.11+
- PostgreSQL 13+
- FastAPI, SQLAlchemy, Pydantic, asyncpg
- Docker (for local development)

---

##Quick Start

### 1. Clone the repository:
```bash
git clone https://github.com/dfwdfq/gman.git
cd gman
```

### 2. Create `.env` file:
```bash
chmod +x prepare.bash
./prepare.bash
```

### 3. Run with Docker:
```bash
docker-compose up --build
```
Note: It can fail for the first, because it need to create DB first.P.S. Docker witchcraft
### 4. Access Swagger UI:
```
http://localhost:8000/docs
```

---

##  API Endpoints

### **1. `POST /api/graph/` — Create Graph**
**Description**: Creates a new DAG with validation:
- Node names must be Latin letters only.
- No cycles allowed.
- No duplicate edges between nodes.

**Example Request Body**:
```json
{
  "nodes": [{"name": "A"}, {"name": "B"}],
  "edges": [{"source": "A", "target": "B"}]
}
```

**Response**:
```json
{"id": 1}  # Unique ID for the created graph
```

---

### **2. `GET /api/graph/{graph_id}` — Read Graph**
**Description**: Returns nodes and edges for a graph.

**Response**:
```json
{
  "id": 1,
  "nodes": [{"name": "A"}, {"name": "B"}],
  "edges": [{"source": "A", "target": "B"}]
}
```

---

### **3. `GET /api/graph/{graph_id}/adjacency_list` — Get Adjacency List**
**Description**: Returns graph in adjacency list format (outgoing edges).

**Response**:
```json
{
  "adjacency_list": {
    "A": ["B"],
    "B": []
  }
}
```

---

### **4. `GET /api/graph/{graph_id}/reverse_adjacency_list` — Get Reverse Adjacency List**
**Description**: Returns transposed graph (incoming edges).

**Response**:
```json
{
  "adjacency_list": {
    "A": [],
    "B": ["A"]
  }
}
```

---

### **5. `DELETE /api/graph/{graph_id}/node/{node_name}` — Delete Node**
**Description**: Removes a node and all connected edges via cascading deletion.

**Response**:
```json
{}  # No content (204 No Content)
```

---

### ** Postman Tests**
Import the generated Postman collection (`postman_collection.json`) to validate:
- **Cycle detection** (`400 Bad Request`).
- **Node deletion** (`204 No Content`).
- **Adjacency list generation** (`200 OK`).

The reason to prefer Postman over given requirements is basical inability to<br>
waste time configuring Docker once again to create envromnent to test.<br>
Also It is dedicated tool for distinct networking tasks, including<br>
endpoints test. <br><br>Anyway, it's just curl under the hood.<br>
