# LeetCode #1013: Partition Array Into Three Parts With Equal Sum -- bench
# Mirrors three_parts.kara; see ../README.md § Benchmarks.


def can_three_parts_equal_sum(arr):
    total = 0
    for x in arr:
        total += x
    if total % 3 != 0:
        return False
    target = total // 3
    prefix = 0
    cuts = 0
    for i in range(len(arr) - 1):
        prefix += arr[i]
        if cuts == 0 and prefix == target:
            cuts = 1
        elif cuts == 1 and prefix == 2 * target:
            return True
    return False


seed = 1013


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count = 50000
    rounds = 10000
    arr = []
    total = 0
    for _ in range(count):
        x = next_random() % 7 - 2
        arr.append(x)
        total += x
    # the remainder truncated toward zero, as in Kāra, C, Rust and Go
    arr[count - 1] -= total % 3 if total >= 0 else -((-total) % 3)
    yes = 0
    check = 0
    for _ in range(rounds):
        at = (next_random() * 32768 + next_random()) % count
        arr[at] += 3 * (next_random() % 3 - 1)
        answer = can_three_parts_equal_sum(arr)
        if answer:
            yes += 1
        check = (check * 2 + (1 if answer else 0)) % 1000000007
    print(f"{rounds} rounds over {count} values: {yes} split, checksum {check}")


main()
