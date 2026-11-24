# LeetCode #1304: Find N Unique Integers Sum up to Zero -- the Python mirror
# of the ★ arm (the pairs i and -i, and 0 when n is odd), with the same
# harness.


def sum_zero(n):
    out = []
    for i in range(1, n // 2 + 1):
        out.append(i)
        out.append(-i)
    if n % 2 == 1:
        out.append(0)
    return out


def valid(n, got):
    if len(got) != n:
        return False
    s = sorted(got)
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            return False
    return sum(s) == 0


def main():
    line = []
    for n in [5, 3, 1]:
        line.append(f"{n}:{'ok' if valid(n, sum_zero(n)) else 'WRONG'}")
    print(" ".join(line))
    good = 0
    total = 0
    for n in range(1, 1001):
        got = sum_zero(n)
        if valid(n, got):
            good += 1
        total += len(got)
    print(f"1000 sizes: {good} valid, numbers total {total}")


main()
