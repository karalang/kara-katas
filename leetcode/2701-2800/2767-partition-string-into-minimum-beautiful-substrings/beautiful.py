# LeetCode #2767: Partition String Into Minimum Beautiful Substrings --
# the ★ arm in Python (beautiful.kara): the fewest pieces for each prefix,
# each last piece tried from every cut, kept when it starts with a 1 and
# its value is a power of 5.


def is_power_of_five(v):
    while v > 1 and v % 5 == 0:
        v //= 5
    return v == 1


def minimum_beautiful_substrings(s):
    n = len(s)
    best = [-1] * (n + 1)
    best[0] = 0
    for i in range(1, n + 1):
        for j in range(i):
            if best[j] < 0 or s[j] != "1":
                continue
            if is_power_of_five(int(s[j:i], 2)):
                if best[i] < 0 or best[j] + 1 < best[i]:
                    best[i] = best[j] + 1
    return best[n]


seed = 2767


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def binary(v, length):
    return "".join("1" if (v >> (length - 1 - k)) & 1 == 1 else "0" for k in range(length))


def fold(a, acc):
    if a > 0:
        acc[0] += 1
        acc[1] += a
    acc[2] = (acc[2] * 31 + a + 1) % 1000000007


def main():
    for s in ["1011", "111", "0", "1", "11001", "1111101", "101101", "1001110001", "11110100001001"]:
        print(minimum_beautiful_substrings(s))
    acc = [0, 0, 0]
    for length in range(1, 11):
        for v in range(1 << length):
            fold(minimum_beautiful_substrings(binary(v, length)), acc)
    print(f"2046 strings up to 10 long: {acc[0]} split, pieces sum to {acc[1]}, checksum {acc[2]}")
    acc = [0, 0, 0]
    powers = ["1", "101", "11001", "1111101", "1001110001", "110000110101", "11110100001001"]
    for _ in range(3000):
        # powers of 5 joined while they fit in 15, then half the time one
        # place flipped
        s = ""
        while True:
            p = powers[next_random() % 7]
            if len(s) + len(p) > 15:
                break
            s += p
        if next_random() % 2 == 1:
            k = next_random() % len(s)
            s = s[:k] + ("0" if s[k] == "1" else "1") + s[k + 1:]
        fold(minimum_beautiful_substrings(s), acc)
    print(f"3000 joined powers: {acc[0]} split, pieces sum to {acc[1]}, checksum {acc[2]}")


main()
