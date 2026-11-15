# LeetCode #2167: Minimum Time to Remove All Cars Containing Illegal Goods
# -- the Python mirror of removal.kara: one pass from the front, the
# least time that clears the cars so far, and every car after it taken
# from the back.


def minimum_time(s):
    n = len(s)
    left = 0
    best = n
    for i, c in enumerate(s):
        if c == "1":
            left = min(left + 2, i + 1)
        best = min(best, left + n - 1 - i)
    return best


# ---- test harness ---------------------------------------------------------

seed = 2167


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(s):
    print(f'"{s}" -> {minimum_time(s)}')


def main():
    show("1100101")
    show("0010")
    show("0")
    show("1")
    show("11111")
    show("0001000")
    show("1000000001")
    total = 0
    check = 0
    for rnd in range(2000):
        length = next_random() % 20 + 1
        odds = [2, 4, 8][rnd % 3]
        s = "".join("1" if next_random() % odds == 0 else "0" for _ in range(length))
        t = minimum_time(s)
        total += t
        check = (check * 31 + t) % 1000000007
    print(f"2000 trains: {total} in all, checksum {check}")
    s = "".join("1" if next_random() % 3 == 0 else "0" for _ in range(200000))
    print(f"200000 cars: {minimum_time(s)} {minimum_time('1' * 200000)} {minimum_time('10' * 100000)}")


main()
