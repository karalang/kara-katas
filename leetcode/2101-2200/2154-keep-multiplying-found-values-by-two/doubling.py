# LeetCode #2154: Keep Multiplying Found Values by Two -- the Python mirror
# of doubling.kara's ★ arm.


def find_final_value(nums, original):
    found = set(nums)
    value = original
    while value in found:
        value *= 2
    return value


seed = 2154


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(nums, original):
    print(f"[{', '.join(map(str, nums))}], {original} -> {find_final_value(nums, original)}")


def main():
    show([5, 3, 6, 1, 12], 3)
    show([2, 7, 9], 4)
    show([1], 1)
    show([1 << k for k in range(10)], 1)
    show([2, 4], 1)
    show([1000], 1000)
    total = 0
    check = 0
    for rnd in range(2000):
        n = next_random() % 15 + 1
        original = next_random() % 4 + 1
        if rnd % 2 == 0:
            nums = [next_random() % 16 + 1 for _ in range(n)]
        else:
            nums = []
            for k in range(n):
                if next_random() % 4 == 0:
                    nums.append(next_random() % 100 + 1)
                else:
                    nums.append(original << (k % 6))
            for i in range(n - 1, 0, -1):
                j = next_random() % (i + 1)
                nums[i], nums[j] = nums[j], nums[i]
        last = find_final_value(nums, original)
        total += last
        check = (check * 31 + last + n) % 1000000007
    print(f"2000 lists: {total} in all, checksum {check}")
    every = list(range(1, 1001))
    gap = [511 if x == 512 else x for x in range(1, 1001)]
    rand = [next_random() % 1000 + 1 for _ in range(1000)]
    print(f"1000 numbers: {find_final_value(every, 1)} every one, {find_final_value(gap, 1)} but 512, {find_final_value(rand, 1)} at random")


main()
