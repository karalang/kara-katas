# LeetCode #1191: K-Concatenation Maximum Sum -- the ★ arm in Python:
# Kadane's scan over one copy, or two, and the middle copies' sums when the
# array sums above zero. It also checks every answer for arrays repeated at
# most 6 times against the statement read literally: every subarray of the
# k copies laid end to end, the empty one included.

MOD = 1000000007


def k_concatenation_max_sum(arr, k):
    total = sum(arr)
    best = run = 0
    for _ in range(min(k, 2)):
        for x in arr:
            run = max(run + x, 0)
            best = max(best, run)
    if k > 2 and total > 0:
        best += (k - 2) * total
    return best % MOD


def literal(arr, k):
    whole = arr * k
    best = 0
    for i in range(len(whole)):
        s = 0
        for j in range(i, len(whole)):
            s += whole[j]
            best = max(best, s)
    return best % MOD


seed = 1191


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def solve(arr, k):
    got = k_concatenation_max_sum(arr, k)
    if len(arr) * k <= 60:
        assert got == literal(arr, k), (arr, k)
    return got


print(f"[1, 2] k=3: {solve([1, 2], 3)}")
print(f"[1, -2, 1] k=5: {solve([1, -2, 1], 5)}")
print(f"[-1, -2] k=7: {solve([-1, -2], 7)}")
print(f"[5] k=1: {solve([5], 1)}")
print(f"[-5, 10, -5] k=3: {solve([-5, 10, -5], 3)}")
print(f"[2, -1, 2] k=100000: {solve([2, -1, 2], 100000)}")
print(f"[-3, -3, 4, -3] k=4: {solve([-3, -3, 4, -3], 4)}")
print(f"[10000; 100000] k=100000: {solve([10000] * 100000, 100000)}")
check = 0
for _ in range(2000):
    n = next_random() % 8 + 1
    arr = [next_random() % 21 - 10 for _ in range(n)]
    k = next_random() % 6 + 1
    check = (check * 131 + solve(arr, k)) % MOD
print(f"2000 random arrays: checksum {check}")
arr = []
for _ in range(100000):
    high = next_random()
    low = next_random()
    arr.append((high * 32768 + low) % 20001 - 10000)
print(f"100000 random values k=100000: {solve(arr, 100000)}")
lifted = [min(x + 300, 10000) for x in arr]
print(f"100000 lifted values k=100000: {solve(lifted, 100000)}")
