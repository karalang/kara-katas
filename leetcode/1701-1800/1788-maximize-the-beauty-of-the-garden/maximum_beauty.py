# LeetCode #1788: Maximize the Beauty of the Garden -- the ★ arm in Python:
# a prefix sum of the positive beauties, and each beauty's first position.


def maximum_beauty(flowers):
    n = len(flowers)
    positive = [0] * (n + 1)
    for i in range(n):
        positive[i + 1] = positive[i] + max(flowers[i], 0)
    first = {}
    best = None
    for j, v in enumerate(flowers):
        if v in first:
            garden = 2 * v + positive[j] - positive[first[v] + 1]
            best = garden if best is None else max(best, garden)
        else:
            first[v] = j
    return best


seed = 1788


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_flowers(n, most):
    flowers = [next_random() % (2 * most + 1) - most for _ in range(n)]
    a = next_random() % n
    b = next_random() % n
    if a == b:
        flowers[(a + 1) % n] = flowers[a]
    else:
        flowers[b] = flowers[a]
    return flowers


def main():
    print(f"{maximum_beauty([1, 2, 3, 1, 2])} {maximum_beauty([100, 1, 1, -3, 1])} {maximum_beauty([-1, -2, 0, -1])}")
    print(f"{maximum_beauty([5, 5])} {maximum_beauty([-5, -5])} {maximum_beauty([-1, 50, -1])} {maximum_beauty([9, 1, 2, 1, 9])} {maximum_beauty([-9, 4, 4, -9])}")
    high = [10000] * 100000
    low = [-10000] * 100000
    wide = random_flowers(100000, 10000)
    print(f"the most: {maximum_beauty(high)} {maximum_beauty(low)} {maximum_beauty(wide)}")
    check = 0
    for _ in range(3000):
        n = 2 + next_random() % 29
        flowers = random_flowers(n, 10)
        check = (check * 31 + maximum_beauty(flowers) + 1000000) % 1000000007
    print(f"3000 random cases: checksum {check}")


main()
