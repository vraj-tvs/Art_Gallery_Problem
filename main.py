# main.py
from src.dcel import DCEL
from src.triangulation import triangulate_ear_clipping
from src.coloring import three_color_vertices, choose_guards_from_coloring
from src.plotting import plot_pipeline
from src.io_utils import read_polygon_from_json

from argparse import ArgumentParser


def run_demo(json_filepath: str):
    # Load polygon from JSON
    polygon = read_polygon_from_json(json_filepath)
    dcel = DCEL.from_polygon(polygon)
    print("Created DCEL:", dcel)

    triangles = triangulate_ear_clipping(dcel)
    print("Num of Triangles:", len(triangles))

    colors = three_color_vertices(triangles)
    # print("Colors:", colors)

    guards = choose_guards_from_coloring(colors)
    print(f"List of {len(guards)} Guard(s):", guards)

    plot_pipeline(dcel, triangles, colors, guards, show=True)


if __name__ == "__main__":
    parser = ArgumentParser(description="Polygon Triangulation and Guard Placement")
    parser.add_argument(
        "--json_filepath",
        type=str,
        help="Path to the JSON file containing polygon vertices",
    )
    args = parser.parse_args()
    run_demo(args.json_filepath)
