# LeetCode #2522: Partition String Into Substrings With Values at Most K --
# Python mirror of the ★ arm (greedy.kara): each part grown while its value
# stays at most k; the same harness and output.


def minimum_partition(s, k):
    parts = 1
    value = 0
    for c in s:
        d = ord(c) - ord("0")
        if d > k:
            return -1
        value = value * 10 + d
        if value > k:
            parts += 1
            value = d
    return parts


seed = 2522


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    return next_random() * 32768 + next_random()


def digits(length):
    return "".join(chr(next_random() % 9 + 1 + ord("0")) for _ in range(length))


def main():
    fixed = [("165462", 60), ("238182", 5), ("1", 1), ("9", 8), ("111", 11), ("999999999", 999999999), ("9999999999", 999999999), ("123456789", 1)]
    for s, k in fixed:
        print(f'"{s}", {k} -> {minimum_partition(s, k)}')
    for most, big in [(10, False), (60, True)]:
        total = 0
        refused = 0
        check = 0
        for _ in range(2000):
            s = digits(next_random() % most + 1)
            k = wide_random() % 1000000000 + 1 if big else next_random() % 100 + 1
            a = minimum_partition(s, k)
            if a == -1:
                refused += 1
            else:
                total += a
            check = (check * 31 + a + 1) % 1000000007
        print(f"2000 random of up to {most} digits: total {total}, {refused} with -1, checksum {check}")
    print(f"10^5 nines, k 9: {minimum_partition('9' * 100000, 9)}")
    long = digits(100000)
    for k in [500, 1000000000, 8]:
        print(f"10^5 random digits, k {k}: {minimum_partition(long, k)}")


main()
