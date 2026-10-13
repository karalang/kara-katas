# LeetCode #483: Smallest Good Base -- mirror of smallest_good_base.kara
# (the ★ arm).


def is_ones(n, k, m):
    total = 1
    term = 1
    for _ in range(1, m):
        if term > (n - total) // k:
            return False
        term *= k
        total += term
    return total == n


def smallest_good_base(n):
    value = int(n)
    m = 63
    while m >= 3:
        root = int(float(value) ** (1.0 / (m - 1)))
        for k in range(root, root + 2):
            if k >= 2 and is_ones(value, k, m):
                return f"{k}"
        m -= 1
    return f"{value - 1}"


def show(n):
    print(f"n = {n} -> {smallest_good_base(n)}")


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    for n in ["13", "4681", "1000000000000000000", "3", "15", "21", "1000000",
              "2251799813685247", "999999999999999999", "919818571896748567"]:
        show(n)
    count = 300
    seed = [483]
    total = 0
    checksum = 0
    for c in range(count):
        n = 0
        if c % 3 != 2:
            k = 2 + next_random(seed) % 2000
            m = 3 + next_random(seed) % 6
            n = 1
            term = 1
            for _ in range(1, m):
                if term > 1000000000000000000 // k:
                    break
                term *= k
                n += term
        else:
            r = (next_random(seed) * 32768 + next_random(seed)) * 32768 + next_random(seed)
            if c % 30 == 29:
                n = 3 + (r * 32768 + next_random(seed)) % 999999999999999998
            else:
                n = 3 + r % 999999999998
        base = int(smallest_good_base(f"{n}"))
        total += base % 1000000007
        checksum = (checksum * 31 + base % 1000000007 + n % 1000) % 1000000007
    print(f"{count} random cases: bases add up to {total} (mod 10^9 + 7 each), checksum {checksum}")


main()
