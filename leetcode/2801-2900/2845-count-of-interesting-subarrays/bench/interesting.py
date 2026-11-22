# LeetCode #2845: Count of Interesting Subarrays -- the bench, mirrored
# from interesting.kara: a dict from each prefix count mod modulo to how
# often it has come up, read before each new prefix is added.

seed = 2845


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


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, n, rounds = 10, 100000, 20
    cases = []
    for c in range(count):
        nums = []
        for _ in range(n):
            hi = next_random()
            nums.append((hi * 32768 + next_random()) % 1000000000 + 1)
        modulo = next_random() % (10 if c % 2 == 0 else 100000) + 1
        k = next_random() % modulo
        cases.append((nums, modulo, k))
    total = 0
    check = 0
    for r in range(rounds):
        for nums, modulo, k in cases:
            got = count_interesting_subarrays(nums, modulo, k)
            total += got
            check = (check * 31 + got % 1000000007 + r) % 1000000007
    print(f"{count} arrays of {n}, {rounds} rounds: {total} subarrays, checksum {check}")


main()
