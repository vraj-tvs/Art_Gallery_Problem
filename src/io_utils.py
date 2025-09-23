# src/io_utils.py
import json
from typing import List, Tuple, Dict, Any


def read_polygon_from_json(filepath: str) -> List[Tuple[float, float]]:
    """Read polygon vertices from JSON file. Returns list of (x, y) coordinates."""
    with open(filepath, "r", encoding="utf-8") as f:
        data: Dict[str, Any] = json.load(f)

    if "vertices" not in data or not isinstance(data["vertices"], list):
        raise ValueError(
            "Invalid JSON: expected key 'vertices' with a list of [x,y] pairs."
        )

    vertices: List[Tuple[float, float]] = []
    for v in data["vertices"]:
        if not isinstance(v, list) or len(v) != 2:
            raise ValueError(f"Invalid vertex format: {v}. Expected [x, y].")
        x, y = float(v[0]), float(v[1])
        vertices.append((x, y))

    return vertices


def write_polygon_to_json(
    filepath: str, vertices: List[Tuple[float, float]], name: str = "Polygon"
) -> None:
    """Save polygon vertices to JSON file with optional name."""
    data = {"name": name, "vertices": [[float(x), float(y)] for x, y in vertices]}
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
