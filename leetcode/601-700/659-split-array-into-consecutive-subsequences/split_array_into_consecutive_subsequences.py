# LeetCode #659: Split Array into Consecutive Subsequences -- greedy.
# Mirrors the ★ arm (split_array_into_consecutive_subsequences.kara) and
# its test harness.


def is_possible(nums):
    left = {}
    for x in nums:
        left[x] = left.get(x, 0) + 1
    ends = {}
    for x in nums:
        if left.get(x, 0) == 0:
            continue
        left[x] -= 1
        if ends.get(x - 1, 0) > 0:
            ends[x - 1] -= 1
            ends[x] = ends.get(x, 0) + 1
        elif left.get(x + 1, 0) > 0 and left.get(x + 2, 0) > 0:
            left[x + 1] -= 1
            left[x + 2] -= 1
            ends[x + 2] = ends.get(x + 2, 0) + 1
        else:
            return False
    return True


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def word(b):
    return "true" if b else "false"


def show(nums):
    print(f"[{','.join(map(str, nums))}] -> {word(is_possible(nums))}")


def random_runs(runs, low, spread):
    nums = []
    for _ in range(runs):
        start = low + next_random() % (spread + 1)
        length = 3 + next_random() % 3
        nums.extend(range(start, start + length))
    nums.sort()
    return nums


def main():
    global seed
    for nums in [[1, 2, 3, 3, 4, 5], [1, 2, 3, 3, 4, 4, 5, 5], [1, 2, 3, 4, 4, 5], [7], [-1, 0, 1],
                 [1, 2, 4], [1, 1, 2, 2, 3, 3], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 5, 6]]:
        show(nums)
    seed = 659
    yes = 0
    s = 0
    for k in range(300):
        nums = []
        if k % 2 == 0:
            nums = random_runs(1 + next_random() % 8, -10, 20)
            if k % 6 == 0:
                at = next_random() % len(nums)
                if next_random() % 2 == 0:
                    nums.pop(at)
                else:
                    nums.insert(at, nums[at])
        else:
            for _ in range(1 + next_random() % 30):
                nums.append(next_random() % 12)
            nums.sort()
        if not nums:
            nums.append(0)
        ok = is_possible(nums)
        if ok:
            yes += 1
        s = (s * 7 + len(nums) * 2 + (1 if ok else 0)) % 1000000007
    print(f"300 random arrays: {yes} can be split, checksum {s}")
    nums = random_runs(2500, -1000, 1995)
    cut = nums[:10000]
    print(f"{len(cut)} numbers from runs, cut to fit: {word(is_possible(cut))}")
    whole = random_runs(2000, -1000, 1995)
    while len(whole) > 9999:
        whole = random_runs(2000, -1000, 1995)
    print(f"{len(whole)} numbers from runs: {word(is_possible(whole))}")
    whole.insert(5000, whole[5000])
    print(f"the same with one number repeated: {word(is_possible(whole))}")
    print(f"10000 copies of one number: {word(is_possible([0] * 10000))}")


main()
