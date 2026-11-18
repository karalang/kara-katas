# LeetCode #1191 bench: the ★ arm in Python, over the same 4 arrays of 10^5
# values and 200 rounds as the Kāra bench.

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


seed = 1191


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


random = []
for _ in range(100000):
    high = next_random()
    low = next_random()
    random.append((high * 32768 + low) % 20001 - 10000)
lifted = [min(x + 300, 10000) for x in random]
negative = [-abs(x) - 1 for x in random]
alternating = [10000 - i % 7 if i % 2 == 0 else i % 5 - 10000 for i in range(100000)]
arrays = [random, lifted, negative, alternating]
check = 0
for r in range(200):
    for arr in arrays:
        check = (check * 131 + k_concatenation_max_sum(arr, 100000 - r)) % MOD
print(f"200 rounds of 4 arrays of 100000 values: checksum {check}")
