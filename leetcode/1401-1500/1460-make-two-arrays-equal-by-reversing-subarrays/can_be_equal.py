# LeetCode #1460 Make Two Arrays Equal by Reversing Subarrays: a mirror of
# can_be_equal.kara.


def can_be_equal(target, arr):
    # a reversal of two neighbours is a swap, and swaps sort anything, so
    # `arr` can become `target` exactly when the two hold the same values
    return sorted(target) == sorted(arr)


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def draw(n, top):
    return [1 + next_random() % top for _ in range(n)]


def shuffled(values):
    out = list(values)
    for i in range(len(out) - 1, 0, -1):
        j = next_random() % (i + 1)
        out[i], out[j] = out[j], out[i]
    return out


def show(b):
    return "true" if b else "false"


def main():
    global seed
    f = can_be_equal
    e1 = f([1, 2, 3, 4], [2, 4, 1, 3])
    e2 = f([7], [7])
    e3 = f([3, 7, 9], [3, 7, 11])
    e4 = f([1, 1, 1, 1, 1], [1, 1, 1, 1, 1])
    e5 = f([1], [2])
    up = list(range(1, 1001))
    down = up[::-1]
    off = list(down)
    off[500] = 1
    print(" ".join(show(x) for x in [e1, e2, e3, e4, e5, f(up, down), f(up, off)]))
    seed = 1460
    a = draw(1000, 1000)
    b = shuffled(a)
    print(f"1000 shuffled: {show(f(a, b))}")
    yes = 0
    check = 0
    for c in range(3000):
        n = 1 + next_random() % 60
        top = 1 + next_random() % 20
        target = draw(n, top)
        arr = draw(n, top) if c % 3 == 2 else shuffled(target)
        if c % 3 == 1:
            k = next_random() % n
            arr[k] = 1 + next_random() % top
        got = f(target, arr)
        if got:
            yes += 1
        check = (check * 3 + (1 if got else 0)) % 1000000007
    print(f"3000 random pairs: {yes} equal, checksum {check}")


main()
