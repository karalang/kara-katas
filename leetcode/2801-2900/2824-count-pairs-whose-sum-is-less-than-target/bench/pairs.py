# LeetCode #2824: Count Pairs Whose Sum is Less than Target -- the
# bench's Python mirror of the ★ arm: the numbers sorted, two pointers
# closing in.


def count_pairs(nums, target):
    s = sorted(nums)
    i, j = 0, len(s) - 1
    count = 0
    while i < j:
        if s[i] + s[j] < target:
            count += j - i
            i += 1
        else:
            j -= 1
    return count


seed = 2824


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, rounds = 200000, 5
    cases = []
    for _ in range(count):
        nums = [next_random() % 101 - 50 for _ in range(50)]
        cases.append((nums, next_random() % 101 - 50))
    total = 0
    check = 0
    for r in range(rounds):
        for nums, target in cases:
            a = count_pairs(nums, target)
            total += a
            check = (check * 31 + a + r) % 1000000007
    print(f"{count} arrays of 50, {rounds} rounds: {total} pairs, checksum {check}")


main()
