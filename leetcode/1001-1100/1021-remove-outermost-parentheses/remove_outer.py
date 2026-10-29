# LeetCode #1021: Remove Outermost Parentheses -- a depth counter
# Mirrors remove_outer.kara (the ★ arm) and prints the same output.


def remove_outer_parentheses(s):
    out = []
    depth = 0
    for c in s:
        if c == "(":
            if depth > 0:
                out.append(c)
            depth += 1
        else:
            depth -= 1
            if depth > 0:
                out.append(c)
    return "".join(out)


seed = 1021


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_valid(pairs, open_):
    s = []
    left = pairs
    depth = 0
    while left > 0 or depth > 0:
        if depth == 0:
            opens = True
        elif left == 0:
            opens = False
        else:
            opens = next_random() % 8 < open_
        if opens:
            s.append("(")
            left -= 1
            depth += 1
        else:
            s.append(")")
            depth -= 1
    return "".join(s)


def checksum(check, s):
    h = check
    for c in s:
        h = (h * 31 + (1 if c == "(" else 2)) % 1000000007
    return h


def main():
    examples = ["(()())(())", "(()())(())(()(()))", "()()", "()", "(())", "((()))", "(()(()))()(((())))", "()(())()((()))"]
    for s in examples:
        print(f'"{s}" -> "{remove_outer_parentheses(s)}"')
    groups = [(3000, 5, 4), (1000, 20, 4), (300, 100, 2), (300, 100, 6), (30, 2000, 4), (30, 2000, 7)]
    for count, pairs, open_ in groups:
        kept = 0
        primitives = 0
        check = 0
        for _ in range(count):
            s = random_valid(pairs, open_)
            answer = remove_outer_parentheses(s)
            kept += len(answer)
            primitives += (len(s) - len(answer)) // 2
            check = checksum(check, answer)
        print(f"{count} random strings of {pairs} pairs ({open_}/8 open): {kept} kept, {primitives} primitives, checksum {check}")
    deep = "(" * 3000 + ")" * 3000
    flat = "()" * 3000
    d = remove_outer_parentheses(deep)
    f = remove_outer_parentheses(flat)
    print(f"nested 3000 deep: {len(d)} kept, checksum {checksum(0, d)}; 3000 side by side: {len(f)} kept")


main()
