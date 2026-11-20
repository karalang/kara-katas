# LeetCode #1276 bench, in Python: the ★ arm (by algebra) on 100,000 random
# pairs of tomato and cheese slice counts up to 10^7, a third made from
# burgers and a third near such a count, drawn once; 1000 rounds, every
# answer folded into a checksum.


def num_of_burgers(tomato_slices, cheese_slices):
    if tomato_slices % 2 != 0:
        return []
    jumbo = tomato_slices // 2 - cheese_slices
    small = 2 * cheese_slices - tomato_slices // 2
    if jumbo < 0 or small < 0:
        return []
    return [jumbo, small]


seed = 1276


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    cases = []
    for case in range(100000):
        jumbo = next_random() % 2500000
        small = next_random() % 2500000
        if case % 3 == 0:
            t, c = 4 * jumbo + 2 * small, jumbo + small
        elif case % 3 == 1:
            t = 4 * jumbo + 2 * small + next_random() % 5 - 2
            c = jumbo + small + next_random() % 3 - 1
        else:
            t = next_random() % 10000001
            c = next_random() % 5000001
        cases.append((max(t, 0), max(c, 0)))
    check = 0
    for rnd in range(1000):
        for t, c in cases:
            answer = num_of_burgers(t + rnd, c)
            if len(answer) == 2:
                check = (check * 131 + answer[0] * 7 + answer[1]) % 1000000007
            else:
                check = (check * 131 + 1) % 1000000007
    print(f"1000 rounds of 100000 pairs: checksum {check}")


main()
