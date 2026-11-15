# LeetCode #2206: Divide Array Into Equal Pairs -- Python mirror of
# pairs.kara (the ★ arm).


def divide_array(nums):
    count = [0] * 501
    for x in nums:
        count[x] += 1
    for c in count:
        if c % 2 == 1:
            return False
    return True


seed = 2206


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(nums):
    print(f"[{', '.join(map(str, nums))}] -> {str(divide_array(nums)).lower()}")


def main():
    show([3, 2, 3, 2, 2, 2])
    show([1, 2, 3, 4])
    show([5, 5])
    show([1, 1, 1, 1])
    show([7, 7, 7, 8])
    show([500, 1, 1, 500])
    yes = 0
    check = 0
    for c in range(3000):
        half = next_random() % 10 + 1
        top = [2, 5, 500][c % 3]
        nums = []
        if c % 2 == 0:
            for _ in range(half):
                x = next_random() % top + 1
                nums.append(x)
                nums.append(x)
            for i in range(len(nums) - 1, 0, -1):
                j = next_random() % (i + 1)
                nums[i], nums[j] = nums[j], nums[i]
        else:
            nums = [next_random() % top + 1 for _ in range(2 * half)]
        paired = divide_array(nums)
        if paired:
            yes += 1
        check = (check * 31 + (2 if paired else 1) + len(nums)) % 1000000007
    print(f"3000 arrays: {yes} divide, checksum {check}")
    nums = []
    for i in range(500):
        nums.append(i % 500 + 1)
        nums.append((499 - i) % 500 + 1)
    print(f"1000 numbers in pairs -> {str(divide_array(nums)).lower()}")
    nums[999] = 250
    print(f"1000 numbers, the last changed -> {str(divide_array(nums)).lower()}")


main()
