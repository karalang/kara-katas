# LeetCode #1207: Unique Number of Occurrences -- the ★ arm in Python: each
# value's count in a dict, and the counts put in a set, which has as many
# as the dict exactly when no two values share a count.


def unique_occurrences(arr):
    counts = {}
    for v in arr:
        counts[v] = counts.get(v, 0) + 1
    return len(set(counts.values())) == len(counts)


# ---- test harness ---------------------------------------------------------

seed = 1207


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def b(x):
    return "true" if x else "false"


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    cases = [
        [1, 2, 2, 1, 1, 3],
        [1, 2],
        [-3, 0, 1, -3, 1, 1, 1, -3, 10, 0],
        [7],
        [-1000, 1000, 1000],
        [5, 5, 5, 5],
        [1, 1, 2, 2],
        [1, 2, 2, 3, 3, 3, 4, 4, 4, 4],
    ]
    for arr in cases:
        print(f"{show(arr)}: {b(unique_occurrences(arr))}")
    yes = check = 0
    for k in range(1000):
        n = next_random() % 30 + 1
        spread = next_random() % 6 + 1
        arr = [next_random() % spread - 3 for _ in range(n)]
        answer = unique_occurrences(arr)
        yes += answer
        check = (check * 131 + (2 if answer else 1) + k % 7) % 1000000007
    print(f"1000 small cases: {yes} true, checksum {check}")
    big = [v for v in range(1, 44) for _ in range(v)] + [-1000] * 54
    print(f"1000 values, counts 1 to 43 and 54: {b(unique_occurrences(big))}")
    big[999] = 1
    print(f"the same with one -1000 made a 1: {b(unique_occurrences(big))}")
    distinct = [i * 2 - 1000 for i in range(1000)]
    print(f"1000 distinct values: {b(unique_occurrences(distinct))}")


main()
