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


class OnePlaneHeuristic:
    def __init__(self, graph, days=21, max_hours=16):
        self.graph = graph
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

    def route_score(self, start, dest, hours_left):
        edge = self.graph.get_graph()[start].edges[dest]

        gain = self.graph.get_edge_gain(start, dest)
        time_needed = self.route_time(start, dest)

        destination_storage = self.storage_cost_for_hours(
            dest,
            max(0, hours_left - time_needed)
        )

        time_penalty = time_needed * 100

        demand_bonus = edge.tickets_sold * 5

        return gain + demand_bonus - destination_storage - time_penalty

    def best_next_route(self, airport, hours_left):
        best_dest = None
        best_score = float("-inf")

        for dest in self.graph.get_graph()[airport].edges:
            edge = self.graph.get_graph()[airport].edges[dest]

            if edge.in_use:
                continue

            time_needed = self.route_time(airport, dest)

            if time_needed > hours_left:
                continue

            score = self.route_score(airport, dest, hours_left)

            if score > best_score:
                best_score = score
                best_dest = dest

        return best_dest, best_score

    def simulate(self, start_airport):
        current_airport = start_airport
        total_gain = 0
        history = []

        for day in range(1, self.days + 1):
            hours_left = self.max_hours
            routes_flown_today = 0

            while hours_left > 0:
                best_dest, best_score = self.best_next_route(
                    current_airport,
                    hours_left
                )

                stay_cost = self.storage_cost_for_hours(
                    current_airport,
                    hours_left
                )

                if best_dest is None or best_score <= -stay_cost:
                    total_gain -= stay_cost

                    history.append({
                        "day": day,
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
                    break

                hours_left_after = hours_left - time_needed

                gain = self.graph.get_edge_gain(current_airport, best_dest)
                destination_storage = self.storage_cost_for_hours(
                    best_dest,
                    hours_left_after
                )
                net_gain = gain - destination_storage
                total_gain += net_gain
                routes_flown_today += 1

                history.append({
                    "day": day,
                    "action": "FLY",
                    "start": current_airport,
                    "end": best_dest,
                    "gain": gain,
                    "storage_cost_after_flight": destination_storage,
                    "net_gain": net_gain,
                    "score": best_score,
                    "flight_time": flight_time,
                    "ground_time": ground_time,
                    "time_used": time_needed,
                    "hours_left_after": hours_left_after,
                    "routes_flown_today": routes_flown_today
                })

                self.graph.set_flown(current_airport, best_dest)
                current_airport = best_dest
                hours_left = hours_left_after

            self.graph.update()

        return total_gain, history


if __name__ == "__main__":
    graph = adjusting_graph()
    graph.build_graph()
    solver = OnePlaneHeuristic(graph, days=21, max_hours=16)
    total_gain, history = solver.simulate("SEA")
    print("Total gain:", total_gain)
    for step in history:
        print(step)
