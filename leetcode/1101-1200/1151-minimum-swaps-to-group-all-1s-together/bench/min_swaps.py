# LeetCode #1151: Minimum Swaps to Group All 1's Together -- the Python
# mirror of the ★ arm: a window as long as the count of ones slides along
# the list, and the answer is the count less the most ones it holds.


def min_swaps(data):
    k = sum(data)
    if k == 0:
        return 0
    inside = 0
    for i in range(k):
        inside += data[i]
    most = inside
    for i in range(k, len(data)):
        inside += data[i] - data[i - k]
        if inside > most:
            most = inside
    return k - most


def main():
    seed = 1151

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    lists = []
    for l in range(16):
        ones = 1 + l % 7
        lists.append([1 if next_random() % 8 < ones else 0 for _ in range(100000)])
    total = 0
    check = 0
    for r in range(3000):
        data = lists[r % 16]
        for _ in range(64):
            at = next_random() * 3
            data[at] = 1 - data[at]
        s = min_swaps(data)
        total += s
        check = (check * 31 + s) % 1000000007
    print(f"3000 rounds over 16 lists of 100000 bits: swaps total {total}, checksum {check}")


main()
