# LeetCode #2078: Two Furthest Houses With Different Colors -- Python mirror
# of the ★ arm (houses.kara): the furthest house from the first that
# differs from it, or the furthest from the last, by a scan in from each
# end.


def max_distance(colors):
    n = len(colors)
    j = n - 1
    while colors[j] == colors[0]:
        j -= 1
    i = 0
    while colors[i] == colors[n - 1]:
        i += 1
    return max(j, n - 1 - i)


seed = 2078


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_street(n, kinds):
    while True:
        base = next_random() % (101 - kinds + 1)
        colors = [base + next_random() % kinds for _ in range(n)]
        if any(c != colors[0] for c in colors):
            return colors


def show(v):
    return "[" + ",".join(str(x) for x in v) + "]"


examples = [
    [1, 1, 1, 6, 1, 1, 1],
    [1, 8, 3, 8, 3],
    [0, 1],
    [4, 4, 4, 4, 7],
    [7, 4, 4, 4, 4],
    [2, 3, 3, 3, 2],
    [5, 5, 9, 9, 5, 5],
]
for colors in examples:
    print(f"{show(colors)} -> {max_distance(colors)}")
total = 0
check = 0
for t in range(3000):
    n = next_random() % 99 + 2
    kinds = [2, 3, 100][next_random() % 3]
    if t % 4 == 3:
        colors = [50] * n
        colors[next_random() % n] = 51
    else:
        colors = random_street(n, kinds)
    a = max_distance(colors)
    total += a
    check = (check * 31 + a) % 1000000007
print(f"3000 streets: sum {total}, checksum {check}")
wide = [0] * 100
wide[49] = 100
wide[50] = 100
print(f"100 houses, the middle two apart -> {max_distance(wide)}")
