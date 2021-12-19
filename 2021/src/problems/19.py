from typing import Optional, Set, Tuple

# MIN_MATCHES = 3  # 2D
MIN_MATCHES = 12  # 3D


def get_inputs(file):
    with open(file, "r") as f:
        return [_ for _ in f.read().split("\n\n") if _]


def get_coordinates(line: str) -> Set[Tuple[int, int, int]]:
    output = set()
    for j in line.split("\n")[1:]:
        i = j.split(",")
        if len(i) == 3:
            output.add((int(i[0]), int(i[1]), int(i[2])))
    return output


def rotate_vectors(
    vectors: Set[Tuple[int, int, int]],
    rotation_vector: Tuple[int, int, int],
) -> Set[Tuple[int, int, int]]:
    return {rotate_vector(v, rotation_vector) for v in vectors}


def transform_coordinates_by_vector(
    coordinates: Set[Tuple[int, int, int]],
    v_0: Tuple[int, int, int],
) -> Set[Tuple[int, int, int]]:
    return set(transform_vector_by_vector(v, v_0) for v in coordinates)


def invert_vector(
    v: Tuple[int, int, int],
) -> Tuple[int, int, int]:
    x, y, z = v
    return -x, -y, -z


def transform_vector_by_vector(
    v: Tuple[int, int, int],
    v_0: Tuple[int, int, int],
) -> Tuple[int, int, int]:
    x, y, z = v
    x0, y0, z0 = v_0
    return (x + x0), (y + y0), (z + z0)


def rotate_vector(
    vector: Tuple[int, int, int],
    rotation_vector: Tuple[int, int, int],
) -> Tuple[int, int, int]:
    x, y, z = vector
    rotate_x, rotate_y, rotate_z = rotation_vector
    if rotate_x:
        return rotate_vector(
            (x, z, -y),
            (rotate_x - 1, rotate_y, rotate_z)
        )
    if rotate_y:
        return rotate_vector(
            (-z, y, x),
            (rotate_x, rotate_y - 1, rotate_z)
        )
    if rotate_z:
        return rotate_vector(
            (-y, x, z),
            (rotate_x, rotate_y, rotate_z - 1)
        )
    return vector


def rotate_b_until_matches_a(
    coordinates_a: Set[Tuple[int, int, int]],
    coordinates_b: Set[Tuple[int, int, int]]
) -> Optional[Tuple[Set[Tuple[int, int, int]], Tuple[int, int, int]]]:
    for rotate_x in range(4):
        for rotate_y in range(4):
            for rotate_z in range(4):
                transformed_coordinates_b = rotate_vectors(coordinates_b, (rotate_x, rotate_y, rotate_z))
                overlap = len(transformed_coordinates_b.intersection(coordinates_a))
                if overlap >= MIN_MATCHES:
                    return transformed_coordinates_b, (rotate_x, rotate_y, rotate_z)
    return None


def get_beacon_coordinates(
    coordinates_relative_to_s0: Set[Tuple[int, int, int]],
    new_coordinates: Set[Tuple[int, int, int]]
) -> Optional[Tuple[Set[Tuple[int, int, int]], Tuple[int, int, int]]]:
    for bai in coordinates_relative_to_s0:
        coordinates_relative_to_s0_bi = transform_coordinates_by_vector(
            coordinates_relative_to_s0,
            invert_vector(bai)
        )
        for bbj in new_coordinates:

            coordinates_relative_to_si_bj = transform_coordinates_by_vector(
                new_coordinates,
                invert_vector(bbj)
            )

            result = rotate_b_until_matches_a(coordinates_relative_to_s0_bi, coordinates_relative_to_si_bj)
            if result:
                coordinates_relative_to_si_bj_rotated, rotation_vector = result
                output_relative_to_s0 = transform_coordinates_by_vector(
                    coordinates_relative_to_si_bj_rotated,
                    bai
                )
                si_relative_to_bbj = rotate_vector(invert_vector(bbj), rotation_vector)
                si_relative_to_s0 = transform_vector_by_vector(si_relative_to_bbj, bai)
                return output_relative_to_s0, si_relative_to_s0
    return None


def triangulate(file: str):
    coordinates_by_beacon = list(reversed([get_coordinates(line) for line in get_inputs(file)]))
    total = len(coordinates_by_beacon)
    found_scanners = {(0, 0, 0)}
    all_beacons_relative_to_S0 = set(b for b in coordinates_by_beacon.pop())
    while len(coordinates_by_beacon):
        next_coordinates = coordinates_by_beacon.pop()
        result = get_beacon_coordinates(all_beacons_relative_to_S0, next_coordinates)
        if not result:
            coordinates_by_beacon.insert(0, next_coordinates)
        else:
            new_beacons, new_scanner = result
            all_beacons_relative_to_S0 = all_beacons_relative_to_S0.union(new_beacons)
            found_scanners.add(new_scanner)
            print(f"----------- found {len(found_scanners)}/{total} -----------")

    return get_max_manhattan(found_scanners)


def manhattan(v0: Tuple[int, int, int], v1: Tuple[int, int, int]) -> int:
    x0, y0, z0 = v0
    x1, y1, z1 = v1
    return abs(x1 - x0) + abs(y1 - y0) + abs(z1 - z0)


def get_max_manhattan(scanners: Set[Tuple[int, int, int]]) -> int:
    return max(manhattan(a, b) for a in scanners for b in scanners if a != b)


# print(triangulate("./inputs/19tttt.txt"))
print(triangulate("./inputs/19t.txt"))
# print(triangulate("./inputs/19.txt"))
print("done")
