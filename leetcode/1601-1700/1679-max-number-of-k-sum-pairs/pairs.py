# LeetCode #1679: Max Number of K-Sum Pairs -- the Python mirror of the ★
# arm: one pass with a count of the values still waiting for a partner.


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


def batch(count, longest, most):
    total = 0
    check = 0
    for _ in range(count):
        n = next_random() % longest + 1
        nums = [(next_random() * 32768 + next_random()) % most + 1 for _ in range(n)]
        k = (next_random() * 32768 + next_random()) % (2 * most - 1) + 2
        operations = max_operations(nums, k)
        total += operations
        check = (check * 31 + operations + n) % 1000000007
    print(f"{count} arrays of up to {longest} values up to {most}: {total} operations, checksum {check}")


print(max_operations([1, 2, 3, 4], 5))
print(max_operations([3, 1, 3, 4, 3], 6))
print(max_operations([1, 1, 1], 3))
print(max_operations([2, 2, 2, 2, 2], 4))
print(max_operations([7], 14))
batch(3000, 12, 6)
batch(300, 1000, 1000)
batch(10, 100000, 100000)
