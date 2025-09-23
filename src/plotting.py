# src/plotting.py
import matplotlib.pyplot as plt
from src.dcel import DCEL


def plot_pipeline(dcel: DCEL, triangles, colors, guards, show=True, save_path=None):
    pts = dcel.coords_list()
    fig, ax = plt.subplots(figsize=(6, 6))

    # Polygon boundary
    poly_idx = dcel.boundary_vertex_indices()
    poly_coords = [pts[i] for i in poly_idx] + [pts[poly_idx[0]]]
    ax.plot([p[0] for p in poly_coords], [p[1] for p in poly_coords], "-k", lw=1)

    # Triangles
    for tri in triangles:
        tri_coords = [pts[i] for i in tri] + [pts[tri[0]]]
        ax.plot([p[0] for p in tri_coords], [p[1] for p in tri_coords], "--", lw=0.8)

    # Vertex colors
    cmap = ["C0", "C1", "C2"]
    for v_idx, col in colors.items():
        ax.scatter(
            pts[v_idx][0], pts[v_idx][1], s=80, c=cmap[col], marker="o", zorder=5
        )
        ax.text(pts[v_idx][0] + 0.03, pts[v_idx][1] + 0.03, f"{v_idx}", fontsize=9)

    # Guards
    for g in guards:
        ax.scatter(
            pts[g][0], pts[g][1], s=200, marker="*", c="gold", edgecolor="k", zorder=6
        )

    ax.set_aspect("equal")
    ax.set_title(f"Triangles: {len(triangles)} | Guards: {len(guards)}")

    if save_path:
        plt.savefig(save_path, bbox_inches="tight")
    if show:
        plt.show()
    plt.close(fig)
