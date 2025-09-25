# Dual graph construction over triangulation faces.
#
# GroupID-23 (22114047_22114081_22114098) - Khushal Agrawal, Rushit Pancholi and Vraj Tamkuwala
# Date: 25 Sept, 2025
# dual_graph.py - Builds dual graph by connecting triangle centroids.

import time


class DualGraphApp:
    def __init__(self, canvas, dcel, triangulation_app):
        self.canvas = canvas
        self.dcel = dcel
        self.triangulation_app = triangulation_app
        self.canvas_width = 500
        self.canvas_height = 500
        self.padding = 50
        self.origin_x = self.padding
        self.origin_y = self.canvas_height - self.padding
        self.axis_length = self.canvas_width - 2 * self.padding
        self.graph = {}

    def transform_coordinates(self, x, y):
        transformed_x = self.origin_x + x
        transformed_y = self.origin_y - y
        return transformed_x, transformed_y

    def create_dual_graph(self):
        centroids = {}

        for face in self.dcel.faces:
            if face.outer_half_edge:
                vertices = []
                half_edge = face.outer_half_edge
                start_edge = half_edge
                while True:
                    origin = half_edge.origin
                    vertices.append((origin.x, origin.y))
                    half_edge = half_edge.next
                    if half_edge == start_edge:
                        break

                centroid_x = sum(v[0] for v in vertices) / 3.0
                centroid_y = sum(v[1] for v in vertices) / 3.0
                centroids[face] = (centroid_x, centroid_y)

                transformed_centroid_x, transformed_centroid_y = (
                    self.transform_coordinates(centroid_x, centroid_y)
                )
                self.draw_point(transformed_centroid_x, transformed_centroid_y)

        for face in self.dcel.faces:
            if face.outer_half_edge:
                half_edge = face.outer_half_edge
                start_edge = half_edge
                while True:
                    twin_edge = half_edge.twin
                    if twin_edge and twin_edge.incident_face in centroids:
                        centroid1 = centroids[face]
                        centroid2 = centroids[twin_edge.incident_face]

                        transformed_centroid1 = self.transform_coordinates(
                            centroid1[0], centroid1[1]
                        )
                        transformed_centroid2 = self.transform_coordinates(
                            centroid2[0], centroid2[1]
                        )

                        self.draw_line(transformed_centroid1, transformed_centroid2)
                        if face not in self.graph:
                            self.graph[face] = []
                        if twin_edge.incident_face not in self.graph:
                            self.graph[twin_edge.incident_face] = []

                        self.graph[face].append(twin_edge.incident_face)
                        self.graph[twin_edge.incident_face].append(face)

                    half_edge = half_edge.next
                    if half_edge == start_edge:
                        break

    def draw_point(self, x, y, radius=3, color="black"):
        self.canvas.create_oval(
            x - radius, y - radius, x + radius, y + radius, fill=color
        )
        self.canvas.update()
        time.sleep(0.4)

    def draw_line(self, point1, point2, color="black"):
        self.canvas.create_line(point1[0], point1[1], point2[0], point2[1], fill=color)
        self.canvas.update()
        time.sleep(0.4)
