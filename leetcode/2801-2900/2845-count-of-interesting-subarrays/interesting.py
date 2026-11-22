# LeetCode #2845: Count of Interesting Subarrays -- the Python mirror of
# the ★ arm: a dict from each prefix count mod modulo to how often it
# has come up, read before each new prefix is added.


def count_interesting_subarrays(nums, modulo, k):
    seen = {0: 1}
    prefix = 0
    count = 0
    for x in nums:
        if x % modulo == k:
            prefix = (prefix + 1) % modulo
        want = (prefix - k + modulo) % modulo
        count += seen.get(want, 0)
        seen[prefix] = seen.get(prefix, 0) + 1
    return count


# ---- the harness: the same in every arm --------------------------------

seed = 2845


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def big():
    hi = next_random()
    return hi * 32768 + next_random()


def main():
    c = count_interesting_subarrays
    print(f"{c([3, 2, 4], 2, 1)} {c([3, 1, 9, 6], 3, 0)}")
    print(f"{c([5], 5, 0)} {c([5], 2, 1)}")
    many = [i % 1000 + 1 for i in range(4000)]
    print(f"{c(many, 1, 0)} {c(many, 1000000000, 999999999)}")
    check = 0
    total = 0
    for i in range(3050):
        short = i < 3000
        n = next_random() % 10 + 1 if short else next_random() % 1000 + 1
        top = 10 if short else 1000000000
        nums = [big() % top + 1 for _ in range(n)]
        if short or i % 2 == 0:
            modulo = next_random() % (5 if short else 10) + 1
        else:
            modulo = big() % 1000000000 + 1
        k = big() % modulo
        got = c(nums, modulo, k)
        total += got
        check = (check * 31 + got) % 1000000007
        if i == 2999:
            print(f"3000 short arrays: {total} subarrays, checksum {check}")
            total = 0
            check = 0
    print(f"50 long arrays: {total} subarrays, checksum {check}")


main()
