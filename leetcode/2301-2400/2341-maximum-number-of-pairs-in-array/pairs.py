# LeetCode #2341: Maximum Number of Pairs in Array -- the Python mirror of
# the ★ arm: each value counted in a table of 101, and the pairs every
# count's half, the leftovers its parity.


def number_of_pairs(nums):
    counts = [0] * 101
    for x in nums:
        counts[x] += 1
    pairs = 0
    left = 0
    for c in counts:
        pairs += c // 2
        left += c % 2
    return [pairs, left]


SEED = [2341]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


def show(answer):
    return f"[{answer[0]}, {answer[1]}]"


def main():
    print(show(number_of_pairs([1, 3, 2, 1, 3, 2, 2])))
    print(show(number_of_pairs([1, 1])))
    print(show(number_of_pairs([0])))
    print(show(number_of_pairs([7] * 100)))
    print(show(number_of_pairs([7] * 99)))
    print(show(number_of_pairs(list(range(100)))))
    print(show(number_of_pairs([100, 0, 100, 0, 50])))
    check = 0
    total_pairs = 0
    total_left = 0
    for _ in range(2000):
        n = 1 + next_random() % 100
        spread = 1 + next_random() % 101
        nums = [next_random() % spread for _ in range(n)]
        pairs, left = number_of_pairs(nums)
        check = (check * 31 + pairs * 101 + left) % 1000000007
        total_pairs += pairs
        total_left += left
    print(f"2000 cases: checksum {check}, pairs {total_pairs}, left over {total_left}")


main()
