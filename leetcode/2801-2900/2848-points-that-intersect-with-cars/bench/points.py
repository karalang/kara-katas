# LeetCode #2848: Points That Intersect With Cars -- the bench, mirrored
# from points.kara: each car marks its points on a road of 100, and the
# marked ones are counted.

seed = 2848


def number_of_points(nums):
    covered = [False] * 101
    for start, end in nums:
        for x in range(start, end + 1):
            covered[x] = True
    return sum(1 for c in covered if c)


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, rounds = 10000, 50
    parkings = []
    for _ in range(count):
        cars = next_random() % 100 + 1
        nums = []
        for _ in range(cars):
            start = next_random() % 100 + 1
            a = next_random()
            length = a % (next_random() % 100 + 1)
            nums.append((start, min(start + length, 100)))
        parkings.append(nums)
    total = 0
    check = 0
    for r in range(rounds):
        for nums in parkings:
            points = number_of_points(nums)
            total += points
            check = (check * 31 + points + r) % 1000000007
    print(f"{count} parkings, {rounds} rounds: {total} points, checksum {check}")


main()
