# LeetCode #1043: Partition Array for Maximum Sum -- bench, Python mirror
# of partition_max.kara (the bottom-up table).


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


def main():
    count = 400
    n = 500
    rounds = 40
    seed = [1043]
    arrays = []
    ks = []
    for _ in range(count):
        arr = []
        for _ in range(n):
            hi = next_random(seed)
            lo = next_random(seed)
            arr.append((hi * 32768 + lo) % 1000000001)
        arrays.append(arr)
        ks.append(next_random(seed) % 50 + 1)
    total = 0
    check = 0
    for _ in range(rounds):
        for a in range(count):
            answer = max_sum_after_partitioning(arrays[a], ks[a])
            total += answer
            check = (check * 131 + answer % 1000000007) % 1000000007
    print(f"{count} arrays of {n} values, {rounds} rounds: total {total}, checksum {check}")


main()
