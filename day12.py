import numpy as np


def read_and_parse_input_file(path):
    tiles = []
    final_section = []

    with open(path, "r", encoding="utf-8") as f:
        # --- Read 6 tiles: 0..5 ---
        for expected_index in range(6):
            header = f.readline()
            if not header:
                raise ValueError(f"Unexpected EOF while reading header for tile {expected_index}")

            header = header.strip()
            if not header.endswith(":"):
                raise ValueError(f"Expected tile header like '0:', got {header!r}")

            tile_index_str = header[:-1]
            if not tile_index_str.isdigit():
                raise ValueError(f"Tile header does not start with a number: {header!r}")

            tile_index = int(tile_index_str)
            if tile_index != expected_index:
                raise ValueError(
                    f"Expected tile index {expected_index}, got {tile_index} in header {header!r}"
                )

            rows = []
            for _ in range(3):
                row = f.readline()
                if not row:
                    raise ValueError(f"Unexpected EOF while reading tile {tile_index}")
                row = row.rstrip("\n")
                rows.append(list(row))

            tiles.append(np.array(rows))

            blank = f.readline()
            if blank and blank.strip() != "":
                raise ValueError(
                    f"Expected blank line after tile {tile_index}, got {blank!r}"
                )

        # --- Read final section ---
        for raw in f:
            line = raw.strip()
            if not line:
                continue

            if ":" not in line:
                raise ValueError(f"Missing ':' in final section line: {line!r}")

            dims, values = line.split(":", 1)
            dims = dims.strip()

            if "x" not in dims:
                raise ValueError(f"Invalid dimension format (expected WxH): {line!r}")

            w_str, h_str = dims.split("x", 1)
            w, h = int(w_str), int(h_str)

            nums = [int(x) for x in values.split()]
            # Pattern C: nums[i] = count for tile i
            final_section.append((w, h, nums))

    return tiles, final_section


def all_orientations(tile):
    """Return up to 8 orientations of a tile (rotations + flipped rotations)."""
    rots = [np.rot90(tile, k=i) for i in range(4)]
    flipped = np.flip(tile, axis=1)
    rots_flipped = [np.rot90(flipped, k=i) for i in range(4)]
    return rots + rots_flipped


def placement_to_mask(tile, r, c, W, H):
    """Convert a tile placement into a bitmask over a W×H board."""
    mask = 0
    Ht, Wt = tile.shape
    for dr in range(Ht):
        for dc in range(Wt):
            if tile[dr, dc] == '#':
                bit = (r + dr) * W + (c + dc)
                mask |= (1 << bit)
    return mask


def mask_to_grid(mask, W, H):
    """Convert a board mask back to a grid of '.' / '#' for inspection."""
    grid = []
    for r in range(H):
        row = []
        for c in range(W):
            bit = r * W + c
            row.append('#' if (mask >> bit) & 1 else '.')
        grid.append("".join(row))
    return grid


def compute_all_placements(board, tiles):
    """
    For each tile index, compute all valid placement masks on this board.
    A placement is valid if the tile only covers '.' cells.
    """
    H, W = board.shape
    placements = {i: [] for i in range(len(tiles))}

    for idx, tile in enumerate(tiles):
        orientations = all_orientations(tile)
        seen_orientations = set()

        # Optional: deduplicate symmetric orientations
        unique_orientations = []
        for orient in orientations:
            key = orient.tobytes()
            if key not in seen_orientations:
                seen_orientations.add(key)
                unique_orientations.append(orient)

        for orient in unique_orientations:
            Ht, Wt = orient.shape
            for r in range(H - Ht + 1):
                for c in range(W - Wt + 1):
                    sub = board[r:r + Ht, c:c + Wt]
                    if np.all((orient == '.') | (sub == '.')):
                        mask = placement_to_mask(orient, r, c, W, H)
                        placements[idx].append(mask)

    return placements


def solve_with_backtracking(board, tiles, tile_counts, find_all=False):
    """
    Backtracking solver with:
    - bitmask representation
    - area-based pruning
    - ordering tiles by difficulty (few placements, large area)
    """
    H, W = board.shape
    total_cells = W * H

    # Precompute all placements
    placements = compute_all_placements(board, tiles)

    # Precompute tile areas
    tile_areas = [int(np.sum(tile == '#')) for tile in tiles]

    # Build expanded tile list: e.g. [1,0,1,0,2,2] -> [0,2,4,4,5,5]
    expanded_tiles = []
    for idx, count in enumerate(tile_counts):
        expanded_tiles.extend([idx] * count)

    # Sort tile indices by "difficulty": few placements, large area
    expanded_tiles.sort(
        key=lambda idx: (len(placements[idx]), -tile_areas[idx])
    )

    solutions = []

    def backtrack(i, board_mask):
        # i = index in expanded_tiles
        if i == len(expanded_tiles):
            solutions.append(board_mask)
            return not find_all  # True if we can stop here

        tile_idx = expanded_tiles[i]
        tile_area = tile_areas[tile_idx]

        # --- Area-based pruning: if not enough free cells left, prune
        used_cells = board_mask.bit_count()
        remaining_free = total_cells - used_cells

        remaining_required_area = tile_area
        for j in range(i + 1, len(expanded_tiles)):
            remaining_required_area += tile_areas[expanded_tiles[j]]

        if remaining_required_area > remaining_free:
            return False

        # Try all placements for this tile
        for mask in placements[tile_idx]:
            if (mask & board_mask) == 0:
                if backtrack(i + 1, board_mask | mask):
                    return True

        return False

    found = backtrack(0, 0)
    return found, solutions


def compute_part_one(file_name: str):
    tiles, final_section = read_and_parse_input_file(file_name)
    total_solutions = 0

    for idx, (W, H, counts) in enumerate(final_section):
        print(f"\n=== Instance {idx}: {W}x{H}, counts={counts} ===")

        board = np.array([['.' for _ in range(W)] for _ in range(H)])

        found, solutions = solve_with_backtracking(board, tiles, counts, find_all=False)

        print("Solution found:", found)
        if found and solutions:
            total_solutions += 1
            mask = solutions[0]
            grid = mask_to_grid(mask, W, H)
            print("One solution layout (# = filled):")
            for row in grid:
                print(row)

    return f"Total solutions: {total_solutions}"


if __name__ == '__main__':
    print(f"Part I: {compute_part_one('input/input12.txt')}")
