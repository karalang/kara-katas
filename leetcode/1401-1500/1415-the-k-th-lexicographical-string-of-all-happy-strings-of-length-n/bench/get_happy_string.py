# LeetCode #1415 bench, Python: the first letter from (k - 1) / 2^(n - 1),
# and each letter after it the lower or the higher of the two that differ
# from the one before, workload and checksum as get_happy_string.kara.


def get_happy_string(n, k):
    per_first = 1 << (n - 1)
    if k > 3 * per_first:
        return ""
    letters = "abc"
    rest = k - 1
    last = letters[rest // per_first]
    rest %= per_first
    s = [last]
    bit = per_first // 2
    while bit > 0:
        options = [c for c in letters if c != last]
        last = options[1 if rest >= bit else 0]
        if rest >= bit:
            rest -= bit
        s.append(last)
        bit //= 2
    return "".join(s)


def main():
    seed = 1415
    check = 0
    for _ in range(1000000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        n = 1 + seed // 65536 % 10
        k = 1 + seed // 1024 % 100
        s = get_happy_string(n, k)
        total = 0
        for b in s.encode():
            total = total * 3 + b
        check = (check * 131 + total + len(s)) % 1000000007
    print(f"10^6 cases: checksum {check}")


main()
