from y22.src.utils import io


def main():
    current_day = io.get_day()
    for test in [False]:
        filename = io.get_input_filename(2022, current_day, test=test)
        raw_input = io.get_inputs_raw(filename)

        points = parse_data(raw_input)
        # print(calculate(points, 20))
        print(calculate(points, 4_000_000))


def calculate(points: dict[tuple[int, int], tuple[int, int]], max_search: int) -> int:
    maybes = set()

    # First Pass
    for (sx, sy), (bx, by) in points.items():
        corona_distance = abs(bx - sx) + abs(by - sy) + 1

        for i in range(corona_distance):
            candidates = [
                (corona_distance - i, i),
                (i - corona_distance, -i),
                (i, corona_distance - i),
                (-i, i - corona_distance)
            ]
            for candidate_x, candidate_y in candidates:
                if 0 <= candidate_x <= max_search and 0 <= candidate_y <= max_search:
                    maybes.add((sx + candidate_x, sy + candidate_y))

    # Second Pass
    next_maybes = set(maybes)
    for (sx, sy), (bx, by) in points.items():
        distance = abs(bx - sx) + abs(by - sy)
        for maybe_x, maybe_y in maybes:
            distance_to_maybe = abs(maybe_x - sx) + abs(maybe_y - sy)
            if distance_to_maybe <= distance:
                next_maybes.remove((maybe_x, maybe_y))
        maybes = set(next_maybes)

    for (x, y) in next_maybes:
        if 0 <= x <= max_search and 0 <= y <= max_search:
            return x * 4_000_000 + y
    return -1


def calculate1(
    points: dict[tuple[int, int], tuple[int, int]],
    query: int
) -> int:
    query_row = {}
    query_row_min, query_row_max = 0, 0

    for (sx, sy), (bx, by) in points.items():
        distance = abs(bx - sx) + abs(by - sy)
        distance_to_query_y = abs(query - sy)

        if distance < distance_to_query_y:
            continue
        leftover = distance - distance_to_query_y

        candidates = [(sx, query)]
        for i in range(leftover):
            candidates.append((sx + i + 1, query))
            candidates.append((sx - i - 1, query))

        for candidate in candidates:
            if candidate[1] == query:
                query_row[candidate[0]] = True
                query_row_min = min(query_row_min, candidate[0])
                query_row_max = max(query_row_max, candidate[0])

    count = [
        query_row_min + i
        for i in range(query_row_max - query_row_min)
        if query_row.get(query_row_min + i, False)
    ]
    return len(count)


def parse_data(raw_input):
    output = {}
    for row in raw_input:
        if row == "":
            continue
        data = row.split()
        x = int(data[2][2:-1])
        y = int(data[3][2:-1])
        a = int(data[8][2:-1])
        b = int(data[9][2:])
        output[(x, y)] = (a, b)
    return output


if __name__ == "__main__":
    main()
