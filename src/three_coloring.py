# Three-coloring of triangulation vertices (DFS-based assignment).

# GroupID-23 (22114047_22114081_22114098) - Khushal Agrawal, Rushit Pancholi and Vraj Tamkuwala
# Date: 25 Sept, 2025
# three_coloring.py - Assigns colors ensuring adjacent vertices differ.

import time


class ThreeColoringApp:
    def __init__(self, canvas, dcel, dual_graph_app):
        self.canvas = canvas
        self.dcel = dcel
        self.dual_graph_app = dual_graph_app
        self.canvas_width = 500
        self.canvas_height = 500
        self.padding = 50
        self.origin_x = self.padding
        self.origin_y = self.canvas_height - self.padding
        self.face_and_vertices = {}
        self.colored_vertices = {}

    def coloring_dfs(self, current_face, visited_faces, graph):
        if current_face in visited_faces:
            return
        visited_faces.append(current_face)
        vertex1 = self.face_and_vertices[current_face][0]
        vertex2 = self.face_and_vertices[current_face][1]
        vertex3 = self.face_and_vertices[current_face][2]

        if (
            vertex1 not in self.colored_vertices
            and vertex2 not in self.colored_vertices
            and vertex3 not in self.colored_vertices
        ):
            self.colored_vertices[vertex1] = "#b58900"  # darker yellow
            self.colored_vertices[vertex2] = "#228b22"  # forest green
            self.colored_vertices[vertex3] = "#d33682"  # deep pink/magenta
        elif vertex1 not in self.colored_vertices:
            colors_list = ["#b58900", "#228b22", "#d33682"]
            for color in colors_list:
                if (
                    self.colored_vertices[vertex2] != color
                    and self.colored_vertices[vertex3] != color
                ):
                    self.colored_vertices[vertex1] = color
        elif vertex2 not in self.colored_vertices:
            colors_list = ["#b58900", "#228b22", "#d33682"]
            for color in colors_list:
                if (
                    self.colored_vertices[vertex1] != color
                    and self.colored_vertices[vertex3] != color
                ):
                    self.colored_vertices[vertex2] = color
        elif vertex3 not in self.colored_vertices:
            colors_list = ["#b58900", "#228b22", "#d33682"]
            for color in colors_list:
                if (
                    self.colored_vertices[vertex2] != color
                    and self.colored_vertices[vertex1] != color
                ):
                    self.colored_vertices[vertex3] = color

        for child_faces in graph[current_face]:
            self.coloring_dfs(child_faces, visited_faces, graph)

    def three_color_triangulation(self):
        for face in self.dcel.faces:
            looping_edge = face.outer_half_edge
            starting_vertex = looping_edge.origin
            vertex_list = []

            while True:
                vertex_list.append(looping_edge.origin)
                looping_edge = looping_edge.next
                if looping_edge.origin == starting_vertex:
                    break

            self.face_and_vertices[face] = vertex_list

        visited_faces = []
        starting_face = self.dcel.faces[0]
        self.coloring_dfs(starting_face, visited_faces, self.dual_graph_app.graph)
        for k in self.colored_vertices:
            self.color_vertex(k, self.colored_vertices[k])

    def color_vertex(self, vertex, color):
        adjusted_x = self.origin_x + vertex.x
        adjusted_y = self.origin_y - vertex.y
        self.canvas.create_oval(
            adjusted_x - 5, adjusted_y - 5, adjusted_x + 5, adjusted_y + 5, fill=color
        )
        self.canvas.update()
        time.sleep(0.4)
