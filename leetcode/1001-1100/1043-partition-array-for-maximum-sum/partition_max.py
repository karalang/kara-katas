# LeetCode #1043: Partition Array for Maximum Sum -- Python mirror of
# partition_max.kara (bottom-up over the prefixes), same harness.


def max_sum_after_partitioning(arr, k):
    n = len(arr)
    best = [0] * (n + 1)
    for i in range(1, n + 1):
        largest = 0
        j = 1
        while j <= k and j <= i:
            largest = max(largest, arr[i - j])
            best[i] = max(best[i], best[i - j] + largest * j)
            j += 1
    return best[n]


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def show(arr):
    return "[" + ", ".join(str(x) for x in arr) + "]"


def main():
    examples = [
        ([1, 15, 7, 9, 2, 5, 10], 3),
        ([1, 4, 1, 5, 7, 3, 6, 1, 9, 9, 3], 4),
        ([1], 1),
        ([1, 15, 7, 9, 2, 5, 10], 1),
        ([1, 15, 7, 9, 2, 5, 10], 7),
        ([9, 8, 7, 6, 5, 4, 3, 2, 1], 2),
        ([1, 2, 3, 4, 5, 6, 7, 8, 9], 2),
        ([5, 5, 5, 5, 5], 3),
        ([0, 0, 0, 1000000000, 0, 0, 0], 4),
        ([3, 1, 3, 1, 3, 1, 3], 2),
    ]
    for arr, k in examples:
        print(f"{show(arr)}, k = {k} -> {max_sum_after_partitioning(arr, k)}")
    for n in range(1, 7):
        count = 4**n
        cases = 0
        total = 0
        check = 0
        for code in range(count):
            arr = []
            c = code
            for _ in range(n):
                arr.append(c % 4)
                c //= 4
            for k in range(1, n + 1):
                answer = max_sum_after_partitioning(arr, k)
                cases += 1
                total += answer
                check = (check * 131 + answer) % 1000000007
        print(f"all {count} arrays of {n}, every k: {cases} cases, sum {total}, checksum {check}")
    seed = [1043]
    total = 0
    check = 0
    for _ in range(300):
        n = next_random(seed) % 100 + 1
        k = next_random(seed) % n + 1
        arr = []
        for _ in range(n):
            hi = next_random(seed)
            lo = next_random(seed)
            arr.append((hi * 32768 + lo) % 1000000001)
        answer = max_sum_after_partitioning(arr, k)
        total += answer
        check = (check * 131 + answer % 1000000007) % 1000000007
    print(f"300 random arrays: sum {total}, checksum {check}")
    print(f"500 x 10^9, k = 1: {max_sum_after_partitioning([1000000000] * 500, 1)}")
    print(f"0 to 499, k = 500: {max_sum_after_partitioning(list(range(500)), 500)}")


main()
