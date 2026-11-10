# LeetCode #2106: Maximum Fruits Harvested After at Most K Steps -- Python
# mirror of the ★ arm (harvest.kara): a sliding window over the sorted
# fruits, shrunk while its shorter route costs more than k. Prints the
# same lines.


def steps(l, r, start):
    if l >= start:
        return r - start
    if r <= start:
        return start - l
    return min(2 * (start - l) + (r - start), (start - l) + 2 * (r - start))


def max_total_fruits(fruits, start, k):
    left = 0
    total = 0
    best = 0
    for right in range(len(fruits)):
        total += fruits[right][1]
        while left <= right and steps(fruits[left][0], fruits[right][0], start) > k:
            total -= fruits[left][1]
            left += 1
        best = max(best, total)
    return best


seed = 2106


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(fruits):
    return "[" + ", ".join(f"[{p}, {a}]" for p, a in fruits) + "]"


def main():
    examples = [
        ([[2, 8], [6, 3], [8, 6]], 5, 4),
        ([[0, 9], [4, 1], [5, 7], [6, 2], [7, 4], [10, 9]], 5, 4),
        ([[0, 3], [6, 4], [8, 5]], 3, 2),
        ([[3, 7], [4, 1]], 3, 0),
        ([[1, 2], [2, 3], [5, 4]], 9, 5),
        ([[0, 100], [9, 1], [11, 1], [12, 1]], 10, 12),
        ([[1, 5], [11, 6], [13, 6]], 10, 7),
    ]
    for fruits, start, k in examples:
        print(f"{show(fruits)} from {start} in {k} -> {max_total_fruits(fruits, start, k)}")
    total = 0
    check = 0
    for _ in range(3000):
        n = next_random() % 40 + 1
        taken = [False] * 61
        fruits = []
        while len(fruits) < n:
            p = next_random() % 61
            if not taken[p]:
                taken[p] = True
                fruits.append([p, next_random() % 20 + 1])
        fruits.sort()
        start = next_random() % 61
        k = next_random() % 41
        got = max_total_fruits(fruits, start, k)
        total += got
        check = (check * 31 + got) % 1000000007
    print(f"3000 fields: {total} fruits, checksum {check}")
    wide = [[2 * i, 10000] for i in range(100000)]
    print(f"wide, every step -> {max_total_fruits(wide, 100000, 200000)}")
    print(f"wide, 1000 steps -> {max_total_fruits(wide, 100001, 1000)}")


main()
