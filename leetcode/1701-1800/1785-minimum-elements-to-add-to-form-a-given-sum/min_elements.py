# LeetCode #1785: Minimum Elements to Add to Form a Given Sum -- the ★ arm
# in Python: the gap over the limit, rounded up.


def min_elements(nums, limit, goal):
    gap = abs(goal - sum(nums))
    return (gap + limit - 1) // limit


seed = 1785


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_nums(n, limit):
    out = []
    for _ in range(n):
        a = next_random()
        b = next_random()
        out.append((a * 32768 + b) % (2 * limit + 1) - limit)
    return out


def main():
    print(f"{min_elements([1, -1, 1], 3, -4)} {min_elements([1, -10, 9, 1], 100, 0)}")
    print(f"{min_elements([4, -4], 2, 0)} {min_elements([0], 5, 10)} {min_elements([0], 5, 11)} {min_elements([5], 5, -5)} {min_elements([1], 1, 1000000000)}")
    high = [1000000] * 100000
    ones = random_nums(100000, 1)
    wide = random_nums(100000, 1000000)
    print(f"the most: {min_elements(high, 1000000, -1000000000)} {min_elements(ones, 1, 1000000000)} {min_elements(wide, 1000000, -1000000000)}")
    check = 0
    for _ in range(3000):
        n = 1 + next_random() % 20
        limit = 1 + next_random() % 10
        nums = random_nums(n, limit)
        goal = next_random() % 201 - 100
        check = (check * 31 + min_elements(nums, limit, goal)) % 1000000007
    print(f"3000 random cases: checksum {check}")


main()
