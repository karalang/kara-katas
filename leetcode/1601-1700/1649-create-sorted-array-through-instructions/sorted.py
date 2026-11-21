# LeetCode #1649: Create Sorted Array through Instructions -- the Python
# mirror of the ★ arm: a Fenwick tree over the values, each insertion
# costing the smaller of how many are less and how many are greater.

MOD = 1_000_000_007


def prefix(tree, v):
    total = 0
    i = v
    while i > 0:
        total += tree[i]
        i -= i & -i
    return total


def create_sorted_array(instructions):
    top = max(instructions)
    tree = [0] * (top + 1)
    cost = 0
    for inserted, v in enumerate(instructions):
        less = prefix(tree, v - 1)
        greater = inserted - prefix(tree, v)
        cost = (cost + min(less, greater)) % MOD
        i = v
        while i <= top:
            tree[i] += 1
            i += i & -i
    return cost


# ---- the harness: the same as every arm's ---------------------------------

seed = 1649


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def batch(count, most, top):
    check = 0
    total = 0
    for _ in range(count):
        n = next_random() % most + 1
        instructions = [(next_random() * 32768 + next_random()) % top + 1 for _ in range(n)]
        cost = create_sorted_array(instructions)
        total += cost
        check = (check * 31 + cost + 1) % 1000000007
    print(f"{count} lists of up to {most} instructions up to {top}: costs sum to {total}, checksum {check}")


print(create_sorted_array([1, 5, 6, 2]))
print(create_sorted_array([1, 2, 3, 6, 5, 4]))
print(create_sorted_array([1, 3, 3, 3, 2, 4, 2, 1, 2]))
print(create_sorted_array([7]))
print(create_sorted_array([1, 2, 3, 4, 5]))
print(create_sorted_array([5, 4, 3, 2, 1]))
batch(3000, 8, 5)
batch(300, 1000, 1000)
batch(3, 20000, 100000)
