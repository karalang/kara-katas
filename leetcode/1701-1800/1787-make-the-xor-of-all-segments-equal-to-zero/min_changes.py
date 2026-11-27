# LeetCode #1787: Make the XOR of All Segments Equal to Zero -- the ★ arm in
# Python: a DP over the k groups of positions by i % k, each XOR of the
# values chosen so far kept at its fewest changes.


def min_changes(nums, k):
    best = [2**31 // 2 - 1] * 1024
    best[0] = 0
    for g in range(k):
        count = {}
        size = 0
        i = g
        while i < len(nums):
            count[nums[i]] = count.get(nums[i], 0) + 1
            size += 1
            i += k
        floor = min(best) + size
        nxt = [floor] * 1024
        for x in range(1024):
            for v, c in count.items():
                here = best[x ^ v] + size - c
                if here < nxt[x]:
                    nxt[x] = here
        best = nxt
    return best[0]


seed = 1787


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_nums(n, most):
    return [next_random() % most for _ in range(n)]


def main():
    print(f"{min_changes([1, 2, 0, 3, 0], 1)} {min_changes([3, 4, 5, 2, 1, 7, 3, 4, 7], 3)} {min_changes([1, 2, 4, 1, 2, 5, 1, 2, 6], 3)}")
    print(f"{min_changes([0], 1)} {min_changes([5], 1)} {min_changes([1, 2, 3], 3)} {min_changes([1, 2, 4], 3)} {min_changes([1, 2, 3, 1, 2, 3, 1], 3)} {min_changes([7, 7, 7, 7], 2)} {min_changes([7, 7, 7, 7], 3)}")
    wide = random_nums(2000, 1024)
    print(f"the most: {min_changes(wide, 1)} {min_changes(wide, 7)} {min_changes(wide, 1000)} {min_changes(wide, 2000)}")
    check = 0
    for c in range(1500):
        n = 1 + next_random() % 24
        k = 1 + next_random() % n
        most = 2 + next_random() % 31
        nums = random_nums(n, most)
        if c % 4 == 0:
            for i in range(k, n):
                nums[i] = nums[i - k]
            changed = next_random() % 3
            for _ in range(changed):
                at = next_random() % n
                nums[at] = next_random() % most
        check = (check * 31 + min_changes(nums, k)) % 1000000007
    print(f"1500 random cases: checksum {check}")


main()
