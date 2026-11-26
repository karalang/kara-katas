def max_diff(num):
    s = str(num)
    c = next((c for c in s if c != '9'), None)
    high = s.replace(c, '9') if c is not None else s
    first = s[0]
    if first != '1':
        low = s.replace(first, '1')
    else:
        c = next((c for c in s[1:] if c != '0' and c != '1'), None)
        low = s.replace(c, '0') if c is not None else s
    return int(high) - int(low)


def main():
    seed = 1432
    check = 0
    for _ in range(3000000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        high = seed // 65536
        seed = (seed * 1103515245 + 12345) % 2147483648
        num = 1 + (high * 32768 + seed // 65536) % 100000000
        check = (check * 131 + max_diff(num)) % 1000000007
    print(f"3 * 10^6 numbers: checksum {check}")


main()
