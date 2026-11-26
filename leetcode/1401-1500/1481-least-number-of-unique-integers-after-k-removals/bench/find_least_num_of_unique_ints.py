# LeetCode #1481: Least Number of Unique Integers after K Removals --
# bench, Python mirror of find_least_num_of_unique_ints.kara


def find_least_num_of_unique_ints(arr, k):
    count = {}
    for x in arr:
        count[x] = count.get(x, 0) + 1
    counts = sorted(count.values())
    left = k
    unique = len(counts)
    for c in counts:
        if c > left:
            break
        left -= c
        unique -= 1
    return unique


seed = 1481


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    arr = [1 + next_random() % 30000 for _ in range(100000)]
    check = 0
    for p in range(100):
        arr[check % 100000] = 1 + (check // 7) % 30000
        k = check % 100000
        check = (check * 31 + find_least_num_of_unique_ints(arr, k) + p) % 1000000007
    print(f"100 passes over 100000 values: checksum {check}")


main()
