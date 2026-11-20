# LeetCode #1695: Maximum Erasure Value -- the bench's Python mirror: the ★
# arm on 50 random arrays of 100000 values up to 10^4, all drawn first,
# each answered 60 times.


def maximum_unique_subarray(nums):
    last = [-1] * 10001
    prefix = [0] * (len(nums) + 1)
    start = 0
    best = 0
    for i, v in enumerate(nums):
        prefix[i + 1] = prefix[i] + v
        start = max(start, last[v] + 1)
        last[v] = i
        best = max(best, prefix[i + 1] - prefix[start])
    return best


seed = 1695


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, rounds, n = 50, 60, 100000
    arrays = [[next_random() % 10000 + 1 for _ in range(n)] for _ in range(count)]
    total = 0
    check = 0
    for r in range(rounds):
        for nums in arrays:
            answer = maximum_unique_subarray(nums)
            total += answer
            check = (check * 31 + answer + r) % 1000000007
    print(f"{count} arrays of {n} values, {rounds} rounds: answers sum to {total}, checksum {check}")


main()
