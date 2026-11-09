# LeetCode #2032: Two Out of Three -- Python mirror of the ★ arm
# (three.kara). Each value up to 100 gets a mask of the arrays it appears
# in; the values whose mask has at least two bits are the answer, read in
# ascending order. O(n + 100).


def two_out_of_three(nums1, nums2, nums3):
    mask = [0] * 101
    for x in nums1:
        mask[x] |= 1
    for x in nums2:
        mask[x] |= 2
    for x in nums3:
        mask[x] |= 4
    return [v for v in range(1, 101) if bin(mask[v]).count("1") >= 2]


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def draw(n, top):
    return [next_random() % top + 1 for _ in range(n)]


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    global seed
    examples = [
        ([1, 1, 3, 2], [2, 3], [3]),
        ([3, 1], [2, 3], [1, 2]),
        ([1, 2, 2], [4, 3, 3], [5]),
        ([7], [7], [7]),
        ([5, 5, 5], [6], [5]),
        ([100, 1], [1, 100], [50]),
        ([9, 8, 7], [1, 2, 3], [4, 5, 6]),
        ([4, 4, 2, 2], [2, 3, 4], [3, 3, 1]),
    ]
    for a, b, c in examples:
        print(f"{show(a)} {show(b)} {show(c)} -> {show(two_out_of_three(a, b, c))}")
    seed = 2032
    total = 0
    check = 0
    for _ in range(3000):
        top = next_random() % 30 + 1
        a = draw(next_random() % 20 + 1, top)
        b = draw(next_random() % 20 + 1, top)
        c = draw(next_random() % 20 + 1, top)
        answer = two_out_of_three(a, b, c)
        total += len(answer)
        for v in answer:
            check = (check * 31 + v) % 1000000007
    print(f"3000 problems of up to 20 values: {total} values kept, checksum {check}")
    total = 0
    check = 0
    for _ in range(2000):
        a = draw(100, 100)
        b = draw(100, 100)
        c = draw(100, 100)
        answer = two_out_of_three(a, b, c)
        total += len(answer)
        for v in answer:
            check = (check * 31 + v) % 1000000007
    print(f"2000 problems of 100 values: {total} values kept, checksum {check}")


main()
