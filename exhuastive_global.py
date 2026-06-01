from small_auto import *
from math import inf
from itertools import product
import copy
from Auto_adjusting_adjacency_lists import *

class exhaustive_search:

    def __init__(self, planes, days):
        self.graph = small_auto()
        self.graph.build_graph()
        self.steps = days
        self.planes = planes

    def get_actions(self, position, graph):
        #wait
        actions = [(position, position)]

        #fly
        for k in graph.get_edges(position):
            if not graph.can_fly(position, k):
                actions.append((position, k))
        return actions

    def is_valid(self, joint_action):
        edges = [(src, dst) for src, dst in joint_action if src != dst]
        return len(edges) == len(set(edges))

    def best_path(self, positions, steps, paths, graph):
        current_paths = [paths[p] + [positions[p]] for p in range(self.planes)]

        #base
        if steps == self.steps - 1:
            best_profit = -inf
            best_moves = current_paths

            all_actions = [self.get_actions(positions[p], graph) for p in range(self.planes)]

            for joint in product(*all_actions):
                if not self.is_valid(joint):
                    continue

                total_gain = 0
                final_paths = []
                for p, (src, dst) in enumerate(joint):
                    if src != dst:
                        total_gain += graph.get_edge_gain(src, dst) - graph.get_storage_cost(dst)
                        final_paths.append(current_paths[p] + [dst])
                    else:
                        total_gain -= graph.get_storage_cost(src)
                        final_paths.append(current_paths[p])

                if total_gain > best_profit:
                    best_profit = total_gain
                    best_moves = final_paths

            return best_profit, best_moves

        best_profit = -inf
        best_moves = current_paths

        all_actions = [self.get_actions(positions[p], graph) for p in range(self.planes)]

        for joint in product(*all_actions):
            if not self.is_valid(joint):
                continue

            new_graph = copy.deepcopy(graph)
            total_gain = 0
            new_positions = []

            for p, (src, dst) in enumerate(joint):
                if src != dst:
                    total_gain += graph.get_edge_gain(src, dst) - graph.get_storage_cost(dst)
                    new_graph.set_flown(src, dst)
                    new_positions.append(dst)
                else:
                    total_gain -= graph.get_storage_cost(src)
                    new_positions.append(src)

            new_graph.update()
            future_profit, future_paths = self.best_path(
                tuple(new_positions), steps + 1, current_paths, new_graph
            )
            total = total_gain + future_profit

            if total > best_profit:
                best_profit = total
                best_moves = future_paths

        return best_profit, best_moves

    def main(self):
        airports = list(self.graph.get_graph().keys())
        best_profit = -inf
        best_paths = []

        # Try all combinations of starting airports across all planes
        for start_combo in product(airports, repeat=self.planes):
            profit, paths = self.best_path(
                start_combo, 0,
                [[] for _ in range(self.planes)],
                copy.deepcopy(self.graph)
            )
            if profit > best_profit:
                best_profit = profit
                best_paths = paths

        return best_profit, best_paths


if __name__ == "__main__":
    search = exhaustive_search(planes=2, days=5)
    profit, paths = search.main()
    for i, path in enumerate(paths):
        print(f"Plane {i+1}: {path}")
    print(f"Total profit: {profit}")