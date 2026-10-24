# LeetCode #977: Squares of a Sorted Array -- mirror of the ★ arm
# (sorted_squares.kara), two pointers from the ends.


def sorted_squares(nums):
    n = len(nums)
    out = [0] * n
    lo, hi, at = 0, n - 1, n - 1
    while lo <= hi:
        a = nums[lo] * nums[lo]
        b = nums[hi] * nums[hi]
        if a > b:
            out[at] = a
            lo += 1
        else:
            out[at] = b
            hi -= 1
        at -= 1
    return out


seed = 977


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_sorted(n, top):
    nums = [next_random() % (2 * top + 1) - top for _ in range(n)]
    nums.sort()
    return nums


def main():
    cases = [
        [-4, -1, 0, 3, 10],
        [-7, -3, 2, 3, 11],
        [0],
        [-5],
        [-9, -4, -2, -1],
        [1, 2, 6, 7],
        [-3, -3, 0, 0, 3, 3],
        [-10000, -1, 1, 10000],
        [-2, -1, 0, 1, 2],
        [-10, 1, 2, 3, 4],
    ]
    for nums in cases:
        print(f"{nums}: {sorted_squares(nums)}")
    for count, most, top in [(300, 12, 5), (3000, 60, 1000), (4, 10000, 10000)]:
        total = 0
        check = 0
        for _ in range(count):
            n = most if most == 10000 else 1 + next_random() % most
            for s in sorted_squares(random_sorted(n, top)):
                total += s
                check = (check * 31 + s) % 1000000007
        print(f"{count} random arrays of up to {most} numbers: squares total {total}, checksum {check}")


main()
