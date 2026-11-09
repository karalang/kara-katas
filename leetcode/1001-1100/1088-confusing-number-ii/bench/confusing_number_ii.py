# Benchmark: LeetCode #1088 Confusing Number II -- mirrors
# confusing_number_ii.kara: a depth-first walk over the numbers made of the
# digits that rotate, each carrying its rotation, for 400 random n up to
# 10^9 drawn once.
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


seed = 1088


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    ns = []
    for _ in range(400):
        a = next_random()
        hi = a * 32768 + next_random()
        ns.append(hi % 1000000000 + 1)
    total = 0
    check = 0
    for n in ns:
        a = confusing_number_ii(n)
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"400 n up to 10^9: {total} confusing numbers, checksum {check}")


main()
