# LeetCode #1798: Maximum Number of Consecutive Values You Can Make -- the
# bench in Python: the ★ arm over 200 random lists of 2000 coins built
# once, 20000 calls.


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
    lists = [[1 + next_random() % 200 for _ in range(2000)] for _ in range(200)]
    check = 0
    for call in range(20000):
        coins = lists[(check + call) % 200]
        check = (check * 31 + get_maximum_consecutive(coins)) % 1000000007
    print(f"20000 calls over 200 lists of 2000 coins: checksum {check}")


main()
