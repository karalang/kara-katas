# Benchmark for #402: mirror of remove_k_digits.kara (a stack that keeps
# digits rising).


def remove_kdigits(num, k):
    left = k
    stack = []
    for c in num.encode():
        while left > 0 and stack and stack[-1] > c:
            stack.pop()
            left -= 1
        stack.append(c)
    while left > 0:
        stack.pop()
        left -= 1
    out = []
    for c in stack:
        if not out and c == 48:
            continue
        out.append(chr(c))
    if not out:
        out.append("0")
    return "".join(out)


def main():
    numbers = 300
    n = 100000
    seed = 402
    kept = 0
    checksum = 0
    for _ in range(numbers):
        seed = (seed * 1103515245 + 12345) % 2147483648
        num = [chr(49 + seed // 65536 % 9)]
        for _ in range(1, n):
            seed = (seed * 1103515245 + 12345) % 2147483648
            num.append(chr(48 + seed // 65536 % 10))
        seed = (seed * 1103515245 + 12345) % 2147483648
        k = seed // 65536 % (n + 1)
        r = remove_kdigits("".join(num), k)
        kept += len(r)
        for b in r.encode():
            checksum = (checksum * 31 + b) % 1000000007
    print(f"{numbers} numbers of {n} digits: {kept} digits kept, checksum {checksum}")


main()
