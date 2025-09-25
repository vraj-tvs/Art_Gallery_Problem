# Matplotlib adapter providing a Tk-like canvas API.

# GroupID-23 (22114047_22114081_22114098) - Khushal Agrawal, Rushit Pancholi and Vraj Tamkuwala
# Date: 25 Sept, 2025
# webui/canvas_adapter.py - Bridges algorithm drawing calls to Matplotlib.
#

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple, List

import matplotlib.pyplot as plt


@dataclass
class PlotConfig:
    width: int = 5
    height: int = 5
    bgcolor: str = "#ffffff"


class MatplotlibCanvasAdapter:
    """Adapter providing a Tkinter-like canvas API on top of Matplotlib.

    Methods map a small subset of the Tk canvas API used by the algorithms
    to Matplotlib primitives, enabling reuse in a web environment.
    """

    def __init__(self, config: PlotConfig | None = None):
        self.config = config or PlotConfig()
        self.fig, self.ax = plt.subplots(figsize=(self.config.width, self.config.height))
        self.ax.set_aspect("equal")
        self.ax.set_facecolor(self.config.bgcolor)
        self.fig.patch.set_facecolor(self.config.bgcolor)
        self.ax.axis("off")
        self._live_renderer = None  # function(fig) -> None
        # Fixed canvas bounds in Tk-coordinate space (0..500)
        self._xmin, self._xmax = 0, 500
        self._ymin, self._ymax = 0, 500
        # We keep Matplotlib's normal y-up coordinates; the calling code already
        # performs y inversion using origin_y - y to mimic Tk behavior.
        self.ax.set_xlim(self._xmin, self._xmax)
        self.ax.set_ylim(self._ymin, self._ymax)
        # Graphics object registry to emulate Tk ids
        self._next_id = 1
        self._objects = {}

    def _is_finite(self, *vals) -> bool:
        try:
            return all((v is not None) and float(v) == float(v) for v in vals)
        except Exception:
            return False

    def _clamp(self, v: float, vmin: float, vmax: float) -> float:
        try:
            vf = float(v)
        except Exception:
            return vmin
        if vf < vmin:
            return vmin
        if vf > vmax:
            return vmax
        return vf

    def set_live_renderer(self, render_fn):
        self._live_renderer = render_fn

    def _render_if_live(self):
        if self._live_renderer is not None:
            self._live_renderer(self.fig)

    # Compatibility methods
    def delete(self, tag):
        # tag can be 'all' or an integer id
        if tag == "all":
            self.fig.clf()
            self.ax = self.fig.add_subplot(111)
            self.ax.set_aspect("equal")
            self.ax.set_facecolor(self.config.bgcolor)
            self.fig.patch.set_facecolor(self.config.bgcolor)
            self.ax.axis("off")
            self.ax.set_xlim(self._xmin, self._xmax)
            self.ax.set_ylim(self._ymin, self._ymax)
            self._objects.clear()
        else:
            try:
                artist = self._objects.pop(tag, None)
                if artist is not None:
                    artist.remove()
            except Exception:
                pass
        self._render_if_live()

    def create_line(self, x1, y1, x2, y2, fill="black", dash: Tuple[int, int] | None = None, arrow=None):
        if not self._is_finite(x1, y1, x2, y2):
            return None
        x1 = float(self._clamp(x1, self._xmin, self._xmax))
        x2 = float(self._clamp(x2, self._xmin, self._xmax))
        y1 = float(self._clamp(y1, self._ymin, self._ymax))
        y2 = float(self._clamp(y2, self._ymin, self._ymax))
        (line,) = self.ax.plot([x1, x2], [y1, y2], color=fill)
        if dash:
            # Matplotlib expects a sequence of on/off ink lengths; use set_dashes for compatibility
            try:
                dash_seq = [float(d) for d in dash]
                if dash_seq and min(dash_seq) <= 0:
                    dash_seq = [4.0, 3.0]
                if len(dash_seq) % 2 == 1:
                    dash_seq = dash_seq * 2  # ensure even length
                # Prefer modern linestyle tuple when available
                try:
                    line.set_linestyle((0, dash_seq))
                except Exception:
                    line.set_dashes(dash_seq)
            except Exception:
                pass
        self.ax.set_xlim(self._xmin, self._xmax)
        self.ax.set_ylim(self._ymin, self._ymax)
        obj_id = self._next_id
        self._next_id += 1
        self._objects[obj_id] = line
        return obj_id

    def create_oval(self, x1, y1, x2, y2, fill="black"):
        # Convert bounding box to center and radius
        if not self._is_finite(x1, y1, x2, y2):
            return None
        x1 = float(self._clamp(x1, self._xmin, self._xmax))
        x2 = float(self._clamp(x2, self._xmin, self._xmax))
        y1 = float(self._clamp(y1, self._ymin, self._ymax))
        y2 = float(self._clamp(y2, self._ymin, self._ymax))
        cx = (x1 + x2) / 2.0
        cy = (y1 + y2) / 2.0
        rx = abs(x2 - x1) / 2.0
        ry = abs(y2 - y1) / 2.0
        radius = max(rx, ry)
        if radius <= 0:
            radius = 0.5
        circle = plt.Circle((cx, cy), radius=radius, color=fill)
        self.ax.add_patch(circle)
        self.ax.set_xlim(self._xmin, self._xmax)
        self.ax.set_ylim(self._ymin, self._ymax)
        obj_id = self._next_id
        self._next_id += 1
        self._objects[obj_id] = circle
        return obj_id

    def create_text(self, x, y, text, fill="black", font=("Arial", 10)):
        if not self._is_finite(x, y):
            return None
        size = 10
        try:
            size = int(font[1]) if isinstance(font, (list, tuple)) and len(font) > 1 else 10
        except Exception:
            size = 10
        x = self._clamp(x, self._xmin, self._xmax)
        y = self._clamp(y, self._ymin, self._ymax)
        artist = self.ax.text(x, y, str(text), color=fill, fontsize=size)
        self.ax.set_xlim(self._xmin, self._xmax)
        self.ax.set_ylim(self._ymin, self._ymax)
        obj_id = self._next_id
        self._next_id += 1
        self._objects[obj_id] = artist
        return obj_id

    def update(self):
        self._render_if_live()

    # Utility
    def render(self):
        return self.fig


