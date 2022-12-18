from collections import defaultdict

from y22.src.utils import io

Point = tuple[int, int, int]
Face = tuple[Point, Point]

BUFFER = 2


def main():
    current_day = io.get_day()
    for test in [True, False]:
        filename = io.get_input_filename(2022, current_day, test=test)
        raw_input = io.get_inputs_raw(filename)
        data, max_point = parse_input(raw_input)
        print(simulate(data, max_point))


def get_sides(point: Point) -> set[Face]:
    x, y, z = point
    return {
        ((x, y, z), (x + 1, y + 1, z)),
        ((x, y, z), (x, y + 1, z + 1)),
        ((x, y, z), (x + 1, y, z + 1)),
        ((x + 1, y, z), (x + 1, y + 1, z + 1)),
        ((x, y + 1, z), (x + 1, y + 1, z + 1)),
        ((x, y, z + 1), (x + 1, y + 1, z + 1)),
    }


def get_all_faces(data: set[Point]) -> set[Face]:
    faces_counts: dict[tuple[Point, Point], int] = defaultdict(int)
    for point in data:
        sides = get_sides(point)
        for start, end in sides:
            faces_counts[(start, end)] += 1

    return set(key for key, value in faces_counts.items() if value == 1)


def simulate(data: set[Point], max_point: Point) -> int:
    surface_sides = get_all_faces(data)
    output = set()
    to_search = {((0, 0, 0), (1, 1, 0))}
    searched = set()
    while len(to_search):
        side = to_search.pop()
        searched.add(side)

        if side in surface_sides:
            output.add(side)
            continue

        for next_side in find_ten(side):
            if (
                    next_side not in searched
                    and next_side not in to_search
                    and is_valid_side(next_side, max_point)
            ):
                to_search.add(next_side)
    return len(output)


def is_valid_side(side: Face, max_point: Point) -> bool:
    start, end = side
    start_x, start_y, start_z = start
    end_x, end_y, end_z = end
    max_x, max_y, max_z = max_point

    return (
            (-BUFFER < start_x <= end_x <= max_x + BUFFER) and
            (-BUFFER < start_y <= end_y <= max_y + BUFFER) and
            (-BUFFER < start_z <= end_z <= max_z + BUFFER)
    )


def find_ten(side: Face, verbose: bool = False) -> set[Face]:
    start, end = side
    start_x, start_y, start_z = start
    end_x, end_y, end_z = end

    if start_x == end_x:
        next_start = (start_x - 1, start_y, start_z)
    elif start_y == end_y:
        next_start = (start_x, start_y - 1, start_z)
    elif start_z == end_z:
        next_start = (start_x, start_y, start_z - 1)
    else:
        raise Exception("bad")

    output = get_sides(start).union(get_sides(next_start))
    output.remove(side)
    if verbose:
        print(len(output), output)
    return output


def parse_input(raw_data) -> tuple[set[Point], Point]:
    output: set[Point] = set()
    max_point = 0, 0, 0
    for row in raw_data:
        if row == "":
            continue
        point = tuple([int(_) for _ in row.split(",")])
        max_point = (
            max(max_point[0], point[0]),
            max(max_point[1], point[1]),
            max(max_point[2], point[2])
        )
        output.add(point)

    return output, max_point


if __name__ == "__main__":
    main()
