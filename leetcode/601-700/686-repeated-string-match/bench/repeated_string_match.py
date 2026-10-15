# LeetCode #686: Repeated String Match -- Knuth-Morris-Pratt. Bench.
#
# 100 pairs are built once: `a` of 1,000 to 10,000 letters over two
# letters, and `b` of 10,000 cut from the repetition of `a`, half of
# them with the last letter changed. Then 30 rounds answer every pair.


def repeated_string_match(a, b):
    x = a.encode()
    y = b.encode()
    n = len(x)
    m = len(y)
    fail = [0] * m
    k = 0
    for i in range(1, m):
        while k > 0 and y[i] != y[k]:
            k = fail[k - 1]
        if y[i] == y[k]:
            k += 1
        fail[i] = k
    j = 0
    for i in range(n + m):
        c = x[i % n]
        while j > 0 and c != y[j]:
            j = fail[j - 1]
        if c == y[j]:
            j += 1
        if j == m:
            return (i + 1 + n - 1) // n
    return -1


seed = 686


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count = 100
    rounds = 30
    m = 10000
    firsts = []
    seconds = []
    for c in range(count):
        n = 1000 + next_random() % 9001
        a = bytearray(97 + next_random() % 2 for _ in range(n))
        start = next_random() % n
        b = bytearray(a[(start + i) % n] for i in range(m))
        if c % 2 == 1:
            b[m - 1] = 196 - b[m - 1]
        firsts.append(a.decode())
        seconds.append(b.decode())
    total = 0
    none = 0
    for r in range(rounds):
        for c in range(count):
            k = repeated_string_match(firsts[c], seconds[c])
            if k == -1:
                none += 1
            total = (total * 31 + k + r + 2) % 1000000007
    print(f"{count * rounds} pairs answered: {none} with no answer, checksum {total}")


main()
