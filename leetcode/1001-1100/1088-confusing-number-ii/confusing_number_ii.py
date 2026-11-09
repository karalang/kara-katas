# LeetCode #1088: Confusing Number II -- mirrors confusing_number_ii.kara:
# a depth-first walk over the numbers made of the digits that rotate, each
# carrying its rotation, counting those that differ from it.
import sys

sys.setrecursionlimit(10000)

ROTATED = {0: 0, 1: 1, 6: 9, 8: 8, 9: 6}


def count_from(num, rot, unit, n):
    total = 0
    for d in (0, 1, 6, 8, 9):
        nxt = num * 10 + d
        if nxt > n:
            break
        if nxt == 0:
            continue
        r = ROTATED[d] * unit + rot
        if nxt != r:
            total += 1
        total += count_from(nxt, r, unit * 10, n)
    return total


def confusing_number_ii(n):
    return count_from(0, 0, 1, n)


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    global seed
    cases = [1, 6, 9, 10, 20, 100, 1000, 6969, 10000, 68986, 123456, 1000000]
    for n in cases:
        print(f"{n} -> {confusing_number_ii(n)}")
    small = sum(confusing_number_ii(n) for n in range(1, 1001))
    print(f"n = 1 to 1000: answers sum to {small}")
    seed = 1088
    h = 0
    for _ in range(200):
        digits = next_random() % 6
        n = 1
        for _ in range(digits):
            n *= 10
        hi = next_random() * 32768 + next_random()
        n = hi % n + 1
        h = (h * 31 + confusing_number_ii(n)) % 1000000007
    print(f"200 random n: checksum {h}")


main()
