# LeetCode #2234: Maximum Total Beauty of the Gardens -- the benchmark's
# Python mirror of beauty.kara: every split of complete gardens tried,
# the level of the rest by a binary search on the level.


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


def main():
    flowers = [wide_random() % 100000 + 1 for _ in range(20000)]
    check = 0
    for _ in range(20):
        # punch: one garden drawn again before each pass, and the new
        # flowers drawn anew
        at = next_random() % 20000
        flowers[at] = wide_random() % 100000 + 1
        new_flowers = wide_random() % 1200000000 + 1
        check = (check * 31 + maximum_beauty(flowers, new_flowers, 100000, 100000, 100000)) % 1000000007
    print(f"20 passes over 20000 gardens: checksum {check}")


main()
