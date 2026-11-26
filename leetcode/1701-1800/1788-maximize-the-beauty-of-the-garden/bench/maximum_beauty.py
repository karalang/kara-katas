# LeetCode #1788: Maximize the Beauty of the Garden -- the bench in Python,
# mirroring maximum_beauty.kara: a prefix sum of the positives and each
# beauty's first position.


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


def main():
    gardens = []
    for _ in range(400):
        flowers = [next_random() % 20001 - 10000 for _ in range(2000)]
        flowers[1999] = flowers[0]
        gardens.append(flowers)
    check = 0
    for call in range(10000):
        flowers = gardens[(check + call) % 400]
        check = (check * 31 + maximum_beauty(flowers) + 1000000000) % 1000000007
    print(f"10000 calls over 400 gardens: checksum {check}")


main()
