# LeetCode #873 bench: Python mirror of len_longest_fib_subseq.kara (the
# ★ arm, a dict from value to index) on the same 100 arrays.


def len_longest_fib_subseq(arr):
    n = len(arr)
    index = {x: i for i, x in enumerate(arr)}
    longest = [[2] * n for _ in range(n)]
    best = 0
    for k in range(n):
        for j in range(k):
            before = arr[k] - arr[j]
            if before < arr[j]:
                i = index.get(before)
                if i is not None:
                    longest[j][k] = longest[i][j] + 1
                    best = max(best, longest[j][k])
    return best


# ---- test harness ----------------------------------------------------------

seed = 873


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def increasing(n, gap):
    arr = []
    x = 0
    for _ in range(n):
        x += 1 + next_random() % gap
        arr.append(x)
    return arr


def big():
    hi = next_random()
    return (hi * 32768 + next_random()) % 1000000000 + 1


def scattered(n, run):
    a = next_random() % 1000 + 1
    b = a + next_random() % 1000 + 1
    vals = [a, b]
    while len(vals) < run and a + b <= 1000000000:
        a, b = b, a + b
        vals.append(b)
    while len(vals) < n:
        vals.append(big())
    vals.sort()
    arr = []
    for x in vals:
        if not arr or arr[-1] != x:
            arr.append(x)
    return arr


def main():
    arrays = []
    for k in range(100):
        arrays.append(increasing(1000, k % 5 + 2) if k % 2 == 0 else scattered(1000, 10 + k % 30))
    total = 0
    check = 0
    for arr in arrays:
        answer = len_longest_fib_subseq(arr)
        total += answer
        check = (check * 131 + answer) % 1000000007
    print(f"100 arrays of 1000 values: lengths sum to {total}, checksum {check}")


main()
