"""
Floyed warshel approach to find best path in graph
"""


from Adjacency_lists import *
from math import inf


class FloydWarshall:

    def __init__(self, adjacency, storage_costs, type='max'):
        self.graph = adjacency
        self.node_weights = storage_costs
        self.type = type
        self.dist = {}

    def best_paths(self, length=None):
        nodes = list(self.graph.keys())
        if length is None:
            length = len(nodes)

        self.dist = {u: {v: -inf for v in nodes} for u in nodes}
        for u in nodes:
            self.dist[u][u] = 0

        for t in range(length):
            new_dist = {u: dict(self.dist[u]) for u in nodes}
            for u in nodes:
                for v in nodes:
                    for k in nodes:
                        if k in self.graph and v in self.graph[k]:
                            candidate = self.dist[u][k] + self.graph[k][v]
                            if candidate > new_dist[u][v]:
                                new_dist[u][v] = candidate
            self.dist = new_dist

        return self.dist

    def parse(self, data):
        """
        Pretty-print a 2D dictionary as a table.
        Same style as the Bellman-Ford file.
        """
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
                val = row_data[col]
                display = "-inf" if val == -inf else str(val)
                print(f"{display:>{width}}", end="")
            print()

    def main(self, length=None):
        self.best_paths(length)
        return self.dist


if __name__ == "__main__":
    fw = FloydWarshall(adjacency, storage_costs, "max")
    distances = fw.main()
    fw.parse(distances)
