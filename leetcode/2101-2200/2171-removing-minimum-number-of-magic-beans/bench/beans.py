# LeetCode #2171: Removing Minimum Number of Magic Beans -- the
# benchmark's Python mirror of beans.kara.


def minimum_removal(beans):
    s = sorted(beans)
    n = len(s)
    total = 0
    kept = 0
    for i in range(n):
        total += s[i]
        kept = max(kept, s[i] * (n - i))
    return total - kept


seed = 2171


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    row = []
    for _ in range(400000):
        row.append((next_random() * 32768 + next_random()) % 100000 + 1)
    check = 0
    for _ in range(100):
        start = (next_random() * 32768 + next_random()) % 300001
        removed = minimum_removal(row[start:start + 100000])
        check = (check * 31 + removed % 1000000007) % 1000000007
    print(f"100 solves: checksum {check}")


main()
