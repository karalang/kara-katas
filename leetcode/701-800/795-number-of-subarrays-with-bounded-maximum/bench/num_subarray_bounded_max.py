# LeetCode 795 -- Number of Subarrays with Bounded Maximum: the bench, in
# Python. Mirrors num_subarray_bounded_max.kara: one pass, keeping the
# last place of a number above right and of one in range.


def num_subarray_bounded_max(nums, left, right):
    too_big = -1
    in_range = -1
    count = 0
    for i, x in enumerate(nums):
        if x > right:
            too_big = i
        elif x >= left:
            in_range = i
        if in_range > too_big:
            count += in_range - too_big
    return count


seed = 795


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def big_random():
    a = next_random()
    b = next_random()
    return (a * 32768 + b) % 1000000001


def main():
    arrays = [[big_random() for _ in range(100000)] for _ in range(16)]
    rounds = 8000
    total = 0
    check = 0
    for r in range(rounds):
        a = big_random()
        b = big_random()
        count = num_subarray_bounded_max(arrays[r % 16], min(a, b), max(a, b))
        total += count
        check = (check * 131 + count % 1000000007) % 1000000007
    print(f"{rounds} rounds of 100000 numbers: {total} subarrays, checksum {check}")


main()
