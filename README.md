# BFS + DFS Pathfinding (Python Console)

## Run
```bash
python pathfinding.py
```

## What to look for
- BFS should return a shortest path in an unweighted grid.
- DFS may return a longer path depending on exploration order.
- Compare visited-node counts and the rendered overlays.

## Reflection (Assignment Write-up)
In the provided maps, BFS and DFS both find a path, but their behavior differs:

- **DFS path can be longer than BFS** on maps with branches (Example Map 2 is a good case), because DFS commits to one branch early and only backtracks after dead ends or long detours.
- **Visited counts can differ**: BFS often touches many nodes around the shortest route in concentric “layers,” while DFS may go deep into one corridor and visit fewer or more total nodes depending on layout.
- **Why BFS is shortest-path here**: with 4-direction movement and uniform edge cost (every move costs 1), BFS explores by distance from `S`. The first time `G` is discovered, that route is guaranteed minimal in step count.
- **Why DFS is not shortest-path guaranteed**: DFS prioritizes depth over distance. Its first found route depends on neighbor order, not global minimum distance.

## Monster Chase (Turn-Based) idea
`pathfinding.py` includes a simple `game_loop(mode="BFS"|"DFS")`:
- `P` is the player, `M` is the monster, `#` walls, `.` floor, optional `G` exit.
- Each turn, the player moves with WASD (no wall clipping).
- Monster recomputes a path to player each turn with selected mode and moves one step.
- BFS monster is usually more direct; DFS monster can be more erratic.

In a Python shell:
```python
from pathfinding import game_loop
game_loop("BFS")
```
