# LeetCode #2896: Apply Operations to Make Two Strings Equal -- the bench, as
# flips.kara: 5000 pairs of 500 characters, each answered 20 times by
# the pairing arm.


def min_operations(s1, s2, x):
    places = [i for i in range(len(s1)) if s1[i] != s2[i]]
    m = len(places)
    if m % 2 == 1:
        return -1
    doubled = [0] * (m + 1)
    for i in range(1, m + 1):
        doubled[i] = doubled[i - 1] + x
        if i >= 2:
            doubled[i] = min(doubled[i], doubled[i - 2] + 2 * (places[i - 1] - places[i - 2]))
    return doubled[m] // 2


seed = 2896


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def bits(n):
    return "".join("0" if next_random() % 2 == 0 else "1" for _ in range(n))


def main():
    count, rounds, n = 5000, 20, 500
    cases = []
    for c in range(count):
        x = next_random() % 500 + 1
        s1 = bits(n)
        if c % 2 == 0:
            s2 = bits(n)
        else:
            chars = list(s1)
            for _ in range(next_random() % 20):
                at = next_random() % n
                chars[at] = "1" if chars[at] == "0" else "0"
            s2 = "".join(chars)
        cases.append((s1, s2, x))
    total = 0
    check = 0
    for r in range(rounds):
        for s1, s2, x in cases:
            cost = min_operations(s1, s2, x)
            total += cost
            check = (check * 31 + cost + 1 + r) % 1000000007
    print(f"{count} pairs of {n}, {rounds} rounds: costs total {total}, checksum {check}")


main()
