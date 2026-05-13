"""
Changing edge weights based on last flights, each path has an auto lock for a plane
"""

from dataclasses import dataclass

@dataclass
class Node:
    name: str
    people: int
    storage_cost: int

    ground_time: int
    num_planes: int

    edges: dict
    
@dataclass
class Edge:
    cost: int

    flight_time: int
    in_use: bool


class adjusting_graph:

    def __init__(self):
        self.graph = {}

    def add_node(self, name, people, storage_cost, time, num_planes, edges):
        self.graph[name] = Node(name, people, storage_cost, time, num_planes, edges)
        pass

    def build_graph(self):
        pass



    def update(self):
        pass

    def state(self):
        pass

