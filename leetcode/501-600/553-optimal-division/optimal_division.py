# LeetCode #553: Optimal Division -- Python mirror of the ★ arm (the
# shape is always the same); see optimal_division.kara.


def optimal_division(nums):
    n = len(nums)
    out = []
    for i in range(n):
        if i > 0:
            out.append("/")
        if i == 1 and n > 2:
            out.append("(")
        out.append(str(nums[i]))
    if n > 2:
        out.append(")")
    return "".join(out)


# ---- test harness ---------------------------------------------------------

seed = 553


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(nums):
    print(f"[{', '.join(str(x) for x in nums)}] -> {optimal_division(nums)}")


def main():
    show([1000, 100, 10, 2])
    show([2, 3, 4])
    show([7])
    show([8, 2])
    show([2, 1000])
    show([6, 2, 3, 4, 5])
    show([2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    show([1000, 999, 998, 997, 996, 995, 994, 993, 992, 991])
    numbers = chars = h = 0
    for _ in range(300):
        n = 1 + next_random() % 10
        nums = []
        while len(nums) < n:
            x = 2 + next_random() % 999
            if x not in nums:
                nums.append(x)
        text = optimal_division(nums)
        numbers += n
        for b in text.encode():
            chars += 1
            h = (h * 131 + b) % 1000000007
    print(f"300 random arrays: {numbers} numbers, {chars} characters, checksum {h}")


main()
