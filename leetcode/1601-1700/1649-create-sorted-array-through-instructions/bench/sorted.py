# LeetCode #1649: Create Sorted Array through Instructions -- the bench's
# Python mirror: the ★ arm on 60 random lists of 100000 instructions from
# 1 to 100000, all drawn first.

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


seed = 1649


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


lists = [[next_random() % 100000 + 1 for _ in range(100000)] for _ in range(60)]
check = 0
total = 0
for instructions in lists:
    cost = create_sorted_array(instructions)
    total += cost
    check = (check * 31 + cost + 1) % 1000000007
print(f"60 lists of 100000 instructions: costs sum to {total}, checksum {check}")
