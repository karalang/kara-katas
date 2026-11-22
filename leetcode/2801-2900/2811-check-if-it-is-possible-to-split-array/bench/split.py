# LeetCode #2811: Check if it is Possible to Split Array -- the bench in
# Python: the ★ arm over 100000 arrays of 100 numbers up to 100, m from
# 150 to 200, all drawn first, then each answered 10 times.


def can_split_array(nums, m):
    return len(nums) <= 2 or any(nums[i] + nums[i + 1] >= m for i in range(len(nums) - 1))


seed = 2811


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count = 100000
    rounds = 10
    cases = []
    for _ in range(count):
        nums = [next_random() % 100 + 1 for _ in range(100)]
        cases.append((nums, 150 + next_random() % 51))
    yes = 0
    check = 0
    for r in range(rounds):
        for nums, m in cases:
            a = 1 if can_split_array(nums, m) else 0
            yes += a
            check = (check * 31 + a + r) % 1000000007
    print(f"{count} arrays of 100, {rounds} rounds: {yes} can split, checksum {check}")


main()
