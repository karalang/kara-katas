# LeetCode #2338: Count the Number of Ideal Arrays -- the Python mirror of
# the ★ arm: the strictly increasing divisor chains of each length, level
# by level, each length k + 1 times the C(n - 1, k) ways to spread it over
# the n places.

MOD = 1000000007
LONGEST = 14


def power(base, exp, modulus):
    result = 1
    base %= modulus
    while exp > 0:
        if exp % 2 == 1:
            result = result * base % modulus
        base = base * base % modulus
        exp //= 2
    return result


def binomials(m, count, modulus):
    out = [1]
    for k in range(1, count):
        out.append(out[k - 1] * ((m - k + 1) % modulus) % modulus * power(k, modulus - 2, modulus) % modulus)
    return out


def ideal_arrays(n, max_value):
    ways = binomials(n - 1, LONGEST, MOD)
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


SEED = [2338]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


def main():
    print(ideal_arrays(2, 5))
    print(ideal_arrays(5, 3))
    print(ideal_arrays(2, 1))
    print(ideal_arrays(10000, 1))
    print(ideal_arrays(10000, 60))
    print(ideal_arrays(3, 10000))
    print(ideal_arrays(300, 3000))
    check = 0
    total = 0
    for _ in range(2000):
        n = 2 + next_random() % 39
        max_value = 1 + next_random() % 80
        count = ideal_arrays(n, max_value)
        check = (check * 31 + count) % MOD
        total += count
    print(f"2000 cases: checksum {check}, total {total}")


main()
