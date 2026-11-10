# LeetCode #2089: Find Target Indices After Sorting Array -- Python mirror
# of the ★ arm's benchmark (target.kara): the same 10000 arrays, each asked
# for every target, two counts and the indices collected into a `list`.

seed = 2089


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def target_indices(nums, target):
    less = sum(1 for x in nums if x < target)
    equal = sum(1 for x in nums if x == target)
    return list(range(less, less + equal))


def main():
    arrays = [[next_random() % 100 + 1 for _ in range(100)] for _ in range(10000)]
    total = check = 0
    for nums in arrays:
        for target in range(1, 101):
            got = target_indices(nums, target)
            total += sum(got) * target
            check = (check * 31 + len(got) * 100 + (got[0] if got else 0)) % 1000000007
    print(f"1000000 answers: sum {total}, checksum {check}")


main()
