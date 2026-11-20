# LeetCode #1276: Number of Burgers with No Waste of Ingredients -- Python
# mirror of the ★ arm: by algebra.


def num_of_burgers(tomato_slices, cheese_slices):
    if tomato_slices % 2 != 0:
        return []
    jumbo = tomato_slices // 2 - cheese_slices
    small = 2 * cheese_slices - tomato_slices // 2
    if jumbo < 0 or small < 0:
        return []
    return [jumbo, small]


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    global seed
    print(f"{num_of_burgers(16, 7)} {num_of_burgers(17, 4)} {num_of_burgers(4, 17)} {num_of_burgers(0, 0)} {num_of_burgers(2, 1)}")
    seed = 1276
    made = 0
    check = 0
    for case in range(3000):
        big = next_random() % 2 == 0
        span = 2500000 if big else 30
        jumbo = next_random() % span
        small = next_random() % span
        if case % 3 == 0:
            t, c = 4 * jumbo + 2 * small, jumbo + small
        elif case % 3 == 1:
            t = 4 * jumbo + 2 * small + next_random() % 5 - 2
            c = jumbo + small + next_random() % 3 - 1
        else:
            t = next_random() % (4 * span)
            c = next_random() % (2 * span)
        t, c = max(t, 0), max(c, 0)
        answer = num_of_burgers(t, c)
        if len(answer) == 2:
            made += 1
            check = (check * 131 + answer[0] * 7 + answer[1]) % 1000000007
        else:
            check = (check * 131 + len(answer) + 1) % 1000000007
    print(f"3000 random cases: {made} with burgers, checksum {check}")
    print(f"{num_of_burgers(10000000, 2500000)} {num_of_burgers(10000000, 5000000)} {num_of_burgers(10000000, 3000000)} {num_of_burgers(10000000, 10000000)} {num_of_burgers(9999999, 3000000)}")


main()
