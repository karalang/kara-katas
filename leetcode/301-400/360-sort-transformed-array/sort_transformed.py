# LeetCode #360: Sort Transformed Array -- mirror of sort_transformed.kara.


def f(x, a, b, c):
    return a * x * x + b * x + c


def sort_transformed_array(nums, a, b, c):
    n = len(nums)
    out = [0] * n
    lo, hi = 0, n - 1
    if a >= 0:
        k = n - 1
        while lo <= hi:
            left, right = f(nums[lo], a, b, c), f(nums[hi], a, b, c)
            if left >= right:
                out[k] = left
                lo += 1
            else:
                out[k] = right
                hi -= 1
            k -= 1
    else:
        k = 0
        while lo <= hi:
            left, right = f(nums[lo], a, b, c), f(nums[hi], a, b, c)
            if left <= right:
                out[k] = left
                lo += 1
            else:
                out[k] = right
                hi -= 1
            k += 1
    return out


def show(label, nums, a, b, c):
    print(f"{label}: [{', '.join(map(str, sort_transformed_array(nums, a, b, c)))}]")


def main():
    show("example 1", [-4, -2, 2, 4], 1, 3, 5)
    show("example 2", [-4, -2, 2, 4], -1, 3, 5)

    show("empty", [], 1, 2, 3)
    show("one element", [7], -2, 0, 1)
    show("a = 0, rising line", [-3, 0, 5], 0, 2, 1)
    show("a = 0, falling line", [-3, 0, 5], 0, -2, 1)
    show("a = b = 0, constant", [1, 2, 3], 0, 0, 9)
    show("vertex inside the input", [-5, -1, 0, 1, 2, 6], 1, -2, 0)
    show("vertex left of the input", [2, 3, 9], 1, 4, 0)
    show("vertex right of the input", [-9, -3, -2], -1, 0, 0)
    show("duplicates", [-2, -2, 0, 2, 2], 3, 0, -1)
    show("large values", [-100, -50, 0, 50, 100], 100, -100, 100)

    seed = 360
    checksum = 0
    total = 0
    for _ in range(2000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        n = (seed // 65536) % 31
        nums = []
        for _ in range(n):
            seed = (seed * 1103515245 + 12345) % 2147483648
            nums.append((seed // 65536) % 201 - 100)
        nums.sort()
        seed = (seed * 1103515245 + 12345) % 2147483648
        a = (seed // 65536) % 21 - 10
        seed = (seed * 1103515245 + 12345) % 2147483648
        b = (seed // 65536) % 21 - 10
        seed = (seed * 1103515245 + 12345) % 2147483648
        c = (seed // 65536) % 21 - 10
        out = sort_transformed_array(nums, a, b, c)
        total += len(out)
        for v in out:
            checksum = (checksum * 31 + v + 1000000) % 1000000007
    print(f"2000 random inputs: {total} values, checksum {checksum}")


main()
