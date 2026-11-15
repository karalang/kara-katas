# LeetCode #1577: Number of Ways Where Square of Number Is Equal to
# Product of Two Numbers -- bench: the ★ arm (a walk with a Map of the
# values seen) over 10 pairs of arrays of 1000 values, each a power of 2
# or 3 times a factor below 100, drawn first.


def ways(squares, products):
    total = 0
    for x in squares:
        target = x * x
        seen = {}
        for y in products:
            if target % y == 0:
                total += seen.get(target // y, 0)
            seen[y] = seen.get(y, 0) + 1
    return total


def num_triplets(nums1, nums2):
    return ways(nums1, nums2) + ways(nums2, nums1)


seed = 1577


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def main():
    arrays = []
    for _ in range(20):
        nums = []
        for _ in range(1000):
            v = next_random() % 100 + 1
            for _ in range(next_random() % 4):
                v *= 2 + next_random() % 2
            nums.append(min(v, 100000))
        arrays.append(nums)
    check = 0
    total = 0
    for p in range(10):
        w = num_triplets(arrays[2 * p], arrays[2 * p + 1])
        total += w
        check = mix(check, w)
    print(f"10 pairs of arrays of 1000 values: triplets total {total}, checksum {check}")


main()
