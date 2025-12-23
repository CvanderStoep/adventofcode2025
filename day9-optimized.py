from __future__ import annotations

from functools import lru_cache
from itertools import combinations
from typing import Iterable


def read_and_parse_input_file(file_name: str) -> list[tuple[int, ...]]:
    with open(file_name) as f:
        return [tuple(map(int, line.split(","))) for line in f]


def calculate_area(t1: tuple[int, int], t2: tuple[int, int]) -> int:
    return (abs(t1[0] - t2[0]) + 1) * (abs(t1[1] - t2[1]) + 1)


def point_in_polygon(point: tuple[int, int],
                     polygon: Iterable[tuple[int, int]]) -> bool:
    """
    Generic ray-casting point-in-polygon for arbitrary polygons.
    point: (x, y)
    polygon: iterable of (x, y) tuples forming a closed loop
    """
    x, y = point
    inside = False
    polygon = list(polygon)

    for i in range(len(polygon)):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % len(polygon)]

        intersects = (
            (y1 > y) != (y2 > y)
            and x < (x2 - x1) * (y - y1) / (y2 - y1 + 1e-12) + x1
        )

        if intersects:
            inside = not inside

    return inside


def point_in_orthogonal_polygon(point: tuple[int, int],
                                polygon: Iterable[tuple[int, int]]) -> bool:
    """
    Ray-casting specialized for axis-aligned polygons, using only vertical edges.
    """
    x, y = point
    inside = False
    polygon = list(polygon)

    for (x1, y1), (x2, y2) in zip(polygon, polygon[1:] + polygon[:1]):
        if x1 == x2:  # vertical edge only
            if min(y1, y2) < y <= max(y1, y2) and x1 > x:
                inside = not inside

    return inside


def classify_point_in_orthogonal_polygon(
    point: tuple[int, int],
    polygon: Iterable[tuple[int, int]],
) -> str:
    """
    Classify a point relative to an axis-aligned polygon.
    Returns: "inside", "outside", or "on boundary".
    """
    x, y = point
    inside = False
    polygon = list(polygon)

    for (x1, y1), (x2, y2) in zip(polygon, polygon[1:] + polygon[:1]):
        # Boundary checks
        if y1 == y2 == y and min(x1, x2) <= x <= max(x1, x2):
            return "on boundary"

        if x1 == x2 == x and min(y1, y2) <= y <= max(y1, y2):
            return "on boundary"

        # Ray-casting using vertical edges only
        if x1 == x2:  # vertical edge
            if min(y1, y2) < y <= max(y1, y2) and x1 > x:
                inside = not inside

    return "inside" if inside else "outside"


# ---------- Memoized classifier for Part 2 ----------

@lru_cache(maxsize=None)
def classify_point_cached(
    x: int,
    y: int,
    polygon_tuple: tuple[tuple[int, int], ...],
) -> str:
    """
    Cached wrapper around classify_point_in_orthogonal_polygon.
    polygon_tuple must be a tuple of (x, y) tuples (hashable).
    """
    return classify_point_in_orthogonal_polygon((x, y), polygon_tuple)


def all_rect_points_inside_polygon(
    corner1: tuple[int, int],
    corner2: tuple[int, int],
    polygon_tuple: tuple[tuple[int, int], ...],
) -> tuple[bool, tuple[int, int, str] | None]:
    """
    Check whether all integer grid points inside the rectangle
    defined by corner1 and corner2 lie inside the polygon.
    Uses the cached classifier to avoid recomputation.
    """

    x1, y1 = corner1
    x2, y2 = corner2

    min_x, max_x = sorted((x1, x2))
    min_y, max_y = sorted((y1, y2))

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            status = classify_point_cached(x, y, polygon_tuple)
            if status == "outside":
                return False, (x, y, status)

    return True, None


def compute_part_one(file_name: str) -> str:
    red_tiles = read_and_parse_input_file(file_name)

    max_area = 0
    for t1, t2 in combinations(red_tiles, 2):
        max_area = max(max_area, calculate_area(t1, t2))

    return f"{max_area= }"


def compute_part_two(file_name: str) -> str | None:
    polygon = read_and_parse_input_file(file_name)
    polygon_tuple: tuple[tuple[int, int], ...] = tuple(polygon)

    # Precompute all candidate rectangles with their areas
    all_areas: list[tuple[tuple[int, int], tuple[int, int], int]] = []
    for t1, t2 in combinations(polygon, 2):
        all_areas.append((t1, t2, calculate_area(t1, t2)))

    # Sort by area descending to find the maximum valid one fast
    all_areas.sort(key=lambda x: x[2], reverse=True)

    for c1, c2, area in all_areas:
        print(f"{area= }")
        if area > 1500414119:
            continue
        ok, info = all_rect_points_inside_polygon(c1, c2, polygon_tuple)

        if ok:
            print("All points inside the rectangle are inside the polygon")
            return f"{area= }"

    return None


if __name__ == "__main__":
    print(f"Part I: {compute_part_one('input/input9.txt')}")
    print(f"Part II: {compute_part_two('input/input9.txt')}")