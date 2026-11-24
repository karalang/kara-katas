# LeetCode #1326: Minimum Number of Taps to Open to Water a Garden -- Python
# mirror of the ★ Kāra arm: each tap turned into how far right it waters
# from the leftmost point it reaches, the best kept for each point; then the
# garden crossed as a jump game, a tap opened each time the watered stretch
# runs out, the farthest any tap starting inside it reaches.


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
    shut = [0] * 10001
    ones = [1] * 10001
    middle = [0] * 201
    middle[100] = 100
    short = middle + [0]
    print(f"{min_taps(5, [3, 4, 1, 1, 0, 0])} {min_taps(3, [0, 0, 0, 0])} {min_taps(7, [1, 2, 1, 0, 2, 1, 0, 1])} {min_taps(8, [4, 0, 0, 0, 0, 0, 0, 0, 4])} {min_taps(8, [4, 0, 0, 0, 4, 0, 0, 0, 4])} {min_taps(10000, shut)} {min_taps(10000, ones)} {min_taps(200, middle)} {min_taps(201, short)}")
    total = 0
    check = 0
    for t in range(600):
        n = 1 + next_random() % 10000 if t % 6 == 0 else 1 + next_random() % 60
        reach = 3 if t % 3 == 0 else 10 if t % 3 == 1 else 100
        open_ = 1 if t % 4 == 0 else 3 if t % 4 == 1 else 20
        ranges = []
        for _ in range(n + 1):
            r = 1 + next_random() % reach if next_random() % open_ == 0 else 0
            ranges.append(r)
        got = min_taps(n, ranges)
        total += got
        check = (check * 131 + got + 1) % 1000000007
    print(f"600 random gardens: taps total {total}, checksum {check}")


main()
