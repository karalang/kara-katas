# LeetCode 813 -- Largest Sum of Averages: the bench, with the ★ arm's one
# row of prefix-sum DP.

seed = 813


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def largest_sum_of_averages(nums, k):
    n = len(nums)
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + nums[i]
    best = [0.0] * (n + 1)
    for i in range(1, n + 1):
        best[i] = prefix[i] / i
    for _ in range(1, k):
        i = n
        while i >= 1:
            for p in range(1, i):
                candidate = best[p] + (prefix[i] - prefix[p]) / (i - p)
                if candidate > best[i]:
                    best[i] = candidate
            i -= 1
    return best[n]


# 64 arrays of 100 numbers from 1 to 10000 are made once. Each round writes
# a new number into one place of the next array and finds its largest sum
# of averages in at most k groups, k going round 1 to 100.
def main():
    arrays = [[1 + next_random() % 10000 for _ in range(100)] for _ in range(64)]
    rounds = 6000
    total = 0.0
    check = 0
    for r in range(rounds):
        a = r % 64
        arrays[a][r // 64 % 100] = 1 + next_random() % 10000
        answer = largest_sum_of_averages(arrays[a], 1 + r % 100)
        total += answer
        check = (check * 131 + int(answer * 1000.0)) % 1000000007
    print(f"{rounds} rounds of 100 numbers: total {total:.5f}, checksum {check}")


main()
