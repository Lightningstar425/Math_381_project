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


class adjusting_graph:

    def __init__(self):
        self.graph = {}
        self.update_people = { "BOS":  42, "JFK":  48, "LAX":  55, "ORD":  52, "ATL":  58,
                            "DFW":  54, "DEN":  47, "SFO":  50, "SEA":  45, "MIA":  51, "LAS":  60,   
                            "PHX":  49, "MSP":  41, "DTW":  40, "CLT":  43}

    def add_node(self, name, people, storage_cost, time, num_planes, edges):
        self.graph[name] = Node(name, people, storage_cost, time, num_planes, edges)


    def build_graph(self): 

        """Nodes were generated with AI for fast creation of data, no code logic was built with AI"""
        # ── BOS · Boston Logan ────────────────────────────────────────
        bos_edges = {
            "JFK": Edge(lambda t: min(t, 150) * 230 - 1160,  120, 1, False),
            "DTW": Edge(lambda t: min(t, 150) * 250 - 1230,  115, 2, False),
            "CLT": Edge(lambda t: min(t, 150) * 285 - 1310,  115, 2, False),
            "MSP": Edge(lambda t: min(t, 150) * 310 - 1360,  120, 3, False),
            "ORD": Edge(lambda t: min(t, 150) * 315 - 1375,  155, 3, False),
            "ATL": Edge(lambda t: min(t, 150) * 330 - 1430,  145, 3, False),
            "MIA": Edge(lambda t: min(t, 150) * 355 - 1510,  135, 4, False),
            "DFW": Edge(lambda t: min(t, 150) * 385 - 1620,  125, 5, False),
            "DEN": Edge(lambda t: min(t, 150) * 375 - 1590,  120, 5, False),
            "LAX": Edge(lambda t: min(t, 150) * 420 - 1780,  165, 6, False),
            "SEA": Edge(lambda t: min(t, 150) * 400 - 1474,  200, 6, False),
        }
        self.add_node("BOS", 100, 680,
                      lambda p: min(8, round(p * 0.025 + 1)), 0, bos_edges)
 
        # ── JFK · New York JFK ────────────────────────────────────────
        jfk_edges = {
            "BOS": Edge(lambda t: min(t, 150) * 225 - 1155,  130, 1, False),
            "CLT": Edge(lambda t: min(t, 150) * 265 - 1270,  130, 2, False),
            "DTW": Edge(lambda t: min(t, 150) * 255 - 1250,  130, 2, False),
            "ORD": Edge(lambda t: min(t, 150) * 305 - 1355,  180, 2, False),
            "MIA": Edge(lambda t: min(t, 150) * 330 - 1400,  170, 3, False),
            "ATL": Edge(lambda t: min(t, 150) * 320 - 1380,  160, 2, False),
            "DFW": Edge(lambda t: min(t, 150) * 370 - 1560,  150, 4, False),
            "DEN": Edge(lambda t: min(t, 150) * 365 - 1550,  145, 4, False),
            "LAX": Edge(lambda t: min(t, 150) * 430 - 1800,  190, 6, False),
            "SEA": Edge(lambda t: min(t, 150) * 410 - 1760,  175, 6, False),
            "SFO": Edge(lambda t: min(t, 150) * 425 - 1795,  180, 6, False),
        }
        self.add_node("JFK", 150, 920,
                      lambda p: min(10, round(p * 0.030 + 1)), 0, jfk_edges)
 
        # ── LAX · Los Angeles International ──────────────────────────
        lax_edges = {
            "SFO": Edge(lambda t: min(t, 150) * 200 - 1140,  140, 1, False),
            "LAS": Edge(lambda t: min(t, 150) * 210 - 1150,  120, 1, False),
            "PHX": Edge(lambda t: min(t, 150) * 215 - 1145,  110, 1, False),
            "SEA": Edge(lambda t: min(t, 150) * 290 - 1315,  160, 3, False),
            "DEN": Edge(lambda t: min(t, 150) * 310 - 1360,  150, 3, False),
            "DFW": Edge(lambda t: min(t, 150) * 340 - 1455,  170, 3, False),
            "MIA": Edge(lambda t: min(t, 150) * 400 - 1720,  140, 5, False),
            "ATL": Edge(lambda t: min(t, 150) * 390 - 1645,  160, 5, False),
            "ORD": Edge(lambda t: min(t, 150) * 400 - 1680,  180, 4, False),
            "JFK": Edge(lambda t: min(t, 150) * 430 - 1800,  190, 6, False),
            "BOS": Edge(lambda t: min(t, 150) * 420 - 1780,  165, 6, False),
        }
        self.add_node("LAX", 200, 1100,
                      lambda p: min(10, round(p * 0.028 + 1)), 0, lax_edges)
 
        # ── ORD · Chicago O'Hare ──────────────────────────────────────
        ord_edges = {
            "MSP": Edge(lambda t: min(t, 150) * 220 - 1180,  130, 1, False),
            "DTW": Edge(lambda t: min(t, 150) * 210 - 1162,  115, 1, False),
            "BOS": Edge(lambda t: min(t, 150) * 315 - 1375,  155, 3, False),
            "JFK": Edge(lambda t: min(t, 150) * 305 - 1355,  180, 2, False),
            "CLT": Edge(lambda t: min(t, 150) * 280 - 1305,  130, 2, False),
            "ATL": Edge(lambda t: min(t, 150) * 290 - 1335,  170, 2, False),
            "MIA": Edge(lambda t: min(t, 150) * 340 - 1465,  140, 3, False),
            "DFW": Edge(lambda t: min(t, 150) * 325 - 1405,  160, 3, False),
            "DEN": Edge(lambda t: min(t, 150) * 300 - 1350,  150, 2, False),
            "SFO": Edge(lambda t: min(t, 150) * 390 - 1660,  160, 4, False),
            "SEA": Edge(lambda t: min(t, 150) * 380 - 1625,  150, 4, False),
            "LAX": Edge(lambda t: min(t, 150) * 400 - 1680,  180, 4, False),
        }
        self.add_node("ORD", 180, 860,
                      lambda p: min(9, round(p * 0.027 + 1)), 0, ord_edges)
 
        # ── ATL · Atlanta Hartsfield-Jackson ──────────────────────────
        atl_edges = {
            "CLT": Edge(lambda t: min(t, 150) * 210 - 1155,  115, 1, False),
            "MIA": Edge(lambda t: min(t, 150) * 270 - 1280,  150, 2, False),
            "JFK": Edge(lambda t: min(t, 150) * 320 - 1382,  160, 2, False),
            "BOS": Edge(lambda t: min(t, 150) * 330 - 1432,  145, 3, False),
            "ORD": Edge(lambda t: min(t, 150) * 290 - 1335,  170, 2, False),
            "DFW": Edge(lambda t: min(t, 150) * 312 - 1392,  160, 3, False),
            "DEN": Edge(lambda t: min(t, 150) * 330 - 1432,  140, 3, False),
            "MSP": Edge(lambda t: min(t, 150) * 292 - 1335,  130, 3, False),
            "LAX": Edge(lambda t: min(t, 150) * 390 - 1645,  160, 5, False),
            "PHX": Edge(lambda t: min(t, 150) * 360 - 1542,  130, 4, False),
            "SEA": Edge(lambda t: min(t, 150) * 402 - 1702,  140, 5, False),
        }
        self.add_node("ATL", 220, 790,
                      lambda p: min(10, round(p * 0.026 + 1)), 0, atl_edges)
 
        # ── DFW · Dallas / Fort Worth ─────────────────────────────────
        dfw_edges = {
            "PHX": Edge(lambda t: min(t, 150) * 250 - 1252,  115, 2, False),
            "LAS": Edge(lambda t: min(t, 150) * 272 - 1292,  115, 3, False),
            "DEN": Edge(lambda t: min(t, 150) * 280 - 1312,  140, 2, False),
            "ATL": Edge(lambda t: min(t, 150) * 312 - 1392,  160, 3, False),
            "ORD": Edge(lambda t: min(t, 150) * 325 - 1405,  160, 3, False),
            "MIA": Edge(lambda t: min(t, 150) * 332 - 1422,  130, 3, False),
            "JFK": Edge(lambda t: min(t, 150) * 372 - 1562,  150, 4, False),
            "BOS": Edge(lambda t: min(t, 150) * 385 - 1622,  125, 5, False),
            "SFO": Edge(lambda t: min(t, 150) * 362 - 1532,  150, 3, False),
            "LAX": Edge(lambda t: min(t, 150) * 342 - 1452,  170, 3, False),
            "SEA": Edge(lambda t: min(t, 150) * 372 - 1572,  140, 4, False),
        }
        self.add_node("DFW", 190, 770,
                      lambda p: min(9, round(p * 0.027 + 1)), 0, dfw_edges)
 
        # ── DEN · Denver International ────────────────────────────────
        den_edges = {
            "LAS": Edge(lambda t: min(t, 150) * 242 - 1222,  115, 2, False),
            "PHX": Edge(lambda t: min(t, 150) * 237 - 1212,  105, 2, False),
            "MSP": Edge(lambda t: min(t, 150) * 272 - 1292,  130, 2, False),
            "DFW": Edge(lambda t: min(t, 150) * 280 - 1312,  140, 2, False),
            "ORD": Edge(lambda t: min(t, 150) * 302 - 1352,  150, 2, False),
            "ATL": Edge(lambda t: min(t, 150) * 330 - 1432,  140, 3, False),
            "SFO": Edge(lambda t: min(t, 150) * 297 - 1342,  140, 3, False),
            "SEA": Edge(lambda t: min(t, 150) * 302 - 1362,  130, 3, False),
            "LAX": Edge(lambda t: min(t, 150) * 312 - 1362,  150, 3, False),
            "JFK": Edge(lambda t: min(t, 150) * 367 - 1552,  145, 4, False),
            "BOS": Edge(lambda t: min(t, 150) * 377 - 1592,  120, 5, False),
        }
        self.add_node("DEN", 160, 730,
                      lambda p: min(8, round(p * 0.026 + 1)), 0, den_edges)
 
        # ── SFO · San Francisco International ────────────────────────
        sfo_edges = {
            "LAX": Edge(lambda t: min(t, 150) * 202 - 1142,  140, 1, False),
            "LAS": Edge(lambda t: min(t, 150) * 222 - 1162,  105, 1, False),
            "PHX": Edge(lambda t: min(t, 150) * 242 - 1222,  105, 2, False),
            "SEA": Edge(lambda t: min(t, 150) * 252 - 1242,  130, 2, False),
            "DEN": Edge(lambda t: min(t, 150) * 297 - 1342,  140, 3, False),
            "DFW": Edge(lambda t: min(t, 150) * 362 - 1532,  150, 3, False),
            "ORD": Edge(lambda t: min(t, 150) * 392 - 1662,  160, 4, False),
            "JFK": Edge(lambda t: min(t, 150) * 425 - 1792,  180, 6, False),
        }
        self.add_node("SFO", 170, 1060,
                      lambda p: min(9, round(p * 0.027 + 1)), 0, sfo_edges)
 
        # ── SEA · Seattle-Tacoma ──────────────────────────────────────
        sea_edges = {
            "SFO": Edge(lambda t: min(t, 150) * 252 - 1242,  130, 2, False),
            "LAX": Edge(lambda t: min(t, 150) * 292 - 1312,  160, 3, False),
            "LAS": Edge(lambda t: min(t, 150) * 272 - 1282,  105, 3, False),
            "PHX": Edge(lambda t: min(t, 150) * 277 - 1292,  105, 3, False),
            "DEN": Edge(lambda t: min(t, 150) * 302 - 1362,  130, 3, False),
            "ORD": Edge(lambda t: min(t, 150) * 382 - 1622,  150, 4, False),
            "DFW": Edge(lambda t: min(t, 150) * 372 - 1572,  140, 4, False),
            "ATL": Edge(lambda t: min(t, 150) * 402 - 1702,  140, 5, False),
            "JFK": Edge(lambda t: min(t, 150) * 412 - 1762,  175, 6, False),
            "BOS": Edge(lambda t: min(t, 150) * 400 - 1474,  200, 6, False),
        }
        self.add_node("SEA", 130, 740,
                      lambda p: min(8, round(p * 0.025 + 1)), 0, sea_edges)
 
        # ── MIA · Miami International ─────────────────────────────────
        mia_edges = {
            "CLT": Edge(lambda t: min(t, 150) * 262 - 1272,  115, 2, False),
            "ATL": Edge(lambda t: min(t, 150) * 272 - 1282,  150, 2, False),
            "JFK": Edge(lambda t: min(t, 150) * 332 - 1402,  170, 3, False),
            "BOS": Edge(lambda t: min(t, 150) * 357 - 1512,  135, 4, False),
            "ORD": Edge(lambda t: min(t, 150) * 342 - 1462,  140, 3, False),
            "DFW": Edge(lambda t: min(t, 150) * 332 - 1422,  130, 3, False),
            "LAX": Edge(lambda t: min(t, 150) * 402 - 1722,  140, 5, False),
        }
        self.add_node("MIA", 140, 810,
                      lambda p: min(8, round(p * 0.025 + 1)), 0, mia_edges)
 
        # ── LAS · Las Vegas Harry Reid ────────────────────────────────
        las_edges = {
            "LAX": Edge(lambda t: min(t, 150) * 212 - 1152,  120, 1, False),
            "SFO": Edge(lambda t: min(t, 150) * 222 - 1162,  105, 1, False),
            "PHX": Edge(lambda t: min(t, 150) * 197 - 1132,  90, 1, False),
            "DEN": Edge(lambda t: min(t, 150) * 242 - 1222,  115, 2, False),
            "SEA": Edge(lambda t: min(t, 150) * 272 - 1282,  105, 3, False),
            "DFW": Edge(lambda t: min(t, 150) * 272 - 1292,  115, 3, False),
            "ORD": Edge(lambda t: min(t, 150) * 352 - 1502,  130, 4, False),
        }
        self.add_node("LAS", 120, 700,
                      lambda p: min(7, round(p * 0.024 + 1)), 0, las_edges)
 
        # ── PHX · Phoenix Sky Harbor ──────────────────────────────────
        phx_edges = {
            "LAX": Edge(lambda t: min(t, 150) * 217 - 1147,  110, 1, False),
            "LAS": Edge(lambda t: min(t, 150) * 197 - 1132,  90, 1, False),
            "SFO": Edge(lambda t: min(t, 150) * 242 - 1222,  105, 2, False),
            "DEN": Edge(lambda t: min(t, 150) * 237 - 1212,  105, 2, False),
            "DFW": Edge(lambda t: min(t, 150) * 252 - 1252,  115, 2, False),
            "SEA": Edge(lambda t: min(t, 150) * 277 - 1292,  105, 3, False),
            "ATL": Edge(lambda t: min(t, 150) * 362 - 1542,  130, 4, False),
            "ORD": Edge(lambda t: min(t, 150) * 357 - 1522,  130, 4, False),
        }
        self.add_node("PHX", 110, 705,
                      lambda p: min(7, round(p * 0.024 + 1)), 0, phx_edges)
 
        # ── MSP · Minneapolis-St. Paul ────────────────────────────────
        msp_edges = {
            "ORD": Edge(lambda t: min(t, 150) * 222 - 1182,  130, 1, False),
            "DTW": Edge(lambda t: min(t, 150) * 207 - 1157,  105, 2, False),
            "DEN": Edge(lambda t: min(t, 150) * 272 - 1292,  130, 2, False),
            "ATL": Edge(lambda t: min(t, 150) * 292 - 1332,  130, 3, False),
            "DFW": Edge(lambda t: min(t, 150) * 297 - 1342,  115, 3, False),
            "BOS": Edge(lambda t: min(t, 150) * 312 - 1362,  120, 3, False),
            "SEA": Edge(lambda t: min(t, 150) * 372 - 1592,  130, 4, False),
            "LAX": Edge(lambda t: min(t, 150) * 392 - 1652,  140, 4, False),
        }
        self.add_node("MSP", 100, 715,
                      lambda p: min(7, round(p * 0.025 + 1)), 0, msp_edges)
 
        # ── DTW · Detroit Metropolitan ────────────────────────────────
        dtw_edges = {
            "ORD": Edge(lambda t: min(t, 150) * 212 - 1162,  115, 1, False),
            "MSP": Edge(lambda t: min(t, 150) * 207 - 1157,  105, 2, False),
            "BOS": Edge(lambda t: min(t, 150) * 262 - 1262,  115, 2, False),
            "JFK": Edge(lambda t: min(t, 150) * 257 - 1252,  130, 2, False),
            "ATL": Edge(lambda t: min(t, 150) * 282 - 1312,  130, 2, False),
            "DFW": Edge(lambda t: min(t, 150) * 322 - 1402,  115, 3, False),
            "DEN": Edge(lambda t: min(t, 150) * 312 - 1382,  115, 3, False),
            "LAX": Edge(lambda t: min(t, 150) * 402 - 1682,  150, 5, False),
        }
        self.add_node("DTW", 105, 725,
                      lambda p: min(7, round(p * 0.025 + 1)), 0, dtw_edges)
 
        # ── CLT · Charlotte Douglas ───────────────────────────────────
        clt_edges = {
            "ATL": Edge(lambda t: min(t, 150) * 212 - 1157,  115, 1, False),
            "MIA": Edge(lambda t: min(t, 150) * 262 - 1272,  115, 2, False),
            "ORD": Edge(lambda t: min(t, 150) * 282 - 1302,  130, 2, False),
            "BOS": Edge(lambda t: min(t, 150) * 302 - 1362,  115, 2, False),
            "JFK": Edge(lambda t: min(t, 150) * 287 - 1322,  130, 2, False),
            "DFW": Edge(lambda t: min(t, 150) * 312 - 1382,  115, 3, False),
            "DEN": Edge(lambda t: min(t, 150) * 332 - 1422,  115, 3, False),
            "LAX": Edge(lambda t: min(t, 150) * 402 - 1692,  140, 5, False),
        }
        self.add_node("CLT", 115, 745,
                      lambda p: min(7, round(p * 0.025 + 1)), 0, clt_edges)
  


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
    graph = adjusting_graph()
    graph.build_graph()
    print(graph.get_edge_gain('BOS', "JFK"))
    graph.update()
    print(graph.get_edges('BOS'))
