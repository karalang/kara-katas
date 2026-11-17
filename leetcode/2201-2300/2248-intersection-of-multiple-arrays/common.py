# LeetCode #2248: Intersection of Multiple Arrays -- the Python mirror of
# common.kara: a count for every value from 1 to 1000, kept where it
# reaches the number of arrays, read in order. O(total + 1000).


def intersection(nums):
    count = [0] * 1001
    for row in nums:
        for v in row:
            count[v] += 1
    return [v for v in range(1, 1001) if count[v] == len(nums)]


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_row(count, top):
    values = list(range(1, top + 1))
    for i in range(len(values) - 1, 0, -1):
        j = next_random() % (i + 1)
        values[i], values[j] = values[j], values[i]
    return values[:count]


def fold_list(values):
    acc = len(values)
    for v in values:
        acc = (acc * 1009 + v) % 1000000007
    return acc


def main():
    global seed
    examples = [
        [[3, 1, 2, 4, 5], [1, 2, 3, 4], [3, 4, 5, 6]],
        [[1, 2, 3], [4, 5, 6]],
        [[5, 1, 3]],
        [[7], [7], [7]],
        [[1000, 1], [1, 500, 1000]],
        [[9, 8, 7], [7, 9, 8]],
    ]
    for nums in examples:
        print(f"{nums} -> {intersection(nums)}")
    seed = 2248
    found = 0
    check = 0
    for _ in range(2000):
        rows = next_random() % 6 + 1
        nums = []
        for _ in range(rows):
            count = next_random() % 12 + 1
            nums.append(random_row(count, 20))
        common = intersection(nums)
        found += len(common)
        check = (check * 31 + fold_list(common)) % 1000000007
    print(f"2000 cases: {found} values in common, checksum {check}")
    whole = [random_row(1000, 1000)]
    print(f"one array of 1000: checksum {fold_list(intersection(whole))}")
    singles = [[999] for _ in range(1000)]
    print(f"1000 arrays of one: {intersection(singles)}")
    tens = [random_row(100, 120) for _ in range(10)]
    print(f"10 arrays of 100: {intersection(tens)}")


main()
