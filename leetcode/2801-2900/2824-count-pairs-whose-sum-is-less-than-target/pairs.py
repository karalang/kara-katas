# LeetCode #2824: Count Pairs Whose Sum is Less than Target -- the Python
# mirror of the ★ arm: the numbers sorted, two pointers closing in.


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


# ---- the harness: the same in every arm --------------------------------

seed = 2824


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    print(count_pairs([-1, 1, 2, 3, 1], 2))
    print(count_pairs([-6, 2, 5, -2, -7, -1, 3], -2))
    print(count_pairs([5], 50))
    print(count_pairs([-50] * 50, 50))
    print(count_pairs([50] * 50, -50))
    total = 0
    check = 0
    for _ in range(5000):
        n = next_random() % 50 + 1
        nums = [next_random() % 101 - 50 for _ in range(n)]
        target = next_random() % 101 - 50
        a = count_pairs(nums, target)
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"5000 arrays: {total} pairs, checksum {check}")


main()
