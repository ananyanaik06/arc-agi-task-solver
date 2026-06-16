import json
GREEN = 3
def dimensions(grid):
    return len(grid), len(grid[0])

def horizontal_blue_rows(grid):
    rows, cols = dimensions(grid)

    separators = []

    for r in range(rows):
        is_separator = True

        for c in range(cols):
            if grid[r][c] != 1:
                is_separator = False
                break

        if is_separator:
            separators.append(r)

    return separators

def vertical_blue_cols(grid):

    rows, cols = dimensions(grid)

    separators = []

    for c in range(cols):

        is_separator = True

        for r in range(rows):
            if grid[r][c] != 1:
                is_separator = False
                break

        if is_separator:
            separators.append(c)

    return separators

def is_problem1(grid):

    h = horizontal_blue_rows(grid)
    v = vertical_blue_cols(grid)

    if len(h) == 3:
        return True

    if len(v) == 3:
        return True

    return False

def split_horizontal(grid, sep):

    obj1 = grid[:sep[0]]

    obj2 = grid[sep[0]+1 : sep[1]]

    obj3 = grid[sep[1]+1 : sep[2]]

    obj4 = grid[sep[2]+1 :]

    return obj1, obj2, obj3, obj4

def split_vertical(grid, sep):

    obj1 = []
    obj2 = []
    obj3 = []
    obj4 = []

    for row in grid:

        obj1.append(row[:sep[0]])

        obj2.append(row[sep[0]+1 : sep[1]])

        obj3.append(row[sep[1]+1 : sep[2]])

        obj4.append(row[sep[2]+1 :])

    return obj1, obj2, obj3, obj4

def get_single_color(obj):

    colors = set()

    for row in obj:
        for cell in row:
            colors.add(cell)

    return colors.pop()

def get_objects(grid):

    h = horizontal_blue_rows(grid)

    if len(h) == 3:
        return split_horizontal(grid, h), "horizontal"

    v = vertical_blue_cols(grid)

    if len(v) == 3:
        return split_vertical(grid, v), "vertical"

    return None, None

def count_dominoes(obj):

    rows, cols = dimensions(obj)

    visited = [[False] * cols for _ in range(rows)]

    count = 0

    for r in range(rows):
        for c in range(cols):

            if obj[r][c] == 0:
                continue

            if visited[r][c]:
                continue

            count += 1

            visited[r][c] = True

            if r + 1 < rows and obj[r + 1][c] != 0:
                visited[r + 1][c] = True

            elif c + 1 < cols and obj[r][c + 1] != 0:
                visited[r][c + 1] = True

    return count

def pattern_mask(obj):

    rows, cols = dimensions(obj)

    mask = []

    for r in range(rows):

        row = []

        for c in range(cols):

            if obj[r][c] == 0:
                row.append(0)
            else:
                row.append(1)

        mask.append(row)

    return mask

def crop_object(obj):

    rows, cols = dimensions(obj)

    min_row = rows
    max_row = -1

    min_col = cols
    max_col = -1

    for r in range(rows):
        for c in range(cols):

            if obj[r][c] != 0:

                min_row = min(min_row, r)
                max_row = max(max_row, r)

                min_col = min(min_col, c)
                max_col = max(max_col, c)

    cropped = []

    for r in range(min_row, max_row + 1):

        row = []

        for c in range(min_col, max_col + 1):
            row.append(obj[r][c])

        cropped.append(row)

    return cropped

def construct_output(mask, k, orientation, foreground, background):

    mask_rows = len(mask)
    mask_cols = len(mask[0])

    if orientation == "horizontal":

        out_rows = k * mask_rows + (k - 1)
        out_cols = mask_cols

    else:

        out_rows = mask_rows
        out_cols = k * mask_cols + (k - 1)

    output = [
        [background] * out_cols
        for _ in range(out_rows)
    ]

    for copy in range(k):

        if orientation == "horizontal":

            start_row = copy * (mask_rows + 1)

            for r in range(mask_rows):
                for c in range(mask_cols):

                    if mask[r][c] == 1:
                        output[start_row + r][c] = foreground

        else:

            start_col = copy * (mask_cols + 1)

            for r in range(mask_rows):
                for c in range(mask_cols):

                    if mask[r][c] == 1:
                        output[r][start_col + c] = foreground

    return output

