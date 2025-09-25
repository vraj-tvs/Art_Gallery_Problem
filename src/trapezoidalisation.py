# Trapezoidalization via horizontal sweep lines through vertices.

# GroupID-23 (22114047_22114081_22114098) - Khushal Agrawal, Rushit Pancholi and Vraj Tamkuwala
# Date: 25 Sept, 2025
# trapezoidalisation.py - Draws horizontal helper lines during sweep.


import time


class TrapezoidalisationApp:
    def __init__(self, canvas, dcel, polygon_app):
        self.canvas = canvas
        self.dcel = dcel
        self.polygon_app = polygon_app
        self.canvas_width = 500
        self.canvas_height = 500
        self.padding = 50
        self.origin_x = self.padding
        self.origin_y = self.canvas_height - self.padding
        self.horizontal_lines = []

    def draw_trapezoidalisation(self):
        vertices = sorted(self.dcel.vertices, key=lambda v: v.y, reverse=True)

        for vertex in vertices:
            self.draw_horizontal_line(vertex)
            self.canvas.update()
            time.sleep(0.4)

    def draw_horizontal_line(self, vertex):
        x1 = 0
        x2 = self.canvas_width - 2 * self.padding

        adjusted_y = self.origin_y - vertex.y
        line_id = self.canvas.create_line(
            self.origin_x + x1,
            adjusted_y,
            self.origin_x + x2,
            adjusted_y,
            fill="blue",
            dash=(4, 2),
        )
        self.horizontal_lines.append(line_id)

    def remove_horizontal_line(self, vertex):
        if self.horizontal_lines:
            line_id = self.horizontal_lines.pop(0)
            self.canvas.delete(line_id)

    def reset_canvas(self):
        for line_id in self.horizontal_lines:
            self.canvas.delete(line_id)
        self.horizontal_lines.clear()
