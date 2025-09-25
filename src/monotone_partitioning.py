# Monotone partitioning step (adds diagonals to make y-monotone pieces).
#
# GroupID-23 (22114047_22114081_22114098) - Khushal Agrawal, Rushit Pancholi and Vraj Tamkuwala
# Date: 25 Sept, 2025
# monotone_partitioning.py - Finds supporting vertices and draws diagonals.
#

import time


class MonotonePartitioningApp:
    def __init__(self, canvas, dcel, trapezoidal_app):
        self.canvas = canvas
        self.dcel = dcel
        self.trapezoidal_app = trapezoidal_app
        self.canvas_width = 500
        self.canvas_height = 500
        self.padding = 50
        self.origin_x = self.padding
        self.origin_y = self.canvas_height - self.padding

    def draw_monotone_partitioning(self):
        vertices = sorted(self.dcel.vertices, key=lambda v: v.y, reverse=True)
        vertex_types = self.dcel.find_vertices()
        for vertex in vertices:
            if vertex in vertex_types["min_cusp_vertices"]:
                self.handle_min_cusp(vertex)
            elif vertex in vertex_types["max_cusp_vertices"]:
                self.handle_max_cusp(vertex)
            self.trapezoidal_app.remove_horizontal_line(vertex)
            self.canvas.update()
            time.sleep(0.4)

    def handle_min_cusp(self, vertex):
        supporting_vertex_below = self.find_supporting_vertex_below(vertex)
        if supporting_vertex_below:
            self.draw_diagonal(vertex, supporting_vertex_below)

    def handle_max_cusp(self, vertex):
        supporting_vertex_above = self.find_supporting_vertex_above(vertex)
        if supporting_vertex_above:
            self.draw_diagonal(vertex, supporting_vertex_above)

    def find_supporting_vertex_below(self, vertex):
        vertices_below = sorted(
            [v for v in self.dcel.vertices if v.y < vertex.y],
            key=lambda v: v.y,
            reverse=True,
        )
        for v in vertices_below:
            if self.is_visible(vertex, v):
                return v
        return None

    def find_supporting_vertex_above(self, vertex):
        vertices_above = sorted(
            [v for v in self.dcel.vertices if v.y > vertex.y], key=lambda v: v.y
        )
        for v in vertices_above:
            if self.is_visible(vertex, v):
                return v
        return None

    def is_visible(self, vertex1, vertex2):
        for i in range(len(self.dcel.vertices)):
            start_vertex = self.dcel.vertices[i]
            end_vertex = self.dcel.vertices[(i + 1) % len(self.dcel.vertices)]
            if (
                vertex1 != start_vertex
                and vertex1 != end_vertex
                and vertex2 != start_vertex
                and vertex2 != end_vertex
            ):
                if self.segments_intersect(vertex1, vertex2, start_vertex, end_vertex):
                    return False
        return True

    def segments_intersect(self, p1, p2, p3, p4):
        def orientation(p, q, r):
            val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
            if val == 0:
                return 0
            return 1 if val > 0 else 2

        def on_segment(p, q, r):
            return (
                q.x <= max(p.x, r.x)
                and q.x >= min(p.x, r.x)
                and q.y <= max(p.y, r.y)
                and q.y >= min(p.y, r.y)
            )

        o1 = orientation(p1, p2, p3)
        o2 = orientation(p1, p2, p4)
        o3 = orientation(p3, p4, p1)
        o4 = orientation(p3, p4, p2)

        if o1 != o2 and o3 != o4:
            return True
        if o1 == 0 and on_segment(p1, p3, p2):
            return True
        if o2 == 0 and on_segment(p1, p4, p2):
            return True
        if o3 == 0 and on_segment(p3, p1, p4):
            return True
        if o4 == 0 and on_segment(p3, p2, p4):
            return True
        return False

    def draw_diagonal(self, vertex1, vertex2):
        x1, y1 = vertex1.x, vertex1.y
        x2, y2 = vertex2.x, vertex2.y

        adjusted_x1 = self.origin_x + x1
        adjusted_y1 = self.origin_y - y1
        adjusted_x2 = self.origin_x + x2
        adjusted_y2 = self.origin_y - y2

        self.canvas.create_line(
            adjusted_x1,
            adjusted_y1,
            adjusted_x2,
            adjusted_y2,
            fill="#808080",
            dash=(4, 3),
        )
        self.dcel.add_diagonal(vertex1, vertex2)

    def draw_diagonal_only(self, vertex1, vertex2):
        x1, y1 = vertex1.x, vertex1.y
        x2, y2 = vertex2.x, vertex2.y

        adjusted_x1 = self.origin_x + x1
        adjusted_y1 = self.origin_y - y1
        adjusted_x2 = self.origin_x + x2
        adjusted_y2 = self.origin_y - y2

        self.canvas.create_line(
            adjusted_x1,
            adjusted_y1,
            adjusted_x2,
            adjusted_y2,
            fill="#808080",
            dash=(4, 3),
        )
        self.canvas.update()
        time.sleep(0.4)
