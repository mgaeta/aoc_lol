from collections import defaultdict

from y22.src.utils import io

# TIME = 24
TIME = 32


def main():
    current_day = io.get_day()
    for test in [False]:
        filename = io.get_input_filename(2022, current_day, test=test)
        raw_input = io.get_inputs_raw(filename)
        data = parse_input(raw_input)
        print(simulate(data))


def get_key(
        inventory: dict[str, int],
        robots: dict[str, int],
        time_remaining: int
) -> tuple[int, int, int, int, int, int, int, int, int]:
    return (
        inventory["ore"],
        inventory["clay"],
        inventory["obsidian"],
        inventory["geode"],
        robots["ore"],
        robots["clay"],
        robots["obsidian"],
        robots["geode"],
        time_remaining
    )


def can_buy(
        robot: str,
        costs: dict[str, dict[str, int]],
        inventory: dict[str, int],
        verbose: bool = False
) -> bool:
    for item, amount in costs[robot].items():
        if verbose:
            print("item", item, "amount", amount, "inventory[item]", inventory[item])
        if inventory[item] < amount:
            return False
    return True


def should_buy(
        robot: str,
        costs: dict[str, dict[str, int]],
        robots: dict[str, int],
        verbose: bool = False
) -> bool:
    """
    There shouldn't be a reason to purchase the N+1th ore robot if the most
    expensive robot only asks for N ore.
    """
    if robot == "geode":
        return True
    if verbose:
        print("should buy", robot, costs)
    for robot_option, cost in costs.items():
        max_amount = -1
        for item, amount in cost.items():
            if robot == item and amount > max_amount:
                max_amount = amount
        if robots[robot] < max_amount:
            return True
    return False


def get_score(
        memo,
        costs: dict[str, dict[str, int]],
        inventory: dict[str, int],
        robots: dict[str, int],
        time_remaining: int = TIME,
        verbose: bool = False,
) -> int:
    if time_remaining <= 1:
        return inventory["geode"] + robots["geode"] * time_remaining

    key = get_key(inventory, robots, time_remaining)
    if verbose:
        print(key)
    if key in memo:
        return memo[key]

    if verbose:
        print("- INVENTORY ------------")
        print(inventory)
        print("------------------------")

    purchase_options = [""]
    for robot, cost in costs.items():
        if can_buy(robot, costs, inventory, verbose) and should_buy(robot, costs, robots):
            purchase_options.append(robot)

    if "geode" in purchase_options:
        purchase_options = ["geode"]
    elif "obsidian" in purchase_options:
        purchase_options = ["obsidian"]

    if verbose:
        print("purchase_options", purchase_options)

    # HARVEST
    for robot, count in robots.items():
        inventory[robot] += count

    # RECEIVE
    best_score = -1
    for robot in purchase_options:
        next_inventory = inventory.copy()
        next_robots = robots.copy()
        if robot:
            next_robots[robot] += 1
            for item, amount in costs[robot].items():
                next_inventory[item] -= amount

        score = get_score(
            memo,
            costs,
            inventory=next_inventory,
            robots=next_robots,
            time_remaining=time_remaining - 1,
            verbose=verbose,
        )
        if score > best_score:
            best_score = score

    # MEMOIZE
    memo[key] = best_score
    return best_score


def simulate(data):
    output = 0

    for row in data[:3]:
        memo = {}
        inventory = defaultdict(int)
        robots = defaultdict(int)
        robots["ore"] = 1
        score = get_score(
            memo,
            row["plans"],
            inventory=inventory,
            robots=robots,
            time_remaining=TIME,
            verbose=False
        )
        print(score)
        output += row["id"] * score
    return output


def parse_input(raw_data):
    output = []
    for row in raw_data:
        if row == "":
            continue

        p = row.split(":")
        blueprint_id = int(p[0][9:])

        plans = defaultdict(dict)
        for sentence in p[1][1:].split(". "):
            words = sentence.split()
            cost_parts = " ".join(words[4:]).split(" and ")
            for cost_part in cost_parts:
                amount, v = cost_part.split(" ")
                amount = int(amount)
                v = v.replace(".", "")

                plans[words[1]][v] = amount

        output.append({
            "id": blueprint_id,
            "plans": plans,
        })
    return output


if __name__ == "__main__":
    main()
