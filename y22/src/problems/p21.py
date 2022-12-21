from y22.src.utils import io

ME = "humn"


def main():
    current_day = io.get_day()
    for test in [False]:
        filename = io.get_input_filename(2022, current_day, test=test)
        raw_input = io.get_inputs_raw(filename)
        monkeys = parse_input(raw_input)
        print(get_value(monkeys, "root"))
        print(get_equality(monkeys, "root"))


def get_value(monkeys: dict[str, dict[str, any]], monkey: str) -> int:
    value = monkeys[monkey]["value"]
    if value is not None:
        return value

    children = monkeys[monkey]["children"]
    symbol = monkeys[monkey]["symbol"]

    value_a = get_value(monkeys, children[0])
    value_b = get_value(monkeys, children[1])

    if symbol == "+":
        return value_a + value_b
    if symbol == "-":
        return value_a - value_b
    if symbol == "/":
        return value_a // value_b
    if symbol == "*":
        return value_a * value_b


def has_me(monkeys: dict[str, dict[str, any]], monkey: str) -> bool:
    if monkey == ME:
        return True

    if monkeys[monkey]["value"] is not None:
        return False

    children = monkeys[monkey]["children"]
    return (
        has_me(monkeys, children[0]) or 
        has_me(monkeys, children[1])
    )


def get_equality(monkeys: dict[str, dict[str, any]], monkey: str, target: int | None = None ) -> int:
    if monkey == ME:
        return target

    children = monkeys[monkey]["children"]
    symbol = monkeys[monkey]["symbol"]

    other_child = 1 if has_me(monkeys, children[0]) else 0
    other_value = get_value(monkeys, children[other_child])

    if monkey == "root":
        next_target = other_value
    elif other_child == 0:
        if symbol == "+":
            next_target = target - other_value
        elif symbol == "-":
            next_target = other_value - target
        elif symbol == "/":
            next_target = other_value // target
        elif symbol == "*":
            next_target = target // other_value
        else:
            raise Exception("bad")
    else:
        if symbol == "+":
            next_target = target - other_value
        elif symbol == "-":
            next_target = target + other_value
        elif symbol == "/":
            next_target = target * other_value
        elif symbol == "*":
            next_target = target // other_value
        else:
            raise Exception("bad")

    return get_equality(monkeys, children[1 - other_child], next_target)


def parse_input(raw_data):
    monkeys = {}
    for row in raw_data:
        if row == "":
            continue

        monkey, formula = row.split(": ")

        symbol = None
        value = None
        children = []
        if any([_ in formula for _ in ["+", "-", "/", "*"]]):
            a, symbol, b = formula.split(" ")
            children = [a, b]
        else:
            value = int(formula)

        monkeys[monkey] = {
            "symbol": symbol,
            "children": children,
            "value": value
        }

    return monkeys


if __name__ == "__main__":
    main()
