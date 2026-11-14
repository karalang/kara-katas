# LeetCode #2150: Find All Lonely Numbers in the Array -- the benchmark's
# Python mirror of lonely.kara.


def find_lonely(nums):
    count = {}
    for x in nums:
        count[x] = count.get(x, 0) + 1
    return [x for x, c in count.items() if c == 1 and x - 1 not in count and x + 1 not in count]


seed = 2150


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    high = next_random()
    return high * 32768 + next_random()


def main():
    n = 100000
    lists = [[wide() % 1000001 for _ in range(n)] for _ in range(4)]
    total = 0
    check = 0
    for rnd in range(25):
        for l in range(4):
            at = wide() % n
            lists[l][at] = wide() % 1000001
            out = find_lonely(lists[l])
            total += len(out)
            check = (check * 31 + sum(out) % 1000000007 + len(out) + rnd) % 1000000007
    print(f"100 searches: {total} lonely in all, checksum {check}")


main()
