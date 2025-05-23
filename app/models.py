from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Graph(Base):
    ''''
    'Base' table it has relations to Vertexes and Edges
    '''
    
    __tablename__ = 'graphs'
    
    id = Column(Integer, primary_key=True)
    vertices = relationship("Vertex", back_populates="graph", cascade="all, delete-orphan")
    edges = relationship("Edge", back_populates="graph", cascade="all, delete-orphan")

class Vertex(Base):
    __tablename__ = 'vertices'
    
    id = Column(Integer, primary_key=True)

    #parent graph
    graph_id = Column(Integer, ForeignKey('graphs.id'), nullable=False)
    name = Column(String(255), nullable=False)
    
    graph = relationship("Graph", back_populates="vertices")

    #all those edges starting from this vertex
    outgoing_edges = relationship("Edge", foreign_keys="[Edge.source_vertex_id]", back_populates="source_vertex", cascade="all, delete-orphan")
    incoming_edges = relationship("Edge", foreign_keys="[Edge.target_vertex_id]", back_populates="target_vertex", cascade="all, delete-orphan")

    #they should be unique
    __table_args__ = (
        UniqueConstraint('graph_id', 'name', name='uix_graph_vertex_name'),
    )

class Edge(Base):
    ''''
    directed edge between 2 verticies.
    '''
    __tablename__ = 'edges'
    
    id = Column(Integer, primary_key=True)
    graph_id = Column(Integer, ForeignKey('graphs.id'), nullable=False)

    #the start point of edge
    source_vertex_id = Column(Integer, ForeignKey('vertices.id'), nullable=False)

    #its end
    target_vertex_id = Column(Integer, ForeignKey('vertices.id'), nullable=False)
    
    graph = relationship("Graph", back_populates="edges")
    source_vertex = relationship("Vertex", foreign_keys=[source_vertex_id], back_populates="outgoing_edges")
    
    target_vertex = relationship("Vertex", foreign_keys=[target_vertex_id], back_populates="incoming_edges")

    #AFAIK only one edge should exist between two any vertices, so ensure 
    __table_args__ = (
        UniqueConstraint('graph_id', 'source_vertex_id', 'target_vertex_id', name='uix_graph_edge'),
    )
