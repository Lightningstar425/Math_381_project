"""
Class to run bellman-ford on a given adjacency list
"""

from math import *


class bellmanford:
    
    def __init__(self, adjacency, type='max'):
        self.graph = adjacency
        self.type = type
        self.best_paths = {}

    
    def best_path(self, node, index, length):
        d = [inf for i in len(node)]
        d[index] = 0

    def get_all_paths(self):
        for i, node in enumerate(self.graph):
            self.best_paths[node] = self.best_path(self.graph(node), i, 0)








    def main(self):
        pass


