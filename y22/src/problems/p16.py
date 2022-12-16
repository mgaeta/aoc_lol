from y22.src.utils import io


DEADLINE = 30
ELEPHANT_FACTOR = 4

def main():
    current_day = io.get_day()
    for test in [False]:
        filename = io.get_input_filename(2022, current_day, test=test)
        raw_input = io.get_inputs_raw(filename)

        start = "AA"
        data = parse_input(raw_input)
        good_valves = determine_good_valves(data)
        distance_map = calculate_distances(data, good_valves, start)
        part_1, _ = calculate(data, good_valves, distance_map, DEADLINE, start)
        print(part_1 + 1)
        print(calculate_2(data, good_valves, distance_map, DEADLINE - ELEPHANT_FACTOR, start))


def calculate_2(
        data: dict[str, tuple[int, list[str], bool]],
        good_valves: set[str],
        distance_map: dict[tuple[str, str], int],
        time_remaining: int,
        start: str
) -> int:
    _, optimal_path = calculate(data, good_valves, distance_map, time_remaining, start)
    first_valve, _, t = optimal_path[1]

    exclude_a = {first_valve}
    exclude_b = set()

    while True:
        copy_a = set(_ for _ in good_valves if _ not in exclude_a)
        copy_b = set(_ for _ in good_valves if _ not in exclude_b)

        s_a, h_a = calculate(data, copy_a, distance_map, time_remaining, start)
        s_b, h_b = calculate(data, copy_b, distance_map, time_remaining, start)

        x_a = {v[0]: v[2] for v in h_a[1:]}
        x_b = {v[0]: v[2] for v in h_b[1:]}

        repeats_keys = set(x_a.keys()).intersection(x_b.keys())
        if not repeats_keys:
            return s_a + s_b + 2

        best_repeat = -1
        repeat_owner = None
        first_repeat = None
        for key in repeats_keys:
            v_a = x_a[key]
            v_b = x_b[key]

            if v_a >= v_b > best_repeat:
                best_repeat = v_a
                repeat_owner = 0
                first_repeat = key
            elif v_b >= v_a > best_repeat:
                best_repeat = v_b
                repeat_owner = 1
                first_repeat = key
        if repeat_owner == 0:
            exclude_b.add(first_repeat)
        else:
            exclude_a.add(first_repeat)


def get_best_score(scores: dict[list[str], int]) -> int:
    return max(scores.values())


def calculate(
        data: dict[str, tuple[int, list[str], bool]],
        good_valves: set[str],
        distance_map: dict[tuple[str, str], int],
        time_remaining: int,
        start: str
) -> tuple[int, list[str, int, int]]:
    start_rate = data[start][0]
    best_score = -1
    best_history: list[tuple[str, int, int]] = []
    current = start
    for next_valve in good_valves:
        distance = distance_map[current, next_valve]
        t = time_remaining - distance - 1
        if t < 1:
            continue
        rate = data[next_valve][0]
        remaining_values = good_valves.copy()
        remaining_values.remove(next_valve)
        s, h = calculate(data, remaining_values, distance_map, t, next_valve)
        score = rate * t + s
        if score > best_score:
            best_score = score
            best_history = h
    return best_score, [(start, start_rate, time_remaining)] + best_history


def determine_good_valves(data: dict[str, tuple[int, list[str], bool]]) -> set[str]:
    output = set()
    for name, (rate, _, _) in data.items():
        if rate > 0:
            output.add(name)
    return output


def calculate_distances(
        data: dict[str, tuple[int, list[str], bool]],
        good_valves: set[str],
        start: str
) -> dict[tuple[str, str], int]:
    output = {}
    for a in good_valves:
        distance = calculate_distance(data, start, a)
        output[(a, start)] = distance
        output[(start, a)] = distance

        for b in good_valves:
            if a < b:
                distance = calculate_distance(data, a, b)
                output[(a, b)] = distance
                output[(b, a)] = distance
    return output


def calculate_distance(
        data: dict[str, tuple[int, list[str], bool]],
        start: str,
        end: str
) -> int:
    count = 0
    _, x, _ = data[start]
    current_level = x.copy()
    while len(current_level):
        count += 1
        if end in current_level:
            return count
        next_level = set()
        while len(current_level):
            next_valve = current_level.pop()
            _, neighbors, _ = data[next_valve]
            for neighbor in neighbors:
                next_level.add(neighbor)
        current_level = next_level


def parse_input(raw_input):
    output = {}
    for row in raw_input:
        if row == "":
            continue
        words = row.split()
        x = words[1]
        y = int(words[4][5:-1])
        z = "".join(words[9:]).split(",")
        output[x] = (y, z, False)
    return output


if __name__ == "__main__":
    main()
