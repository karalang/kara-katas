# LeetCode #1576: Replace All ?'s to Avoid Consecutive Repeating Characters
# -- the Python mirror of the ★ arm: each '?' left to right made the first
# of 'a', 'b', 'c' that is neither the char before it nor the char after
# it. O(n)


def modify_string(s):
    cs = list(s)
    n = len(cs)
    for i in range(n):
        if cs[i] == "?":
            for c in "abc":
                if (i == 0 or cs[i - 1] != c) and (i + 1 == n or cs[i + 1] != c):
                    cs[i] = c
                    break
    return "".join(cs)


# ---- the harness: the same in every arm

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def draw(n, odds, letters):
    s = []
    last = " "
    for _ in range(n):
        if next_random() % odds == 0:
            s.append("?")
            last = "?"
        else:
            k = next_random() % letters
            if chr(ord("a") + k) == last:
                k = (k + 1) % letters
            c = chr(ord("a") + k)
            s.append(c)
            last = c
    return "".join(s)


def batch(count, most, letters):
    check = 0
    marks = 0
    for _ in range(count):
        n = (next_random() * 32768 + next_random()) % most + 1
        odds = next_random() % 4 + 1
        s = draw(n, odds, letters)
        marks += s.count("?")
        for c in modify_string(s):
            check = mix(check, ord(c))
    print(f"{count} strings of up to {most} characters, {marks} marks: checksum {check}")


def main():
    global seed
    examples = ["?zs", "ubv?w", "j?qg??b", "??yw?ipkj?", "?", "??", "a?a", "a?b", "???????", "ab?ba"]
    for s in examples:
        print(f"{s} -> {modify_string(s)}")
    seed = 1576
    batch(3000, 8, 3)
    batch(300, 1000, 26)
    batch(30, 100, 2)


main()
