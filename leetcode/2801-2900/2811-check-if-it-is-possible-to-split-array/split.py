# LeetCode #2811: Check if it is Possible to Split Array -- the Python
# mirror of the ★ arm: two numbers or fewer, or two neighbours summing to
# at least m.


def can_split_array(nums, m):
    return len(nums) <= 2 or any(nums[i] + nums[i + 1] >= m for i in range(len(nums) - 1))


seed = 2811


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(b):
    return "true" if b else "false"


def main():
    print(show(can_split_array([2, 2, 1], 4)))
    print(show(can_split_array([2, 1, 3], 5)))
    print(show(can_split_array([2, 3, 3, 2, 3], 6)))
    print(show(can_split_array([1, 1], 200)))
    print(show(can_split_array([100] * 100, 200)))
    print(show(can_split_array([99] * 100, 199)))
    yes = 0
    check = 0
    for _ in range(3000):
        n = next_random() % 7 + 1
        nums = [next_random() % 6 + 1 for _ in range(n)]
        a = can_split_array(nums, next_random() % 12 + 1)
        yes += 1 if a else 0
        check = (check * 2 + (1 if a else 0)) % 1000000007
    print(f"3000 small arrays: {yes} can split, checksum {check}")
    yes = 0
    check = 0
    for _ in range(50):
        n = next_random() % 100 + 1
        nums = [next_random() % 100 + 1 for _ in range(n)]
        a = can_split_array(nums, next_random() % 200 + 1)
        yes += 1 if a else 0
        check = (check * 2 + (1 if a else 0)) % 1000000007
    print(f"50 large arrays: {yes} can split, checksum {check}")


main()
