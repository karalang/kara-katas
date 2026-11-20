# LeetCode #2338: Count the Number of Ideal Arrays -- the bench, the ★ arm
# in Python: the strictly increasing divisor chains of each length counted
# level by level, each length k + 1 spread over the n places in
# C(n - 1, k) ways.

MOD = 1000000007
LONGEST = 14


def power(base, exp):
    result = 1
    base %= MOD
    while exp > 0:
        if exp % 2 == 1:
            result = result * base % MOD
        base = base * base % MOD
        exp //= 2
    return result


def binomials(m, count):
    out = [1]
    for k in range(1, count):
        out.append(out[k - 1] * ((m - k + 1) % MOD) % MOD * power(k, MOD - 2) % MOD)
    return out


def ideal_arrays(n, max_value):
    ways = binomials(n - 1, LONGEST)
    ends = [1] * (max_value + 1)
    ends[0] = 0
    answer = 0
    for k in range(LONGEST):
        total = 0
        for v in range(1, max_value + 1):
            total = (total + ends[v]) % MOD
        answer = (answer + total * ways[k]) % MOD
        following = [0] * (max_value + 1)
        for d in range(1, max_value + 1):
            if ends[d] != 0:
                m = 2 * d
                while m <= max_value:
                    following[m] = (following[m] + ends[d]) % MOD
                    m += d
        ends = following
    return answer


def scrambled(index):
    return index * 2654435761 % 2147483647


def main():
    check = 0
    for q in range(300):
        n = 2 + scrambled(q + 1) % 9999
        max_value = 5000 + scrambled(q + 1001) % 5001
        check = (check * 31 + ideal_arrays(n, max_value)) % 1000000007
    print(f"300 queries of n up to 10^4 and maxValue 5000 to 10^4: checksum {check}")


main()
