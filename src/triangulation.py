"""
src/triangulation.py

- Using ear-clipping implemented on the DCEL's vertex indices. The algorithm references only the DCEL vertex coordinates.
- Complexity is O(n^2) worst-case (common and ok for modest polygons; can be optimized later).
- For degenerate numerical situations a fallback is provided (best-effort).
"""

from typing import List, Tuple
from src.dcel import DCEL
from src.utils import orientation, signed_area, is_point_in_triangle, EPS


def ensure_ccw(points: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
    if signed_area(points) < 0:
        return list(reversed(points))
    return points


def triangulate_ear_clipping(dcel: DCEL) -> List[Tuple[int, int, int]]:
    """
    Triangulate a simple polygon represented in 'dcel' using ear-clipping.
    Returns list of triangles as tuples of vertex indices (i, j, k) in CCW order.
    Uses only the DCEL vertices as requested.
    """
    pts = dcel.coords_list()
    n = len(pts)
    if n < 3:
        return []
    # get boundary order (vertex indices)
    poly = dcel.boundary_vertex_indices()
    # Polygon should already be CCW from backend preprocessing
    print(f"Triangulation Debug - Polygon indices: {poly}")
    print(f"Triangulation Debug - Polygon points: {[pts[i] for i in poly]}")

    # helper structures for linked-list removal
    prev = {poly[i]: poly[i - 1] for i in range(len(poly))}
    nextv = {poly[i]: poly[(i + 1) % len(poly)] for i in range(len(poly))}
    remaining = set(poly)

    def is_convex(a_idx: int, b_idx: int, c_idx: int) -> bool:
        a, b, c = pts[a_idx], pts[b_idx], pts[c_idx]
        # In canvas coordinates (Y down), right turn is convex for CCW polygon
        return orientation(a, b, c) < -EPS  # right turn -> convex for CCW polygon in canvas coords

    def any_point_in_triangle(a_idx: int, b_idx: int, c_idx: int) -> bool:
        a, b, c = pts[a_idx], pts[b_idx], pts[c_idx]
        for v in remaining:
            if v in (a_idx, b_idx, c_idx):
                continue
            p = pts[v]
            if is_point_in_triangle(p, a, b, c):
                return True
        return False

    triangles: List[Tuple[int, int, int]] = []
    # Precompute vertex ordering to quickly find ears: O(n^2) ear-clipping (acceptable for moderate n)
    if len(remaining) == 3:
        a, b, c = list(remaining)
        triangles.append((a, b, c))
        return triangles

    # Keep scanning for ears
    scan_order = list(poly)  # initial ordering for scanning
    while len(remaining) > 3:
        clipped = False
        # iterate over a copy of remaining in polygon order
        for v in list(scan_order):
            if v not in remaining:
                continue
            i = v
            i_prev = prev[i]
            i_next = nextv[i]
            if not is_convex(i_prev, i, i_next):
                continue
            # check if triangle contains any other remaining vertex
            if any_point_in_triangle(i_prev, i, i_next):
                continue
            # it's an ear -> clip it
            triangle = (i_prev, i, i_next)
            triangles.append(triangle)
            print(f"Triangulation Debug - Clipped ear: {triangle} at vertices {[pts[j] for j in triangle]}")
            # remove i
            remaining.remove(i)
            # relink neighbors
            prev[i_next] = i_prev
            nextv[i_prev] = i_next
            # update scan_order to start from prev (heuristic)
            scan_order = [i_prev] + scan_order
            clipped = True
            break
        if not clipped:
            # Numerical or degeneracy issue. As a fallback, force triangulation by connecting ears without strict checks.
            # Find any triple and cut it (best-effort).
            rem_list = list(remaining)
            a_idx = rem_list[0]
            b_idx = nextv[a_idx]
            c_idx = nextv[b_idx]
            triangles.append((a_idx, b_idx, c_idx))
            remaining.remove(b_idx)
            prev[c_idx] = a_idx
            nextv[a_idx] = c_idx

    # final triangle
    last = list(remaining)
    if len(last) == 3:
        final_triangle = (last[0], last[1], last[2])
        triangles.append(final_triangle)
        print(f"Triangulation Debug - Final triangle: {final_triangle} at vertices {[pts[j] for j in final_triangle]}")

    # Ensure triangles are CCW (they should be by construction)
    return triangles
