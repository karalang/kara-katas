# LeetCode #386: Lexicographical Numbers -- step to the next number.
# Mirrors lexical_order.kara.


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


def show(n):
    v = lexical_order(n)
    print(f"n = {n}: [{', '.join(str(x) for x in v)}]")


def summary(n):
    v = lexical_order(n)
    seen = [False] * (n + 1)
    ok = len(v) == n
    checksum = 0
    for i, x in enumerate(v):
        if x < 1 or x > n or seen[x]:
            ok = False
        else:
            seen[x] = True
        if i > 0 and not str(v[i - 1]) < str(x):
            ok = False
        checksum = (checksum * 31 + x) % 1000000007
    last = v[-1] if v else 0
    return f"n = {n}: {len(v)} numbers, last {last}, in order {'true' if ok else 'false'}, checksum {checksum}"


def main():
    for n in [13, 2, 1, 9, 10, 21, 100]:
        show(n)
    for n in [99, 101, 199, 999, 1000, 4321, 9999, 10000, 50000]:
        print(summary(n))


main()
