# LeetCode #2171: Removing Minimum Number of Magic Beans -- the Python
# mirror of beans.kara: the bags sorted, each tried as the smallest left.


def minimum_removal(beans):
    s = sorted(beans)
    n = len(s)
    total = 0
    kept = 0
    for i in range(n):
        total += s[i]
        kept = max(kept, s[i] * (n - i))
    return total - kept


# ---- test harness ---------------------------------------------------------

seed = 2171


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(beans):
    print(f"[{', '.join(str(b) for b in beans)}] -> {minimum_removal(beans)}")


def main():
    show([4, 1, 6, 5])
    show([2, 10, 3, 2])
    show([7])
    show([3, 3, 3, 3])
    show([1, 1, 1, 100000])
    show([1, 2, 3, 4, 5, 6, 7, 8])
    total = 0
    check = 0
    for rnd in range(2000):
        top = [10, 1000, 100000][rnd % 3]
        length = next_random() % 20 + 1
        beans = []
        for _ in range(length):
            beans.append((next_random() * 32768 + next_random()) % top + 1)
        removed = minimum_removal(beans)
        total += removed
        check = (check * 31 + removed % 1000000007) % 1000000007
    print(f"2000 rows: {total} in all, checksum {check}")
    wide = []
    for _ in range(100000):
        wide.append((next_random() * 32768 + next_random()) % 100000 + 1)
    full = [100000] * 100000
    full[0] = 1
    print(f"100000 bags: {minimum_removal(wide)} {minimum_removal(full)}")


main()
