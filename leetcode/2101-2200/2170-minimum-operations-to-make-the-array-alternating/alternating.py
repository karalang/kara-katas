# LeetCode #2170: Minimum Operations to Make the Array Alternating -- the
# Python mirror of alternating.kara: each side's two most frequent counts,
# the second taken when both sides' favourite is the same number.


def top_two(nums, start):
    counts = {}
    for i in range(start, len(nums), 2):
        counts[nums[i]] = counts.get(nums[i], 0) + 1
    first = (0, 0)
    second = (0, 0)
    for value, count in counts.items():
        if count > first[1]:
            second = first
            first = (value, count)
        elif count > second[1]:
            second = (value, count)
    return first, second


def minimum_operations(nums):
    n = len(nums)
    even_first, even_second = top_two(nums, 0)
    odd_first, odd_second = top_two(nums, 1)
    if even_first[0] != odd_first[0]:
        return n - even_first[1] - odd_first[1]
    return n - max(even_first[1] + odd_second[1], even_second[1] + odd_first[1])


# ---- test harness ---------------------------------------------------------

seed = 2170


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(nums):
    print(f"[{', '.join(map(str, nums))}] -> {minimum_operations(nums)}")


def main():
    show([3, 1, 3, 2, 4, 3])
    show([1, 2, 2, 2, 2])
    show([7])
    show([5, 5])
    show([5, 6])
    show([4, 9, 4, 9, 4])
    show([1, 1, 1, 1, 2, 1, 2])
    total = 0
    check = 0
    for rnd in range(2000):
        length = next_random() % 20 + 1
        top = [2, 4, 100000][rnd % 3]
        nums = [(next_random() * 32768 + next_random()) % top + 1 for _ in range(length)]
        ops = minimum_operations(nums)
        total += ops
        check = (check * 31 + ops) % 1000000007
    print(f"2000 lists: {total} in all, checksum {check}")
    few = [next_random() % 3 + 1 for _ in range(100000)]
    many = [(next_random() * 32768 + next_random()) % 100000 + 1 for _ in range(100000)]
    same = [8] * 100000
    print(f"100000 numbers: {minimum_operations(few)} {minimum_operations(many)} {minimum_operations(same)}")


main()
