from __future__ import annotations

from collections import deque
from typing import Dict, List, Optional, Set, Tuple

Pos = Tuple[int, int]  # (row, col)
Grid = List[List[str]]

EXAMPLE_MAP_1 = """
########
#S.....#
#.###..#
#...#G.#
########
""".strip("\n")

EXAMPLE_MAP_2 = """
########
#S..#..#
#......#
#...#..#
#......#
#.#....#
#..#..G#
########
""".strip("\n")

MONSTER_MAP = """
############
#P....#....#
#.#.#.#.##.#
#.#.#...#..#
#...###.#G.#
#.###...#..#
#....#..M..#
############
""".strip("\n")


def parse_grid(text: str) -> Tuple[Grid, Pos, Pos]:
    """
    Convert a multiline string map into a grid plus start and goal positions.

    Map legend:
    '#' wall
    '.' floor
    'S' start (exactly one)
    'G' goal (exactly one)
    """
    rows = [list(line.rstrip()) for line in text.splitlines() if line.strip()]
    if not rows:
        raise ValueError("Grid is empty")

    width = len(rows[0])
    if any(len(row) != width for row in rows):
        raise ValueError("Grid must be rectangular")

    start: Optional[Pos] = None
    goal: Optional[Pos] = None
    allowed = {"#", ".", "S", "G"}

    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch not in allowed:
                raise ValueError(f"Unexpected map char {ch!r} at {(r, c)}")
            if ch == "S":
                if start is not None:
                    raise ValueError("Map must contain exactly one S")
                start = (r, c)
            elif ch == "G":
                if goal is not None:
                    raise ValueError("Map must contain exactly one G")
                goal = (r, c)

    if start is None or goal is None:
        raise ValueError("Map must contain exactly one S and one G")

    return rows, start, goal


def neighbors(grid: Grid, node: Pos) -> List[Pos]:
    """Return valid 4-direction neighbors that are not walls."""
    r, c = node
    out: List[Pos] = []
    h, w = len(grid), len(grid[0])

    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < h and 0 <= nc < w and grid[nr][nc] != "#":
            out.append((nr, nc))
    return out


def reconstruct_path(parent: Dict[Pos, Pos], start: Pos, goal: Pos) -> Optional[List[Pos]]:
    """Reconstruct path from start->goal using parent pointers. Return None if goal unreachable."""
    if goal == start:
        return [start]
    if goal not in parent:
        return None

    cur = goal
    path = [cur]
    while cur != start:
        cur = parent[cur]
        path.append(cur)
    path.reverse()
    return path


def bfs_path(grid: Grid, start: Pos, goal: Pos) -> Tuple[Optional[List[Pos]], Set[Pos]]:
    """
    Queue-based BFS.
    Return (path, visited).
    - path is a list of positions from start to goal (inclusive), or None.
    - visited contains all explored/seen nodes.
    """
    queue: deque[Pos] = deque([start])
    visited: Set[Pos] = {start}
    parent: Dict[Pos, Pos] = {}

    while queue:
        node = queue.popleft()
        if node == goal:
            break

        for nxt in neighbors(grid, node):
            if nxt in visited:
                continue
            visited.add(nxt)
            parent[nxt] = node
            queue.append(nxt)

    return reconstruct_path(parent, start, goal), visited


def dfs_path(grid: Grid, start: Pos, goal: Pos) -> Tuple[Optional[List[Pos]], Set[Pos]]:
    """
    Stack-based DFS (iterative, no recursion).
    Return (path, visited).
    """
    stack: List[Pos] = [start]
    visited: Set[Pos] = {start}
    parent: Dict[Pos, Pos] = {}

    while stack:
        node = stack.pop()
        if node == goal:
            break

        # Reverse traversal to keep a consistent visual exploration order.
        for nxt in reversed(neighbors(grid, node)):
            if nxt in visited:
                continue
            visited.add(nxt)
            parent[nxt] = node
            stack.append(nxt)

    return reconstruct_path(parent, start, goal), visited


