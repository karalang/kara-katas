# LeetCode #1460 bench in Python: the ★ arm (both arrays sorted and
# compared) on the same 200 pairs of 1000 values and 50 passes.


def can_be_equal(target, arr):
    return sorted(target) == sorted(arr)


seed = 1460


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    targets = []
    arrs = []
    for _ in range(200):
        target = [1 + next_random() % 1000 for _ in range(1000)]
        arr = list(target)
        for i in range(999, 0, -1):
            j = next_random() % (i + 1)
            arr[i], arr[j] = arr[j], arr[i]
        targets.append(target)
        arrs.append(arr)
    check = 0
    for pass_ in range(50):
        for p in range(200):
            arrs[p][check % 1000] = targets[p][(check // 7) % 1000]
            same = can_be_equal(targets[p], arrs[p])
            check = (check * 31 + (1 if same else 0) + pass_) % 1000000007
    print(f"50 passes over 200 pairs of 1000 values: checksum {check}")


main()
