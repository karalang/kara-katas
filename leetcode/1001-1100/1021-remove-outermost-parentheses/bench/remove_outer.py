# LeetCode #1021: Remove Outermost Parentheses -- bench
# Mirrors ./remove_outer.kara; see ../README.md § Benchmarks.


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


def main():
    count = 100
    rounds = 30
    seed = 1021

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    strings = []
    chars = 0
    for _ in range(count):
        pairs = (next_random() * 32768 + next_random()) % 50000 + 1
        open_ = 2 + next_random() % 5
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
        s = "".join(s)
        chars += len(s)
        strings.append(s)
    kept = 0
    check = 0
    for _ in range(rounds):
        for s in strings:
            answer = remove_outer_parentheses(s)
            n = len(answer)
            middle = ord(answer[n // 2]) if n > 0 else 0
            kept += n
            check = (check * 31 + n * 2 + middle) % 1000000007
    print(f"{count} strings, {chars} characters, {rounds} rounds: {kept} kept, checksum {check}")


main()
