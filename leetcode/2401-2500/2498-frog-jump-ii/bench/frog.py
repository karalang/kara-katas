# LeetCode #2498: Frog Jump II -- benchmark mirror of the ★ arm (frog.kara):
# 20 rows of 10^5 stones, built once, then the passes; each moves one
# stone of every row to a place between its neighbours chosen by the
# checksum so far, asks, and puts it back.


def max_jump(stones):
    cost = stones[1] - stones[0]
    for i in range(2, len(stones)):
        cost = max(cost, stones[i] - stones[i - 2])
    return cost


seed = 2498


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    n = 100000
    passes = 55
    rows = []
    for _ in range(20):
        stones = [0]
        for _ in range(1, n):
            stones.append(stones[-1] + next_random() % 10000 + 1)
        rows.append(stones)
    check = 0
    for p in range(passes):
        for stones in rows:
            at = check % (n - 2) + 1
            was = stones[at]
            room = stones[at + 1] - stones[at - 1] - 1
            if room > 0:
                stones[at] = stones[at - 1] + 1 + (check + p) % room
            check = (check * 31 + max_jump(stones) + p) % 1000000007
            stones[at] = was
    print(f"{passes} passes over 20 rows of 10^5: checksum {check}")


main()
