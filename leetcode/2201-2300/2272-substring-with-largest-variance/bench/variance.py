# LeetCode #2272: Substring With Largest Variance -- the bench, the ★ arm.

MIN = -(2 ** 63) // 2


def largest_variance(s):
    data = s.encode()
    seen = [False] * 26
    for c in data:
        seen[c - 97] = True
    best = 0
    for a in range(97, 123):
        for b in range(97, 123):
            if a == b or not seen[a - 97] or not seen[b - 97]:
                continue
            diff = 0
            with_b = MIN
            for c in data:
                if c == a:
                    diff += 1
                    with_b += 1
                elif c == b:
                    with_b = diff - 1
                    diff = max(diff - 1, 0)
                best = max(best, with_b)
    return best


# ---- bench harness ---------------------------------------------------------

seed = 2272


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    check = 0
    for t in range(40):
        k = [3, 5, 10, 26][t % 4]
        s = "".join(chr(97 + next_random() % k) for _ in range(10000))
        check = (check * 31 + largest_variance(s)) % 1000000007
    print(f"40 strings of 10^4: checksum {check}")


main()
