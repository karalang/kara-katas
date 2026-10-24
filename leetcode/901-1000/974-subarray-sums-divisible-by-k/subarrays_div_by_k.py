# LeetCode #974: Subarray Sums Divisible by K -- Python mirror of
# subarrays_div_by_k.kara.


def subarrays_div_by_k(nums, k):
    count = [0] * k
    count[0] = 1
    s = total = 0
    for x in nums:
        s += x
        r = (s % k + k) % k
        total += count[r]
        count[r] += 1
    return total


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_nums(n, span):
    return [next_random() % (2 * span + 1) - span for _ in range(n)]


def main():
    global seed
    cases = [
        ([4, 5, 0, -2, -3, 1], 5),
        ([5], 9),
        ([0, 0, 0], 2),
        ([-1, 2, 9], 2),
        ([7, -7], 7),
        ([-5, -5, -5], 5),
        ([-3, 1, -1, 3], 4),
        ([10000, -10000, 10000], 10000),
        ([1, 2, 3], 10000),
        ([2, -2, 2, -2], 3),
    ]
    for nums, k in cases:
        print(f"{nums} with k = {k}: {subarrays_div_by_k(nums, k)}")
    seed = 974
    for count, most, span, top in [(300, 12, 10, 6), (3000, 60, 10000, 50),
                                   (4, 30000, 10000, 10000)]:
        total = check = 0
        for _ in range(count):
            n = most if most == 30000 else 1 + next_random() % most
            nums = random_nums(n, span)
            k = 2 + next_random() % (top - 1)
            got = subarrays_div_by_k(nums, k)
            total += got
            check = (check * 31 + got) % 1000000007
        print(f"{count} random cases of up to {most} numbers: "
              f"{total} subarrays, checksum {check}")


main()
