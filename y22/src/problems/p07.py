from y22.src.utils import io


def main():
    current_day = io.get_day()

    for test in [True, False]:
        filename = io.get_input_filename(2022, current_day, test=test)
        raw_input = io.get_inputs_raw(filename)
        registry = build_file_system(raw_input)
        print(get_answer_2(registry))


class Node:
    def __init__(self, parent: "Node", name: str, size: int | None) -> None:
        self.children = []
        self.parent = parent
        self.name = name
        self.size = size
        self._size_cache = size

    def __repr__(self):
        return f"<{self.name}: {self.get_size()}>"

    def get_fullname(self):
        if self.parent is None:
            return "/"
        return f"{self.parent.get_fullname()}/{self.name}"

    def get_size(self):
        if self._size_cache is not None:
            return self._size_cache

        if len(self.children) == 0:
            return self.size

        output = 0
        for child in self.children:
            output += child.get_size()

        self._size_cache = output
        return output


def build_file_system(raw_input):
    registry = {}

    root = Node(None, "/", None)
    current_node = root
    registry["/"] = root
    for row in raw_input[1:]:
        if row == "":
            continue

        if row == "$ ls":
            continue

        if row == "$ cd ..":
            current_node = current_node.parent
            continue

        if row.startswith("$ cd "):
            _, __, next_dir = row.split(" ")
            for child in current_node.children:
                if child.name == next_dir:
                    current_node = child
            continue

        if row.startswith("dir"):
            _, name = row.split(" ")
            next_child = Node(current_node, name, None)
            registry[next_child.get_fullname()] = next_child
        else:
            size_str, name = row.split(" ")
            next_child = Node(current_node, name, int(size_str))
        current_node.children.append(next_child)

    return registry


def get_answer_1(registry):
    output = 0
    for key, value in registry.items():
        if value.get_size() <= 100_000 and len(value.children):
            output += value.get_size()
    return output


def get_answer_2(registry):
    closest_value = 70_000_000
    free_space = 70_000_000 - registry["/"].get_size()

    for value in registry.values():
        next_size = value.get_size()
        if 30_000_000 - free_space <= next_size < closest_value:
            closest_value = next_size
    return closest_value


if __name__ == "__main__":
    main()
