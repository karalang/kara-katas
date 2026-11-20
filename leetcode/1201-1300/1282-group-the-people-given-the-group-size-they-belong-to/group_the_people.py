# LeetCode #1282: Group the People Given the Group Size They Belong To --
# Python mirror of the ★ arm: one open group per size, handed out when full.


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


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def canonical(groups):
    return sorted((sorted(g) for g in groups), key=lambda g: g[0])


def valid(sizes, groups):
    seen = [False] * len(sizes)
    for g in groups:
        for p in g:
            if p < 0 or p >= len(sizes) or seen[p] or sizes[p] != len(g):
                return False
            seen[p] = True
    return all(seen)


def show(groups):
    return "[" + ",".join("[" + ",".join(str(p) for p in g) + "]" for g in groups) + "]"


def problem(most):
    n = next_random() % most + 1
    sizes = []
    while len(sizes) < n:
        left = n - len(sizes)
        cap = left if next_random() % 4 == 0 else min(left, 8)
        s = next_random() % cap + 1
        sizes.extend([s] * s)
    i = n - 1
    while i > 0:
        j = next_random() % (i + 1)
        sizes[i], sizes[j] = sizes[j], sizes[i]
        i -= 1
    return sizes


def main():
    global seed
    for sizes in [[3, 3, 3, 3, 3, 1, 3], [2, 1, 3, 3, 3, 2], [1, 1, 1], [4, 4, 4, 4]]:
        groups = group_the_people(sizes)
        print(f"{show(canonical(groups))} {'true' if valid(sizes, groups) else 'false'}")
    seed = 1282
    people = count = ok = check = 0
    for _ in range(1000):
        sizes = problem(500)
        people += len(sizes)
        groups = group_the_people(sizes)
        count += len(groups)
        if valid(sizes, groups):
            ok += 1
        for g in canonical(groups):
            for p in g:
                check = (check * 131 + p + 1) % 1000000007
            check = (check * 131 + 7) % 1000000007
    print(f"1000 random problems: {people} people in {count} groups, {ok} valid, checksum {check}")


if __name__ == "__main__":
    main()
