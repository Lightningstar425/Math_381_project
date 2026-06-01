"""
Global greedy heuristic for airline scheduling.

At each step, all planes compete for the best available route.
The algorithm selects the highest-scoring route among all
possible plane-route combinations.

The score is based on:
- route profit
- ticket demand
- time required
- storage cost

Planes keep flying until no good route remains or there is
not enough time left in the day.

Each route can only be flown once per day.
"""

from Auto_adjusting_adjacency_lists import adjusting_graph


class MultiPlaneHeuristic_Global:
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

    def best_global_move(self,
                         plane_airports,
                         plane_hours,
                         active_planes,
                         used_routes_today):
        best_move = None
        best_score = float("-inf")

        for plane_id in active_planes:
            current_airport = plane_airports[plane_id]
            hours_left = plane_hours[plane_id]

            if current_airport not in self.graph.get_graph():
                continue

            for dest in self.graph.get_graph()[current_airport].edges:
                edge = self.graph.get_graph()[current_airport].edges[dest]

                if edge.in_use:
                    continue

                if (current_airport, dest) in used_routes_today:
                    continue

                time_needed = self.route_time(current_airport, dest)

                if time_needed <= 0 or time_needed > hours_left:
                    continue

                score, net_gain = self.route_score(
                    current_airport,
                    dest,
                    hours_left
                )

                if score > best_score:
                    best_score = score
                    best_move = {
                        "plane_id": plane_id,
                        "start": current_airport,
                        "dest": dest,
                        "score": score,
                        "net_gain": net_gain
                    }

        return best_move

    def simulate(self, start_airport):
        plane_airports = [start_airport for _ in range(self.num_planes)]
        total_gain = 0
        history = []

        for day in range(1, self.days + 1):
            used_routes_today = set()
            plane_hours = [self.max_hours for _ in range(self.num_planes)]
            routes_flown_today = [0 for _ in range(self.num_planes)]
            active_planes = set(range(self.num_planes))

            while active_planes:
                move = self.best_global_move(
                    plane_airports,
                    plane_hours,
                    active_planes,
                    used_routes_today
                )

                if move is None or move["score"] <= 0:
                    for plane_id in list(active_planes):
                        current_airport = plane_airports[plane_id]
                        hours_left = plane_hours[plane_id]

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
                            "routes_flown_today": routes_flown_today[plane_id]
                        })

                    active_planes.clear()
                    break

                plane_id = move["plane_id"]
                current_airport = move["start"]
                best_dest = move["dest"]
                best_score = move["score"]

                flight_time, ground_time = self.flight_and_ground_time(
                    current_airport,
                    best_dest
                )
                time_needed = flight_time + ground_time

                if time_needed <= 0 or time_needed > plane_hours[plane_id]:
                    active_planes.remove(plane_id)
                    continue

                hours_left_after = plane_hours[plane_id] - time_needed
                gain = self.graph.get_edge_gain(current_airport, best_dest)

                storage_after_flight = self.storage_cost_for_hours(
                    best_dest,
                    hours_left_after
                )
                storage_if_stay = self.storage_cost_for_hours(
                    current_airport,
                    plane_hours[plane_id]
                )
                net_gain = gain - storage_after_flight + storage_if_stay
                total_gain += net_gain
                routes_flown_today[plane_id] += 1

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
                    "routes_flown_today": routes_flown_today[plane_id]
                })

                used_routes_today.add((current_airport, best_dest))
                self.mark_route_flown(current_airport, best_dest)

                plane_airports[plane_id] = best_dest
                plane_hours[plane_id] = hours_left_after

                if plane_hours[plane_id] <= 0:
                    active_planes.remove(plane_id)

            self.graph.update()

        return total_gain, history


if __name__ == "__main__":
    graph = adjusting_graph()
    graph.build_graph()
    solver = MultiPlaneHeuristic_Global(graph, num_planes=3, days=20, max_hours=16)
    total_gain, history = solver.simulate("SEA")
    print("Total gain:", total_gain)
    for step in history:
        print(step)
