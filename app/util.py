from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from app.models import Graph, Vertex, Edge
from app.schemas import GraphCreate, GraphCreateResponse, GraphReadResponse
from typing import List, Dict, Any
from collections import defaultdict
#import logging

#logger = logging.getLogger("uvicorn.error")
#logger.setLevel(logging.DEBUG)

async def create_graph(db: AsyncSession, graph_data: GraphCreate):
    #check for cycles before saving
    if __detect_cycle(graph_data.nodes, [(edge.source, edge.target) for edge in graph_data.edges]):
        raise ValueError("Cycle detected in graph")

    #create new graph
    db_graph = Graph()
    db.add(db_graph)
    await db.flush()


    node_name_to_id = {}
    for node in graph_data.nodes:
        db_vertex = Vertex(name=node.name, graph_id=db_graph.id)
        db.add(db_vertex)
        await db.flush()
        node_name_to_id[node.name] = db_vertex.id


    #validate unique edges
    edge_set = set()
    for edge in graph_data.edges:
        if (edge.source, edge.target) in edge_set:
            raise ValueError("Duplicate edge detected")
        edge_set.add((edge.source, edge.target))

        source_id = node_name_to_id.get(edge.source)
        target_id = node_name_to_id.get(edge.target)
        if not source_id or not target_id:
            raise ValueError("Edge references non-existent node")

        db_edge = Edge(
            graph_id=db_graph.id,
            source_vertex_id=source_id,
            target_vertex_id=target_id
        )
        db.add(db_edge)
    
    await db.commit()
    return GraphCreateResponse(id=db_graph.id)

async def get_graph(db: AsyncSession, graph_id: int):
    query = (
        select(Graph)
        .where(Graph.id == graph_id)
        .options(
            joinedload(Graph.vertices),
            joinedload(Graph.edges)
        )
    )
    result = await db.execute(query)
    graph = result.unique().scalars().first()
    
    if not graph:
        raise ValueError(f"Graph with ID {graph_id} not found")
    
    nodes = [{"name": vertex.name} for vertex in graph.vertices]
    edges = [
        {"source": edge.source_vertex.name, "target": edge.target_vertex.name}
        for edge in graph.edges
    ]
    
    return {"id": graph.id, "nodes": nodes, "edges": edges}

async def get_graph_data(db: AsyncSession, graph_id: int):
    result = await db.execute(
        select(Graph)
        .where(Graph.id == graph_id)
        .options(
            joinedload(Graph.vertices),
            joinedload(Graph.edges)
        )
    )
    graph = result.unique().scalars().first()
    
    if not graph:
        raise ValueError(f"Graph with ID {graph_id} not found")
    
    return {
        "id": graph.id,
        "nodes": [{"name": vertex.name} for vertex in graph.vertices],
        "edges": [
            {"source": edge.source_vertex.name, "target": edge.target_vertex.name}
            for edge in graph.edges
        ]
    }

def build_adjacency_list(graph_data: Dict[str, Any]) -> Dict[str, List[str]]:
    adj_list = {}
    for edge in graph_data["edges"]:
        src = edge["source"]
        tgt = edge["target"]
        adj_list.setdefault(src, []).append(tgt)
    return {"adjacency_list": adj_list}

def build_reverse_adjacency_list(graph_data: Dict[str, Any]) -> Dict[str, List[str]]:
    reversed_adj = {}
    for edge in graph_data["edges"]:
        src = edge["source"]
        tgt = edge["target"]
        reversed_adj.setdefault(tgt, []).append(src)
    return {"adjacency_list": reversed_adj}

async def delete_node(db: AsyncSession, graph_id: int, node_name: str):
    result = await db.execute(
        select(Graph)
        .where(Graph.id == graph_id)
        .options(joinedload(Graph.vertices))
    )
    graph = result.scalars().first()
    
    if not graph:
        raise ValueError(f"Graph with ID {graph_id} not found")
    
    node = None
    for vertex in graph.vertices:
        if vertex.name == node_name:
            node = vertex
            break
    
    if not node:
        raise ValueError(f"Node '{node_name}' not found in graph {graph_id}")
    
    await db.delete(node)
    await db.commit()


def __detect_cycle(nodes, edges):
    adj = defaultdict(list)
    node_names = [node.name for node in nodes]
    for src, tgt in edges:
        adj[src].append(tgt)
    
    visited = set()
    recursion_stack = set()

    def dfs(node):
        if node in recursion_stack:
            return True
        if node in visited:
            return False
        
        visited.add(node)
        recursion_stack.add(node)
        
        for neighbor in adj.get(node, []):
            if dfs(neighbor):
                return True
        
        recursion_stack.remove(node)
        return False

    for node in node_names:
        if node not in visited:
            if dfs(node):
                return True
    return False

