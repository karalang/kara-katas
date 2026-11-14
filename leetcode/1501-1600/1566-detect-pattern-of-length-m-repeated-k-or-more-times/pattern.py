# LeetCode #1566: Detect Pattern of Length M Repeated K or More Times --
# the Python mirror of pattern.kara, the ★ arm: a run of m (k - 1) places
# each equal to the value m on. Prints byte-identical output.


def contains_pattern(arr, m, k):
    run = 0
    for i in range(len(arr) - m):
        if arr[i] == arr[i + m]:
            run += 1
            if run == m * (k - 1):
                return True
        else:
            run = 0
    return False


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def batch(count, most):
    check = 0
    found = 0
    for _ in range(count):
        n = next_random() % (most - 1) + 2
        own = next_random() % 4 + 1
        arr = [next_random() % own + 1 for _ in range(n)]
        m = next_random() % 4 + 1
        k = next_random() % 4 + 2
        if next_random() % 2 == 0 and m * k <= n:
            start = next_random() % (n - m * k + 1)
            for i in range(m, m * k):
                arr[start + i] = arr[start + i % m]
        yes = contains_pattern(arr, m, k)
        if yes:
            found += 1
        check = mix(check, n if yes else 0)
    print(f"{count} arrays of up to {most} values: {found} with a pattern, checksum {check}")


def main():
    global seed
    examples = [
        ([1, 2, 4, 4, 4, 4], 1, 3),
        ([1, 2, 1, 2, 1, 1, 1, 3], 2, 2),
        ([1, 2, 1, 2, 1, 3], 2, 3),
        ([1, 2, 3, 1, 2], 2, 2),
        ([2, 2, 2, 2], 2, 3),
        ([2, 2], 1, 2),
        ([1, 2], 1, 2),
        ([3, 1, 2, 3, 1, 2, 3, 1, 2], 3, 3),
        ([3, 1, 2, 3, 1, 2, 3, 1, 9], 3, 3),
    ]
    for arr, m, k in examples:
        print(f"{arr}, m = {m}, k = {k} -> {'true' if contains_pattern(arr, m, k) else 'false'}")
    seed = 1566
    batch(3000, 10)
    batch(300, 100)
    batch(30, 100000)


main()
