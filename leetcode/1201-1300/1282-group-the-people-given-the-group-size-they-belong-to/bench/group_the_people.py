# LeetCode #1282 bench, in Python: the ★ arm (one open group per size, handed
# out when full) on 50 problems of 10000 people, built once, 500 rounds,
# every group folded into a checksum.


def group_the_people(group_sizes):
    n = len(group_sizes)
    open_ = [[] for _ in range(n + 1)]
    groups = []
    for person, size in enumerate(group_sizes):
        open_[size].append(person)
        if len(open_[size]) == size:
            groups.append(list(open_[size]))
            open_[size].clear()
    return groups


seed = 1282


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def problem(n):
    sizes = []
    while len(sizes) < n:
        left = n - len(sizes)
        cap = min(left, 1000) if next_random() % 4 == 0 else min(left, 8)
        s = next_random() % cap + 1
        sizes.extend([s] * s)
    i = n - 1
    while i > 0:
        j = next_random() % (i + 1)
        sizes[i], sizes[j] = sizes[j], sizes[i]
        i -= 1
    return sizes


def main():
    problems = [problem(10000) for _ in range(50)]
    check = 0
    for rnd in range(500):
        for sizes in problems:
            for g in group_the_people(sizes):
                for p in g:
                    check = (check * 131 + p + rnd) % 1000000007
                check = (check * 131 + 7) % 1000000007
    print(f"500 rounds of 50 problems of 10000 people: checksum {check}")


if __name__ == "__main__":
    main()
