# LeetCode #1562: Find Latest Group of Size M -- the Python mirror of
# latest.kara, the ★ arm: each group's length kept at both its ends, and a
# count of groups of length m. Prints byte-identical output.


def find_latest_step(arr, m):
    n = len(arr)
    length = [0] * (n + 2)
    groups_of_m = 0
    latest = -1
    for step, a in enumerate(arr):
        left = length[a - 1]
        right = length[a + 1]
        total = left + right + 1
        if left == m:
            groups_of_m -= 1
        if right == m:
            groups_of_m -= 1
        if total == m:
            groups_of_m += 1
        length[a - left] = total
        length[a + right] = total
        if groups_of_m > 0:
            latest = step + 1
    return latest


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
        n = (next_random() * 32768 + next_random()) % most + 1
        arr = list(range(1, n + 1))
        for i in range(n - 1, 0, -1):
            j = (next_random() * 32768 + next_random()) % (i + 1)
            arr[i], arr[j] = arr[j], arr[i]
        if next_random() % 2 == 0:
            m = next_random() % min(n, 8) + 1
        else:
            m = next_random() % n + 1
        step = find_latest_step(arr, m)
        if step >= 0:
            found += 1
        check = mix(check, step)
    print(f"{count} orders of up to {most} positions: {found} with a group, checksum {check}")


def main():
    global seed
    examples = [
        ([3, 5, 1, 2, 4], 1),
        ([3, 1, 5, 4, 2], 2),
        ([1], 1),
        ([2, 1], 2),
        ([2, 1], 1),
        ([1, 2, 3, 4], 2),
        ([4, 3, 2, 1], 1),
        ([1, 3, 5, 2, 4], 1),
        ([2, 4, 6, 1, 3, 5], 3),
    ]
    for arr, m in examples:
        print(f"{arr}, m = {m} -> {find_latest_step(arr, m)}")
    seed = 1562
    batch(3000, 8)
    batch(300, 1000)
    batch(30, 100000)


main()
