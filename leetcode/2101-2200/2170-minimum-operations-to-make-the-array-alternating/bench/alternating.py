# LeetCode #2170: Minimum Operations to Make the Array Alternating -- the
# benchmark's Python mirror of alternating.kara.


def top_two(nums, start, end):
    counts = {}
    for i in range(start, end, 2):
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


def minimum_operations(nums, lo, n):
    even_first, even_second = top_two(nums, lo, lo + n)
    odd_first, odd_second = top_two(nums, lo + 1, lo + n)
    if even_first[0] != odd_first[0]:
        return n - even_first[1] - odd_first[1]
    return n - max(even_first[1] + odd_second[1], even_second[1] + odd_first[1])


seed = 2170


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    row = []
    for _ in range(400000):
        a = next_random()
        b = next_random()
        row.append((a * 32768 + b) % 1000 + 1)
    check = 0
    for _ in range(100):
        a = next_random()
        b = next_random()
        start = (a * 32768 + b) % 300001
        ops = minimum_operations(row, start, 100000)
        check = (check * 31 + ops) % 1000000007
    print(f"100 solves: checksum {check}")


main()
