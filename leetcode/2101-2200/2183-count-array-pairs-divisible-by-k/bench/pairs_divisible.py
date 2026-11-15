# LeetCode #2183: Count Array Pairs Divisible by K -- the benchmark's
# Python mirror of pairs_divisible.kara.


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


seed = 2183


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def big_random():
    a = next_random()
    b = next_random()
    return a * 32768 + b


def main():
    row = [big_random() % 100000 + 1 for _ in range(1000000)]
    check = 0
    for _ in range(200):
        start = big_random() % 900001
        k = big_random() % 100000 + 1
        found = count_pairs(row[start:start + 100000], k)
        check = (check * 31 + found % 1000000007) % 1000000007
    print(f"200 solves: checksum {check}")


main()
