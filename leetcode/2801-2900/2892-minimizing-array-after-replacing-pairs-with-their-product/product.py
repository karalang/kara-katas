# LeetCode #2892: Minimizing Array After Replacing Pairs With Their
# Product -- the Python mirror of the ★ arm (product.kara): 1 if a 0 is
# held, else runs of product at most k, greedily left to right.


def min_array_length(nums, k):
    if 0 in nums:
        return 1
    runs = 1
    product = nums[0]
    for x in nums[1:]:
        if product * x <= k:
            product *= x
        else:
            runs += 1
            product = x
    return runs


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def main():
    global seed
    print(f"{min_array_length([2, 3, 3, 7, 3, 5], 20)} {min_array_length([3, 3, 3, 3], 6)}")
    n = 100000
    print(f"{min_array_length([1] * n, 1)} {min_array_length([1000000000] * n, 1000000000)} {min_array_length([2] * n, 1 << 30)}")
    seed = 2892
    total = 0
    check = 0
    for c in range(3100):
        small = c < 3000
        n = next_random() % 8 + 1 if small else wide() % 99001 + 1000
        zero = c % (15 if small else 10) == 0
        nums = []
        for _ in range(n):
            if small:
                nums.append(next_random() % 6 + 1)
            elif next_random() % 2 == 0:
                nums.append(1)
            else:
                nums.append(next_random() % 1000 + 1)
        if zero:
            nums[wide() % n] = 0
        k = next_random() % 40 + 1 if small else wide() % 1000000000 + 1
        length = min_array_length(nums, k)
        total += length
        check = (check * 31 + length) % 1000000007
        if c == 2999:
            print(f"3000 short arrays: lengths total {total}, checksum {check}")
            total = 0
            check = 0
    print(f"100 long arrays: lengths total {total}, checksum {check}")


main()
