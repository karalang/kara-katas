# LeetCode #43 bench — Python reference (mirror of multiply_strings.kara).
# Digit-grid multiply + digit-table render; sink is the byte-sum of every
# rendered result. The interpreted floor (no JIT); confirms the cross-language
# sink independently.
D = "0123456789"


def digits_of(n):
    if n == 0:
        return "0"
    buf = []
    while n > 0:
        buf.append(n % 10)
        n //= 10
    return "".join(D[d] for d in reversed(buf))


def multiply(a, b):
    m, n = len(a), len(b)
    res = [0] * (m + n)
    for i in range(m - 1, -1, -1):
        d1 = ord(a[i]) - 48
        for j in range(n - 1, -1, -1):
            d2 = ord(b[j]) - 48
            lo, hi = i + j + 1, i + j
            s = d1 * d2 + res[lo]
            res[lo] = s % 10
            res[hi] += s // 10
    k = 0
    while k < len(res) and res[k] == 0:
        k += 1
    out = "".join(D[res[t]] for t in range(k, len(res)))
    return out if out else "0"


def main():
    total = 300000
    a = "31415926535897932384626433832795028841"
    parts = []
    for k in range(total):
        v = (k * 2654435761) & 0xFFFFFFFF
        parts.append(multiply(a, digits_of(v)))
    out = "".join(parts)
    print(sum(ord(c) for c in out))


main()
