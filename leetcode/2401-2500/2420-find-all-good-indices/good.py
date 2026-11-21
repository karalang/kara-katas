# LeetCode #2420: Find All Good Indices -- the Python mirror of the ★ arm:
# the run of values ending at each index without rising, from the left,
# and the run starting at each index without falling, from the right.

seed = 2420


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def good_indices(nums, k):
    n = len(nums)
    falling = [1] * n
    rising = [1] * n
    for i in range(1, n):
        if nums[i] <= nums[i - 1]:
            falling[i] = falling[i - 1] + 1
    for i in range(n - 2, -1, -1):
        if nums[i] <= nums[i + 1]:
            rising[i] = rising[i + 1] + 1
    return [i for i in range(k, n - k) if falling[i - 1] >= k and rising[i + 1] >= k]


def values(n, top, turn, step):
    nums = []
    down = True
    for i in range(n):
        if i == 0:
            nums.append(1 + (next_random() * 32768 + next_random()) % top)
        else:
            if next_random() % turn == 0:
                down = not down
            d = next_random() % (step + 1)
            v = nums[i - 1] - d if down else nums[i - 1] + d
            nums.append(min(max(v, 1), top))
    return nums


def show(good):
    return "[" + ",".join(str(g) for g in good) + "]"


def digest(good):
    h = 0
    for g in good:
        h = (h * 31 + g) % 1000000007
    return f"{len(good)} good: {h} {sum(good)}"


def main():
    print(show(good_indices([2, 1, 1, 1, 3, 4, 1], 2)))
    print(show(good_indices([2, 1, 1, 2], 2)))
    print(show(good_indices([5, 5, 5, 5, 5, 5], 2)))
    print(show(good_indices([3, 2, 1, 1, 2, 3], 3)))
    print(show(good_indices([9, 7, 5, 3, 1, 4, 6, 8, 9], 4)))
    print(show(good_indices([1, 2, 3, 4, 5], 1)))
    print(show(good_indices([5, 4, 3, 2, 1], 1)))
    big = values(100000, 1000000, 60, 40)
    print(digest(good_indices(big, 2)))
    print(digest(good_indices(big, 5)))
    print(digest(good_indices(big, 50)))
    print(digest(good_indices(values(100000, 3, 4, 1), 3)))
    check = 0
    count = 0
    for _ in range(3000):
        n = 3 + next_random() % 28
        top = 1 + next_random() % 8
        turn = 1 + next_random() % 6
        step = next_random() % 3
        nums = values(n, top, turn, step)
        k = 1 + next_random() % (n // 2)
        for g in good_indices(nums, k):
            check = (check * 31 + g + 1) % 1000000007
            count += 1
        check = (check * 31 + 1000) % 1000000007
    print(f"3000 random: checksum {check}, {count} good")


if __name__ == "__main__":
    main()
