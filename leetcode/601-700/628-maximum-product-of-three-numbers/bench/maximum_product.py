# LeetCode #628: Maximum Product of Three Numbers -- Python mirror of
# the Kāra bench.
#
# The ★ arm's one pass over the same inputs and rounds.


def maximum_product(nums):
    max1 = max2 = max3 = -(2**63)
    min1 = min2 = 2**63 - 1
    for v in nums:
        if v > max1:
            max3, max2, max1 = max2, max1, v
        elif v > max2:
            max3, max2 = max2, v
        elif v > max3:
            max3 = v
        if v < min1:
            min2, min1 = min1, v
        elif v < min2:
            min2 = v
    return max(max1 * max2 * max3, max1 * min1 * min2)


seed = 628


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    inputs = 20
    rounds = 20000
    all_inputs = []
    for _ in range(inputs):
        spread = 1 + next_random() % 1000
        all_inputs.append([next_random() % (2 * spread + 1) - spread for _ in range(10000)])
    checksum = 0
    for r in range(rounds):
        p = maximum_product(all_inputs[(r * 7) % inputs])
        checksum = (checksum * 31 + p % 1000000007 + 1000000007) % 1000000007
    print(f"{inputs} inputs, {rounds} rounds: checksum {checksum}")


main()
