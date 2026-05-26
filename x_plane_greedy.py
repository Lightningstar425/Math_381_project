

from Auto_adjusting_adjacency_lists import *
from small_auto import *
from math import *
import copy

class x_planes_best_path:

    def __init__(self, planes, days):

        self.graph = small_auto()
        self.graph.build_graph()

        self.daily_graph = {}
        for i in range(0, days):
            self.daily_graph[i] = {}
        self.steps = days
        self.planes = planes
        self.paths = {}


    def best_path(self, start, steps, d, path, graph):
        current_path = path + [start]

        #End, makes sure we don't need table
        if steps == (self.steps - 1):
            best_profit = -1 * graph.get_storage_cost(start)
            best_move = current_path

            for k in graph.get_edges(start):
                gain = graph.get_edge_gain(start, k) - graph.get_storage_cost(k)
                if gain > best_profit:
                    best_profit = gain
                    best_move = current_path + [k]  

            return best_profit, best_move

        best_profit = -inf
        best_move = current_path
        for k in graph.get_edges(start):
            #Fly to some max k
            fly_graph = copy.deepcopy(graph)
            fly_graph.set_flown(start, k)
            fly_graph.update()
            val, val_path = self.best_path(k, steps + 1, d, current_path, fly_graph)
            val += fly_graph.get_edge_gain(start, k) - fly_graph.get_storage_cost(k)

            #Wait where we are
            wait_graph = copy.deepcopy(graph)
            wait_graph.update()
            wait, wait_path = self.best_path(start, steps + 1, d, current_path, wait_graph)
            wait -= wait_graph.get_storage_cost(start)

            if val >= wait and val > best_profit:
                best_profit, best_move = val, val_path
            elif wait > best_profit:
                best_profit, best_move = wait, wait_path

            return best_profit, best_move
       


    def get_all(self):
        all_paths = {}
        for v in self.graph.get_graph():
            d = {"pos": v, "path": [], "day": 0}
            profit, path = self.best_path(v, 0, d, [], self.graph)
            all_paths[v] = {"best_profit": profit, "best_path": path}
        return all_paths

    def get_single_best(self):
        routes = self.get_all()
        best = -inf
        path = []

        for i in routes:
            if routes[i]["best_profit"] > best:
                best = routes[i]["best_profit"]
                path = routes[i]["best_path"]

        return (best, path)
    
    
if __name__ == "__main__":

    graph_explore = x_planes_best_path(1, 21)
    paths = graph_explore.get_all()

    print(graph_explore.get_single_best())
