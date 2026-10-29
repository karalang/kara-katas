# LeetCode #1027: Longest Arithmetic Subsequence -- a table by difference
# Mirrors longest_arith.kara (the ★ arm) and prints the same output.


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


seed = 1027


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(values):
    return "[" + ", ".join(str(v) for v in values) + "]"


def main():
    examples = [
        [3, 6, 9, 12],
        [9, 4, 7, 2, 10],
        [20, 1, 15, 3, 10, 5, 8],
        [83, 20, 17, 43, 52, 78, 68, 45],
        [1, 1],
        [0, 500, 250, 0, 500],
        [12, 28, 13, 6, 34, 36, 53, 24, 29, 2, 23, 0, 22, 25, 53, 34, 23, 50, 35, 43, 53, 11, 48, 56, 44, 53, 31, 6, 31, 57, 46, 6, 17, 42, 48, 28, 5, 24, 0, 14, 43, 12, 21, 6, 30, 37, 16, 56, 19, 45, 51, 10, 22, 38, 39, 23, 8, 29, 60, 18],
    ]
    for nums in examples:
        print(f"{show(nums)} -> {longest_arith_seq_length(nums)}")
    groups = [(500, 8, 10), (300, 30, 20), (100, 100, 3), (60, 100, 500), (5, 1000, 500), (2, 1000, 50)]
    for count, n, top in groups:
        total = 0
        longest = 0
        check = 0
        for _ in range(count):
            nums = [next_random() % (top + 1) for _ in range(n)]
            answer = longest_arith_seq_length(nums)
            total += answer
            longest = max(longest, answer)
            check = (check * 131 + answer) % 1000000007
        print(f"{count} arrays of {n} values from 0 to {top}: sum {total}, longest {longest}, checksum {check}")
    rising = list(range(501))
    alternating = [0 if k % 2 == 0 else 500 for k in range(200)]
    doubled = []
    v = 0
    while v <= 500:
        doubled.append(v)
        doubled.append(v)
        v += 7
    print(f"rising: {longest_arith_seq_length(rising)}, alternating: {longest_arith_seq_length(alternating)}, doubled steps of 7: {longest_arith_seq_length(doubled)}")


main()
