"""
Class to run bellman-ford on a given adjacency list
"""

from math import *


class bellmanford:
    
    def __init__(self, adjacency, storage_costs, type='max'):
        self.graph = adjacency
        self.node_weights = storage_costs
        self.type = type
        self.best_paths = {}

    #Currently doesn't include storage costs
    def best_path(self, node, index, length):
        d = [inf for i in len(node)]
        d[index] = 0
        
        




        return d


    def get_all_paths(self):
        for i, node in enumerate(self.graph):
            self.best_paths[node] = self.best_path(self.graph(node), i, 0)








    def main(self):

        self.get_all_paths
        return self.best_paths


