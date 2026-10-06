# Mirror of differential.kara: schoolbook vs add-shift multiplication on 400 random digit strings.
def multiply(a, b):
    x = [int(c) for c in reversed(a)]
    y = [int(c) for c in reversed(b)]
    acc = [0] * (len(x) + len(y))
    for i in range(len(x)):
        for j in range(len(y)):
            acc[i + j] += x[i] * y[j]
    carry = 0
    for k in range(len(acc)):
        t = acc[k] + carry
        acc[k] = t % 10
        carry = t // 10
    while len(acc) > 1 and acc[-1] == 0:
        acc.pop()
    return ''.join(str(d) for d in reversed(acc))

def add(a, b):
    i, j, carry, rev = len(a) - 1, len(b) - 1, 0, []
    while i >= 0 or j >= 0 or carry > 0:
        t = (int(a[i]) if i >= 0 else 0) + (int(b[j]) if j >= 0 else 0) + carry
        rev.append(str(t % 10))
        carry = t // 10
        i -= 1
        j -= 1
    return ''.join(reversed(rev))

def times_digit(a, d, shift):
    if d == 0:
        return "0"
    acc = "0"
    for _ in range(d):
        acc = add(acc, a)
    return acc + "0" * shift

def multiply2(a, b):
    total = "0"
    for k, c in enumerate(b):
        total = add(total, times_digit(a, int(c), len(b) - 1 - k))
    k = 0
    while k + 1 < len(total) and total[k] == '0':
        k += 1
    return total[k:]

seed, fails, checksum = 4242, 0, 0
for t in range(400):
    seed = (seed * 1103515245 + 12345) % 2147483648
    la = 1 + seed % 18
    seed = (seed * 1103515245 + 12345) % 2147483648
    lb = 1 + seed % 18
    a, b = [], []
    for i in range(la):
        seed = (seed * 1103515245 + 12345) % 2147483648
        a.append(str(1 + (seed // 16) % 9 if i == 0 and la > 1 else (seed // 16) % 10))
    for i in range(lb):
        seed = (seed * 1103515245 + 12345) % 2147483648
        b.append(str(1 + (seed // 16) % 9 if i == 0 and lb > 1 else (seed // 16) % 10))
    a, b = ''.join(a), ''.join(b)
    p, q = multiply(a, b), multiply2(a, b)
    if p != q:
        fails += 1
        print(f"mismatch {t}: {a} * {b}: {p} vs {q}")
    for c in p:
        checksum = (checksum * 17 + ord(c) + t) % 1000000007
print(f"400 products, failures {fails}, checksum {checksum}")
