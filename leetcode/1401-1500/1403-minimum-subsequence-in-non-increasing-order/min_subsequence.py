# Mirror of min_subsequence.kara: the largest numbers taken until they
# outweigh the rest.


def min_subsequence(nums):
    order = sorted(nums, reverse=True)
    rest = sum(order)
    taken = 0
    picked = []
    for x in order:
        picked.append(x)
        taken += x
        rest -= x
        if taken > rest:
            break
    return picked


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def drawn(n, hi):
    return [1 + next_random() % hi for _ in range(n)]


def shown(v):
    return "[" + " ".join(str(x) for x in v) + "]"


def main():
    global seed
    print(" ".join(shown(min_subsequence(c)) for c in [
        [4, 3, 10, 9, 8], [4, 4, 7, 6, 7], [6], [1, 1], [3, 1, 1, 1], [5, 5, 5, 5, 5]]))
    seed = 1403
    top = [100] * 500
    ones = [1] * 500
    big = drawn(500, 100)
    picked = min_subsequence(big)
    print(f"500 numbers: {len(min_subsequence(top))} {len(min_subsequence(ones))} {len(picked)}, sum {sum(picked)}")
    check = 0
    taken = 0
    for i in range(2000):
        n = 1 + next_random() % 40
        hi = 100 if i % 2 == 0 else 5
        picked = min_subsequence(drawn(n, hi))
        taken += len(picked)
        for x in picked:
            check = (check * 131 + x) % 1000000007
        check = (check * 131 + len(picked)) % 1000000007
    print(f"2000 random cases: {taken} taken, checksum {check}")


main()
