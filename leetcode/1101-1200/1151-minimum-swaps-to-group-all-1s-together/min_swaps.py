# LeetCode #1151: Minimum Swaps to Group All 1's Together -- the Python
# mirror of the ★ arm: a window as long as the count of ones slides along
# the list, and the answer is the count less the most ones it holds.


def min_swaps(data):
    k = sum(data)
    if k == 0:
        return 0
    inside = sum(data[:k])
    most = inside
    for i in range(k, len(data)):
        inside += data[i] - data[i - k]
        most = max(most, inside)
    return k - most


seed = 1151


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def bits(n, ones):
    return [1 if next_random() % 8 < ones else 0 for _ in range(n)]


def show(data):
    print(f"data = {data}  ->  {min_swaps(data)}")


def main():
    show([1, 0, 1, 0, 1])
    show([0, 0, 0, 1, 0])
    show([1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1])
    show([0])
    show([1])
    show([1, 1, 1])
    show([1, 0, 0, 0, 1])
    show([1, 1, 0, 0, 1, 1])
    show([0, 1, 0, 1, 1, 0, 1, 0])
    total = 0
    check = 0
    for _ in range(2000):
        n = 1 + next_random() % 60
        ones = next_random() % 9
        data = bits(n, ones)
        s = min_swaps(data)
        total += s
        check = (check * 31 + s + n) % 1000000007
    print(f"2000 random lists: swaps total {total}, checksum {check}")
    print(f"100000 bits 1, 0, 1, 0, ...  ->  {min_swaps([(i + 1) % 2 for i in range(100000)])}")
    print(f"100000 ones  ->  {min_swaps([1] * 100000)}")
    ends = [1 if i < 25000 or i >= 75000 else 0 for i in range(100000)]
    print(f"25000 ones at each end of 100000 bits  ->  {min_swaps(ends)}")
    print(f"100000 zeros  ->  {min_swaps([0] * 100000)}")
    print(f"100000 random bits, 3 in 8 ones  ->  {min_swaps(bits(100000, 3))}")


main()
