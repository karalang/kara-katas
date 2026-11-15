# LeetCode #2190: Most Frequent Number Following Key In an Array -- the
# Python mirror of follow.kara: each number after the key counted, the
# most counted kept as it is met.


def most_frequent(nums, key):
    counts = [0] * 1001
    best = 0
    target = -1
    for i in range(1, len(nums)):
        if nums[i - 1] == key:
            x = nums[i]
            counts[x] += 1
            if counts[x] > best:
                best = counts[x]
                target = x
    return target


# ---- test harness ---------------------------------------------------------

seed = 2190


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def unique_answer(nums, key):
    counts = [0] * 1001
    for i in range(len(nums) - 1):
        if nums[i] == key:
            counts[nums[i + 1]] += 1
    best = 0
    ties = 0
    for c in counts:
        if c > best:
            best = c
            ties = 1
        elif c == best:
            ties += 1
    return best > 0 and ties == 1


def random_case(n, values):
    while True:
        nums = [next_random() % values + 1 for _ in range(n)]
        key = nums[next_random() % (n - 1)]
        if unique_answer(nums, key):
            return nums, key


def show(nums, key):
    print(f"[{', '.join(str(x) for x in nums)}], {key} -> {most_frequent(nums, key)}")


def main():
    show([1, 100, 200, 1, 100], 1)
    show([2, 2, 2, 2, 3], 2)
    show([5, 7], 5)
    show([3, 3, 1, 3, 3], 3)
    show([4, 9, 4, 9, 4], 4)
    show([1000, 999, 1000, 1, 1000, 999], 1000)
    total = 0
    check = 0
    for rnd in range(2000):
        n = next_random() % 29 + 2
        values = [5, 1000][rnd % 2]
        nums, key = random_case(n, values)
        target = most_frequent(nums, key)
        total += target
        check = (check * 31 + target + n) % 1000000007
    print(f"2000 lists: targets add up to {total}, checksum {check}")
    turns = []
    for i in range(500):
        turns.append(7)
        turns.append([1, 2, 3, 1][i % 4])
    wide, key = random_case(1000, 1000)
    print(f"1000 numbers: {most_frequent(turns, 7)} {most_frequent(wide, key)}")


main()
