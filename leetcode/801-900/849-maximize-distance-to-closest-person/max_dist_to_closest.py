# LeetCode #849: Maximize Distance to Closest Person -- Python mirror of the ★ arm and its harness.


def max_dist_to_closest(seats):
    n = len(seats)
    last = -1
    best = 0
    for i in range(n):
        if seats[i] == 1:
            if last < 0:
                best = i
            else:
                best = max(best, (i - last) // 2)
            last = i
    return max(best, n - 1 - last)


def show(seats):
    print(f"{seats} -> {max_dist_to_closest(seats)}")


seed = 849


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    for s in [[1, 0, 0, 0, 1, 0, 1], [1, 0, 0, 0], [0, 1], [1, 0], [0, 0, 1], [1, 0, 1],
              [1, 0, 0, 1], [1, 0, 0, 0, 0, 1], [0, 0, 1, 0, 0, 0, 0, 1, 0], [0, 1, 1, 1, 0],
              [1, 1, 0, 1, 1], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1]]:
        show(s)
    n = 20000
    first = [0] * n
    first[0] = 1
    print(f"one person at the front of 20000: {max_dist_to_closest(first)}")
    middle = [0] * n
    middle[n // 2] = 1
    print(f"one person in the middle: {max_dist_to_closest(middle)}")
    ends = [0] * n
    ends[0] = 1
    ends[n - 1] = 1
    print(f"people at both ends: {max_dist_to_closest(ends)}")
    print(f"every other seat: {max_dist_to_closest([i % 2 for i in range(n)])}")
    sparse = [1 if next_random() % 500 == 0 else 0 for _ in range(n)]
    sparse[n - 1] = 1
    print(f"about one in 500 seats taken: {max_dist_to_closest(sparse)}")
    total = 0
    check = 0
    for _ in range(600):
        n = 2 + next_random() % 30
        density = 1 + next_random() % 6
        seats = [1 if next_random() % 8 < density else 0 for _ in range(n)]
        taken = next_random() % n
        empty = (taken + 1 + next_random() % (n - 1)) % n
        seats[taken] = 1
        seats[empty] = 0
        d = max_dist_to_closest(seats)
        total += d
        check = (check * 31 + d) % 1000000007
    print(f"600 random rows: distances sum to {total}, checksum {check}")


main()
