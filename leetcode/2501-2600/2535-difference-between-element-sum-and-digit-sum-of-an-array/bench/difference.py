# LeetCode #2535 bench, Python mirror of difference.kara.

seed = 2535


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def difference_of_sum(nums):
    element_sum = 0
    digit_sum = 0
    for x in nums:
        element_sum += x
        rest = x
        while rest > 0:
            digit_sum += rest % 10
            rest //= 10
    return abs(element_sum - digit_sum)


def main():
    passes, n = 1000, 2000
    lists = [[next_random() % 2000 + 1 for _ in range(n)] for _ in range(50)]
    check = 0
    for p in range(passes):
        for q in range(50):
            at = check % n
            lists[q][at] = (check + p) % 2000 + 1
            check = (check * 31 + difference_of_sum(lists[q]) + p) % 1000000007
    print(f"{passes} passes over 50 lists of 2000: checksum {check}")


main()
