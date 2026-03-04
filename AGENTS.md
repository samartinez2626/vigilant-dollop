# AGENTS.md

## Project Goal
Teach grid pathfinding by implementing:
- BFS using a queue (`collections.deque`)
- DFS using a stack (Python list, iterative)

## Rules for Codex
- Modify only existing files (`pathfinding.py`, `README.md`, `AGENTS.md`).
- Do not change required function signatures in `pathfinding.py`.
- DFS must be iterative (no recursion).
- BFS must use `collections.deque`.
- Use a `visited` set and `parent` dict for path reconstruction.
- Mark nodes visited when enqueued/pushed.
- Keep changes minimal and keep `main()` runnable.

## Output Contract
Running `python pathfinding.py` must:
- run BFS and DFS on at least 2 maps
- print found/path length/visited count
- print a rendered map with overlays

## Guidance for students
- Put all repo rules in this file so Codex follows stable constraints.
- If Codex goes off-track, paste the failing output and say:
  - "follow AGENTS.md"
  - "minimal diff"
  - "fix only X"
