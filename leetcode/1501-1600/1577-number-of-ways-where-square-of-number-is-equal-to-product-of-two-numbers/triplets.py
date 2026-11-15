# LeetCode #1577: Number of Ways Where Square of Number Is Equal to Product
# of Two Numbers -- the Python mirror of the ★ arm: for each value x of one
# array, a walk over the other that keeps a dict of the values seen so far
# and, at each y dividing x^2, adds how many times x^2 / y was seen. Both
# types are the same count with the arrays swapped. O(n * m) expected


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


# ---- the harness: the same in every arm

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def batch(count, most, top):
    check = 0
    total = 0
    for _ in range(count):
        pair = []
        for _ in range(2):
            n = next_random() % most + 1
            nums = []
            for _ in range(n):
                v = next_random() % top + 1
                for _ in range(next_random() % 4):
                    v *= 2 + next_random() % 2
                nums.append(min(v, 100000))
            pair.append(nums)
        w = num_triplets(pair[0], pair[1])
        total += w
        check = mix(check, w)
    print(f"{count} pairs of up to {most} values: triplets total {total}, checksum {check}")


def main():
    global seed
    examples = [
        ([7, 4], [5, 2, 8, 9]),
        ([1, 1], [1, 1, 1]),
        ([7, 7, 8, 3], [1, 2, 9, 7]),
        ([4, 7, 9, 11, 23], [3, 5, 1024, 12, 18]),
        ([1], [1]),
        ([100000], [100000, 100000]),
    ]
    for a, b in examples:
        print(f"{a}, {b} -> {num_triplets(a, b)}")
    seed = 1577
    batch(3000, 6, 4)
    batch(300, 100, 20)
    batch(10, 1000, 100)


main()
