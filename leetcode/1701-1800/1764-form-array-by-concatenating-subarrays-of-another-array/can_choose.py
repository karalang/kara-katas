# LeetCode #1764: Form Array by Concatenating Subarrays of Another Array --
# the ★ arm in Python, with the same harness.
def can_choose(groups, nums):
    at = 0
    for group in groups:
        n = len(group)
        while True:
            if at + n > len(nums):
                return False
            if nums[at:at + n] == group:
                break
            at += 1
        at += n
    return True


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_values(n, values):
    return [next_random() % values for _ in range(n)]


def random_case(k, most, values, gap, break_one):
    groups, nums = [], []
    for _ in range(k):
        filler = next_random() % (gap + 1)
        nums.extend(random_values(filler, values))
        n = 1 + next_random() % most
        group = random_values(n, values)
        nums.extend(group)
        groups.append(group)
    if break_one:
        g = next_random() % k
        at = next_random() % len(groups[g])
        groups[g][at] = next_random() % values
    return groups, nums


def b(x):
    return "true" if x else "false"


def main():
    global seed
    print(f"{b(can_choose([[1, -1, -1], [3, -2, 0]], [1, -1, 0, 1, -1, -1, 3, -2, 0]))} {b(can_choose([[10, -2], [1, 2, 3, 4]], [1, 2, 3, 4, 10, -2]))} {b(can_choose([[1, 2, 3], [3, 4]], [7, 7, 1, 2, 3, 4, 7, 7]))}")
    print(" ".join(b(can_choose(g, n)) for g, n in [([[5, 6]], [5, 6]), ([[1, 2], [2, 3]], [1, 2, 3]), ([[1, 2, 3, 4]], [1, 2, 3]), ([[1, 1, 2]], [1, 1, 1, 2]), ([[4, 4], [4, 4]], [4, 4, 4, 4])]))
    seed = 1764
    lg, ln = random_case(1, 1000, 3, 0, False)
    sg, sn = random_case(1000, 1, 2, 0, False)
    bg, bn = random_case(20, 40, 2, 10, True)
    print(f"the most: {b(can_choose(lg, ln))} {b(can_choose(sg, sn))} {b(can_choose(bg, bn))}")
    check = 0
    for _ in range(3000):
        k = 1 + next_random() % 5
        break_one = next_random() % 3 == 0
        groups, nums = random_case(k, 4, 3, 3, break_one)
        check = (check * 31 + (1 if can_choose(groups, nums) else 0)) % 1000000007
    print(f"3000 random cases: checksum {check}")


main()
