# Benchmark: LeetCode #1007 Minimum Domino Rotations For Equal Row -- the
# ★ arm, two candidates, on rows of 20000 dominoes, LeetCode's longest.
# Mirrors min_rotations.kara, .c, .rs and go-seq/.


def rotations(tops, bottoms, v):
    to_top = 0
    to_bottom = 0
    for i in range(len(tops)):
        if tops[i] != v and bottoms[i] != v:
            return -1
        if tops[i] != v:
            to_top += 1
        elif bottoms[i] != v:
            to_bottom += 1
    return min(to_top, to_bottom)


def min_domino_rotations(tops, bottoms):
    a = rotations(tops, bottoms, tops[0])
    b = rotations(tops, bottoms, bottoms[0])
    if a == -1:
        return b
    if b == -1:
        return a
    return min(a, b)


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    rounds = 400
    n = 20000
    seed = [1007]
    all_tops = []
    all_bottoms = []
    for t in range(20):
        target = t % 6 + 1
        tops = []
        bottoms = []
        for _ in range(n):
            top = 1 + next_random(seed) % 6
            bottom = 1 + next_random(seed) % 6
            if t % 2 == 0 or next_random(seed) % 2000 != 0:
                if next_random(seed) % 2 == 0:
                    top = target
                else:
                    bottom = target
            tops.append(top)
            bottoms.append(bottom)
        all_tops.append(tops)
        all_bottoms.append(bottoms)
    total = 0
    check = 0
    for r in range(rounds):
        for i in range(20):
            t = (r + i) % 20
            got = min_domino_rotations(all_tops[t], all_bottoms[t])
            total += got
            check = (check * 31 + got + 2) % 1000000007
    print(f"{rounds} rounds over 20 rows of {n} dominoes: answers sum to {total}, checksum {check}")


main()
