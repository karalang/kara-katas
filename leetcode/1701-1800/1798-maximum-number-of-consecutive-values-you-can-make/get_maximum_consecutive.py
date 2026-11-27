# LeetCode #1798: Maximum Number of Consecutive Values You Can Make -- the
# ★ arm in Python: greedy over the sorted coins.


def get_maximum_consecutive(coins):
    reach = 0
    for c in sorted(coins):
        if c > reach + 1:
            break
        reach += c
    return reach + 1


seed = 1798


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    print(f"{get_maximum_consecutive([1, 3])} {get_maximum_consecutive([1, 1, 1, 4])} {get_maximum_consecutive([1, 4, 10, 3, 1])}")
    print(" ".join(str(get_maximum_consecutive(c)) for c in [[1], [2], [8, 4, 2, 1], [1, 1, 1], [5, 1, 1]]))
    big = [40000] * 40000
    small = [1] * 40000
    every = list(range(40000, 0, -1))
    wide = [1 + next_random() % 40000 for _ in range(40000)]
    print(f"the most: {get_maximum_consecutive(big)} {get_maximum_consecutive(small)} {get_maximum_consecutive(every)} {get_maximum_consecutive(wide)}")
    check = 0
    for _ in range(3000):
        n = 1 + next_random() % 15
        top = 1 + next_random() % 12
        coins = [1 + next_random() % top for _ in range(n)]
        check = (check * 31 + get_maximum_consecutive(coins)) % 1000000007
    print(f"3000 random cases: checksum {check}")


main()
