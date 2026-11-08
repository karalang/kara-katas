# LeetCode #2006: Count Number of Pairs With Absolute Difference K -- the
# benchmark's Python twin, the same algorithm as pairs.kara here.


def count_k_difference(nums, k):
    seen = [0] * 101
    pairs = 0
    for x in nums:
        if x - k >= 1:
            pairs += seen[x - k]
        if x + k <= 100:
            pairs += seen[x + k]
        seen[x] += 1
    return pairs


seed = 2006


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 20000 arrays of 200 values up to 100 built once, then the ★ arm on
    # each for 25 rounds, k moving with the round
    arrays = [[next_random() % 100 + 1 for _ in range(200)] for _ in range(20000)]
    calls = total = check = 0
    for r in range(25):
        for a in range(len(arrays)):
            k = (r * 37 + a) % 99 + 1
            answer = count_k_difference(arrays[a], k)
            calls += 1
            total += answer
            check = (check * 31 + answer) % 1000000007
    print(f"{calls} calls: sum {total}, checksum {check}")


main()
