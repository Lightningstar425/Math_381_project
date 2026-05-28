"""
The plane repeatedly chooses the best next route.
Each route gets a score based on:
- route profit
- ticket demand
- time used
- storage cost

Score = gain + demand bonus - time penalty - storage cost

The plane keeps flying until:
there is no good route left/there is not enough time remaining in the day.
"""

from Auto_adjusting_adjacency_lists import adjusting_graph

class MultiPlaneHeuristic:
    def __init__(self, graph, num_planes, days=21, max_hours=16):
        self.graph = graph
        self.num_planes = num_planes
        self.days = days
        self.max_hours = max_hours

    def storage_cost_for_hours(self, airport, hours):
        return self.graph.get_storage_cost(airport) * hours / 24

    def flight_and_ground_time(self, start, dest):
        flight_time = self.graph.get_flight_time(start, dest)
        ground_time = self.graph.get_landing_time(dest)

        if ground_time < 0:
            ground_time = 0

        return flight_time, ground_time

    def route_time(self, start, dest):
        flight_time, ground_time = self.flight_and_ground_time(start, dest)
        return flight_time + ground_time

    def mark_route_flown(self, start, dest):
        edge = self.graph.get_graph()[start].edges[dest]
        start_node = self.graph.get_graph()[start]
        dest_node = self.graph.get_graph()[dest]

        edge.in_use = True

        passengers = min(150, edge.tickets_sold, start_node.people)
        start_node.people = max(0, start_node.people - passengers)
        edge.tickets_sold = max(0, edge.tickets_sold - passengers)

        start_node.num_planes -= 1
        dest_node.num_planes += 1

    def route_score(self, start, dest, hours_left):
        edge = self.graph.get_graph()[start].edges[dest]

        gain = self.graph.get_edge_gain(start, dest)
        time_needed = self.route_time(start, dest)
        hours_left_after = hours_left - time_needed

        storage_after_flight = self.storage_cost_for_hours(
            dest,
            max(0, hours_left_after)
        )
        storage_if_stay = self.storage_cost_for_hours(start, hours_left)

        time_penalty = time_needed * 10
        demand_bonus = edge.tickets_sold * 5

        net_gain = gain - storage_after_flight + storage_if_stay
        score = net_gain + demand_bonus - time_penalty

        return score, net_gain

    def best_next_route(self, airport, hours_left, used_routes_today):
        best_dest = None
        best_score = float("-inf")
        best_net_gain = float("-inf")

        if airport not in self.graph.get_graph():
            return None, best_score, best_net_gain

        for dest in self.graph.get_graph()[airport].edges:
            edge = self.graph.get_graph()[airport].edges[dest]

            if edge.in_use:
                continue

            if (airport, dest) in used_routes_today:
                continue

            time_needed = self.route_time(airport, dest)

            if time_needed <= 0 or time_needed > hours_left:
                continue

            score, net_gain = self.route_score(airport, dest, hours_left)

            if score > best_score:
                best_score = score
                best_net_gain = net_gain
                best_dest = dest

        return best_dest, best_score, best_net_gain

    def simulate(self, start_airport):
        plane_airports = [start_airport for _ in range(self.num_planes)]
        total_gain = 0
        history = []

        for day in range(1, self.days + 1):
            used_routes_today = set()

            for plane_id in range(self.num_planes):
                current_airport = plane_airports[plane_id]
                hours_left = self.max_hours
                routes_flown_today = 0

                while hours_left > 0:
                    best_dest, best_score, best_net_gain = self.best_next_route(
                        current_airport,
                        hours_left,
                        used_routes_today
                    )

                    if best_dest is None or best_score <= 0:
                        stay_cost = self.storage_cost_for_hours(
                            current_airport,
                            hours_left
                        )
                        total_gain -= stay_cost

                        history.append({
                            "day": day,
                            "plane": plane_id + 1,
                            "action": "STOP",
                            "airport": current_airport,
                            "hours_left": hours_left,
                            "storage_cost": stay_cost,
                            "routes_flown_today": routes_flown_today
                        })
                        break

                    flight_time, ground_time = self.flight_and_ground_time(
                        current_airport,
                        best_dest
                    )
                    time_needed = flight_time + ground_time

                    if time_needed <= 0 or time_needed > hours_left:
                        stay_cost = self.storage_cost_for_hours(
                            current_airport,
                            hours_left
                        )
                        total_gain -= stay_cost
                        history.append({
                            "day": day,
                            "plane": plane_id + 1,
                            "action": "STOP",
                            "airport": current_airport,
                            "hours_left": hours_left,
                            "storage_cost": stay_cost,
                            "routes_flown_today": routes_flown_today
                        })
                        break

                    hours_left_after = hours_left - time_needed
                    gain = self.graph.get_edge_gain(current_airport, best_dest)

                    storage_after_flight = self.storage_cost_for_hours(
                        best_dest,
                        hours_left_after
                    )
                    storage_if_stay = self.storage_cost_for_hours(
                        current_airport,
                        hours_left
                    )
                    net_gain = gain - storage_after_flight + storage_if_stay
                    total_gain += net_gain
                    routes_flown_today += 1

                    history.append({
                        "day": day,
                        "plane": plane_id + 1,
                        "action": "FLY",
                        "start": current_airport,
                        "end": best_dest,
                        "gain": gain,
                        "storage_if_stay": storage_if_stay,
                        "storage_cost_after_flight": storage_after_flight,
                        "net_gain": net_gain,
                        "score": best_score,
                        "flight_time": flight_time,
                        "ground_time": ground_time,
                        "time_used": time_needed,
                        "hours_left_after": hours_left_after,
                        "routes_flown_today": routes_flown_today
                    })

                    used_routes_today.add((current_airport, best_dest))
                    self.mark_route_flown(current_airport, best_dest)
                    current_airport = best_dest
                    hours_left = hours_left_after

                plane_airports[plane_id] = current_airport

            self.graph.update()

        return total_gain, history


if __name__ == "__main__":
    graph = adjusting_graph()
    graph.build_graph()
    solver = MultiPlaneHeuristic(graph, num_planes=5, days=20, max_hours=16)
    total_gain, history = solver.simulate("SEA")
    print("Total gain:", total_gain)
    for step in history:
        print(step)

