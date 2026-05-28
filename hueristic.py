from small_auto import *
from math import inf
import copy

class heuristic_search:

    def __init__(self, days):
        self.graph = small_auto()
        self.graph.build_graph()
        self.steps = days

    def greedy_path(self, start):
        graph = copy.deepcopy(self.graph)
        current = start
        path = [start]
        total_profit = 0

        for step in range(self.steps):
            best_val = -1 * graph.get_storage_cost(current)
            best_next = None

            for k in graph.get_edges(current):
                if not graph.can_fly(current, k):
                    gain = graph.get_edge_gain(current, k) - graph.get_storage_cost(k)
                    if gain > best_val:
                        best_val = gain
                        best_next = k

            if best_next is not None:
                total_profit += best_val
                graph.set_flown(current, best_next)
                current = best_next
            else:
                total_profit += best_val

            graph.update()
            path.append(current)

        return total_profit, path

    def get_all(self):
        results = {}
        for v in self.graph.get_graph():
            profit, path = self.greedy_path(v)
            results[v] = {"best_profit": profit, "best_path": path}
        return results


if __name__ == "__main__":
    h = heuristic_search(days=5)
    results = h.get_all()
    for airport, data in results.items():
        print(f"{airport}: profit={data['best_profit']}, path={data['best_path']}")