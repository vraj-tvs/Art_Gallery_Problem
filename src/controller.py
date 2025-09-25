# GroupID-23 (22114047_22114081_22114098) - Khushal Agrawal, Rushit Pancholi and Vraj Tamkuwala
# Date: 25 Sept, 2025
# controller.py - Tkinter desktop GUI controller wiring the algorithm pipeline to UI widgets

import tkinter as tk
from tkinter import messagebox

from pipeline import ArtGalleryPipeline
from ui import Toolbar, CanvasPanel, ThemeManager, HeaderBar, StatusBar


class ArtGalleryController:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Optimal Street Light PLacement")
        self.root.geometry("900x650")
        self.root.resizable(False, False)

        # Theme setup
        self.theme = ThemeManager(self.root)

        # Layout
        self.header = HeaderBar(self.root, "Optimal Street Light PLacement")
        self.canvas_panel = CanvasPanel(self.root)
        self.toolbar = Toolbar(self.root)
        self.status = StatusBar(self.root)

        self.pipeline = ArtGalleryPipeline(self.canvas_panel.widget())

        # Build buttons
        self.toolbar.add_button(
            "generate",
            "Generate Street Light PLacement",
            self.on_generate,
            enabled=True,
        )
        self.toolbar.add_button(
            "trapezoidal", "Trapezoidalisation", self.on_trapezoidal, enabled=False
        )
        self.toolbar.add_button(
            "monotone", "Monotone Partitioning", self.on_monotone, enabled=False
        )
        self.toolbar.add_button(
            "triangulation", "Triangulation", self.on_triangulation, enabled=False
        )
        self.toolbar.add_button(
            "dual_graph", "Dual Graph", self.on_dual_graph, enabled=False
        )
        self.toolbar.add_button(
            "three_coloring", "3 Coloring", self.on_three_coloring, enabled=False
        )
        self.toolbar.add_button(
            "vertex_guards", "Vertex Guards", self.on_vertex_guards, enabled=False
        )

    # State helpers
    def _advance(self, next_key: str | None = None):
        self.toolbar.disable_all()
        self.toolbar.enable("generate")
        if next_key:
            self.toolbar.enable(next_key)
        self.status.set_message("Ready")

    # Button handlers
    def on_generate(self):
        self.status.set_message("Generating polygon…")
        self._advance(None)
        if self.pipeline.step_generate_polygon():
            self.status.set_message(
                "Polygon generated. Continue with trapezoidalisation."
            )
            self._advance("trapezoidal")

    def on_trapezoidal(self):
        self.status.set_message("Drawing trapezoidalisation…")
        if self.pipeline.step_trapezoidalisation():
            self.status.set_message(
                "Trapezoidalisation done. Continue with monotone partitioning."
            )
            self._advance("monotone")
        else:
            messagebox.showwarning("Warning", "Please generate a polygon first.")

    def on_monotone(self):
        self.status.set_message("Computing monotone partitioning…")
        if self.pipeline.step_monotone_partitioning():
            self.status.set_message(
                "Monotone partitioning complete. Continue with triangulation."
            )
            self._advance("triangulation")
        else:
            messagebox.showwarning("Warning", "Please generate a polygon first.")

    def on_triangulation(self):
        self.status.set_message("Triangulating…")
        if self.pipeline.step_triangulation():
            self.status.set_message("Triangulation done. Build the dual graph next.")
            self._advance("dual_graph")
        else:
            messagebox.showwarning("Warning", "Please generate a polygon first.")

    def on_dual_graph(self):
        self.status.set_message("Creating dual graph…")
        if self.pipeline.step_dual_graph():
            self.status.set_message("Dual graph created. Proceed to 3-coloring.")
            self._advance("three_coloring")
        else:
            messagebox.showwarning("Warning", "Please generate a polygon first.")

    def on_three_coloring(self):
        self.status.set_message("3-coloring triangulation…")
        if self.pipeline.step_three_coloring():
            self.status.set_message("3-coloring complete. Compute vertex guards.")
            self._advance("vertex_guards")
        else:
            messagebox.showwarning("Warning", "Please generate a polygon first.")

    def on_vertex_guards(self):
        self.status.set_message("Selecting vertex guards…")
        if self.pipeline.step_vertex_guards():
            self.status.set_message("Vertex guards highlighted.")
            self._advance(None)
        else:
            messagebox.showwarning("Warning", "Please generate a polygon first.")

    def run(self):
        self.root.mainloop()


def main():
    ArtGalleryController().run()
