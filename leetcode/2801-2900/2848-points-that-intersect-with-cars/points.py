# LeetCode #2848: Points That Intersect With Cars -- the Python mirror
# of the ★ arm: each car marks its points on a road of 100, and the
# marked ones are counted.


def number_of_points(nums):
    covered = [False] * 101
    for start, end in nums:
        for x in range(start, end + 1):
            covered[x] = True
    return sum(1 for c in covered if c)


# ---- the harness: the same in every arm --------------------------------

seed = 2848


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    p = number_of_points
    print(f"{p([[3, 6], [1, 5], [4, 7]])} {p([[1, 3], [5, 8]])}")
    print(f"{p([[7, 7]])} {p([[1, 100]])}")
    print(f"{p([[i, i] for i in range(1, 101)])}")
    check = 0
    total = 0
    for c in range(3300):
        short = c < 3000
        cars = next_random() % 6 + 1 if short else next_random() % 100 + 1
        road = 20 if short else 100
        nums = []
        for _ in range(cars):
            start = next_random() % road + 1
            a = next_random()
            length = a % (next_random() % road + 1)
            nums.append([start, min(start + length, road)])
        points = p(nums)
        total += points
        check = (check * 31 + points) % 1000000007
        if c == 2999:
            print(f"3000 short roads: {total} points, checksum {check}")
            total = 0
            check = 0
    print(f"300 long roads: {total} points, checksum {check}")


main()
