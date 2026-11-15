# LeetCode #2165: Smallest Value of the Rearranged Number -- the
# benchmark's Python mirror of smallest.kara. Kāra's % takes the
# dividend's sign, so rem() does too.


def rem(a, b):
    r = abs(a) % b
    return -r if a < 0 else r


def smallest_number(num):
    digits = [int(c) for c in str(abs(num))]
    if num < 0:
        digits.sort(reverse=True)
    else:
        digits.sort()
        for i, d in enumerate(digits):
            if d != 0:
                digits[0], digits[i] = digits[i], digits[0]
                break
    size = 0
    for d in digits:
        size = size * 10 + d
    return -size if num < 0 else size


seed = 2165


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    nums = []
    for _ in range(1000):
        length = next_random() % 14 + 1
        num = 0
        for _ in range(length):
            num = num * 10 + next_random() % 10
        if next_random() % 2 == 1:
            num = -num
        nums.append(num)
    check = 0
    for _ in range(1000):
        for k in range(1000):
            nums[k] = nums[k] + next_random() % 2001 - 1000
            s = smallest_number(nums[k])
            check = rem(check * 31 + rem(s, 1000000007) + 1000000007, 1000000007)
    print(f"1000000 solves: checksum {check}")


main()
