# LeetCode #936: Stamping The Sequence -- bench: stamps peeled off in
# reverse. Mirrors moves_to_stamp.kara, .c, .rs and go-seq/.


def moves_to_stamp(stamp, target):
    s = stamp
    t = list(target)
    m = len(s)
    n = len(t)
    erased = 0
    order = []
    progress = True
    while progress and erased < n:
        progress = False
        for p in range(n - m + 1):
            fits = True
            fresh = False
            for k in range(m):
                if t[p + k] == s[k]:
                    fresh = True
                elif t[p + k] != "?":
                    fits = False
            if fits and fresh:
                for k in range(m):
                    if t[p + k] != "?":
                        t[p + k] = "?"
                        erased += 1
                order.append(p)
                progress = True
    if erased < n:
        return []
    order.reverse()
    return order


seed = 936


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds = 100
    count = 50
    n = 1000
    stamps = []
    targets = []
    for c in range(count):
        m = 5 + next_random() % 16
        s = [chr(97 + next_random() % 3) for _ in range(m)]
        out = ["?"] * n
        left = n
        while left > 0:
            p = next_random() % (n - m + 1)
            for k in range(m):
                if out[p + k] == "?":
                    left -= 1
                out[p + k] = s[k]
        if c % 2 == 1:
            at = next_random() % n
            out[at] = chr(97 + next_random() % 3)
        stamps.append("".join(s))
        targets.append("".join(out))
    stamped = 0
    turns = 0
    check = 0
    for r in range(rounds):
        for i in range(count):
            c = (r + i) % count
            moves = moves_to_stamp(stamps[c], targets[c])
            if len(moves) > 0:
                stamped += 1
            turns += len(moves)
            for p in moves:
                check = (check * 1000003 + p + 1) % 1000000007
    print(f"{rounds} rounds over {count} targets of {n} letters: {stamped} stamped, {turns} stamps, checksum {check}")


main()
