import functools
import json

from y22.src.utils import io


def main():
    current_day = io.get_day()
    for test in [True, False]:
        filename = io.get_input_filename(2022, current_day, test=test)
        raw_input = io.get_inputs_raw(filename)

        pairs = parse_inputs(raw_input)
        unsorted = []
        for left, right in pairs:
            unsorted.append(left)
            unsorted.append(right)

        unsorted.append([[2]])
        unsorted.append([[6]])

        sorted_packets = sort_packets(unsorted)
        print(get_decoder_key(sorted_packets))


def sort_packets(unsorted_packets: list[any]) -> list[any]:
    return sorted(unsorted_packets, key=functools.cmp_to_key(compare), reverse=True)


def get_decoder_key(sorted_packets: list[any]) -> int:
    two_packet_index = -1
    for i, value in enumerate(sorted_packets):
        if value == [[2]]:
            two_packet_index = i + 1
        elif value == [[6]]:
            return two_packet_index * (i + 1)
    return -1


def compare(left: list[any] | int, right: list[any] | int, verbose=False) -> int:
    if verbose:
        print(left, right)

    if type(left) == int and type(right) == int:
        if verbose:
            print("int,int:", left, right, right - left)
        return right - left
    elif type(left) == list and type(right) == int:
        return compare(left, [right], verbose=verbose)
    elif type(left) == int and type(right) == list:
        return compare([left], right, verbose=verbose)
    elif type(left) == list and type(right) == list:
        if verbose:
            print("march", left, right)

        for i in range(min(len(left), len(right))):
            cmp = compare(left[i], right[i], verbose=verbose)
            if verbose:
                print("cmp:", cmp)
            if cmp:
                return cmp

            # cmp == 0 when they're the same
            if verbose:
                print("same", left[i], right[i])
        return len(right) - len(left)
    else:
        raise Exception("bad", type(left), type(right))


def get_valid_pairs(raw_input, verbose=False) -> int:
    output = []
    pairs = parse_inputs(raw_input)
    for i, (left, right) in enumerate(pairs):
        if compare(left, right, verbose=verbose) > 0:
            output.append(i + 1)
    if verbose:
        print(output)
    return sum(output)


def parse_inputs(raw_input) -> list[tuple[int, int]]:
    output = []
    left = None
    for i, row in enumerate(raw_input):
        if i % 3 == 0:
            left = row
        if i % 3 == 1:
            output.append((json.loads(left), json.loads(row)))
    return output


if __name__ == "__main__":
    main()
