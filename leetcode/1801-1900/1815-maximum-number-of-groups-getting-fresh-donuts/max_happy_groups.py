# LeetCode #1815: Maximum Number of Groups Getting Fresh Donuts -- the ★
# arm in Python: only each group's size modulo the batch matters; groups of
# remainder 0 are always happy, a group of remainder r and one of b - r
# make one happy group and then end a batch together, and what is left is
# a search over how many groups of each remainder remain, memoized by those
# counts and the leftover donuts they imply.


def max_happy_groups(batch_size, groups):
    b = batch_size
    count = [0] * b
    for g in groups:
        count[g % b] += 1
    happy = count[0]
    count[0] = 0
    for r in range(1, b):
        s = b - r
        if r < s:
            k = min(count[r], count[s])
            happy += k
            count[r] -= k
            count[s] -= k
        elif r == s:
            happy += count[r] // 2
            count[r] %= 2
    memo = {}

    def best(left):
        key = tuple(count)
        if key in memo:
            return memo[key]
        top = 0
        for r in range(1, b):
            if count[r] > 0:
                count[r] -= 1
                top = max(top, best((left + r) % b))
                count[r] += 1
        top += 1 if left == 0 and any(count) else 0
        memo[key] = top
        return top

    return happy + best(0)


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    # LeetCode's two examples
    print(max_happy_groups(3, [1, 2, 3, 4, 5, 6]), max_happy_groups(4, [1, 3, 2, 5, 2, 2, 1, 6]))
    # the edges: a batch of one; one group; every group a whole batch; no
    # pair to make; the largest groups
    print(
        max_happy_groups(1, [7, 8, 9]),
        max_happy_groups(5, [3]),
        max_happy_groups(4, [8, 4, 12]),
        max_happy_groups(9, [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]),
        max_happy_groups(7, [1000000000, 999999999, 999999998]),
    )
    # the constraints' most: 30 groups at a batch of 9, every remainder
    print("the most:", max_happy_groups(9, [k * 7 + 1 for k in range(30)]), max_happy_groups(8, [k % 7 + 1 for k in range(30)]))
    # 300 random cases: a batch of 1 to 9 and 1 to 30 groups
    seed = [1815]
    check = 0
    for _ in range(300):
        b = 1 + next_random(seed) % 9
        n = 1 + next_random(seed) % 30
        groups = [1 + (next_random(seed) * 32768 + next_random(seed)) % 1000000000 for _ in range(n)]
        check = (check * 31 + max_happy_groups(b, groups)) % 1000000007
    print(f"300 random cases: checksum {check}")


main()