def solve_problem1(grid):

    objects, orientation = get_objects(grid)

    obj1, obj2, obj3, obj4 = objects

    obj1 = crop_object(obj1)

    mask = pattern_mask(obj1)

    k = count_dominoes(obj2)

    foreground = get_single_color(obj3)

    background = get_single_color(obj4)

    return construct_output(
        mask,
        k,
        orientation,
        foreground,
        background
    )




def get_background_color(grid):

    freq = {}

    for row in grid:
        for cell in row:

            if cell not in freq:
                freq[cell] = 0

            freq[cell] += 1

    return max(freq, key=freq.get)

def find_largest_green_boundary(grid):

    rows = len(grid)
    cols = len(grid[0])

    best_area = -1
    best_rect = None

    for r1 in range(rows):
        for r2 in range(r1 + 2, rows):

            for c1 in range(cols):
                for c2 in range(c1 + 2, cols):

                    valid = True

                    # top edge
                    for c in range(c1, c2 + 1):
                        if grid[r1][c] != GREEN:
                            valid = False
                            break

                    if not valid:
                        continue

                    # bottom edge
                    for c in range(c1, c2 + 1):
                        if grid[r2][c] != GREEN:
                            valid = False
                            break

                    if not valid:
                        continue

                    # left edge
                    for r in range(r1, r2 + 1):
                        if grid[r][c1] != GREEN:
                            valid = False
                            break

                    if not valid:
                        continue

                    # right edge
                    for r in range(r1, r2 + 1):
                        if grid[r][c2] != GREEN:
                            valid = False
                            break

                    if not valid:
                        continue

                    area = (r2 - r1 + 1) * (c2 - c1 + 1)

                    if area > best_area:
                        best_area = area
                        best_rect = (r1, r2, c1, c2)

    return best_rect

def dfs(grid, r, c, visited, component, background, fill_color,green_cells):

    rows = len(grid)
    cols = len(grid[0])

    if r < 0 or r >= rows:
        return

    if c < 0 or c >= cols:
        return

    if visited[r][c]:
        return

    if grid[r][c] == background:
        return

    if grid[r][c] == fill_color:
        return
    if (r, c) in green_cells:
        return

    visited[r][c] = True

    component.append((r, c))

    dfs(grid, r + 1, c, visited, component, background, fill_color, green_cells)
    dfs(grid, r - 1, c, visited, component, background, fill_color, green_cells)
    dfs(grid, r, c + 1, visited, component, background, fill_color, green_cells)
    dfs(grid, r, c - 1, visited, component, background,fill_color, green_cells)

def bounding_box(obj):

    min_r = min(r for r, c in obj)
    max_r = max(r for r, c in obj)

    min_c = min(c for r, c in obj)
    max_c = max(c for r, c in obj)

    return min_r, max_r, min_c, max_c

def find_objects(grid, background,fill_color, green_cells):

    rows = len(grid)
    cols = len(grid[0])

    visited = [[False] * cols for _ in range(rows)]

    objects = []

    for r in range(rows):
        for c in range(cols):

            if visited[r][c]:
                continue

            if grid[r][c] == background:
                continue

            if (r, c) in green_cells:
                continue

            component = []

            dfs(
                grid,
                r,
                c,
                visited,
                component,
                background,
                fill_color,
                green_cells
            )
            if len(component) > 0:
                objects.append(component)
            

    return objects

def get_colors(grid, obj):

    colors = set()

    for r, c in obj:
        colors.add(grid[r][c])

    return colors

