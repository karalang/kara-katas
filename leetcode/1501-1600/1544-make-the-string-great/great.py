# LeetCode #1544: Make The String Great -- Python mirror of great.kara (the
# ★ arm, a stack); its output is byte-identical.


def make_good(s):
    stack = []
    for c in s:
        if stack and stack[-1] != c and stack[-1].lower() == c.lower():
            stack.pop()
        else:
            stack.append(c)
    return "".join(stack)


seed = 1544


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def letter(letters):
    base = ord("a") if next_random() % 2 == 0 else ord("A")
    return chr(base + next_random() % letters)


def batch(count, most, letters):
    check = 0
    empty = 0
    for _ in range(count):
        n = next_random() % most + 1
        used = next_random() % letters + 1
        s = "".join(letter(used) for _ in range(n))
        great = make_good(s)
        if not great:
            empty += 1
        check = mix(check, len(great))
        for b in great.encode():
            check = mix(check, b)
    print(f"{count} strings of up to {most} letters: {empty} empty, checksum {check}")


def main():
    examples = ["leEeetcode", "abBAcC", "s", "aA", "Aa", "aa", "abBA", "aBbAcCdD", "AbBa", "xyzZYX", "abcCBAd"]
    for s in examples:
        print(f'"{s}" -> "{make_good(s)}"')
    batch(3000, 12, 3)
    batch(300, 100, 2)
    batch(300, 100, 26)


main()
