from y22.src.utils import io


FACTOR = 811589153


def main():
    current_day = io.get_day()
    for test in [True, False]:
        filename = io.get_input_filename(2022, current_day, test=test)
        raw_input = io.get_inputs_raw(filename)
        data = parse_input(raw_input)
        print(mix(data))
        print(mix(data, FACTOR, 10))


def sequence_to_str(x: list[tuple[int, int]]) -> str:
    return ", ".join([str(_[1]) for _ in x])


def mix(ring: list[tuple[int, int]], factor: int = 1, count: int = 1):
    for j in range(count):
        for i in range(len(ring)):
            ring = step(ring, find_id(ring, i), factor)
    return find_coordinates(ring, factor)


def step(ring: list[tuple[int, int]], index: int, factor: int) -> list[tuple[int, int]]:
    item = ring[index]
    i, value = item
    target = (index + (value * factor)) % (len(ring) - 1)

    if target > index:
        return ring[:index] + ring[index + 1:target+1] + [item] + ring[target + 1:]
    else:
        return ring[:target] + [item] + ring[target:index] + ring[index + 1:]


def find_value(ring: list[tuple[int, int]], value: int) -> int:
    for i, (_, v) in enumerate(ring):
        if v == value:
            return i
    raise Exception("bad")


def find_id(ring: list[tuple[int, int]], id_: int) -> int:
    for i, (_id, _) in enumerate(ring):
        if _id == id_:
            return i
    raise Exception("cannot find", id_)


def find_coordinates(ring: list[tuple[int, int]], factor: int):
    i = find_value(ring, 0)

    return sum([
        ring[(i + 1000) % len(ring)][1] * factor,
        ring[(i + 2000) % len(ring)][1] * factor,
        ring[(i + 3000) % len(ring)][1] * factor,
    ])


def parse_input(raw_data):
    output = []
    for row in raw_data:
        if row == "":
            continue

        output.append(int(row))
    return list(enumerate(output))


if __name__ == "__main__":
    main()
