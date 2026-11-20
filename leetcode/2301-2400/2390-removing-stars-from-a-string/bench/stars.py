# LeetCode #2390: Removing Stars From a String -- the bench, the ★ arm in
# Python: a stack, a letter pushed and a star popping.

seed = 2390


def remove_stars(s):
    stack = []
    for c in s:
        if c == 42:
            if stack:
                stack.pop()
        else:
            stack.append(c)
    return bytes(stack)


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def starred(length, odds):
    out = []
    depth = 0
    for _ in range(length):
        if depth > 0 and next_random() % odds == 0:
            out.append(42)
            depth -= 1
        else:
            out.append(97 + next_random() % 26)
            depth += 1
    return bytes(out)


def main():
    strings = [starred(100000, 3) for _ in range(20)]
    check = 0
    for p in range(100):
        for s in strings:
            t = remove_stars(s)
            for b in t:
                check = (check * 31 + (b - 96)) % 1000000007
            check = (check * 31 + len(t) + p) % 1000000007
    print(f"100 passes over 20 strings of 10^5 characters: checksum {check}")


if __name__ == "__main__":
    main()
