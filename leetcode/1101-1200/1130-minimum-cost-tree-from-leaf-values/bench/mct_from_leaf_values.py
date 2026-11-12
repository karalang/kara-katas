# LeetCode #1130: Minimum Cost Tree From Leaf Values -- the bench in Python,
# the ★ arm over lists of leaves with a list stack, the same 4096 arrays
# and 400 rounds.


def mct_from_leaf_values(arr):
    cost = 0
    stack = []
    for a in arr:
        while stack and stack[-1] <= a:
            mid = stack.pop()
            partner = min(stack[-1], a) if stack else a
            cost += mid * partner
        stack.append(a)
    while len(stack) > 1:
        top = stack.pop()
        cost += top * stack[-1]
    return cost


seed = 1130


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    arrays = [[next_random() % 15 + 1 for _ in range(40)] for _ in range(4096)]
    total = 0
    check = 0
    for rnd in range(400):
        for j in range(4096):
            at = (rnd * 7919 + j * 104729) % 40
            arrays[j][at] = arrays[j][at] % 15 + 1
            c = mct_from_leaf_values(arrays[j])
            total += c
            check = (check * 31 + c) % 1000000007
    print(f"400 rounds over 4096 arrays of 40 leaves: costs total {total}, checksum {check}")


main()
