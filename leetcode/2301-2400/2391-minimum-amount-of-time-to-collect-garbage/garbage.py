# LeetCode #2391: Minimum Amount of Time to Collect Garbage -- a Python
# mirror of the ★ arm: the units counted once, and each truck's travel the
# prefix sum up to the last house holding its kind. Prints the same
# output as garbage.kara.

seed = 0


def garbage_collection(garbage, travel):
    minutes = 0
    last = [0, 0, 0]
    for i, house in enumerate(garbage):
        for c in house:
            minutes += 1
            last["MPG".index(c)] = i
    prefix = [0]
    for t in travel:
        prefix.append(prefix[-1] + t)
    for kind in range(3):
        minutes += prefix[last[kind]]
    return minutes


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def houses(n, longest, kinds):
    out = []
    for _ in range(n):
        length = 1 + next_random() % longest
        out.append("".join("MPG"[next_random() % kinds] for _ in range(length)))
    return out


def main():
    global seed
    print(garbage_collection(["G", "P", "GP", "GG"], [2, 4, 3]))
    print(garbage_collection(["MMM", "PGM", "GP"], [3, 10]))
    print(garbage_collection(["MPG"], []))
    print(garbage_collection(["GGG", "M", "M"], [5, 7]))
    seed = 2391
    n = 100000
    street = houses(n, 10, 3)
    travel = [1 + next_random() % 100 for _ in range(1, n)]
    glass = ["G"] * n
    glass[0] = "MPG"
    print(f"10^5 houses: {garbage_collection(street, travel)}, {garbage_collection(glass, travel)}")
    check = 0
    largest = 0
    for _ in range(3000):
        n = 1 + next_random() % 30
        kinds = 1 + next_random() % 3
        street = houses(n, 1 + next_random() % 10, kinds)
        travel = [1 + next_random() % 100 for _ in range(1, n)]
        t = garbage_collection(street, travel)
        check = (check * 31 + t) % 1000000007
        largest = max(largest, t)
    print(f"3000 streets: checksum {check}, the longest {largest} minutes")


if __name__ == "__main__":
    main()
