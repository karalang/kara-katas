# LeetCode #1502: Can Make Arithmetic Progression From Sequence -- the
# benchmark, the same algorithm as progression.kara: sort, then every gap equals the first.


def can_make(arr):
    a = sorted(arr)
    d = a[1] - a[0]
    return all(a[i + 1] - a[i] == d for i in range(len(a) - 1))


seed = 1502


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def random_array(most):
    n = next_random() % (most - 1) + 2
    kind = next_random() % 3
    if kind == 2:
        spread = next_random() % 50 + 1
        arr = [next_random() % spread - spread // 2 for _ in range(n)]
    else:
        start = next_random() % 2001 - 1000
        d = next_random() % 21 - 10
        arr = [start + i * d for i in range(n)]
        if kind == 1:
            at = next_random() % n
            arr[at] += 1 if next_random() % 2 == 0 else -1
    for i in range(n - 1, 0, -1):
        j = next_random() % (i + 1)
        arr[i], arr[j] = arr[j], arr[i]
    return arr


def main():
    arrays = [random_array(1000) for _ in range(3000)]
    can = check = 0
    for _ in range(10):
        for arr in arrays:
            answer = 1 if can_make(list(arr)) else 0
            can += answer
            check = mix(check, answer)
    print(f"30000 answers over 3000 arrays of 2 to 1000 numbers: {can} can, checksum {check}")


main()
