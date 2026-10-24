# LeetCode #991: Broken Calculator -- mirror of the ★ arm
# (broken_calc.kara), greedy from the target back to the start.


def broken_calc(start_value, target):
    ops = 0
    t = target
    while t > start_value:
        if t % 2 == 1:
            t += 1
        else:
            t //= 2
        ops += 1
    return ops + start_value - t


seed = 991


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    cases = [
        (2, 3), (5, 8), (3, 10),
        (1, 1), (10, 1), (1, 1000000000), (1000000000, 1),
        (1000000000, 1000000000), (7, 1000000000), (999999999, 1000000000),
        (3, 1024), (1, 536870913),
    ]
    for s, t in cases:
        print(f"startValue = {s}, target = {t} -> {broken_calc(s, t)}")
    for count, most_s, most_t in [(300, 20, 20), (3000, 1000, 1000), (3000, 1000000000, 1000000000), (300, 1000, 1000000000)]:
        total = 0
        check = 0
        for _ in range(count):
            s = 1 + (next_random() * 32768 + next_random()) % most_s
            t = 1 + (next_random() * 32768 + next_random()) % most_t
            got = broken_calc(s, t)
            total += got
            check = (check * 31 + got + 1) % 1000000007
        print(f"{count} random pairs, start up to {most_s}, target up to {most_t}: {total} operations, checksum {check}")


main()
