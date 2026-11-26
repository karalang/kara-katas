# LeetCode #1465 bench in Python: the ★ arm (each way's cuts sorted and
# its widest gap taken) on the same 100 cakes of 5000 cuts each way and 20
# passes.


def widest(size, cuts):
    s = sorted(cuts)
    best = s[0]
    for i in range(1, len(s)):
        best = max(best, s[i] - s[i - 1])
    return max(best, size - s[-1])


def max_area(h, w, horizontal_cuts, vertical_cuts):
    return widest(h, horizontal_cuts) * widest(w, vertical_cuts) % 1000000007


seed = 1465


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    across = []
    down = []
    for _ in range(100):
        across.append([1 + (next_random() * 32768 + next_random()) % 499999999 for _ in range(5000)])
        down.append([1 + (next_random() * 32768 + next_random()) % 499999999 for _ in range(5000)])
    check = 0
    for pass_ in range(20):
        for c in range(100):
            h = 1000000000 - check % 1000
            w = 1000000000 - check // 1000 % 1000
            got = max_area(h, w, across[c], down[c])
            check = (check * 31 + got + pass_) % 1000000007
    print(f"20 passes over 100 cakes of 5000 cuts each way: checksum {check}")


main()
