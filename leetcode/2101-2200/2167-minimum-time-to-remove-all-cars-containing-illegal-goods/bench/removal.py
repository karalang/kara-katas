# LeetCode #2167: Minimum Time to Remove All Cars Containing Illegal Goods
# -- the benchmark's Python mirror of removal.kara.


def minimum_time(s):
    n = len(s)
    left = 0
    best = n
    for i, c in enumerate(s):
        if c == "1":
            left = min(left + 2, i + 1)
        best = min(best, left + n - 1 - i)
    return best


seed = 2167


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    train = "".join("1" if next_random() % 3 == 0 else "0" for _ in range(400000))
    check = 0
    for _ in range(100):
        start = (next_random() * 32768 + next_random()) % 200001
        t = minimum_time(train[start:start + 200000])
        check = (check * 31 + t) % 1000000007
    print(f"100 solves: checksum {check}")


main()
