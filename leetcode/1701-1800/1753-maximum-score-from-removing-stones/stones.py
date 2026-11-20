# LeetCode #1753: Maximum Score From Removing Stones -- mirrors stones.kara
# (the ★ arm): a closed form.


def maximum_score(a, b, c):
    total = a + b + c
    return min(total // 2, total - max(a, b, c))


seed = 1753


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    high = next_random()
    return high * 32768 + next_random()


def batch(count, most):
    total = 0
    check = 0
    for _ in range(count):
        a = wide() % most + 1
        b = wide() % most + 1
        c = wide() % most + 1
        answer = maximum_score(a, b, c)
        total += answer
        check = (check * 31 + answer + a) % 1000000007
    print(f"{count} sets of piles of up to {most}: scores add to {total}, checksum {check}")


for piles in [(2, 4, 6), (4, 4, 6), (1, 8, 8), (1, 1, 1), (1, 2, 100000), (100000, 100000, 100000)]:
    print(maximum_score(*piles))
batch(3000, 6)
batch(3000, 1000)
batch(300, 100000)
