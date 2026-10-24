# LeetCode #955: Delete Columns to Make Sorted II -- Python mirror of the
# Kara bench program (pairs settled).


def min_deletion_size(strs):
    n = len(strs)
    m = len(strs[0])
    settled = [False] * n
    deleted = 0
    for c in range(m):
        breaks = False
        for i in range(n - 1):
            if not settled[i] and strs[i][c] > strs[i + 1][c]:
                breaks = True
                break
        if breaks:
            deleted += 1
            continue
        for i in range(n - 1):
            if strs[i][c] < strs[i + 1][c]:
                settled[i] = True
    return deleted


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    rounds, count, n, m = 120, 200, 100, 100
    seed = [955]
    sets = []
    for s in range(count):
        letters = 2 + s % 3
        strs = []
        for _ in range(n):
            strs.append("".join(chr(97 + next_random(seed) % letters) for _ in range(m)))
        p = s % 12
        strs.sort(key=lambda w: w[:p])
        sets.append(strs)
    total = 0
    check = 0
    for r in range(rounds):
        for i in range(count):
            k = (r + i) % count
            d = min_deletion_size(sets[k])
            total += d
            check = (check * 31 + d) % 1000000007
    print(f"{rounds} rounds over {count} sets of {n} strings of {m} letters: {total} columns deleted, checksum {check}")


main()
