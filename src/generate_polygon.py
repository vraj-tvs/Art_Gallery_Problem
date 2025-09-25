# Polygon generation utilities and UI drawing.
#
# GroupID-23 (22114047_22114081_22114098) - Khushal Agrawal, Rushit Pancholi and Vraj Tamkuwala
# Date: 25 Sept, 2025
# generate_polygon.py - Generates a simple polygon and renders axes/edges.


import random
import time
import math
import tkinter as tk
from tkinter import simpledialog

from dcel import DCEL


class GeneratePolygonApp:
    def __init__(self, canvas):
        self.canvas = canvas
        self.points = []
        self.num_vertices = 0
        self.canvas_width = 500
        self.canvas_height = 500
        self.padding = 50
        self.axis_length = self.canvas_width - 2 * self.padding
        self.dcel = DCEL()

    def generate_polygon(self):
        self.num_vertices = simpledialog.askinteger(
            "Input", "Enter number of vertices (n):", minvalue=3, maxvalue=100
        )
        if self.num_vertices:
            self.canvas.delete("all")
            self.draw_axes()
            self.points = self.generate_random_points(self.num_vertices)
            self.points = self.check_for_invalid_edges(self.points)
            centroid = self.calculate_centroid(self.points)
            self.points = self.sort_points_anticlockwise(self.points, centroid)

            self.dcel.construct_polygon(self.points)
            self.draw_polygon_with_delay()

    def generate_polygon_with_n(self, n: int):
        if n and n >= 3:
            self.num_vertices = n
            self.canvas.delete("all")
            self.draw_axes()
            self.points = self.generate_random_points(self.num_vertices)
            self.points = self.check_for_invalid_edges(self.points)
            centroid = self.calculate_centroid(self.points)
            self.points = self.sort_points_anticlockwise(self.points, centroid)
            self.dcel.construct_polygon(self.points)
            self.draw_polygon_with_delay()

    def draw_axes(self):
        origin_x = self.padding
        origin_y = self.canvas_height - self.padding

        self.canvas.create_line(
            origin_x,
            origin_y,
            origin_x + self.axis_length,
            origin_y,
            fill="black",
            arrow=tk.LAST,
        )
        self.canvas.create_line(
            origin_x,
            origin_y,
            origin_x,
            origin_y - self.axis_length,
            fill="black",
            arrow=tk.LAST,
        )

        self.canvas.create_text(
            origin_x + self.axis_length + 10,
            origin_y + 10,
            text="X",
            fill="black",
            font=("Arial", 10),
        )
        self.canvas.create_text(
            origin_x - 10,
            origin_y - self.axis_length - 10,
            text="Y",
            fill="black",
            font=("Arial", 10),
        )

    def generate_random_points(self, n):
        points = set()
        x_coords = set()
        y_coords = set()

        while len(points) < n:
            x = random.randint(0, self.axis_length)
            y = random.randint(0, self.axis_length)

            if x not in x_coords and y not in y_coords:
                points.add((x, y))
                x_coords.add(x)
                y_coords.add(y)

        return list(points)

    def check_for_invalid_edges(self, points):
        def has_invalid_edge(p1, p2):
            return p1[0] == p2[0] or p1[1] == p2[1]

        valid_points = points.copy()
        for i in range(len(points)):
            current_point = points[i]
            next_point = points[(i + 1) % len(points)]
            if has_invalid_edge(current_point, next_point):
                while has_invalid_edge(current_point, next_point):
                    next_point = (
                        random.randint(0, self.axis_length),
                        random.randint(0, self.axis_length),
                    )
                    if next_point not in valid_points:
                        valid_points[i] = next_point

        return valid_points

    def calculate_centroid(self, points):
        x_coords = [p[0] for p in points]
        y_coords = [p[1] for p in points]
        centroid_x = sum(x_coords) / len(points)
        centroid_y = sum(y_coords) / len(points)
        return (centroid_x, centroid_y)

    def sort_points_anticlockwise(self, points, centroid):
        def angle_from_centroid(point):
            return math.atan2(point[1] - centroid[1], point[0] - centroid[0])

        return sorted(points, key=angle_from_centroid)

    def draw_polygon_with_delay(self):
        origin_x = self.padding
        origin_y = self.canvas_height - self.padding

        for i in range(len(self.points)):
            x, y = self.points[i]
            adjusted_x = origin_x + x
            adjusted_y = origin_y - y

            self.canvas.create_oval(
                adjusted_x - 3,
                adjusted_y - 3,
                adjusted_x + 3,
                adjusted_y + 3,
                fill="black",
            )
            self.canvas.create_text(
                adjusted_x + 10,
                adjusted_y - 10,
                text=f"({x}, {y})",
                fill="black",
                font=("Arial", 5),
            )

            self.canvas.update()
            time.sleep(0.4)

            next_point = self.points[(i + 1) % len(self.points)]
            adjusted_next_x = origin_x + next_point[0]
            adjusted_next_y = origin_y - next_point[1]
            self.canvas.create_line(
                adjusted_x, adjusted_y, adjusted_next_x, adjusted_next_y, fill="black"
            )

            self.canvas.update()

    def draw_polygon_without_delay(self):
        origin_x = self.padding
        origin_y = self.canvas_height - self.padding

        for i in range(len(self.points)):
            x, y = self.points[i]
            adjusted_x = origin_x + x
            adjusted_y = origin_y - y

            self.canvas.create_oval(
                adjusted_x - 3,
                adjusted_y - 3,
                adjusted_x + 3,
                adjusted_y + 3,
                fill="black",
            )
            self.canvas.create_text(
                adjusted_x + 10,
                adjusted_y - 10,
                text=f"({x}, {y})",
                fill="black",
                font=("Arial", 5),
            )
            self.canvas.update()

            next_point = self.points[(i + 1) % len(self.points)]
            adjusted_next_x = origin_x + next_point[0]
            adjusted_next_y = origin_y - next_point[1]
            self.canvas.create_line(
                adjusted_x, adjusted_y, adjusted_next_x, adjusted_next_y, fill="black"
            )
            self.canvas.update()
