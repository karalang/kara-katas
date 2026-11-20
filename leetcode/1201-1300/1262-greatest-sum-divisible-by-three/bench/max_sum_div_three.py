# LeetCode #1262 bench, in Python: the ★ arm (the best sum with each
# remainder modulo 3, in a list of three copied before each number) on 100
# random lists of 4 * 10^4 numbers from 1 to 10^4 built once, 30 rounds;
# every answer folded into a checksum.


def max_sum_div_three(nums):
    # -1 marks a remainder no sum has reached yet.
    best = [0, -1, -1]
    for x in nums:
        before = best[:]
        for r in range(3):
            if before[r] >= 0:
                s = before[r] + x
                if s > best[s % 3]:
                    best[s % 3] = s
    return best[0]


def main():
    seed = 1262

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    lists = [[next_random() % 10000 + 1 for _ in range(40000)] for _ in range(100)]
    check = 0
    for rnd in range(30):
        for l in range(100):
            best = max_sum_div_three(lists[l])
            check = (check * 131 + best + rnd) % 1000000007
    print(f"30 rounds of 100 lists of 40000: checksum {check}")


main()
