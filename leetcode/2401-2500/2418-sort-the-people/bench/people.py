# LeetCode #2418: Sort the People -- the bench, the ★ arm in Python: the
# indexes sorted by height, tallest first, and each index's name read out.


def sort_people(names, heights):
    order = list(range(len(names)))
    order.sort(key=lambda i: -heights[i])
    return [names[i] for i in order]


seed = 2418


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 10 groups of 1000 people, names of 1 to 20 letters, distinct heights
    # up to 10^5; each pass sorts every group and folds the first letter
    # of every name, plus the pass
    groups = []
    for _ in range(10):
        names = []
        for _ in range(1000):
            n = 1 + next_random() % 20
            names.append("".join(chr(97 + next_random() % 26) for _ in range(n)))
        pool = list(range(1, 100001))
        for i in range(1000):
            a = next_random()
            j = i + (a * 32768 + next_random()) % (100000 - i)
            pool[i], pool[j] = pool[j], pool[i]
        groups.append((names, pool[:1000]))
    check = 0
    for p in range(500):
        for names, heights in groups:
            for name in sort_people(names, heights):
                check = (check * 31 + ord(name[0]) + p) % 1000000007
    print(f"500 passes over 10 groups of 1000 people: checksum {check}")


main()
