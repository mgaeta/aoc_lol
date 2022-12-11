from y22.src.utils import io


def main():
    current_day = io.get_day()

    for test in [False]:
        filename = io.get_input_filename(2022, current_day, test=test)
        raw_input = io.get_inputs_raw(filename)

        monkeys = parse_monkey_data(raw_input)
        print(simulate2(monkeys))


def calculate_monkey_business(counts: list[int]) -> int:
    counts.sort(reverse=True)
    return counts[0] * counts[1]


def get_lcd(monkeys: list[dict[str, int | str]]) -> int:
    product = 1
    for monkey in monkeys:
        product *= monkey["test_divisible_by"]
    return product


def simulate2(monkeys: list[dict[str, int | str | list[int]]], rounds: int = 10000) -> int:
    lcd = get_lcd(monkeys)
    counts = [0] * len(monkeys)
    for current_round in range(rounds):
        for monkey_index, monkey in enumerate(monkeys):
            while len(monkey["items"]):
                current_item = monkey["items"].pop(0)
                counts[monkey_index] += 1
                if monkey["operation_symbol"] == "^":
                    current_item = current_item * current_item
                elif monkey["operation_symbol"] == "+":
                    current_item = current_item + monkey["operation_amount"]
                elif monkey["operation_symbol"] == "*":
                    current_item = current_item * monkey["operation_amount"]

                current_item = current_item % lcd

                if current_item % monkey["test_divisible_by"] == 0:
                    next_monkey = monkey["true_monkey"]
                else:
                    next_monkey = monkey["false_monkey"]

                monkeys[next_monkey]["items"].append(current_item)

    return calculate_monkey_business(counts)


def simulate1(monkeys: list[dict[str, int | str | list[int]]], rounds: int = 20) -> int:
    counts = [0] * len(monkeys)
    for current_round in range(rounds):
        for monkey_index, monkey in enumerate(monkeys):
            while len(monkey["items"]):
                current_item = monkey["items"].pop(0)
                counts[monkey_index] += 1
                if monkey["operation_symbol"] == "^":
                    current_item = current_item * current_item
                elif monkey["operation_symbol"] == "+":
                    current_item = current_item + monkey["operation_amount"]
                elif monkey["operation_symbol"] == "*":
                    current_item = current_item * monkey["operation_amount"]

                current_item = current_item // 3

                if current_item % monkey["test_divisible_by"] == 0:
                    next_monkey = monkey["true_monkey"]
                else:
                    next_monkey = monkey["false_monkey"]

                monkeys[next_monkey]["items"].append(current_item)

    return calculate_monkey_business(counts)


def parse_monkey_data(raw_input) -> list[dict[str, int | str | list[int]]]:
    monkeys = []
    current_monkey = {}
    for i, row in enumerate(raw_input):
        if i % 7 == 1:
            current_monkey["items"] = [int(_) for _ in row.split(": ")[1].split(", ")]
        if i % 7 == 2:
            current_monkey["operation_symbol"] = row[23]
            amount = row[25:]
            if amount == "old":
                current_monkey["operation_symbol"] = "^"
            else:
                current_monkey["operation_amount"] = int(amount)
        if i % 7 == 3:
            current_monkey["test_divisible_by"] = int(row[21:])
        if i % 7 == 4:
            current_monkey["true_monkey"] = int(row[29:])
        if i % 7 == 5:
            current_monkey["false_monkey"] = int(row[30:])
        if i % 7 == 6:
            monkeys.append(current_monkey)
            current_monkey = {}
    return monkeys


if __name__ == "__main__":
    main()
