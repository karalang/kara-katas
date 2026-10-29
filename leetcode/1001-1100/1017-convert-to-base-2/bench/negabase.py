# LeetCode #1017: Convert to Base -2 -- bench
# Mirrors negabase.kara; see ../README.md § Benchmarks.


def base_neg2(n):
    if n == 0:
        return "0"
    rest = n
    digits = []
    while rest != 0:
        bit = rest & 1
        digits.append("1" if bit == 1 else "0")
        rest = (rest - bit) // -2
    return "".join(reversed(digits))


def main():
    most = 3000000
    digits = 0
    check = 0
    for n in range(most + 1):
        form = base_neg2(n)
        digits += len(form)
        for ch in form:
            check = (check * 3 + (2 if ch == "1" else 1)) % 1000000007
        check = (check * 3) % 1000000007
    print(f"n = 0..{most}: {digits} digits, checksum {check}")


main()
