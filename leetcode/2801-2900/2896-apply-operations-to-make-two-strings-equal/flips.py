# LeetCode #2896: Apply Operations to Make Two Strings Equal -- the Python
# mirror of the ★ arm (flips.kara): the differences paired in order, in
# doubled costs, x for half a pair or twice the gap to the one before.


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


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def bits(n):
    return "".join("0" if next_random() % 2 == 0 else "1" for _ in range(n))


def main():
    global seed
    print(f"{min_operations('1100011000', '0101001010', 2)} {min_operations('10110', '00011', 4)}")
    zeros = "0" * 500
    ones = "1" * 500
    thirds = "".join("1" if i % 3 == 0 else "0" for i in range(500))
    print(f"{min_operations(zeros, ones, 500)} {min_operations(zeros, ones, 1)} {min_operations(zeros, thirds, 5)}")
    seed = 2896
    total = 0
    check = 0
    impossible = 0
    for c in range(3300):
        small = c < 3000
        n = next_random() % 10 + 1 if small else next_random() % 401 + 100
        x = next_random() % 5 + 1 if small else next_random() % 500 + 1
        s1 = bits(n)
        if small or c % 2 == 0:
            s2 = bits(n)
        else:
            chars = list(s1)
            for _ in range(next_random() % 20):
                at = next_random() % n
                chars[at] = "1" if chars[at] == "0" else "0"
            s2 = "".join(chars)
        cost = min_operations(s1, s2, x)
        if cost < 0:
            impossible += 1
        else:
            total += cost
        check = (check * 31 + cost + 1) % 1000000007
        if c == 2999 or c == 3299:
            print(f"{'3000 short' if small else '300 long'} pairs: {impossible} impossible, costs total {total}, checksum {check}")
            total = 0
            check = 0
            impossible = 0


main()
