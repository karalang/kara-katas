# Benchmark for #360 -- mirror of sort_transformed.kara.
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


def rem(v, m):
    # Truncated remainder, as Kara, C, Rust and Go compute v % m.
    r = abs(v) % m
    return r if v >= 0 else -r


def main():
    seed = 360
    checksum = 0
    nums = [0] * 50000
    for _ in range(200):
        x = -1000000
        for i in range(50000):
            seed = (seed * 1103515245 + 12345) % 2147483648
            x += (seed // 65536) % 81
            nums[i] = x
        seed = (seed * 1103515245 + 12345) % 2147483648
        a = (seed // 65536) % 21 - 10
        seed = (seed * 1103515245 + 12345) % 2147483648
        b = (seed // 65536) % 21 - 10
        seed = (seed * 1103515245 + 12345) % 2147483648
        c = (seed // 65536) % 21 - 10
        for v in sort_transformed_array(nums, a, b, c):
            checksum = (checksum * 31 + rem(v, 1000000007) + 1000000007) % 1000000007
    print(f"checksum {checksum}")


main()
