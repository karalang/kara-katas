# LeetCode #2183: Count Array Pairs Divisible by K -- the Python mirror of
# pairs_divisible.kara: each number counted under its gcd with k, and
# every two gcds whose product is a multiple of k paired.


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def count_pairs(nums, k):
    by_gcd = [0] * (k + 1)
    for x in nums:
        by_gcd[gcd(x, k)] += 1
    divisors = []
    d = 1
    while d * d <= k:
        if k % d == 0:
            if by_gcd[d] > 0:
                divisors.append(d)
            if d * d != k and by_gcd[k // d] > 0:
                divisors.append(k // d)
        d += 1
    pairs = 0
    for a in range(len(divisors)):
        for b in range(a, len(divisors)):
            g = divisors[a]
            h = divisors[b]
            if g * h % k == 0:
                if a == b:
                    pairs += by_gcd[g] * (by_gcd[g] - 1) // 2
                else:
                    pairs += by_gcd[g] * by_gcd[h]
    return pairs


# ---- test harness ---------------------------------------------------------

seed = 2183


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def big_random():
    a = next_random()
    b = next_random()
    return a * 32768 + b


def show(nums, k):
    print(f"[{', '.join(map(str, nums))}], {k} -> {count_pairs(nums, k)}")


def main():
    show([1, 2, 3, 4, 5], 2)
    show([1, 2, 3, 4], 5)
    show([7], 1)
    show([6, 10, 15], 30)
    show([4, 9], 6)
    show([100000, 100000, 100000], 100000)
    total = 0
    check = 0
    for rnd in range(2000):
        n = next_random() % 30 + 1
        if rnd % 2 == 0:
            k = next_random() % 12 + 1
            nums = [next_random() % 20 + 1 for _ in range(n)]
        else:
            k = big_random() % 100000 + 1
            nums = [big_random() % 100000 + 1 for _ in range(n)]
        found = count_pairs(nums, k)
        total += found
        check = (check * 31 + found % 1000000007 + k) % 1000000007
    print(f"2000 lists: {total} pairs in all, checksum {check}")
    same = [100000] * 100000
    mixed = [big_random() % 100000 + 1 for _ in range(100000)]
    print(f"100000 numbers: {count_pairs(same, 100000)} {count_pairs(mixed, 100000)} {count_pairs(mixed, 83160)} {count_pairs(mixed, 99991)}")


main()
