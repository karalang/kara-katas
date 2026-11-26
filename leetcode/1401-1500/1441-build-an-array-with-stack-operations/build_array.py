# LeetCode #1441: Build an Array With Stack Operations -- the Python mirror
# of build_array.kara: the stream read from 1, each number pushed, and
# popped again unless it is the next number of the target


def build_array(target, n):
    ops = []
    nxt = 0
    for x in range(1, n + 1):
        if nxt == len(target):
            break
        ops.append("Push")
        if target[nxt] == x:
            nxt += 1
        else:
            ops.append("Pop")
    return ops


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def drawn(n):
    keep = 1 + next_random() % 100
    target = [x for x in range(1, n + 1) if next_random() % 100 < keep]
    if not target:
        target.append(1 + next_random() % n)
    return target


def folded(ops):
    h = 0
    for op in ops:
        h = (h * 3 + (1 if op == "Push" else 2)) % 1000000007
    return h


def main():
    global seed
    cases = [([1, 3], 3), ([1, 2, 3], 3), ([1, 2], 4), ([3], 3), ([1], 1), ([2, 4], 5), ([1, 4, 5], 9)]
    print(" ".join(",".join(build_array(t, n)) for t, n in cases))
    all_ = list(range(1, 101))
    even = [2 * x for x in range(1, 51)]
    print(f"n = 100: {len(build_array(all_, 100))} {len(build_array([100], 100))} {len(build_array(even, 100))}")
    seed = 1441
    check = 0
    total = 0
    for _ in range(2000):
        n = 1 + next_random() % 100
        target = drawn(n)
        ops = build_array(target, n)
        total += len(ops)
        check = (check * 131 + folded(ops)) % 1000000007
    print(f"2000 random cases: {total} operations, checksum {check}")


main()