def render(grid: Grid, path: Optional[List[Pos]] = None, visited: Optional[Set[Pos]] = None) -> str:
    """
    Render the grid as text.
    Overlay rules (recommended):
    - path tiles shown as '*'
    - visited tiles shown as '·' (middle dot) or '+'
    - preserve 'S' and 'G'
    """
    canvas = [row[:] for row in grid]
    visited = visited or set()
    path_set = set(path or [])

    for r, c in visited:
        if canvas[r][c] in {"S", "G", "#"}:
            continue
        canvas[r][c] = "+"

    for r, c in path_set:
        if canvas[r][c] in {"S", "G", "#"}:
            continue
        canvas[r][c] = "*"

    return "\n".join("".join(row) for row in canvas)


def run_one(label: str, grid_text: str) -> None:
    grid, start, goal = parse_grid(grid_text)

    print("=" * 60)
    print(label)
    print("- Raw map")
    print(render(grid))

    path_bfs, visited_bfs = bfs_path(grid, start, goal)
    print("\n- BFS")
    print(f"found={path_bfs is not None} path_len={(len(path_bfs) if path_bfs else None)} visited={len(visited_bfs)}")
    print(render(grid, path=path_bfs, visited=visited_bfs))

    path_dfs, visited_dfs = dfs_path(grid, start, goal)
    print("\n- DFS")
    print(f"found={path_dfs is not None} path_len={(len(path_dfs) if path_dfs else None)} visited={len(visited_dfs)}")
    print(render(grid, path=path_dfs, visited=visited_dfs))


def parse_monster_grid(text: str) -> Tuple[Grid, Pos, Pos, Optional[Pos]]:
    """Parse game map with P (player), M (monster), optional G (exit)."""
    rows = [list(line.rstrip()) for line in text.splitlines() if line.strip()]
    player = monster = goal = None

    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch == "P":
                player = (r, c)
                rows[r][c] = "."
            elif ch == "M":
                monster = (r, c)
                rows[r][c] = "."
            elif ch == "G":
                goal = (r, c)

    if player is None or monster is None:
        raise ValueError("Monster map must include both P and M")

    return rows, player, monster, goal


def game_loop(mode: str = "BFS") -> None:
    """Simple turn-based Monster Chase demo. Mode can be BFS or DFS."""
    mode = mode.upper()
    if mode not in {"BFS", "DFS"}:
        raise ValueError("mode must be BFS or DFS")

    grid, player, monster, goal = parse_monster_grid(MONSTER_MAP)
    moves = {"w": (-1, 0), "a": (0, -1), "s": (1, 0), "d": (0, 1)}

    while True:
        display = [row[:] for row in grid]
        pr, pc = player
        mr, mc = monster
        display[pr][pc] = "P"
        display[mr][mc] = "M"
        print("\n" + "=" * 60)
        print(f"Monster Chase mode={mode}")
        print("Reach G before the monster catches you.")
        print("\n".join("".join(row) for row in display))

        if player == monster:
            print("The monster caught you. You lose!")
            return
        if goal is not None and player == goal:
            print("You reached the exit. You win!")
            return

        step = input("Move (W/A/S/D, Q to quit): ").strip().lower()
        if step == "q":
            print("Goodbye!")
            return
        if step not in moves:
            print("Invalid key.")
            continue

        dr, dc = moves[step]
        candidate = (player[0] + dr, player[1] + dc)
        if grid[candidate[0]][candidate[1]] != "#":
            player = candidate

        grid_for_search = [row[:] for row in grid]
        grid_for_search[player[0]][player[1]] = "G"
        grid_for_search[monster[0]][monster[1]] = "S"

        if mode == "BFS":
            monster_path, _ = bfs_path(grid_for_search, monster, player)
        else:
            monster_path, _ = dfs_path(grid_for_search, monster, player)

        if monster_path and len(monster_path) > 1:
            monster = monster_path[1]


def main() -> None:
    run_one("Example Map 1", EXAMPLE_MAP_1)
    run_one("Example Map 2", EXAMPLE_MAP_2)

    print("\n" + "=" * 60)
    print("Reflection")
    print("- On Example Map 2, DFS usually returns a longer path than BFS because DFS dives down one corridor first.")
    print("- BFS explores in layers (distance 1, then 2, then 3...), so first time it reaches G is guaranteed shortest.")
    print("- DFS has no shortest-path guarantee in unweighted grids; it depends on neighbor order and may backtrack late.")
    print("\nOptional interactive demo: run `game_loop(\"BFS\")` or `game_loop(\"DFS\")` in a Python shell.")


if __name__ == "__main__":
    main()
