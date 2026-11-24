# LeetCode #1338: Reduce Array Size to The Half -- Python mirror of the ★
# arm: each value counted, the counts sorted largest first and taken until
# at least half the array is gone.


def min_set_size(arr):
    counts = {}
    for x in arr:
        counts[x] = counts.get(x, 0) + 1
    sizes = sorted(counts.values(), reverse=True)
    removed = 0
    chosen = 0
    for s in sizes:
        if 2 * removed >= len(arr):
            break
        removed += s
        chosen += 1
    return chosen


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    global seed
    print(f"{min_set_size([3, 3, 3, 3, 5, 5, 5, 2, 2, 7])} {min_set_size([7, 7, 7, 7, 7, 7])} {min_set_size([1, 2])} {min_set_size([1, 1, 2, 2])}")
    seed = 1338
    distinct = list(range(1, 100001))
    drawn = [1 + next_random() % 100000 for _ in range(100000)]
    print(f"10^5 values: {min_set_size(distinct)} {min_set_size(drawn)}")
    check = 0
    for t in range(400):
        n = 2 * (1 + next_random() % 1500) if t % 20 == 0 else 2 * (1 + next_random() % 8)
        top = 3 if t % 3 == 0 else (50 if t % 3 == 1 else 100000)
        arr = []
        for _ in range(n):
            if t % 2 == 0:
                v = 1 + next_random() % top
            else:
                a = next_random() % top
                v = 1 + a * (next_random() % top) // top
            arr.append(v)
        check = (check * 131 + min_set_size(arr) + n) % 1000000007
    print(f"400 random arrays: checksum {check}")


main()
