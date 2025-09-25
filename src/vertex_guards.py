# Vertex guards selection from 3-coloring (choose minimal color class).

# GroupID-23 (22114047_22114081_22114098) - Khushal Agrawal, Rushit Pancholi and Vraj Tamkuwala
# Date: 25 Sept, 2025
# vertex_guards.py - Highlights chosen guard vertices visibly on the canvas.


class VertexGuardsApp:
    def __init__(self, canvas, dcel, three_coloring_app):
        self.canvas = canvas
        self.dcel = dcel
        self.three_coloring_app = three_coloring_app
        self.canvas_width = 500
        self.canvas_height = 500
        self.padding = 50
        self.origin_x = self.padding
        self.origin_y = self.canvas_height - self.padding

    def decide_vertex_guards(self):
        y_count = 0
        g_count = 0
        p_count = 0

        yellow_vertices = []
        green_vertices = []
        pink_vertices = []

        self.canvas.delete("all")
        self.three_coloring_app.dual_graph_app.triangulation_app.monotone_app.trapezoidal_app.polygon_app.draw_axes()
        self.three_coloring_app.dual_graph_app.triangulation_app.monotone_app.trapezoidal_app.polygon_app.draw_polygon_without_delay()

        # Count colors using the hex palette defined in three_coloring
        YELLOW = "#b58900"
        GREEN = "#228b22"
        PINK = "#d33682"

        for k in self.three_coloring_app.colored_vertices:
            if self.three_coloring_app.colored_vertices[k] == YELLOW:
                y_count += 1
                yellow_vertices.append(k)
            elif self.three_coloring_app.colored_vertices[k] == GREEN:
                g_count += 1
                green_vertices.append(k)
            else:
                p_count += 1
                pink_vertices.append(k)

        if y_count <= g_count and y_count <= p_count:
            min_color = YELLOW
            min_color_vertices = yellow_vertices
        elif g_count <= p_count:
            min_color = GREEN
            min_color_vertices = green_vertices
        else:
            min_color = PINK
            min_color_vertices = pink_vertices

        for k in min_color_vertices:
            self.draw_guard_vertex(k, min_color)

    def draw_guard_vertex(self, vertex, color):
        adjusted_x = self.origin_x + vertex.x
        adjusted_y = self.origin_y - vertex.y
        r = 9
        # Use a bright, highly visible guard color regardless of three-coloring
        GUARD_COLOR = "#ff0000"
        self.canvas.create_oval(
            adjusted_x - r,
            adjusted_y - r,
            adjusted_x + r,
            adjusted_y + r,
            fill=GUARD_COLOR,
        )
        # Inner contrast dot
        self.canvas.create_oval(
            adjusted_x - 3,
            adjusted_y - 3,
            adjusted_x + 3,
            adjusted_y + 3,
            fill="#ffffff",
        )
        self.canvas.update()
