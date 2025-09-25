# Tkinter UI components: theme, toolbar, canvas panel, header, status bar.

# GroupID-23 (22114047_22114081_22114098) - Khushal Agrawal, Rushit Pancholi and Vraj Tamkuwala
# Date: 25 Sept, 2025
# ui.py - Reusable UI elements for the desktop application.

import tkinter as tk
from tkinter import ttk


class ThemeManager:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.style = ttk.Style(root)
        # Choose a base theme available across platforms
        try:
            self.style.theme_use("clam")
        except Exception:
            pass

        # Palette
        self.bg = "#1e1f26"
        self.surface = "#2a2b33"
        self.accent = "#5b8def"
        self.text = "#e6e6e6"
        self.muted = "#9aa0a6"

        # Apply base window colors
        self.root.configure(bg=self.bg)

        # Configure styles
        self.style.configure("TFrame", background=self.bg)
        self.style.configure("Surface.TFrame", background=self.surface)
        self.style.configure(
            "Heading.TLabel",
            background=self.bg,
            foreground=self.text,
            font=("Segoe UI", 14, "bold"),
        )
        self.style.configure("Subtle.TLabel", background=self.bg, foreground=self.muted)
        self.style.configure("TLabel", background=self.bg, foreground=self.text)
        self.style.configure(
            "Toolbar.TButton",
            padding=(8, 6),
            background=self.surface,
            foreground=self.text,
            borderwidth=0,
        )
        self.style.map(
            "Toolbar.TButton",
            background=[("active", self.accent)],
            foreground=[("disabled", "#666")],
        )
        self.style.configure(
            "Status.TLabel",
            background=self.surface,
            foreground=self.muted,
            font=("Segoe UI", 10),
        )


class Toolbar:
    def __init__(self, parent: tk.Widget):
        self.frame = ttk.Frame(parent, style="Surface.TFrame")
        self.frame.pack(side=tk.RIGHT, padx=20, pady=20, fill=tk.Y)

        self._buttons = {}

    def add_button(self, key: str, label: str, command, enabled: bool = True):
        state = tk.NORMAL if enabled else tk.DISABLED
        btn = ttk.Button(
            self.frame,
            text=label,
            command=command,
            state=state,
            style="Toolbar.TButton",
        )
        btn.pack(pady=6, padx=6, fill=tk.X)
        self._buttons[key] = btn
        return btn

    def set_enabled(self, key: str, enabled: bool):
        if key in self._buttons:
            self._buttons[key].config(state=tk.NORMAL if enabled else tk.DISABLED)

    def disable_all(self):
        for btn in self._buttons.values():
            btn.config(state=tk.DISABLED)

    def enable(self, key: str):
        self.set_enabled(key, True)


class CanvasPanel:
    def __init__(self, parent: tk.Widget, width: int = 500, height: int = 500):
        self.frame = ttk.Frame(parent, style="Surface.TFrame")
        self.frame.pack(side=tk.LEFT, padx=20, pady=20)
        self.canvas = tk.Canvas(
            self.frame, width=width, height=height, bg="#111214", highlightthickness=0
        )
        self.canvas.pack()

    def widget(self) -> tk.Canvas:
        return self.canvas


class HeaderBar:
    def __init__(self, parent: tk.Widget, title: str):
        self.frame = ttk.Frame(parent, style="TFrame")
        self.frame.pack(side=tk.TOP, fill=tk.X, padx=16, pady=(12, 0))
        self.title_label = ttk.Label(self.frame, text=title, style="Heading.TLabel")
        self.title_label.pack(side=tk.LEFT)


class StatusBar:
    def __init__(self, parent: tk.Widget):
        self.frame = ttk.Frame(parent, style="Surface.TFrame")
        self.frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.label = ttk.Label(self.frame, text="Ready", style="Status.TLabel")
        self.label.pack(side=tk.LEFT, padx=12, pady=6)

    def set_message(self, message: str):
        self.label.config(text=message)
