# LeetCode #2234: Maximum Total Beauty of the Gardens -- the mirror of
# beauty.kara: the gardens sorted and capped, every split of complete
# gardens tried, and the level of the rest by a binary search on the
# level.


def maximum_beauty(flowers, new_flowers, target, full, partial):
    s = sorted(min(f, target) for f in flowers)
    n = len(s)
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + s[i]
    best = 0
    cost = 0
    c = n
    while c >= 0:
        if c < n:
            cost += target - s[c]
        if cost > new_flowers:
            break
        complete = (n - c) * full
        if c == 0:
            best = max(best, complete)
        elif s[c - 1] < target:
            left = new_flowers - cost
            low, high = s[0], target - 1
            while low < high:
                m = (low + high + 1) // 2
                a, b = 0, c
                while a < b:
                    mid = (a + b) // 2
                    if s[mid] < m:
                        a = mid + 1
                    else:
                        b = mid
                if m * a - prefix[a] <= left:
                    low = m
                else:
                    high = m - 1
            best = max(best, complete + low * partial)
        c -= 1
    return best


seed = 2234


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    high = next_random()
    return high * 32768 + next_random()


def show(flowers, new_flowers, target, full, partial):
    print(f"[{', '.join(map(str, flowers))}], new {new_flowers}, target {target}, full {full}, partial {partial} -> {maximum_beauty(flowers, new_flowers, target, full, partial)}")


def main():
    show([1, 3, 1, 1], 7, 6, 12, 1)
    show([2, 4, 5, 3], 10, 5, 2, 6)
    show([5, 5, 5], 1, 5, 3, 9)
    show([4], 3, 10, 7, 2)
    show([1, 1], 10000000000, 10, 1, 100)
    show([1, 2, 3], 3, 4, 100000, 1)
    show([20, 1, 15, 2], 6, 10, 5, 3)
    check = 0
    for c in range(3000):
        n = next_random() % 20 + 1
        top = [10, 1000, 100000][c % 3]
        flowers = [wide_random() % top + 1 for _ in range(n)]
        target = wide_random() % top + 1
        new_flowers = wide_random() % (3 * top * n) + 1
        full = wide_random() % 100000 + 1
        partial = wide_random() % 100000 + 1
        check = (check * 31 + maximum_beauty(flowers, new_flowers, target, full, partial)) % 1000000007
    print(f"3000 cases: checksum {check}")
    flowers = [wide_random() % 100000 + 1 for _ in range(100000)]
    for new_flowers in [10000000000, 1000000000, 100000]:
        print(f"10^5 gardens, new {new_flowers}: {maximum_beauty(flowers, new_flowers, 100000, 100000, 100000)}")


main()
