# LeetCode #873: Length of Longest Fibonacci Subsequence -- Python mirror of
# the ★ arm (the longest run ending in each pair, found through a value
# index) and its test harness; prints the same output as
# len_longest_fib_subseq.kara.


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


def show(arr):
    text = [str(x) for x in arr]
    if len(text) > 12:
        shown = f"{text[0]}, {text[1]}, {text[2]}, ... {text[-1]} ({len(text)} values)"
    else:
        shown = ", ".join(text)
    print(f"[{shown}] -> {len_longest_fib_subseq(arr)}")


def main():
    show([1, 2, 3, 4, 5, 6, 7, 8])
    show([1, 3, 7, 11, 12, 14, 18])
    show([1, 2, 3])
    show([1, 2, 4])
    show([2, 4, 7, 8, 9, 10, 14, 15, 18, 23, 32, 50])
    show([1, 999999999, 1000000000])
    show([1, 2, 1000000000])
    show([5, 6, 11, 17, 28, 45, 73])
    show([3, 4, 5, 7, 9, 12, 16, 21, 28, 37])
    fib = [1, 2]
    while fib[-1] + fib[-2] <= 1000000000:
        fib.append(fib[-1] + fib[-2])
    show(fib)
    show(list(range(1, 1001)))
    total = 0
    none = 0
    for k in range(3000):
        arr = increasing(k % 10 + 3, k % 4 + 1)
        answer = len_longest_fib_subseq(arr)
        total += answer
        if answer == 0:
            none += 1
    print(f"3000 arrays of 3 to 12 values: lengths sum to {total}, {none} with no run")
    total = 0
    check = 0
    for k in range(4):
        arr = increasing(1000, k // 2 + 2) if k % 2 == 0 else scattered(1000, k * 10)
        answer = len_longest_fib_subseq(arr)
        total += answer
        check = (check * 131 + answer * 7 + arr[-1] % 1000) % 1000000007
    print(f"4 arrays of 1000 values: lengths sum to {total}, checksum {check}")


main()
