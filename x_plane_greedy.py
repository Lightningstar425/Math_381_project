from small_auto import *
from math import inf
import copy

class greedy_sequential:

    def __init__(self, planes, days):
        self.graph = small_auto()
        self.graph.build_graph()
        self.steps = days
        self.planes = planes

    def best_single_path(self, start, steps, path, graph, prev_paths):
        current_path = path + [start]

        # base case
        if steps == self.steps - 1:
            restricted = copy.deepcopy(graph)
            for prev in prev_paths:
                u, v = prev[steps], prev[steps + 1]
                if u != v:
                    restricted.set_flown(u, v)  # apply prev planes' last flights

            best_profit = -restricted.get_storage_cost(start)
            best_move = current_path
            for k in restricted.get_edges(start):
                if not restricted.can_fly(start, k):
                    gain = restricted.get_edge_gain(start, k) - restricted.get_storage_cost(k)
                    if gain > best_profit:
                        best_profit = gain
                        best_move = current_path + [k]
            return best_profit, best_move

        storage_cost = graph.get_storage_cost(start)

        # wait
        wait_graph = copy.deepcopy(graph)
        for prev in prev_paths:          # apply prev planes' flights this step
            u, v = prev[steps], prev[steps + 1]
            if u != v:
                wait_graph.set_flown(u, v)
        wait_graph.update()
        wait, wait_path = self.best_single_path(start, steps + 1, current_path, wait_graph, prev_paths)
        wait -= storage_cost
        best_profit, best_move = wait, wait_path

        # fly
        for k in graph.get_edges(start):
            fly_graph = copy.deepcopy(graph)
            for prev in prev_paths:      # apply prev planes' flights this step
                u, v = prev[steps], prev[steps + 1]
                if u != v:
                    fly_graph.set_flown(u, v)

            if not fly_graph.can_fly(start, k):  # k not taken by a prev plane
                edge_gain = graph.get_edge_gain(start, k) - graph.get_storage_cost(k)
                fly_graph.set_flown(start, k)
                fly_graph.update()
                val, val_path = self.best_single_path(k, steps + 1, current_path, fly_graph, prev_paths)
                val += edge_gain
                if val > best_profit:
                    best_profit, best_move = val, val_path

        return best_profit, best_move

    def main(self):
        all_paths = []
        total_profit = 0

        for _ in range(self.planes):
            best = -inf
            best_path = []
            for v in self.graph.get_graph():
                profit, path = self.best_single_path(
                    v, 0, [], copy.deepcopy(self.graph), all_paths
                )
                if profit > best:
                    best = profit
                    best_path = path

            all_paths.append(best_path)
            total_profit += best

        return total_profit, all_paths


if __name__ == "__main__":
    search = greedy_sequential(planes=2, days=4)
    profit, paths = search.main()
    for i, path in enumerate(paths):
        print(f"Plane {i+1}: {path}")
    print(f"Total profit: {profit}")