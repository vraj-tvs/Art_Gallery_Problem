# src/utils.py
from typing import Tuple

EPS: float = 1e-9


def orientation(
    a: Tuple[float, float], b: Tuple[float, float], c: Tuple[float, float]
) -> float:
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def signed_area(poly: list[Tuple[float, float]]) -> float:
    n = len(poly)
    a = 0.0
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        a += x1 * y2 - x2 * y1
    return 0.5 * a


def is_point_in_triangle(
    p: Tuple[float, float],
    a: Tuple[float, float],
    b: Tuple[float, float],
    c: Tuple[float, float],
) -> bool:
    o1 = orientation(p, a, b)
    o2 = orientation(p, b, c)
    o3 = orientation(p, c, a)
    if (abs(o1) < EPS) or (abs(o2) < EPS) or (abs(o3) < EPS):
        return False
    has_neg = (o1 < -EPS) or (o2 < -EPS) or (o3 < -EPS)
    has_pos = (o1 > EPS) or (o2 > EPS) or (o3 > EPS)
    return not (has_neg and has_pos)


def point_on_segment(
    p: Tuple[float, float], a: Tuple[float, float], b: Tuple[float, float]
) -> bool:
    if abs(orientation(a, b, p)) > EPS:
        return False
    return (
        min(a[0], b[0]) - EPS <= p[0] <= max(a[0], b[0]) + EPS
        and min(a[1], b[1]) - EPS <= p[1] <= max(a[1], b[1]) + EPS
    )
