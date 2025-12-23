import sys
# https://github.com/shabeeliqbal/advent-of-code-2025/blob/main/day%209/day%209%20p2.py

file_name = "input/input9.txt"
with open(file_name, encoding="utf-8") as f:
    file = [tuple(map(int, row.split(","))) for row in (line.strip() for line in f) if row]

def calculate_area(a, b):
    return (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1)

def rectangle(i, j):
    return {
        "top": min(file[i][1], file[j][1]),
        "left": min(file[i][0], file[j][0]),
        "bottom": max(file[i][1], file[j][1]),
        "right": max(file[i][0], file[j][0]),
    }

bounding_box = []
for i in range(len(file)):
    if i == 0:
        bounding_box.append(rectangle(len(file) - 1, i))
    else:
        bounding_box.append(rectangle(i - 1, i))

def aabb_collision(a, b):
    left_gap = a["left"] >= b["right"]
    right_gap = a["right"] <= b["left"]
    top_gap = a["top"] >= b["bottom"]
    bottom_gap = a["bottom"] <= b["top"]
    return not (right_gap or left_gap or top_gap or bottom_gap)

areas = []
for i in range(len(file) - 1):
    for j in range(i + 1, len(file)):
        areas.append((calculate_area(file[i], file[j]), rectangle(i, j)))

areas.sort(key=lambda x: x[0], reverse=True)
for area_val, rect in areas:
    inside = True
    for bb in bounding_box:
        if aabb_collision(rect, bb):
            inside = False
            break
    if inside:
        print(area_val)
        break