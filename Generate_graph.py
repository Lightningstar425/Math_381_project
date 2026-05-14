"""
Class generates a graph that can be looked at from a given adjacency list
"""

import networkx as nx
import plotly.graph_objects as go

from Adjacency_lists import storage_costs, airport_info, adjacency


class Generate_graph:

    def __init__(self, storage_costs, airport_info, adjacency):
        self.storage_costs = storage_costs
        self.airport_info = airport_info
        self.adjacency = adjacency
        self.graph = nx.DiGraph()
        self.build_graph()

    def build_graph(self):
        for airport in self.airport_info:
            self.graph.add_node(
                airport,
                name=self.airport_info[airport]["name"],
                city=self.airport_info[airport]["city"],
                storage_cost=self.storage_costs[airport]
            )

        for start in self.adjacency:
            for destination, gain in self.adjacency[start].items():
                self.graph.add_edge(
                    start,
                    destination,
                    gain=gain
                )
                
    def curved_route_points(self, lon1, lat1, lon2, lat2, curve=0.15, steps=30):
        """
        Creates curved points between two airports to help show opposite direction separately.
        I use Bezier curve to control the curvature of each route to make them separate.
        """
        lons = []
        lats = []

        mid_lon = (lon1 + lon2) / 2
        mid_lat = (lat1 + lat2) / 2

        dx = lon2 - lon1
        dy = lat2 - lat1

        control_lon = mid_lon - dy * curve
        control_lat = mid_lat + dx * curve

        for i in range(steps + 1):
            t = i / steps
            lon = ((1 - t) ** 2 * lon1
                   + 2 * (1 - t) * t * control_lon
                   + t ** 2 * lon2)
            lat = ((1 - t) ** 2 * lat1
                   + 2 * (1 - t) * t * control_lat
                   + t ** 2 * lat2)
            lons.append(lon)
            lats.append(lat)

        return lons, lats
    
    def draw_all_routes(self):
        """
        Draws all routes on a map, and it's dense but it shows the airports and 
        their storage costs clearly on the map, 
        and separte two routes for any two airports.
        And it also displays the gains for routes
        """
        airport_pos = {
            "SEA": (-122.3, 47.6),
            "SFO": (-122.4, 37.6),
            "LAX": (-118.4, 33.9),
            "LAS": (-115.2, 36.1),
            "PHX": (-112.0, 33.4),
            "DEN": (-104.7, 39.9),
            "DFW": (-97.0, 32.9),
            "MSP": (-93.2, 44.9),
            "ORD": (-87.9, 41.9),
            "DTW": (-83.4, 42.2),
            "ATL": (-84.4, 33.6),
            "CLT": (-80.9, 35.2),
            "MIA": (-80.3, 25.8),
            "JFK": (-73.8, 40.6),
            "BOS": (-71.0, 42.4),
        }

        fig = go.Figure()

        for start, dest, data in self.graph.edges(data=True):
            start_lon, start_lat = airport_pos[start]
            dest_lon, dest_lat = airport_pos[dest]

            if self.graph.has_edge(dest, start):
                curve = 0.22
            else:
                curve = 0.08

            route_lons, route_lats = self.curved_route_points(
                start_lon,
                start_lat,
                dest_lon,
                dest_lat,
                curve=curve,
                steps=25
            )

            hover_text = (
                f"Route: {start} → {dest}<br>"
                f"Gain: {data['gain']}<br>"
                f"Direction matters: {start} → {dest} is different from {dest} → {start}"
            )

            fig.add_trace(go.Scattergeo(
                lon=route_lons,
                lat=route_lats,
                mode="lines",
                line=dict(
                    width=max(0.5, data["gain"] / 10000),
                ),
                opacity=0.28,
                text=[hover_text] * len(route_lons),
                hoverinfo="text",
                showlegend=False
            ))

        airport_lons = []
        airport_lats = []
        airport_labels = []
        airport_sizes = []

        for airport in self.graph.nodes:
            lon, lat = airport_pos[airport]
            airport_lons.append(lon)
            airport_lats.append(lat)
            airport_labels.append(
                f"Airport: {airport}<br>"
                f"City: {self.graph.nodes[airport]['city']}<br>"
                f"Storage cost per day: {self.graph.nodes[airport]['storage_cost']}"
            )
            airport_sizes.append(self.graph.nodes[airport]["storage_cost"] / 35)

        fig.add_trace(go.Scattergeo(
            lon=airport_lons,
            lat=airport_lats,
            mode="markers+text",
            text=list(self.graph.nodes),
            textposition="top center",
            marker=dict(
                size=airport_sizes,
                line=dict(width=1)
            ),
            hovertext=airport_labels,
            hoverinfo="text",
            showlegend=False
        ))

        fig.update_layout(
            title="Initial Airline Route Graph: All Routes on U.S. Map",
            geo=dict(
                scope="usa",
                projection_type="albers usa",
                showland=True,
                showcountries=True,
                showsubunits=True,
                showlakes=True,
                landcolor="rgb(235, 235, 235)",
                lakecolor="rgb(220, 240, 255)",
                countrycolor="rgb(120, 120, 120)",
                subunitcolor="rgb(170, 170, 170)",
            ),
            margin=dict(l=0, r=0, t=50, b=0)
        )

        fig.show(renderer="browser")

    def draw_top_routes(self, top_n):
        """
        Only draws the top n profitable routes.
        """
        airport_pos = {
            "SEA": (-122.3, 47.6),
            "SFO": (-122.4, 37.6),
            "LAX": (-118.4, 33.9),
            "LAS": (-115.2, 36.1),
            "PHX": (-112.0, 33.4),
            "DEN": (-104.7, 39.9),
            "DFW": (-97.0, 32.9),
            "MSP": (-93.2, 44.9),
            "ORD": (-87.9, 41.9),
            "DTW": (-83.4, 42.2),
            "ATL": (-84.4, 33.6),
            "CLT": (-80.9, 35.2),
            "MIA": (-80.3, 25.8),
            "JFK": (-73.8, 40.6),
            "BOS": (-71.0, 42.4),
        }

        top_edges = sorted(
            self.graph.edges(data=True),
            key=lambda edge: edge[2]["gain"],
            reverse=True
        )[:top_n]

        fig = go.Figure()

        for start, dest, data in top_edges:
            start_lon, start_lat = airport_pos[start]
            dest_lon, dest_lat = airport_pos[dest]

            if self.graph.has_edge(dest, start):
                curve = 0.28
            else:
                curve = 0.10

            route_lons, route_lats = self.curved_route_points(
                start_lon,
                start_lat,
                dest_lon,
                dest_lat,
                curve=curve
            )

            hover_text = (
                f"Route: {start} → {dest}<br>"
                f"Gain: {data['gain']}<br>"
            )

            fig.add_trace(go.Scattergeo(
                lon=route_lons,
                lat=route_lats,
                mode="lines",
                line=dict(
                    width=max(1, data["gain"] / 10000),
                ),
                opacity=0.7,
                text=[hover_text] * len(route_lons),
                hoverinfo="text",
                showlegend=False
            ))

        airport_lons = []
        airport_lats = []
        airport_labels = []
        airport_sizes = []

        for airport in self.graph.nodes:
            lon, lat = airport_pos[airport]
            airport_lons.append(lon)
            airport_lats.append(lat)
            airport_labels.append(
                f"Airport: {airport}<br>"
                f"City: {self.graph.nodes[airport]['city']}<br>"
                f"Storage cost per day: {self.graph.nodes[airport]['storage_cost']}"
            )
            airport_sizes.append(self.graph.nodes[airport]["storage_cost"] / 35)

        fig.add_trace(go.Scattergeo(
            lon=airport_lons,
            lat=airport_lats,
            mode="markers+text",
            text=list(self.graph.nodes),
            textposition="top center",
            marker=dict(
                size=airport_sizes,
                line=dict(width=1)
            ),
            hovertext=airport_labels,
            hoverinfo="text",
            showlegend=False
        ))

        fig.update_layout(
            title=f"Top {top_n} Airline Routes on Map",
            geo=dict(
                scope="usa",
                projection_type="albers usa",
                showland=True,
                showcountries=True,
                showsubunits=True,
                showlakes=True,
                landcolor="rgb(235, 235, 235)",
                lakecolor="rgb(220, 240, 255)",
                countrycolor="rgb(120, 120, 120)",
                subunitcolor="rgb(170, 170, 170)",
            ),
            margin=dict(l=0, r=0, t=50, b=0)
        )

        fig.show(renderer="browser")

    def get_graph(self):
        return self.graph


if __name__ == "__main__":
    graph = Generate_graph(storage_costs, airport_info, adjacency)
    graph.draw_top_routes(20)
    graph.draw_all_routes()

