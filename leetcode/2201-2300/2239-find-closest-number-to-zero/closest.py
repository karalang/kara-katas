# LeetCode #2239: Find Closest Number to Zero -- the mirror of
# closest.kara: one scan, a number kept when nearer to zero or as near
# and larger.


def find_closest_number(nums):
    closest = nums[0]
    for x in nums:
        if abs(x) < abs(closest) or (abs(x) == abs(closest) and x > closest):
            closest = x
    return closest


seed = 2239


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    high = next_random()
    return high * 32768 + next_random()


def show(nums):
    print(f"[{', '.join(map(str, nums))}] -> {find_closest_number(nums)}")


def main():
    show([-4, -2, 1, 4, 8])
    show([2, -1, 1])
    show([-1])
    show([-5, 5])
    show([3, 0, -3])
    show([-100000, 100000])
    show([-3, -3, 2, -2])
    check = 0
    positive = 0
    for c in range(3000):
        n = next_random() % 50 + 1
        top = [10, 1000, 100000][c % 3]
        nums = [wide_random() % (2 * top + 1) - top for _ in range(n)]
        closest = find_closest_number(nums)
        if closest > 0:
            positive += 1
        check = (check * 31 + closest + 100000) % 1000000007
    print(f"3000 arrays: checksum {check}, {positive} positive")
    nums = [wide_random() % 200001 - 100000 for _ in range(1000)]
    print(f"1000 random numbers: {find_closest_number(nums)}")
    far = [-501 - k if k % 2 == 0 else 501 + k for k in range(1000)]
    far.append(-501)
    print(f"1000 numbers beyond 500: {find_closest_number(far)}")


main()
