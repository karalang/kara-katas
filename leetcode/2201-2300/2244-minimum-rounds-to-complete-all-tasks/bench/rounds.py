# LeetCode #2244: Minimum Rounds to Complete All Tasks -- the benchmark's
# Python mirror of rounds.kara: the tasks of each difficulty counted in a
# dict; a lone task gives -1, any other count c takes ceil(c / 3)
# rounds, summed.


def minimum_rounds(tasks):
    counts = {}
    for t in tasks:
        counts[t] = counts.get(t, 0) + 1
    rounds = 0
    for c in counts.values():
        if c == 1:
            return -1
        rounds += (c + 2) // 3
    return rounds


seed = 2244


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    high = next_random()
    return high * 32768 + next_random()


def main():
    check = 0
    for _ in range(40):
        kinds = [wide_random() % 1000000000 + 1 for _ in range(30000)]
        tasks = []
        for _ in range(50000):
            t = kinds[wide_random() % 30000]
            tasks.append(t)
            tasks.append(t)
        check = (check * 31 + minimum_rounds(tasks) + 1) % 1000000007
    print(f"40 lists of 100000 tasks: checksum {check}")


main()
