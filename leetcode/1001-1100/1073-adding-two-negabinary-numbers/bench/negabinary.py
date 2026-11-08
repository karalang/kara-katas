# LeetCode #1073: Adding Two Negabinary Numbers -- the benchmark's Python
# mirror of negabinary.kara: the same addition from the low end with a
# carry, over 2000 pairs of numbers built once, each added 20 times.


def add_negabinary(a, b):
    i, j, carry = len(a) - 1, len(b) - 1, 0
    digits = []
    while i >= 0 or j >= 0 or carry != 0:
        s = carry
        if i >= 0:
            s += a[i]
            i -= 1
        if j >= 0:
            s += b[j]
            j -= 1
        digits.append(s & 1)
        carry = -(s >> 1)
    while len(digits) > 1 and digits[-1] == 0:
        digits.pop()
    digits.reverse()
    return digits


seed = 1073


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_number(longest):
    n = next_random() % longest + 1
    if n == 1:
        return [next_random() % 2]
    return [1] + [next_random() % 2 for _ in range(n - 1)]


def main():
    pairs = []
    for _ in range(2000):
        a = random_number(1000)
        b = random_number(1000)
        pairs.append((a, b))
    digits = check = 0
    for _ in range(20):
        for a, b in pairs:
            x = add_negabinary(a, b)
            digits += len(x)
            check = (check * 31 + len(x) + x[len(x) // 2]) % 1000000007
    print(f"40000 calls: {digits} digits, checksum {check}")


main()
