# LeetCode #1027: Longest Arithmetic Subsequence -- bench
# Mirrors ./longest_arith.kara; see ../README.md § Benchmarks.


def longest_arith_seq_length(nums):
    n = len(nums)
    run = [[0] * 1001 for _ in range(n)]
    best = 2
    for i in range(1, n):
        for j in range(i):
            d = nums[i] - nums[j] + 500
            length = run[j][d] + 1 if run[j][d] > 0 else 2
            if length > run[i][d]:
                run[i][d] = length
            best = max(best, length)
    return best


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    count = 40
    rounds = 3
    seed = [1027]
    tops = [5, 50, 500, 500]
    arrays = []
    for k in range(count):
        arrays.append([next_random(seed) % (tops[k % 4] + 1) for _ in range(1000)])
    total = 0
    check = 0
    for _ in range(rounds):
        for nums in arrays:
            answer = longest_arith_seq_length(nums)
            total += answer
            check = (check * 131 + answer) % 1000000007
    print(f"{count} arrays of 1000 values, {rounds} rounds: sum {total}, checksum {check}")


main()
