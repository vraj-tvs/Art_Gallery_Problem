# src/dcel.py
from __future__ import annotations
from typing import Optional, List, Tuple


class Vertex:
    """A DCEL vertex."""

    def __init__(self, x: float, y: float, idx: int):
        self.x = float(x)
        self.y = float(y)
        self.incident_edge: Optional[HalfEdge] = None
        self.idx = idx  # unique integer id

    def coords(self) -> Tuple[float, float]:
        return (self.x, self.y)

    def __repr__(self):
        return f"V{self.idx}({self.x:.3f},{self.y:.3f})"


class HalfEdge:
    """A half-edge in DCEL. For polygon boundary we will create one half-edge per directed boundary edge."""

    def __init__(self):
        self.origin: Optional[Vertex] = None
        self.twin: Optional[HalfEdge] = None
        self.next: Optional[HalfEdge] = None
        self.prev: Optional[HalfEdge] = None
        self.face: Optional[Face] = None

    def __repr__(self):
        o = self.origin.idx if self.origin else None
        n = self.next.origin.idx if self.next and self.next.origin else None
        return f"HE(origin={o}, next_origin={n})"


class Face:
    """A face in DCEL. For simple polygon we will have one interior face and one exterior face."""

    def __init__(self, fid: int):
        self.fid = fid
        self.outer_component: Optional[HalfEdge] = None
        self.inner_components: List[HalfEdge] = []

    def __repr__(self):
        return f"Face({self.fid})"


class DCEL:
    """Minimal DCEL implementation sufficient for representing a simple polygon boundary.
    This stores vertices and boundary half-edges and one interior face."""

    def __init__(self):
        self.vertices: List[Vertex] = []
        self.half_edges: List[HalfEdge] = []
        self.faces: List[Face] = []

    @staticmethod
    def from_polygon(points: List[Tuple[float, float]]) -> DCEL:
        """
        Build DCEL from a simple polygon given as list of (x,y) in order (CW or CCW).
        The DCEL will contain one interior face and the boundary half-edges.
        """
        dcel = DCEL()
        n = len(points)
        # create vertices
        for i, (x, y) in enumerate(points):
            dcel.vertices.append(Vertex(x, y, i))

        # create halfedges for boundary (one halfedge per directed edge)
        hes = [HalfEdge() for _ in range(n)]
        for i in range(n):
            he = hes[i]
            he.origin = dcel.vertices[i]
            dcel.vertices[i].incident_edge = he
            he.next = hes[(i + 1) % n]
            he.prev = hes[(i - 1) % n]
            dcel.half_edges.append(he)

        # we don't create explicit twin half-edges for the exterior (they remain None)
        interior_face = Face(fid=0)
        interior_face.outer_component = hes[0]
        # assign face to boundary half-edges
        for he in hes:
            he.face = interior_face

        dcel.faces.append(interior_face)
        return dcel

    def boundary_vertex_indices(self) -> List[int]:
        """Return indices of boundary vertices in order following half-edge links."""
        if not self.half_edges:
            return []
        start = self.half_edges[0]
        res = []
        he = start
        while True:
            res.append(he.origin.idx)
            he = he.next
            if he is start:
                break
        return res

    def coords_list(self) -> List[Tuple[float, float]]:
        return [v.coords() for v in self.vertices]

    def __repr__(self):
        return f"DCEL(V={len(self.vertices)}, HE={len(self.half_edges)}, F={len(self.faces)})"
