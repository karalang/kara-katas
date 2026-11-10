# LeetCode #2089: Find Target Indices After Sorting Array -- Python mirror
# of the ★ arm (target.kara): the values less than the target and those
# equal to it counted, and the indices the range between.

seed = 2089


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def target_indices(nums, target):
    less = sum(1 for x in nums if x < target)
    equal = sum(1 for x in nums if x == target)
    return list(range(less, less + equal))


def show(v):
    return "[" + ",".join(str(x) for x in v) + "]"


def main():
    examples = [
        ([1, 2, 5, 2, 3], 2),
        ([1, 2, 5, 2, 3], 3),
        ([1, 2, 5, 2, 3], 5),
        ([1, 2, 5, 2, 3], 4),
        ([7], 7),
        ([9, 9, 9, 9], 9),
        ([100, 1, 50, 1, 100, 50], 50),
    ]
    for nums, target in examples:
        print(f"{show(nums)} {target} -> {show(target_indices(nums, target))}")
    found = check = 0
    for _ in range(2000):
        n = next_random() % 100 + 1
        top = [3, 10, 100][next_random() % 3]
        nums = [next_random() % top + 1 for _ in range(n)]
        target = next_random() % top + 1
        got = target_indices(nums, target)
        found += len(got)
        for i in got:
            check = (check * 31 + i + 1) % 1000000007
        check = (check * 31 + 1000) % 1000000007
    print(f"2000 arrays: {found} indices, checksum {check}")
    print(f"100 of 100: {len(target_indices([100] * 100, 100))} indices")
    some = [i % 50 + 1 for i in range(100)]
    print(f"1 to 50 twice, 50: {show(target_indices(some, 50))}, 51: {show(target_indices(some, 51))}")


main()
