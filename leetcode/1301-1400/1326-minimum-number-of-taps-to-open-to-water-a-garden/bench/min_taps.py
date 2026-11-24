# LeetCode #1326 bench, Python mirror of the Kāra bench: the ★ arm (each tap
# turned into how far right it waters from its leftmost point, then the
# garden crossed as a jump game) on 20 gardens of 10^4 built once, a tap
# open one time in 1, 3, 10 or 30; then 300 passes, each setting one tap of
# every garden from the checksum so far, answering it and folding the
# answer plus the pass into the checksum.


def min_taps(n, ranges):
    farthest = [0] * (n + 1)
    for i in range(n + 1):
        r = ranges[i]
        left = max(i - r, 0)
        right = min(i + r, n)
        farthest[left] = max(farthest[left], right)
    taps = 0
    watered = 0
    nxt = 0
    for x in range(n):
        nxt = max(nxt, farthest[x])
        if x == watered:
            if nxt <= x:
                return -1
            taps += 1
            watered = nxt
    return taps


seed = 1326


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    n = 10000
    gardens = []
    for t in range(20):
        open_ = 1 if t % 4 == 0 else 3 if t % 4 == 1 else 10 if t % 4 == 2 else 30
        ranges = []
        for _ in range(n + 1):
            r = 1 + next_random() % 100 if next_random() % open_ == 0 else 0
            ranges.append(r)
        gardens.append(ranges)
    check = 0
    for p in range(300):
        for t in range(20):
            ranges = gardens[t]
            ranges[check % (n + 1)] = (check // 7) % 101
            taps = min_taps(n, ranges)
            check = (check * 31 + taps + 1 + p) % 1000000007
    print(f"300 passes over 20 gardens of 10^4: checksum {check}")


main()
