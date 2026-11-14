# LeetCode #1544: Make The String Great -- bench: the ★ arm (a stack of
# chars) over 1000 strings of 1 to 100 letters (the constraint's bound),
# each over its own first 1 to 3 letters in both cases, built once, each
# made great 500 times. Python mirror of great.kara.


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


def main():
    strings = []
    for _ in range(1000):
        n = next_random() % 100 + 1
        used = next_random() % 3 + 1
        s = []
        for _ in range(n):
            base = ord("a") if next_random() % 2 == 0 else ord("A")
            s.append(chr(base + next_random() % used))
        strings.append("".join(s))
    check = 0
    total = 0
    for _ in range(500):
        for s in strings:
            great = make_good(s)
            total += len(great)
            check = mix(check, len(great))
    print(f"500 passes over 1000 strings of up to 100 letters: {total} letters kept, checksum {check}")


main()
