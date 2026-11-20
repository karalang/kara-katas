# LeetCode #1679: Max Number of K-Sum Pairs -- the bench's Python mirror:
# the ★ arm on 50 arrays of 100000 values up to 100000, each with a k up to
# 200000, all drawn first, each answered 10 times, with a dict.


def max_operations(nums, k):
    waiting = {}
    operations = 0
    for x in nums:
        partner = k - x
        c = waiting.get(partner)
        if c is not None and c > 0:
            waiting[partner] = c - 1
            operations += 1
        else:
            waiting[x] = waiting.get(x, 0) + 1
    return operations


seed = 1679


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    arrays, n, most, rounds = 50, 100000, 100000, 10
    cases = []
    for _ in range(arrays):
        nums = [(next_random() * 32768 + next_random()) % most + 1 for _ in range(n)]
        k = (next_random() * 32768 + next_random()) % (2 * most - 1) + 2
        cases.append((nums, k))
    total = 0
    check = 0
    for r in range(rounds):
        for nums, k in cases:
            operations = max_operations(nums, k)
            total += operations
            check = (check * 31 + operations + r) % 1000000007
    print(f"{arrays} arrays of {n} values, {rounds} rounds: {total} operations, checksum {check}")


main()
