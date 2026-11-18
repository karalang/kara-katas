# LeetCode #2226: Maximum Candies Allocated to K Children -- the mirror of
# candies.kara: a binary search on the answer, x candies each possible
# when the piles cut into x-sized shares give at least k of them.


def maximum_candies(candies, k):
    low = 0
    high = max(candies)
    while low < high:
        x = (low + high + 1) // 2
        shares = 0
        for pile in candies:
            shares += pile // x
        if shares >= k:
            low = x
        else:
            high = x - 1
    return low


seed = 2226


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    high = next_random()
    return high * 32768 + next_random()


def fmt(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def show(candies, k):
    print(f"{fmt(candies)}, k = {k} -> {maximum_candies(candies, k)}")


def main():
    show([5, 8, 6], 3)
    show([2, 5], 11)
    show([1], 1)
    show([10000000], 1)
    show([9], 3)
    show([4, 7, 5], 4)
    check = 0
    for c in range(3000):
        n = next_random() % 20 + 1
        top = [10, 1000, 10000000][c % 3]
        candies = []
        total = 0
        for _ in range(n):
            pile = wide_random() % top + 1
            candies.append(pile)
            total += pile
        k = wide_random() % (total + total // 10 + 1) + 1
        check = (check * 31 + maximum_candies(candies, k)) % 1000000007
    print(f"3000 cases: checksum {check}")
    piles = [wide_random() % 10000000 + 1 for _ in range(100000)]
    for k in [1, 100000, 1000000000, 1000000000000]:
        print(f"10^5 piles, k = {k}: {maximum_candies(piles, k)}")


main()
