
from Adjacency_lists import *
from math import *


class best_step:

    def __init__(self, num_steps, adjacency, storage_costs):
        self.length = num_steps
        self.best = {}
        self.steps = []

        self.graph = adjacency
        self.node_weights = storage_costs



    def greedy(self, step, position, best, path):
        """
        Always takes best availible path, possible conflicts when paths are of equal value (upgrade to DP)
        """
        if step == 0:
            return best
        else:
            local_max = {"name":"MJA", "max": -inf}
            for key in self.graph[position]:
                if self.graph[position][key] > local_max["max"]:
                    local_max['max'] = self.graph[position][key]
                    local_max['name'] = key
            path.append(local_max['name'])
            best += local_max['max']
            return self.greedy(step-1, local_max['name'], best, path)

    def get_all_paths(self):

        for node in self.graph:
            path = []
            var = self.greedy(self.length, node, 0, path)
            self.best[node] = {}
            self.best[node]['max_gain'] = var
            self.best[node]['path'] = path
        return self.best


    def stats(self):
        stat_info = {"max": 0, "start": "", "route":[]}

        for paths in self.best:
            if self.best[paths]["max_gain"] > stat_info['max']:
                stat_info['max'] = self.best[paths]["max_gain"]
                stat_info["start"] = paths
                stat_info['route'] = self.best[paths]["path"]
        return stat_info

if __name__ == "__main__":
    graph_explore = best_step(5, adjacency, storage_costs)
    paths = graph_explore.get_all_paths()
    stats = graph_explore.stats()
    print(paths)
    print(stats)

    
