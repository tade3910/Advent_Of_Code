import z3

def parse_expected(token: str) -> list[bool]:
    return [c == '#' for c in token]

def get_int(v: str) -> int:
    if v == "":
        return 0
    try:
        return int(v)
    except ValueError:
        raise ValueError(f"Cannot convert {v} to int")

def get_int_slice(token: str) -> list[int]:
    if not token:
        return []
    parts = token.split(",")
    return [get_int(p) for p in parts]

def part2(filename: str):
    total_presses = 0

    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            tokens = line.split(" ")

            buttons = []
            # expected = [] //don't even need this lol
            joltages = []

            for token in tokens:
                specified = token[0]
                content = token[1:-1]

                if specified == '[':
                    continue
                elif specified == '(':
                    buttons.append(get_int_slice(content))
                else:
                    pass
                    joltages = get_int_slice(content)
            presses = [z3.Int(f"press{i}") for i in range(len(buttons)) ]
            s = z3.Optimize()
            s.add(z3.And([press >= 0 for press in presses]))
            s.add(z3.And([
                sum(presses[j] for j, button in enumerate(buttons) if i in button) == joltage
                    for i, joltage in enumerate(joltages)
            ]))
            s.minimize(sum(presses))
            assert s.check() == z3.sat

            m = s.model()
            for press in presses:
                total_presses = total_presses + m[press].as_long()
    print(total_presses)

part2("input.txt")
