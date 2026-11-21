# LeetCode #2418: Sort the People -- the Python mirror of the ★ arm: the
# indexes sorted by height, tallest first, each index's name read out.

seed = 0


def sort_people(names, heights):
    order = list(range(len(names)))
    order.sort(key=lambda i: -heights[i])
    return [names[i] for i in order]


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_people(n, longest, kinds, top):
    names = []
    for _ in range(n):
        length = 1 + next_random() % longest
        b = []
        for _ in range(length):
            base = 97 if next_random() % 2 == 0 else 65
            b.append(chr(base + next_random() % kinds))
        names.append("".join(b))
    pool = list(range(1, top + 1))
    for i in range(n):
        j = i + (next_random() * 32768 + next_random()) % (top - i)
        pool[i], pool[j] = pool[j], pool[i]
    return names, pool[:n]


def show(names):
    return "[" + ",".join(names) + "]"


def digest(names):
    h = 0
    for name in names:
        for b in name.encode():
            h = (h * 31 + b) % 1000000007
        h = (h * 31 + 1) % 1000000007
    return h


def main():
    global seed
    print(show(sort_people(["Mary", "John", "Emma"], [180, 165, 170])))
    print(show(sort_people(["Alice", "Bob", "Bob"], [155, 185, 150])))
    print(show(sort_people(["Zed"], [100000])))
    print(show(sort_people(["c", "b", "a"], [3, 2, 1])))
    print(show(sort_people(["a", "b", "c", "d"], [1, 2, 3, 4])))
    seed = 2418
    names, heights = random_people(1000, 20, 26, 100000)
    print(digest(sort_people(names, heights)))
    check = 0
    for _ in range(2000):
        n = 1 + next_random() % 10
        top = n + next_random() % 21
        names, heights = random_people(n, 3, 2, top)
        check = (check * 31 + digest(sort_people(names, heights))) % 1000000007
    print(f"2000 random: checksum {check}")


if __name__ == "__main__":
    main()
