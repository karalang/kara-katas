# LeetCode #2150: Find All Lonely Numbers in the Array -- the Python
# mirror of lonely.kara's ★ arm.


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


def lonely(nums):
    return sorted(find_lonely(nums))


def fmt(nums):
    return "[" + ", ".join(map(str, nums)) + "]"


def show(nums):
    print(f"{fmt(nums)} -> {fmt(lonely(nums))}")


def main():
    show([10, 6, 5, 8])
    show([1, 3, 5, 3])
    show([7])
    show([7, 7])
    show([4, 2, 3, 5])
    show([0, 1000000, 2, 999998])
    total = 0
    check = 0
    for rnd in range(2000):
        n = next_random() % 12 + 1
        top = [10, 31, 1001][rnd % 3]
        nums = [next_random() % top for _ in range(n)]
        out = lonely(nums)
        total += len(out)
        for x in out:
            check = (check * 31 + x + 1) % 1000000007
        check = (check * 31 + n) % 1000000007
    print(f"2000 lists: {total} lonely in all, checksum {check}")
    evens = [2 * i for i in range(100000)]
    runs = [i if i < 66667 else i - 66667 for i in range(100000)]
    rand = []
    for _ in range(100000):
        hi = next_random()
        rand.append((hi * 32768 + next_random()) % 1000001)
    for name, nums in [("evens", evens), ("runs", runs), ("at random", rand)]:
        out = lonely(nums)
        s = 0
        for x in out:
            s = (s * 31 + x + 1) % 1000000007
        print(f"100000 numbers {name}: {len(out)} lonely, checksum {s}")


main()
