# src/dual_graph.py
from typing import List, Tuple, Dict, Set


def build_triangle_adjacency(
    triangles: List[Tuple[int, int, int]],
) -> Dict[int, Set[int]]:
    """
    Build adjacency of triangles (dual graph). Output: mapping triangle_idx -> set(neighbor_triangle_idx).
    Two triangles are adjacent if they share an edge (i.e., share two vertex indices).
    """
    edge_map: Dict[Tuple[int, int], int] = {}  # canonical edge -> triangle idx
    adjacency: Dict[int, Set[int]] = {i: set() for i in range(len(triangles))}
    for tidx, tri in enumerate(triangles):
        verts = list(tri)
        edges = [(verts[0], verts[1]), (verts[1], verts[2]), (verts[2], verts[0])]
        for a, b in edges:
            key = (min(a, b), max(a, b))
            if key in edge_map:
                other = edge_map[key]
                adjacency[tidx].add(other)
                adjacency[other].add(tidx)
            else:
                edge_map[key] = tidx
    return adjacency
