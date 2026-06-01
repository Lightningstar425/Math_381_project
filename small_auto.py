"""
Changing edge weights based on last flights, each path has an auto lock for a plane

-Marie Andken
"""

from dataclasses import dataclass

@dataclass
class Node:
    name: str
    people: int
    storage_cost: int

    ground_time: callable
    num_planes: int

    edges: dict #

@dataclass
class Edge:
    gain: callable

    tickets_sold: int
    flight_time: int
    in_use: bool


class small_auto:

    def __init__(self):
        self.graph = {}
        self.update_people = { "BOS":  42, "JFK":  48, "LAX":  55, "ORD":  52, "ATL":  58,
                            "DFW":  54, "DEN":  47, "SFO":  50, "SEA":  45, "MIA":  51, "LAS":  60,   
                            "PHX":  49, "MSP":  41, "DTW":  40, "CLT":  43}

    def add_node(self, name, people, storage_cost, time, num_planes, edges):
        self.graph[name] = Node(name, people, storage_cost, time, num_planes, edges)


    def build_graph(self): 

            # ── BOS ─────────────────────────────────────────────
        bos_edges = {
            "JFK": Edge(lambda t: min(t,150)*230 - 1160, 120, 1, False),
            "ORD": Edge(lambda t: min(t,150)*315 - 1375, 155, 3, False),
            "MIA": Edge(lambda t: min(t,150)*355 - 1510, 135, 4, False),
        }
        self.add_node(
            "BOS", 100, 680,
            lambda p: min(8, round(p * 0.025 + 1)),
            0,
            bos_edges
        )

        # ── JFK ─────────────────────────────────────────────
        jfk_edges = {
            "BOS": Edge(lambda t: min(t,150)*225 - 1155, 130, 1, False),
            "ORD": Edge(lambda t: min(t,150)*305 - 1355, 180, 2, False),
            "MIA": Edge(lambda t: min(t,150)*330 - 1400, 170, 3, False),
            "DEN": Edge(lambda t: min(t,150)*365 - 1550, 145, 4, False),
        }
        self.add_node(
            "JFK", 150, 920,
            lambda p: min(10, round(p * 0.030 + 1)),
            0,
            jfk_edges
        )

        # ── ORD ─────────────────────────────────────────────
        ord_edges = {
            "BOS": Edge(lambda t: min(t,150)*315 - 1375, 155, 3, False),
            "JFK": Edge(lambda t: min(t,150)*305 - 1355, 180, 2, False),
            "DEN": Edge(lambda t: min(t,150)*300 - 1350, 150, 2, False),
            "MIA": Edge(lambda t: min(t,150)*340 - 1465, 140, 3, False),
            "LAX": Edge(lambda t: min(t,150)*400 - 1680, 180, 4, False),
        }
        self.add_node(
            "ORD", 180, 860,
            lambda p: min(9, round(p * 0.027 + 1)),
            0,
            ord_edges
        )

        # ── DEN ─────────────────────────────────────────────
        den_edges = {
            "JFK": Edge(lambda t: min(t,150)*367 - 1552, 145, 4, False),
            "ORD": Edge(lambda t: min(t,150)*302 - 1352, 150, 2, False),
            "LAX": Edge(lambda t: min(t,150)*312 - 1362, 150, 3, False),
            "MIA": Edge(lambda t: min(t,150)*332 - 1422, 140, 4, False),
        }
        self.add_node(
            "DEN", 160, 730,
            lambda p: min(8, round(p * 0.026 + 1)),
            0,
            den_edges
        )

        # ── LAX ─────────────────────────────────────────────
        lax_edges = {
            "DEN": Edge(lambda t: min(t,150)*310 - 1360, 150, 3, False),
            "ORD": Edge(lambda t: min(t,150)*400 - 1680, 180, 4, False),
            "MIA": Edge(lambda t: min(t,150)*400 - 1720, 140, 5, False),
        }
        self.add_node(
            "LAX", 200, 1100,
            lambda p: min(10, round(p * 0.028 + 1)),
            0,
            lax_edges
        )

        # ── MIA ─────────────────────────────────────────────
        mia_edges = {
            "BOS": Edge(lambda t: min(t,150)*357 - 1512, 135, 4, False),
            "JFK": Edge(lambda t: min(t,150)*332 - 1402, 170, 3, False),
            "ORD": Edge(lambda t: min(t,150)*342 - 1462, 140, 3, False),
            "DEN": Edge(lambda t: min(t,150)*332 - 1422, 130, 3, False),
            "LAX": Edge(lambda t: min(t,150)*402 - 1722, 140, 5, False),
        }
        self.add_node(
            "MIA", 140, 810,
            lambda p: min(8, round(p * 0.025 + 1)),
            0,
            mia_edges
        )

    def set_flown(self, u, v): 
        #call to say arc (u, v) has been flown today/claimed 
        #people have left the airport
        self.graph[u].edges[v].in_use = True

        #update tickets/people
        tickets = self.graph[u].edges[v].tickets_sold
        self.graph[u].people -= min(150, tickets)
        self.graph[u].edges[v].tickets_sold -= min(150, tickets)

        #update planes 
        self.graph[v].num_planes += 1
        self.graph[u].num_planes -= 1




    def update(self):
        for node in self.graph:
            self.graph[node].people += self.update_people[node]

            for edge in self.graph[node].edges:
                self.graph[node].edges[edge].in_use = False
                self.graph[node].edges[edge].tickets_sold += int(self.graph[node].people / len(self.graph[node].edges))
        
        return self


    #Assumes flying u to v
    def get_edge_gain(self, u, v):
        return self.graph[u].edges[v].gain(self.graph[u].edges[v].tickets_sold)
    
    #Assumes flying u to v
    def get_flight_time(self, u, v):
        return self.graph[u].edges[v].flight_time
    
    #Assumes flying u to v
    def can_fly(self, u, v):
        return self.graph[u].edges[v].in_use

    def get_landing_time(self, v):
        return self.graph[v].ground_time(self.graph[v].people)

    def get_storage_cost(self, v):
        return self.graph[v].storage_cost

    def get_graph(self):
        return self.graph
    
    #get edges
    def get_edges(self, v):
        return self.graph[v].edges
    
    ##used in updating heuristic graphs #
    # removes people
    def set_people(self, u, v):
        tickets = self.graph[u].edges[v].tickets_sold
        self.graph[u].people -= min(150, tickets)

        self.graph[u].edges[v].tickets_sold -= min(150, tickets)

    #restricts a flight time
    def restrict_route(self, u, v):
        self.graph[u].edges[v].in_use = True

    #used to apply the above restrictions held in daily_graph (x_plane_greedy uses this)
    def apply_restrictions(self, daily_graph):
        for node in self.graph:
            for edge in self.graph[node].edges:
                if daily_graph.graph[node].edges[edge].in_use:
                    self.graph[node].edges[edge].in_use = True
    
    def apply_depletion(self, depletion):
        for airport, removed in depletion.items():
            self.graph[airport].people = max(0, self.graph[airport].people - removed)




if __name__ == "__main__":
    graph = small_auto()
    graph.build_graph()
    print(graph.get_edge_gain('BOS', "JFK"))
    graph.update()
    print(graph.get_edges('BOS'))
