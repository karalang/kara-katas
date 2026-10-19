# LeetCode 779 — K-th Symbol in Grammar, the ones in k - 1.
# Mirrors kth_symbol_in_grammar.kara (the ★ arm) and its harness.


def kth_grammar(n, k):
    return bin(k - 1).count("1") % 2


seed = 779


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(n, k):
    print(f"n = {n}, k = {k} -> {kth_grammar(n, k)}")


def main():
    show(1, 1)
    show(2, 1)
    show(2, 2)
    show(30, 1)
    show(30, 536870912)
    show(30, 536870911)
    show(30, 268435457)
    for n in range(1, 6):
        row = "".join(str(kth_grammar(n, k)) for k in range(1, (1 << (n - 1)) + 1))
        print(f"row {n}: {row}")
    ones = 0
    check = 0
    for _ in range(1000):
        n = 1 + next_random() % 30
        a = next_random()
        b = next_random()
        k = 1 + (a * 32768 + b) % (1 << (n - 1))
        answer = kth_grammar(n, k)
        ones += answer
        check = (check * 3 + answer + 1) % 1000000007
    print(f"1000 random queries: {ones} ones, checksum {check}")


main()
