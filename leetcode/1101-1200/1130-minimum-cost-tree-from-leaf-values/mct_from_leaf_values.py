# LeetCode #1130: Minimum Cost Tree From Leaf Values -- the Python mirror
# of the ★ arm: a stack of leaves in decreasing order, each leaf that a
# larger or equal one arrives after paired off with the smaller of its two
# neighbours.


def mct_from_leaf_values(arr):
    cost = 0
    stack = []
    for a in arr:
        while stack and stack[-1] <= a:
            mid = stack.pop()
            cost += mid * (min(stack[-1], a) if stack else a)
        stack.append(a)
    while len(stack) > 1:
        cost += stack.pop() * stack[-1]
    return cost


seed = 1130


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    cases = [
        [6, 2, 4],
        [4, 11],
        [1, 2, 3, 4],
        [4, 3, 2, 1],
        [3, 1, 2],
        [2, 2, 2, 2, 2],
        [1, 15, 1, 15, 1, 15],
        list(range(1, 16)),
        [15] * 40,
    ]
    for arr in cases:
        print(f"{arr} -> {mct_from_leaf_values(arr)}")
    total = 0
    check = 0
    for _ in range(2000):
        n = next_random() % 39 + 2
        arr = [next_random() % 15 + 1 for _ in range(n)]
        c = mct_from_leaf_values(arr)
        total += c
        check = (check * 31 + c) % 1000000007
    print(f"2000 random arrays: costs total {total}, checksum {check}")
    big = [next_random() % 15 + 1 for _ in range(40)]
    print(f"40 random leaves: {mct_from_leaf_values(big)}")
    print(f"40 leaves rising and falling: {mct_from_leaf_values([abs(20 - i) % 15 + 1 for i in range(40)])}")


main()