def merge_objects(grid, objects):

    merged = []
    used = [False] * len(objects)

    for i in range(len(objects)):

        if used[i]:
            continue

        current = objects[i][:]

        colors1 = get_colors(grid, objects[i])

        used[i] = True

        for j in range(i + 1, len(objects)):

            if used[j]:
                continue

            colors2 = get_colors(grid, objects[j])

            if colors1 == colors2:

                current.extend(objects[j])

                used[j] = True

        merged.append(current)

    return merged

def bounding_box(obj):

    min_r = min(r for r, c in obj)
    max_r = max(r for r, c in obj)

    min_c = min(c for r, c in obj)
    max_c = max(c for r, c in obj)

    return min_r, max_r, min_c, max_c

def get_color_list(grid, obj):

    colors = []

    seen = set()

    for r, c in obj:

        color = grid[r][c]

        if color not in seen:

            seen.add(color)
            colors.append(color)

    return colors

def rectangle_boundary(top, bottom, left, right):

    cells = []

    for c in range(left, right + 1):

        cells.append((top, c))
        cells.append((bottom, c))

    for r in range(top + 1, bottom):

        cells.append((r, left))
        cells.append((r, right))

    return cells

def get_corner_color(grid, obj):

    top, bottom, left, right = bounding_box(obj)

    obj_set = set(obj)

    corners = [
        (top, left),
        (top, right),
        (bottom, left),
        (bottom, right)
    ]

    for r, c in corners:

        if (r, c) in obj_set:
            return grid[r][c]

    r, c = obj[0]
    return grid[r][c]

def paint_object(
    grid,
    obj,
    output,
    r1,
    r2,
    c1,
    c2,
    top,
    bottom,
    left,
    right,
    colors
):

    boundary = rectangle_boundary(
        top,
        bottom,
        left,
        right
    )
    
    # ------------------
    # single color case
    # ------------------

    if len(colors) == 1:

        color = colors[0]

        for r, c in boundary:

            if not (r1 < r < r2 and c1 < c < c2):
                continue

            out_r = r - (r1 + 1)
            out_c = c - (c1 + 1)

            output[out_r][out_c] = color

        return

    # ------------------
    # two color case
    # ------------------

    corner_color = get_corner_color(
        grid,
        obj
    )

    if colors[0] == corner_color:
        other_color = colors[1]
    else:
        other_color = colors[0]

    for r, c in boundary:

        if not (r1 < r < r2 and c1 < c < c2):
            continue

        out_r = r - (r1 + 1)
        out_c = c - (c1 + 1)

        local_r = r - top
        local_c = c - left

        if (local_r + local_c) % 2 == 0:

            output[out_r][out_c] = corner_color

        else:

            output[out_r][out_c] = other_color

def solve_problem2(grid):

    background = get_background_color(grid)

    r1, r2, c1, c2 = find_largest_green_boundary(grid)

    green_cells = set()

    for r in range(r1, r2 + 1):
        for c in range(c1, c2 + 1):

            if grid[r][c] == 3:
                green_cells.add((r, c))

    fill_color = grid[r1 + 1][c1 + 1]
   
    height = r2 - r1 - 1
    width = c2 - c1 - 1

    output = [
        [fill_color] * width
        for _ in range(height)
    ]

    objects = find_objects(
        grid,
        background,
        fill_color,
        green_cells
    )

    objects = merge_objects(
        grid,
        objects
    )
    for obj in objects:

        print(
            bounding_box(obj),
            get_colors(grid, obj)
        )
    for obj in objects:

        top, bottom, left, right = bounding_box(obj)
       
        
        colors = get_color_list(
            grid,
            obj
        )

        paint_object(
            grid,
            obj,
            output,
            r1,
            r2,
            c1,
            c2,
            top,
            bottom,
            left,
            right,
            colors
        )

    return output



import json

with open("test1.json") as f:
    grid = json.load(f)

if is_problem1(grid):
    answer = solve_problem1(grid)
else:
    answer = solve_problem2(grid)

with open("output.json", "w") as f:
    json.dump(answer, f)