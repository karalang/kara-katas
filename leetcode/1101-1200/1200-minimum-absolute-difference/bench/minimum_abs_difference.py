# LeetCode #1200 bench: the ★ arm in Python, over the same 20 arrays of
# 10^5 values and 10 rounds as the Kāra bench.


def minimum_abs_difference(arr):
    arr = sorted(arr)
    least = min(arr[i] - arr[i - 1] for i in range(1, len(arr)))
    return [[arr[i - 1], arr[i]] for i in range(1, len(arr)) if arr[i] - arr[i - 1] == least]


def main():
    seed = 1200

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    spans = [1000000, 100000, 60000]
    arrays = []
    for k in range(20):
        span = spans[k % 3]
        taken = [False] * (2 * span + 1)
        arr = []
        while len(arr) < 100000:
            high = next_random()
            low = next_random()
            v = (high * 32768 + low) % (2 * span + 1) - span
            if not taken[v + span]:
                taken[v + span] = True
                arr.append(v)
        arrays.append(arr)
    check = 0
    for _ in range(10):
        for arr in arrays:
            pairs = minimum_abs_difference(arr)
            check = (check * 131 + len(pairs)) % 1000000007
            for p in pairs:
                check = (check * 131 + p[0] + p[1] + 2000000) % 1000000007
    print(f"10 rounds of 20 arrays of 100000 values: checksum {check}")


main()
