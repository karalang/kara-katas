# LeetCode #969: Pancake Sorting -- Python mirror of pancake_sort.kara.


def flip(a, k):
    i, j = 0, k - 1
    while i < j:
        a[i], a[j] = a[j], a[i]
        i += 1
        j -= 1


def pancake_sort(arr):
    a = list(arr)
    flips = []
    size = len(a)
    while size > 1:
        i = 0
        while a[i] != size:
            i += 1
        if i != size - 1:
            if i != 0:
                flip(a, i + 1)
                flips.append(i + 1)
            flip(a, size)
            flips.append(size)
        size -= 1
    return flips


# ---- test harness -----------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_permutation(n):
    a = list(range(1, n + 1))
    i = n - 1
    while i > 0:
        j = next_random() % (i + 1)
        a[i], a[j] = a[j], a[i]
        i -= 1
    return a


def show(v):
    return "[" + ",".join(str(x) for x in v) + "]"


def sorts(arr, flips):
    a = list(arr)
    n = len(a)
    for k in flips:
        if k < 1 or k > n:
            return False
        a[:k] = a[:k][::-1]
    return a == list(range(1, n + 1))


def checksum(flips):
    check = 0
    for k in flips:
        check = (check * 131 + k) % 1000000007
    return check


def tf(b):
    return "true" if b else "false"


def main():
    global seed
    cases = [
        [3, 2, 4, 1],
        [1, 2, 3],
        [1],
        [2, 1],
        [3, 1, 2],
        [2, 3, 1],
        [6, 5, 4, 3, 2, 1],
        [2, 3, 4, 5, 1],
        [1, 3, 2, 4, 6, 5],
        [5, 1, 4, 2, 3, 6],
    ]
    for arr in cases:
        flips = pancake_sort(arr)
        print(f"{show(arr)}: {show(flips)}, sorts {tf(sorts(arr, flips))}")
    seed = 969
    pancakes = total = sorted_ = check = 0
    for _ in range(300):
        n = 1 + next_random() % 12
        arr = random_permutation(n)
        pancakes += n
        flips = pancake_sort(arr)
        total += len(flips)
        if sorts(arr, flips):
            sorted_ += 1
        check = (check * 31 + checksum(flips) + 1) % 1000000007
    print(f"300 random stacks of {pancakes} pancakes: {total} flips, {sorted_} sorted, checksum {check}")
    odd_even = [2 * v + 1 if v < 50 else 2 * (v - 50) + 2 for v in range(100)]
    upside_down = [100 - v for v in range(100)]
    big = [
        ("a random stack", random_permutation(100)),
        ("the stack upside down", upside_down),
        ("odd above even", odd_even),
    ]
    for name, arr in big:
        flips = pancake_sort(arr)
        print(f"{name} of 100: {len(flips)} flips, sorts {tf(sorts(arr, flips))}, checksum {checksum(flips)}")


main()
