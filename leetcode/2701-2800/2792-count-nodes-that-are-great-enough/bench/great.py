# LeetCode #2792: Count Nodes That Are Great Enough -- the bench in
# Python: the ★ arm over 20 random trees of 10^4 nodes with values up to
# 10^4 and k = 10, all drawn first, then each answered 20 times.


def count_great_enough_nodes(vals, left, right, k):
    n = len(vals)
    order = []
    stack = [0]
    while stack:
        u = stack.pop()
        order.append(u)
        for c in (left[u], right[u]):
            if c >= 0:
                stack.append(c)
    least = [[] for _ in range(n)]
    great = 0
    for u in reversed(order):
        mine = [vals[u]]
        for c in (left[u], right[u]):
            if c >= 0:
                mine.extend(least[c])
        mine.sort()
        del mine[k:]
        if len(mine) == k and mine[k - 1] < vals[u]:
            great += 1
        least[u] = mine
    return great


seed = 2792


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count = 20
    rounds = 20
    n = 10000
    cases = []
    for _ in range(count):
        vals = [next_random() % 10000 + 1 for _ in range(n)]
        left = [-1] * n
        right = [-1] * n
        for i in range(1, n):
            while True:
                p = next_random() % i
                if next_random() % 2 == 0:
                    if left[p] < 0:
                        left[p] = i
                        break
                elif right[p] < 0:
                    right[p] = i
                    break
        cases.append((vals, left, right))
    total = 0
    check = 0
    for r in range(rounds):
        for vals, left, right in cases:
            a = count_great_enough_nodes(vals, left, right, 10)
            total += a
            check = (check * 31 + a + r) % 1000000007
    print(f"{count} trees of 10^4, {rounds} rounds: great enough sum to {total}, checksum {check}")


main()
