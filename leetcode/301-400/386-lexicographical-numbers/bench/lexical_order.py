# Benchmark for #386: mirror of lexical_order.kara (step to the next number).


def lexical_order(n):
    out = []
    cur = 1
    for _ in range(n):
        out.append(cur)
        if cur * 10 <= n:
            cur *= 10
        else:
            while cur % 10 == 9 or cur + 1 > n:
                cur //= 10
            cur += 1
    return out


def main():
    checksum = 0
    for q in range(6000):
        v = lexical_order(50000 - q % 1000)
        total = 0
        for k in range(len(v)):
            total += v[k] * (k + 1)
        checksum = (checksum * 31 + total) % 1000000007
    print(f"6000 lists, checksum {checksum}")


main()
