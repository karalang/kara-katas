# LeetCode #415 bench — Python reference (mirror of add_strings.kara).
# Two-pointer column add + digit-table render; sink is the byte-sum of every
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


def add_strings(a, b):
    i, j, carry = len(a) - 1, len(b) - 1, 0
    buf = []
    while i >= 0 or j >= 0 or carry > 0:
        s = carry
        if i >= 0:
            s += ord(a[i]) - 48
            i -= 1
        if j >= 0:
            s += ord(b[j]) - 48
            j -= 1
        buf.append(s % 10)
        carry = s // 10
    return "".join(D[d] for d in reversed(buf))


def main():
    total = 500000
    a = "31415926535897932384626433832795028841"
    parts = []
    for k in range(total):
        v = (k * 2654435761) & 0xFFFFFFFF
        parts.append(add_strings(a, digits_of(v)))
    out = "".join(parts)
    print(sum(ord(c) for c in out))


main()
