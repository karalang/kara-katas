# LeetCode #2057: Smallest Index With Equal Value -- Python mirror of the ★
# arm (equal.kara): the indices walked from the front, the first whose last
# digit is its element returned. Output is byte-identical to the Kāra arms.


def smallest_equal(nums):
    for i in range(len(nums)):
        if i % 10 == nums[i]:
            return i
    return -1


# ---- test harness ---------------------------------------------------------

seed = 2057


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def draw(n, rare):
    nums = []
    for i in range(n):
        d = next_random() % 10
        nums.append((d + 1) % 10 if d == i % 10 and next_random() % rare != 0 else d)
    return nums


def show(xs):
    return "[" + ", ".join(str(x) for x in xs) + "]"


def main():
    examples = [
        [0, 1, 2],
        [4, 3, 2, 1],
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 0],
        [9],
        [0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [2, 0, 3, 4, 5, 6, 7, 8, 9, 1, 2, 2, 2],
    ]
    for nums in examples:
        print(f"{show(nums)} -> {smallest_equal(nums)}")
    found = total = check = 0
    for _ in range(5000):
        n = next_random() % 100 + 1
        rare = next_random() % 20 + 1
        at = smallest_equal(draw(n, rare))
        if at >= 0:
            found += 1
        total += at
        check = (check * 31 + at + 2) % 1000000007
    print(f"5000 arrays: {found} found, sum {total}, checksum {check}")


main()
