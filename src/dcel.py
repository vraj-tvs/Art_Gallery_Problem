"""
src/dcel.py

- This is a minimal DCEL sufficient to represent a single simple polygon boundary (one interior face).
- Each polygon vertex has an incident_edge pointing to the outgoing half-edge.
- We do not create twin edges for the exterior face (not needed for our triangulation pipeline). The DCEL is extendable if you want to store more topology later.
"""

from __future__ import annotations
from typing import Optional, List, Tuple


class Vertex:
    """A DCEL vertex."""

    def __init__(self, x: float, y: float, idx: int) -> None:
        self.x: float = float(x)
        self.y: float = float(y)
        self.incident_edge: Optional[HalfEdge] = None
        self.idx: int = idx

    def coords(self) -> Tuple[float, float]:
        return (self.x, self.y)

    def __repr__(self) -> str:
        return f"V{self.idx}({self.x:.3f},{self.y:.3f})"


class HalfEdge:
    """A half-edge in DCEL."""

    def __init__(self) -> None:
        self.origin: Optional[Vertex] = None
        self.twin: Optional[HalfEdge] = None
        self.next: Optional[HalfEdge] = None
        self.prev: Optional[HalfEdge] = None
        self.face: Optional[Face] = None

    def __repr__(self) -> str:
        o = self.origin.idx if self.origin else None
        n = self.next.origin.idx if self.next and self.next.origin else None
        return f"HE(origin={o}, next_origin={n})"


class Face:
    """A face in DCEL."""

    def __init__(self, fid: int) -> None:
        self.fid: int = fid
        self.outer_component: Optional[HalfEdge] = None
        self.inner_components: List[HalfEdge] = []

    def __repr__(self) -> str:
        return f"Face({self.fid})"


class DCEL:
    """Minimal DCEL implementation for a simple polygon."""

    def __init__(self) -> None:
        self.vertices: List[Vertex] = []
        self.half_edges: List[HalfEdge] = []
        self.faces: List[Face] = []

    @staticmethod
    def from_polygon(points: List[Tuple[float, float]]) -> DCEL:
        dcel = DCEL()
        n = len(points)

        for i, (x, y) in enumerate(points):
            dcel.vertices.append(Vertex(x, y, i))

        hes: List[HalfEdge] = [HalfEdge() for _ in range(n)]
        for i in range(n):
            he = hes[i]
            he.origin = dcel.vertices[i]
            dcel.vertices[i].incident_edge = he
            he.next = hes[(i + 1) % n]
            he.prev = hes[(i - 1) % n]
            dcel.half_edges.append(he)

        interior_face = Face(fid=0)
        interior_face.outer_component = hes[0]
        for he in hes:
            he.face = interior_face

        dcel.faces.append(interior_face)
        return dcel

    def boundary_vertex_indices(self) -> List[int]:
        if not self.half_edges:
            return []
        start = self.half_edges[0]
        res: List[int] = []
        he: Optional[HalfEdge] = start
        while he is not None:
            if he.origin:
                res.append(he.origin.idx)
            he = he.next
            if he is start:
                break
        return res

    def coords_list(self) -> List[Tuple[float, float]]:
        return [v.coords() for v in self.vertices]

    def __repr__(self) -> str:
        return f"DCEL(V={len(self.vertices)}, HE={len(self.half_edges)}, F={len(self.faces)})"
