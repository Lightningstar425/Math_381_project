

from Auto_adjusting_adjacency_lists import *
from small_auto import *
from math import *
import copy

class x_planes_best_path:

    def __init__(self, planes, days):

        self.graph = small_auto()
        self.graph.build_graph()
        self.max_profit = 0

        self.daily_graph = {}
        for i in range(0, days):
            self.daily_graph[i] = copy.deepcopy(self.graph)
        self.steps = days
        self.planes = planes
        self.paths = []


    def best_path(self, start, steps, d, path, graph):
        current_path = path + [start]

        #base case
        if steps == (self.steps - 1):
            best_profit = -1 * graph.get_storage_cost(start)
            best_move = current_path
            for k in graph.get_edges(start):
                if not graph.can_fly(start, k):
                    gain = graph.get_edge_gain(start, k) - graph.get_storage_cost(k)
                    if gain > best_profit:
                        best_profit = gain
                        best_move = current_path + [k]
            return best_profit, best_move

        best_profit = -inf
        best_move = current_path
        storage_cost = graph.get_storage_cost(start) 

        #wait
        wait_graph = copy.deepcopy(graph)
        wait_graph.apply_restrictions(self.daily_graph[steps])
        wait_graph.update()
        wait, wait_path = self.best_path(start, steps + 1, d, current_path, wait_graph)
        wait -= storage_cost

        best_profit = wait
        best_move = wait_path

        #fly
        for k in graph.get_edges(start):
            fly_graph = copy.deepcopy(graph)
            fly_graph.apply_restrictions(self.daily_graph[steps])
            
            if not fly_graph.can_fly(start, k):
                edge_gain = graph.get_edge_gain(start, k) - graph.get_storage_cost(k)
                fly_graph.set_flown(start, k)
                fly_graph.update()
                val, val_path = self.best_path(k, steps + 1, d, current_path, fly_graph)
                val += edge_gain

                if val > best_profit:
                    best_profit, best_move = val, val_path

        return best_profit, best_move
       


    def get_all_path(self):

        all_paths = {}
        for v in self.graph.get_graph():
            d = {"pos": v, "path": [], "day": 0}
            profit, path = self.best_path(v, 0, d, [], self.daily_graph[0])
            all_paths[v] = {"best_profit": profit, "best_path": path}

        return all_paths
            


    def get_single_best(self):
        #first plane
        
        all_paths = {}
        for v in self.graph.get_graph():
            d = {"pos": v, "path": [], "day": 0}
            profit, path = self.best_path(v, 0, d, [], self.daily_graph[0])
            all_paths[v] = {"best_profit": profit, "best_path": path}

        #get best
        best = -inf
        best_path = []
        for i in all_paths:
            if all_paths[i]["best_profit"] > best:
                best = all_paths[i]["best_profit"]
                best_path = all_paths[i]["best_path"]

        self.paths.append(best_path)
        self.max_profit += best
        self.create_graphs()

    
        
    
    def create_graphs(self):
        new_graph = copy.deepcopy(self.graph)

        for i in range(len(self.paths[0]) - 1):
            # Restrict routes already claimed by previous planes
            day_graph = copy.deepcopy(new_graph)
            for j in range(len(self.paths)):
                if self.paths[j][i] != self.paths[j][i+1]:
                    day_graph.restrict_route(self.paths[j][i], self.paths[j][i+1])

            # Save the day graph
            self.daily_graph[i] = copy.deepcopy(day_graph)

            #hide passengers already used, then update state
            for j in range(len(self.paths)):
                if self.paths[j][i] != self.paths[j][i+1]:
                    new_graph.set_people(self.paths[j][i], self.paths[j][i+1])
            new_graph.update()



        
    def main(self):
        for i in range(self.planes):
            """if i == 3:
                self.daily_graph[3].print_graph()
                self.daily_graph[4].print_graph()"""
            self.get_single_best()
        return self.max_profit, self.paths
    
if __name__ == "__main__":

    graph_explore = x_planes_best_path(4, 5)
    profit, paths = graph_explore.main()
    print(paths)
    print(profit)

    #print(graph_explore.get_single_best(1)

    #graph_explore.create_graphs()
    #for airport, data in paths.items():
    #    print(f"{airport}: profit={data['best_profit']}, path={data['best_path']}")
