# LeetCode #1562: Find Latest Group of Size M -- bench: the ★ arm (group
# lengths kept at both ends, a count of groups of length m) over 20 random
# orders of 100000 positions, built once, each asked for m from 1 to 10.
# Python mirror of latest.kara.


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


seed = 1562


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def main():
    n = 100000
    orders = []
    for _ in range(20):
        arr = list(range(1, n + 1))
        for i in range(n - 1, 0, -1):
            j = (next_random() * 32768 + next_random()) % (i + 1)
            arr[i], arr[j] = arr[j], arr[i]
        orders.append(arr)
    check = 0
    total = 0
    for m in range(1, 11):
        for arr in orders:
            step = find_latest_step(arr, m)
            total += step
            check = mix(check, step)
    print(f"m from 1 to 10 over 20 orders of 100000 positions: steps sum {total}, checksum {check}")


main()
