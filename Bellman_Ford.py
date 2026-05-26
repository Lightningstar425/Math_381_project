"""
Class to run bellman-ford on a given adjacency list
"""
from Adjacency_lists import *
from math import *

from math import inf


class BellmanFord:
    def __init__(self, adjacency, storage_costs, mode="max"):
        self.graph = adjacency
        self.storage_costs = storage_costs
        self.mode = mode

        self.best_paths = {}

    def best_path(self, start, max_steps=None):

        if max_steps is None:
            max_steps = len(self.graph) - 1

        d = dict.fromkeys(self.graph, -inf)
        d[start] = 0
        for _ in range(max_steps):
            updated = False
            new_d = d.copy()
            for v in self.graph:
                if d[v] == -inf:
                    continue

                for u, edge_weight in self.graph[v].items():
                    candidate = d[v] + edge_weight - self.storage_costs.get(u, 0)
                    if candidate > new_d[u]:
                        new_d[u] = candidate
                        updated = True

            d = new_d

            if not updated:
                break

        return d


    def get_all_paths(self, max_steps=None):
        self.best_paths = {}
        for node in self.graph:
            self.best_paths[node] = self.best_path(node, max_steps)

        return self.best_paths


#print pretty
    def parse(self, data):
        cols = list(next(iter(data.values())).keys())
        width = max(
            max(len(str(v)) for row in data.values() for v in row.values()),
            max(len(str(k)) for k in cols),
            max(len(str(k)) for k in data.keys())
        ) + 2
        # Header
        print("".ljust(width), end="")

        for col in cols:
            print(f"{col:>{width}}", end="")

        print()

        print("-" * (width * (len(cols) + 1)))
        for row_name, row_data in data.items():
            print(f"{row_name:<{width}}", end="")
            for col in cols:
                value = row_data[col]
                if value == -inf:
                    value = "INF"
                print(f"{value:>{width}}", end="")
            print()

    
    def main(self, max_steps=None):
        self.get_all_paths(max_steps=max_steps)
        return self.best_paths
    
    def max_value_per_airport(self, data):
        return {airport: max(values.values()) for airport, values in data.items()}


if __name__ == "__main__":

    graph_explore = BellmanFord(adjacency, storage_costs)

    paths = graph_explore.main(max_steps=21)
    graph_explore.parse(paths)

    print(graph_explore.max_value_per_airport(paths))

