from pydantic import BaseModel, model_validator
from typing import List, Dict, Any

class Node(BaseModel):
    name: str

class Edge(BaseModel):
    source: str
    target: str

class GraphCreate(BaseModel):
    nodes: List[Node]
    edges: List[Edge]

    @model_validator(mode='after')
    def validate_unique_nodes(self):
        names = [node.name for node in self.nodes]
        if len(names) != len(set(names)):
            raise ValueError("Duplicate node names in graph")
        return self

class GraphCreateResponse(BaseModel):
    id: int

class GraphReadResponse(BaseModel):
    id: int
    nodes: List[Node]
    edges: List[Edge]

class AdjacencyListResponse(BaseModel):
    adjacency_list: Dict[str, List[str]]

class ErrorResponse(BaseModel):
    message: str
