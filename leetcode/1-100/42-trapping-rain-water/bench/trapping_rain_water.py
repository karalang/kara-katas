"""LeetCode #42 bench mirror — Python, the converging two-pointer solver (★).

Mirrors bench/trapping_rain_water.kara: advance the shorter outer wall, settling each column
with its running max. The buffer is reused in place each iteration with a k-dependent jagged
terrain; fold each answer into a rolling checksum. Same workload + sink as every other
mirror. This is the slow interpreted baseline (long-workload lane).
"""


def trap(height: list[int], n: int) -> int:
    left, right = 0, n - 1
    left_max = right_max = 0
    water = 0
    while left < right:
        if height[left] < height[right]:
            if height[left] >= left_max:
                left_max = height[left]
            else:
                water += left_max - height[left]
            left += 1
        else:
            if height[right] >= right_max:
                right_max = height[right]
            else:
                water += right_max - height[right]
            right -= 1
    return water


def main() -> None:
    total = 200000
    n = 1000
    modulus = 1000000007

    height = [(i * 37) % 100 for i in range(n)]
    acc = 0
    for k in range(total):
        height[k % n] = (k * 19) % 100
        ans = trap(height, n)
        acc = (acc * 131 + ans) % modulus

    print(acc)


if __name__ == "__main__":
    main()
