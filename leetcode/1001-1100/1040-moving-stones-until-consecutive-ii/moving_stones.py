# LeetCode #1040: Moving Stones Until Consecutive II -- Python mirror of
# moving_stones.kara (sorted, then a sliding window); same harness, same
# output.


def moves(stones):
    s = sorted(stones)
    n = len(s)
    most = max(s[n - 1] - s[1] - n + 2, s[n - 2] - s[0] - n + 2)
    least = n
    i = 0
    for j in range(n):
        while s[j] - s[i] >= n:
            i += 1
        inside = j - i + 1
        if inside == n - 1 and s[j] - s[i] == n - 2:
            least = min(least, 2)
        else:
            least = min(least, n - inside)
    return least, most


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_stones(count, top):
    taken = set()
    out = []
    while len(out) < count:
        a = next_random()
        b = next_random()
        x = (a * 32768 + b) % top + 1
        if x not in taken:
            taken.add(x)
            out.append(x)
    return out


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    global seed
    examples = [
        [7, 4, 9],
        [6, 5, 4, 3, 10],
        [100, 101, 104, 102, 103],
        [1, 2, 5],
        [1, 3, 5, 7, 9],
        [1, 2, 3, 4, 10],
        [1, 1000000000, 500000000],
        [8, 7, 6, 5, 4, 3, 2, 1, 100, 200],
    ]
    for stones in examples:
        least, most = moves(stones)
        print(f"{show(stones)} -> [{least}, {most}]")
    for size in range(3, 13):
        sets = 0
        total = 0
        check = 0
        for mask in range(4096):
            stones = [b + 1 for b in range(12) if (mask >> b) & 1 == 1]
            if len(stones) == size:
                least, most = moves(stones)
                sets += 1
                total += least * 100 + most
                check = (check * 131 + least * 1000 + most) % 1000000007
        print(f"all {sets} sets of {size} stones from 1 to 12: total {total}, checksum {check}")
    seed = 1040
    for label, spread in [("wide", 0), ("packed", 2)]:
        total = 0
        check = 0
        for _ in range(300):
            count = next_random() % 198 + 3
            top = 1000000000 if spread == 0 else count * spread
            stones = random_stones(count, top)
            least, most = moves(stones)
            total += least + most
            check = (check * 131 + least * 1000003 + most) % 1000000007
        print(f"300 {label} random sets: total {total}, checksum {check}")
    wide = random_stones(2000, 1000000000)
    a, b = moves(wide)
    print(f"2000 wide: [{a}, {b}]")
    packed = list(range(1, 2000)) + [3000]
    c, d = moves(packed)
    print(f"1 to 1999 and 3000: [{c}, {d}]")


main()
