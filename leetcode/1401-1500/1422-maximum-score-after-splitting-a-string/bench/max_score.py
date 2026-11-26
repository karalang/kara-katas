def max_score(s):
    digits = s.encode()
    ones = digits.count(b"1")
    lead = 0
    best = None
    for d in digits[:-1]:
        lead += 1 if d == 48 else -1
        best = lead if best is None or lead > best else best
    return ones + best


def main():
    seed = 1422
    pool = []
    for _ in range(1000000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        pool.append("0" if seed // 65536 % 2 == 0 else "1")
    text = "".join(pool)
    check = 0
    for _ in range(1000000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        start = seed // 65536 % 999501
        check = (check * 131 + max_score(text[start:start + 500])) % 1000000007
    print(f"10^6 windows of 500 digits: checksum {check}")


main()
