# src/coloring.py
from typing import List, Tuple, Dict
from collections import deque
from src.dual_graph import build_triangle_adjacency


def three_color_vertices(triangles: List[Tuple[int, int, int]]) -> Dict[int, int]:
    if not triangles:
        return {}

    adjacency = build_triangle_adjacency(triangles)
    colors: Dict[int, int] = {}

    first_tri = triangles[0]
    colors[first_tri[0]] = 0
    colors[first_tri[1]] = 1
    colors[first_tri[2]] = 2

    visited_tri: set[int] = {0}
    q: deque[int] = deque([0])

    while q:
        tidx = q.popleft()
        tri = triangles[tidx]
        for nb in adjacency[tidx]:
            if nb in visited_tri:
                continue
            nb_tri = triangles[nb]
            shared_set = set(tri).intersection(nb_tri)
            shared: List[int] = list(shared_set)
            if len(shared) == 2:
                third_candidates = [v for v in nb_tri if v not in shared]
                if third_candidates:
                    third = third_candidates[0]
                    if all(v in colors for v in shared):
                        used = {colors[v] for v in shared}
                        colors[third] = ({0, 1, 2} - used).pop()
            visited_tri.add(nb)
            q.append(nb)

    return colors


def choose_guards_from_coloring(colors: Dict[int, int]) -> List[int]:
    buckets: Dict[int, List[int]] = {0: [], 1: [], 2: []}
    for v, c in colors.items():
        buckets[c].append(v)
    pick = min(buckets.keys(), key=lambda k: len(buckets[k]))
    return sorted(buckets[pick])
