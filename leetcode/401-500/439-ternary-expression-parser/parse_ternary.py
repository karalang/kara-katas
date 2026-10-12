# LeetCode #439: Ternary Expression Parser -- mirror of
# parse_ternary.kara (a stack, scanning from the right).


def parse_ternary(expression):
    e = expression.encode()
    stack = []
    i = len(e)
    while i > 0:
        i -= 1
        if stack and stack[-1] == ord("?"):
            stack.pop()
            yes = stack.pop()
            stack.pop()
            no = stack.pop()
            stack.append(yes if e[i] == ord("T") else no)
        else:
            stack.append(e[i])
    return chr(stack[0])


def show(expression):
    print(f"\"{expression}\": {parse_ternary(expression)}")


seed = 439


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# Appends a random expression of at most depth levels to out and
# returns its value. Each branch of a ternary is a lone digit, T or F
# with chance 1 in 3, so the trees are ragged.
def random_expression(depth, out):
    if depth == 0:
        r = next_random() % 12
        leaf = chr(48 + r) if r < 10 else ("T" if r == 10 else "F")
        out.append(leaf)
        return leaf
    condition = "T" if next_random() % 2 == 0 else "F"
    out.append(condition)
    out.append("?")
    yes = random_expression(0 if next_random() % 3 == 0 else depth - 1, out)
    out.append(":")
    no = random_expression(0 if next_random() % 3 == 0 else depth - 1, out)
    return yes if condition == "T" else no


def main():
    show("T?2:3")
    show("F?1:T?4:5")
    show("T?T?F:5:3")
    show("T?F:T")
    show("F?T?1:2:F?3:4")
    show("F?1:F?2:F?3:F?4:F?5:F?6:F?7:F?8:9")
    show("T?T?T?T?T?1:2:3:4:5:6")
    show("F?T?T?1:2:3:T?F?4:5:6")
    # 300 random expressions of 1 to 10 levels.
    digits = 0
    trues = 0
    length = 0
    checksum = 0
    for _ in range(300):
        out = []
        depth = 1 + next_random() % 10
        random_expression(depth, out)
        expression = "".join(out)
        value = parse_ternary(expression)
        if value == "T":
            trues += 1
        elif value != "F":
            digits += 1
        length += len(expression)
        checksum = (checksum * 31 + ord(value)) % 1000000007
    print(f"300 random expressions, {length} characters: {digits} digits, {trues} T, {300 - digits - trues} F, checksum {checksum}")


main()
