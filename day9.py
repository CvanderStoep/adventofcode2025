from itertools import combinations


def read_and_parse_input_file(file_name: str) -> list[tuple[int, ...]]:
    with open(file_name) as f:
        return [tuple(map(int, line.split(","))) for line in f]


def calculate_area(t1: tuple, t2: tuple) -> int:
    return (abs(t1[0] - t2[0]) + 1) * (abs(t1[1] - t2[1]) + 1)


def point_in_polygon(point, polygon):
    """
    Determine if a point is inside a polygon using the ray-casting algorithm.

    point: (x, y)
    polygon: list of (x, y) tuples forming a closed loop (first and last don't need to match)
    """
    x, y = point
    inside = False

    # iterate over edges
    for i in range(len(polygon)):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % len(polygon)]

        # check if the ray intersects this edge
        intersects = ((y1 > y) != (y2 > y)) and \
                     (x < (x2 - x1) * (y - y1) / (y2 - y1 + 1e-12) + x1)

        if intersects:
            inside = not inside

    return inside


def point_in_orthogonal_polygon(point, polygon):
    x, y = point
    inside = False

    for (x1, y1), (x2, y2) in zip(polygon, polygon[1:] + polygon[:1]):
        # Only vertical edges matter
        if x1 == x2:
            # Check if the vertical segment spans the point's y
            if min(y1, y2) < y <= max(y1, y2):
                # Check if the edge is to the right of the point
                if x1 > x:
                    inside = not inside

    return inside


def classify_point_in_orthogonal_polygon(point, polygon):
    """
    Classify a point relative to an axis-aligned polygon.
    Returns: "inside", "outside", or "on boundary".
    """

    x, y = point
    inside = False

    # Iterate over edges (p1 -> p2)
    for (x1, y1), (x2, y2) in zip(polygon, polygon[1:] + polygon[:1]):

        # --- Boundary check (horizontal or vertical edges) ---
        # Horizontal edge
        if y1 == y2 == y and min(x1, x2) <= x <= max(x1, x2):
            return "on boundary"

        # Vertical edge
        if x1 == x2 == x and min(y1, y2) <= y <= max(y1, y2):
            return "on boundary"

        # --- Ray-casting using only vertical edges ---
        if x1 == x2:  # vertical edge
            # Does this edge cross the horizontal ray at y?
            if min(y1, y2) < y <= max(y1, y2):
                # Is the edge to the right of the point?
                if x1 > x:
                    inside = not inside

    return "inside" if inside else "outside"


def all_rect_points_inside_polygon(corner1, corner2, polygon):
    """
    Check whether all integer grid points inside the rectangle
    defined by corner1 and corner2 lie inside the polygon.
    """

    x1, y1 = corner1
    x2, y2 = corner2

    min_x, max_x = sorted((x1, x2))
    min_y, max_y = sorted((y1, y2))

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            status = classify_point_in_orthogonal_polygon((x, y), polygon)
            if status == "outside":
                return False, (x, y, status)

    return True, None


def compute_part_one(file_name: str) -> str:
    red_tiles = read_and_parse_input_file(file_name)
    print(red_tiles)

    max_area = 0
    for t1, t2 in combinations(red_tiles, 2):
        # print(t1, t2, calculate_area(t1, t2))
        max_area = max(max_area, calculate_area(t1, t2))

    return f'{max_area= }'


def compute_part_two(file_name: str) -> str | None:
    polygon = read_and_parse_input_file(file_name)

    all_areas = []
    for t1, t2 in combinations(polygon, 2):
        all_areas.append([t1, t2, calculate_area(t1, t2)])

    all_areas.sort(key=lambda x: x[2], reverse=True)

    for c1, c2, area in all_areas:
        print(f'{area= }')
        ok, info = all_rect_points_inside_polygon(c1, c2, polygon)

        if ok:
            print("All points inside the rectangle are inside the polygon")
            return f'{area= }'

    return None


if __name__ == '__main__':
    print(f"Part I: {compute_part_one('input/input9.txt')}")
    print(f"Part II: {compute_part_two('input/input9.txt')}")
