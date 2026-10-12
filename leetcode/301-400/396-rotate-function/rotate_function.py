# LeetCode #396: Rotate Function -- Python mirror of rotate_function.kara.


def max_rotate_function(nums):
    n = len(nums)
    total = 0
    f = 0
    for i in range(n):
        total += nums[i]
        f += i * nums[i]
    best = f
    for k in range(1, n):
        f = f + total - n * nums[n - k]
        best = max(best, f)
    return best


seed = 396


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(nums):
    print(f"[{', '.join(str(x) for x in nums)}]: {max_rotate_function(nums)}")


def main():
    show([4, 3, 2, 6])
    show([100])
    show([-5])
    show([1, 2])
    show([2, 1])
    show([-1, -2, -3, -4])
    show([0, 0, 0])
    show([7, 7, 7, 7, 7])
    show([-100, 100, -100, 100, -100])
    total = 0
    checksum = 0
    m = 1000000007
    for _ in range(3000):
        n = 1 + step() % 50
        nums = [step() % 201 - 100 for _ in range(n)]
        r = max_rotate_function(nums)
        total += r
        checksum = (checksum * 31 + r % m + m) % m
    print(f"3000 random arrays: total {total}, checksum {checksum}")


main()
