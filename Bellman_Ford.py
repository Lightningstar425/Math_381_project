"""
Class to run bellman-ford on a given adjacency list
"""
from Adjacency_lists import *
from math import *


class bellmanford:
    
    def __init__(self, adjacency, storage_costs, type='max'):
        self.graph = adjacency
        self.node_weights = storage_costs
        self.type = type
        self.best_paths = {}

    #Currently doesn't include storage costs
    #We have positive cost cycles, so this may not explore everything
    #Goal is to find the best positive cost cycles
    def best_path(self, node, length):
        d = dict.fromkeys(self.graph, -inf)
        d[node] = 0
        i = 0
        for v in self.graph:
            i += 1
            for u in d:
                if u in self.graph[v]:
                    if d[u] < self.graph[v][u] + d[v]:
                        d[u] = self.graph[v][u] + d[v]
                        if i == len(self.graph):
                            #print("Positive cost cycle found") 
                            pass           
        return d





    def get_all_paths(self):
        for i, node in enumerate(self.graph):
            self.best_paths[node] = self.best_path(node, 0)



    def parse(self, data):
        cols = list(next(iter(data.values())).keys())

        width = max(
            max(len(str(v)) for row in data.values() for v in row.values()),
            max(len(k) for k in cols),
            max(len(k) for k in data.keys())
        ) + 2


        print("".ljust(width), end="")
        for col in cols:
            print(f"{col:>{width}}", end="")
        print()


        print("-" * (width * (len(cols) + 1)))

        for row_name, row_data in data.items():
            print(f"{row_name:<{width}}", end="")
            for col in cols:
                print(f"{row_data[col]:>{width}}", end="")
            print()




    def main(self):

        self.get_all_paths()
        return self.best_paths

if __name__ == "__main__":
    graph_explore = bellmanford(adjacency, storage_costs, "max")
    paths = graph_explore.main()
    graph_explore.parse(paths)

