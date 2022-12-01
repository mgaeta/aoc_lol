from typing import Mapping, Sequence

RING_SIZE = 10
memo = {}


def get_inputs(file):
    with open(file, "r") as f:
        return [_ for _ in f.read().split("\n") if _]


def get_roll_counts() -> Mapping[int, int]:
    return {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}


def play_1(i1: int, i2: int) -> int:
    count = 0
    scores = [0, 0]
    positions = [i1, i2]
    turn = 0
    while max(scores) < 1000:
        x = 0
        for i in range(3):
            count += 1
            x += (count % 100)

        next_value = (positions[turn] + x) % RING_SIZE

        scores[turn] += next_value + 1
        positions[turn] = next_value
        turn = int(not turn)

    return min(scores) * count


def play(scores: Sequence[int], positions: Sequence[int]):
    found = memo.get((tuple(scores), tuple(positions)))
    if found:
        return found

    output = [0, 0]
    for value, count in get_roll_counts().items():
        next_position = (positions[0] + value) % RING_SIZE
        current_scores = [
            scores[0] + next_position + 1,
            scores[1]
        ]
        current_positions = [next_position, positions[1]]
        if current_scores[0] >= 21:
            (i_win, u_win) = (1, 0)
        else:
            (u_win, i_win) = play(
                [current_scores[1], current_scores[0]],
                [current_positions[1], current_positions[0]],
            )
        output[0] += i_win * count
        output[1] += u_win * count

    memo[(tuple(scores), tuple(positions))] = output
    return output


def dirac(file: str) -> int:
    inputs = get_inputs(file)
    i1 = int(inputs[0][-1:]) - 1
    i2 = int(inputs[1][-1:]) - 1

    return max(play([0, 0], [i1, i2]))


# print(dirac("./inputs/21t.txt"))
print(dirac("./inputs/21.txt"))
print("done")
