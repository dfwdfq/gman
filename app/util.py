from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Graph, Vertex, Edge
from app.schemas import GraphCreate, GraphCreateResponse, GraphReadResponse
from typing import List, Dict
from collections import defaultdict
import logging

logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.DEBUG)

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
