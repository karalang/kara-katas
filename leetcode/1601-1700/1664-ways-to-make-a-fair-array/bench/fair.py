# LeetCode #1664 bench: the ★ arm, one pass with running sums.
#
# 20 arrays of 10^5 values from 1 to 2, LeetCode's largest length, drawn
# first; then each is answered 50 times.


def ways_to_make_fair(nums):
    total = [0, 0]
    for i, x in enumerate(nums):
        total[i % 2] += x
    before = [0, 0]
    ways = 0
    for i, x in enumerate(nums):
        p = i % 2
        after = [total[0] - before[0], total[1] - before[1]]
        after[p] -= x
        if before[0] + after[1] == before[1] + after[0]:
            ways += 1
        before[p] += x
    return ways


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    global seed
    count, n, rounds = 20, 100000, 50
    seed = 1664
    arrays = [[next_random() % 2 + 1 for _ in range(n)] for _ in range(count)]
    total = 0
    check = 0
    for r in range(rounds):
        for nums in arrays:
            answer = ways_to_make_fair(nums)
            total += answer
            check = (check * 31 + answer + r) % 1000000007
    print(f"{count} arrays of {n} values, {rounds} rounds: {total} fair removals, checksum {check}")


main()
