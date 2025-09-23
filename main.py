# main.py
from src.dcel import DCEL
from src.triangulation import triangulate_ear_clipping
from src.coloring import three_color_vertices, choose_guards_from_coloring
from src.plotting import plot_pipeline

def run_demo():
    # Example polygon
    polygon = [(0,0), (5,0), (6,2), (4,4), (2.5,3.5), (1,4), (0,2)]
    dcel = DCEL.from_polygon(polygon)
    print("Created DCEL:", dcel)

    triangles = triangulate_ear_clipping(dcel)
    print("Triangles:", triangles)

    colors = three_color_vertices(triangles)
    print("Colors:", colors)

    guards = choose_guards_from_coloring(colors)
    print("Guards:", guards)

    plot_pipeline(dcel, triangles, colors, guards, show=True)

if __name__ == "__main__":
    run_demo()
