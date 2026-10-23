# LeetCode #922: Sort Array By Parity II -- mirrors
# sort_array_by_parity_ii.kara (two pointers, in place) and its harness.


def sort_array_by_parity_ii(nums):
    j = 1
    for i in range(0, len(nums), 2):
        if nums[i] % 2 == 1:
            while nums[j] % 2 == 1:
                j += 2
            nums[i], nums[j] = nums[j], nums[i]


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(vals):
    return "[" + ",".join(str(v) for v in vals) + "]"


def is_valid(before, after):
    if len(before) != len(after) or sorted(before) != sorted(after):
        return False
    return all(after[i] % 2 == i % 2 for i in range(len(after)))


def canonical(after):
    return sorted(after[0::2]), sorted(after[1::2])


def run(vals):
    nums = list(vals)
    sort_array_by_parity_ii(nums)
    evens, odds = canonical(nums)
    print(f"{show(vals)}: valid {'true' if is_valid(vals, nums) else 'false'}, evens {show(evens)}, odds {show(odds)}")


def fold(check, vals):
    h = check
    for v in vals:
        h = (h * 1000003 + v) % 1000000007
    return h


def random_case(n, top):
    vals = []
    for k in range(n):
        v = 2 * (next_random() % (top // 2 + 1))
        vals.append(min(v, top - top % 2) if k % 2 == 0 else min(v + 1, top - 1 + top % 2))
    i = n - 1
    while i > 0:
        j = next_random() % (i + 1)
        vals[i], vals[j] = vals[j], vals[i]
        i -= 1
    return vals


def main():
    global seed
    run([4, 2, 5, 7])
    run([2, 3])
    run([0, 1, 2, 3, 4, 5])
    run([1, 0, 3, 2, 5, 4])
    run([7, 7, 8, 8, 7, 8])
    run([1000, 999, 0, 1, 1000, 1])
    run([3, 1, 4, 1, 5, 8, 2, 6])
    seed = 922
    check = 0
    all_valid = True
    for _ in range(300):
        n = 2 * (1 + next_random() % 1000)
        vals = random_case(n, 1000)
        nums = list(vals)
        sort_array_by_parity_ii(nums)
        all_valid = all_valid and is_valid(vals, nums)
        evens, odds = canonical(nums)
        check = fold(fold(check, evens), odds)
    print(f"300 random arrays: all valid {'true' if all_valid else 'false'}, checksum {check}")
    vals = random_case(20000, 1000)
    nums = list(vals)
    sort_array_by_parity_ii(nums)
    evens, odds = canonical(nums)
    print(f"20000 values: valid {'true' if is_valid(vals, nums) else 'false'}, checksum {fold(fold(0, evens), odds)}")


main()
