# LeetCode #2460: Apply Operations to an Array -- the Python mirror of
# apply.kara: the operations in place, then the nonzero values moved
# forward by a write index and the rest filled with zeros.


def apply_operations(nums):
    nums = list(nums)
    n = len(nums)
    for i in range(n - 1):
        if nums[i] == nums[i + 1]:
            nums[i] *= 2
            nums[i + 1] = 0
    k = 0
    for i in range(n):
        if nums[i] != 0:
            nums[k] = nums[i]
            k += 1
    for i in range(k, n):
        nums[i] = 0
    return nums


# ---- test harness ---------------------------------------------------------

seed = 2460


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def fold(values):
    check = 0
    for v in values:
        check = (check * 31 + v + 1) % 1000000007
    return check


def show(values):
    return "[" + ", ".join(str(v) for v in values) + "]"


def main():
    cases = [
        [1, 2, 2, 1, 1, 0],
        [0, 1],
        [2, 2, 2, 2, 2],
        [2, 0, 2, 0, 0, 2],
        [0, 0, 0],
        [3, 0, 0, 3, 3, 3],
        [1000, 1000],
        [4, 2, 2, 4, 8, 8, 16],
    ]
    for nums in cases:
        print(f"{show(nums)} -> {show(apply_operations(nums))}")
    print(f"2000 of 1000: checksum {fold(apply_operations([1000] * 2000))}")
    alternating = [1000 if i % 2 == 0 else 0 for i in range(2000)]
    print(f"2000 alternating: checksum {fold(apply_operations(alternating))}")
    for top in (1001, 4):
        nums = [next_random() % top for _ in range(2000)]
        print(f"2000 random below {top}: checksum {fold(apply_operations(nums))}")
    check = 0
    for _ in range(3000):
        n = 2 + next_random() % 11
        nums = [next_random() % 3 for _ in range(n)]
        check = (check * 31 + fold(apply_operations(nums))) % 1000000007
    print(f"3000 random: checksum {check}")


if __name__ == "__main__":
    main()
