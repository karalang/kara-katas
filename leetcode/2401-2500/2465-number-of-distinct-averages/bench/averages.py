# LeetCode #2465: Number of Distinct Averages -- the bench, the ★ arm in
# Python: sorted, the `i`th smallest paired with the `i`th largest, and
# the pairs' sums put in a set.


def distinct_averages(nums):
    s = sorted(nums)
    n = len(s)
    sums = set()
    for i in range(n // 2):
        sums.add(s[i] + s[n - 1 - i])
    return len(sums)


seed = 2465


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 1000 lists of 100 numbers from 0 to 100 built once; then 900
    # passes, each setting one number of every list from the checksum so
    # far, then answering every list and folding the answer plus the pass
    # into the checksum
    lists = [[next_random() % 101 for _ in range(100)] for _ in range(1000)]
    check = 0
    for p in range(900):
        for a in range(len(lists)):
            lists[a][(check + a) % 100] = check % 101
            check = (check * 31 + distinct_averages(lists[a]) + p) % 1000000007
    print(f"900 passes over 1000 lists of 100: checksum {check}")


main()
