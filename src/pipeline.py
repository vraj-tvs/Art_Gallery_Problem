# High-level pipeline orchestrating all algorithmic steps.

# GroupID-23 (22114047_22114081_22114098) - Khushal Agrawal, Rushit Pancholi and Vraj Tamkuwala
# Date: 25 Sept, 2025
# pipeline.py - Wires polygon generation, trapezoidalization, monotone partitioning,
# triangulation, dual graph, three-coloring, and vertex guards.
#

from typing import Optional

import generate_polygon as generate_polygon_module
import trapezoidalisation as trapezoidalisation_module
import monotone_partitioning as monotone_partitioning_module
import triangulation as triangulation_module
import dual_graph as dual_graph_module
import three_coloring as three_coloring_module
import vertex_guards as vertex_guards_module


class ArtGalleryPipeline:
    """High-level orchestrator for the art gallery problem steps.

    This class composes the existing modules into a cohesive pipeline while
    keeping their internal logic unchanged.
    """

    def __init__(self, canvas):
        self.canvas = canvas
        self.polygon_app: Optional[generate_polygon_module.GeneratePolygonApp] = None
        self.trapezoidal_app: Optional[
            trapezoidalisation_module.TrapezoidalisationApp
        ] = None
        self.monotone_app: Optional[
            monotone_partitioning_module.MonotonePartitioningApp
        ] = None
        self.triangulation_app: Optional[triangulation_module.TriangulationApp] = None
        self.dual_graph_app: Optional[dual_graph_module.DualGraphApp] = None
        self.three_coloring_app: Optional[three_coloring_module.ThreeColoringApp] = None
        self.vertex_guards_app: Optional[vertex_guards_module.VertexGuardsApp] = None

    # Steps
    def step_generate_polygon(self) -> bool:
        self.polygon_app = generate_polygon_module.GeneratePolygonApp(self.canvas)
        self.polygon_app.generate_polygon()
        if not self.polygon_app or not self.polygon_app.dcel:
            return False
        self.polygon_app.dcel.display()
        return True

    def step_trapezoidalisation(self) -> bool:
        if not self.polygon_app or not self.polygon_app.dcel:
            return False
        self.trapezoidal_app = trapezoidalisation_module.TrapezoidalisationApp(
            self.canvas, self.polygon_app.dcel, self.polygon_app
        )
        self.trapezoidal_app.draw_trapezoidalisation()
        return True

    def step_monotone_partitioning(self) -> bool:
        if not self.polygon_app or not self.polygon_app.dcel:
            return False
        self.monotone_app = monotone_partitioning_module.MonotonePartitioningApp(
            self.canvas, self.polygon_app.dcel, self.trapezoidal_app
        )
        self.monotone_app.draw_monotone_partitioning()
        return True

    def step_triangulation(self) -> bool:
        if not self.polygon_app or not self.polygon_app.dcel:
            return False
        self.triangulation_app = triangulation_module.TriangulationApp(
            self.canvas, self.polygon_app.dcel, self.monotone_app
        )
        self.triangulation_app.triangulate_polygon()
        return True

    def step_dual_graph(self) -> bool:
        if not self.polygon_app or not self.polygon_app.dcel:
            return False
        self.dual_graph_app = dual_graph_module.DualGraphApp(
            self.canvas, self.polygon_app.dcel, self.triangulation_app
        )
        self.dual_graph_app.create_dual_graph()
        return True

    def step_three_coloring(self) -> bool:
        if not self.polygon_app or not self.polygon_app.dcel:
            return False
        self.three_coloring_app = three_coloring_module.ThreeColoringApp(
            self.canvas, self.polygon_app.dcel, self.dual_graph_app
        )
        self.three_coloring_app.three_color_triangulation()
        return True

    # Convenience for web UI
    def step_generate_polygon_with_n(self, n: int) -> bool:
        self.polygon_app = generate_polygon_module.GeneratePolygonApp(self.canvas)
        self.polygon_app.generate_polygon_with_n(n)
        if not self.polygon_app or not self.polygon_app.dcel:
            return False
        return True

    def step_vertex_guards(self) -> bool:
        if not self.polygon_app or not self.polygon_app.dcel:
            return False
        self.vertex_guards_app = vertex_guards_module.VertexGuardsApp(
            self.canvas, self.polygon_app.dcel, self.three_coloring_app
        )
        self.vertex_guards_app.decide_vertex_guards()
        return True
