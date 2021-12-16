from typing import Tuple, List


def get_inputs(file):
    with open(file, "r") as f:
        return [_ for _ in f.read().split() if _]


def to_bits(value):
    table = {
        "0": "0000",
        "1": "0001",
        "2": "0010",
        "3": "0011",
        "4": "0100",
        "5": "0101",
        "6": "0110",
        "7": "0111",
        "8": "1000",
        "9": "1001",
        "A": "1010",
        "B": "1011",
        "C": "1100",
        "D": "1101",
        "E": "1110",
        "F": "1111",
    }
    return "".join([
        table[_] for _ in value
    ])


def decode_literal(bits: str, index_start: int, depth: int) -> Tuple[int, int]:
    output = ""
    done = False
    i = 0
    while not done:
        next_blob = bits[index_start + i * 5: index_start + (i+1) * 5]
        i += 1
        if next_blob[0] == "0":
            done = True
        output += next_blob[1:]

    literal = int(output, 2)
    return literal, i * 5


def decode_sub_packets(bits: str, start_index: int, depth: int) -> Tuple[List[int], int]:
    if bits[start_index] == "0":
        WIDTH = 15
        start = start_index + 1 + WIDTH
        packet_length = int(bits[start_index + 1: start], 2)

        values = decode_length(bits[start:start + packet_length], depth + 1)
        bits_consumed = 1 + WIDTH + packet_length
    else:
        WIDTH = 11
        start = start_index + 1 + WIDTH
        packet_count = int(bits[start_index + 1: start], 2)

        values, new_bits_consumed = decode_count(bits[start:], packet_count, depth + 1)
        bits_consumed = 1 + WIDTH + new_bits_consumed

    return values, bits_consumed


def get_headers(bits: str, index: int, depth: int) -> Tuple[int, int]:
    version = int(bits[index: index + 3], 2)
    type_id = int(bits[index + 3: index + 6], 2)
    return version, type_id


def decode_packet(bits: str, start_index: int, depth: int) -> Tuple[int, int]:
    version, type_id = get_headers(bits, start_index, depth)
    bits_consumed = 6
    if type_id == 4:
        literal, new_bits_consumed = decode_literal(bits, start_index + 6, depth)
        bits_consumed += new_bits_consumed
        return literal, bits_consumed

    output = None
    packet_values, new_bits_consumed = decode_sub_packets(bits, start_index + 6, depth)
    bits_consumed += new_bits_consumed

    if type_id == 0:
        output = sum(packet_values)
    elif type_id == 1:
        output = 1
        for i in packet_values:
            output *= i
    elif type_id == 2:
        output = min(packet_values)
    elif type_id == 3:
        output = max(packet_values)
    elif type_id == 5:
        output = 1 if packet_values[0] > packet_values[1] else 0
    elif type_id == 6:
        output = 1 if packet_values[0] < packet_values[1] else 0
    elif type_id == 7:
        output = 1 if packet_values[0] == packet_values[1] else 0

    return output, bits_consumed


def decode_count(bits: str, count: int, depth: int) -> Tuple[List[int], int]:
    output = []
    start_index = 0
    for i in range(count):
        next_output, new_bits_consumed = decode_packet(bits, start_index, depth)
        start_index += new_bits_consumed
        output.append(next_output)
    return output, start_index


def decode_length(bits: str, depth: int) -> List[int]:
    output = []
    start_index = 0
    while start_index < len(bits):
        tail = bits[start_index:]
        if int(tail, 2) == 0:
            break

        packet_value, new_bits_consumed = decode_packet(bits, start_index, depth)
        output.append(packet_value)
        start_index += new_bits_consumed
    return output


def decode(file: str) -> List[int]:
    inputs = get_inputs(file)
    return [decode_length(to_bits(i), 0)[0] for i in inputs]


# print(decode("./inputs/16tt.txt"))
print(decode("./inputs/16t.txt"))
# print(decode("./inputs/16.txt"))
print("done")
