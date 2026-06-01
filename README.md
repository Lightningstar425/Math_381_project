# Exhaustive Search

Brute-force to find optimal paths

## Usage

```python
if __name__ == "__main__":
    search = exhaustive_search(planes=2, days=5)
    profit, paths = search.main()

    for i, path in enumerate(paths):
        print(f"Plane {i+1}: {path}")
    print(f"Total profit: {profit}")
```

## Parameters

- `planes` — number of aircraft
- `days` — length of the scheduling horizon

## MultiPlaneHeuristic_Global

Finds best joint plane movement for each day

## Usage

```python
if __name__ == "__main__":
    graph = adjusting_graph()
    graph.build_graph()
    solver = MultiPlaneHeuristic_Global(graph, num_planes=3, days=20, max_hours=16)
    total_gain, history = solver.simulate("SEA")
    print("Total gain:", total_gain)
    for step in history:
        print(step)
```

## MultiPlaneHeuristic_Global

- `num_planes` — number of aircraft
- `days` — length of the scheduling horizon
- `max_hours` — number of hours a plane can fly a day
