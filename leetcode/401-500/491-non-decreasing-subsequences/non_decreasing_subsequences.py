# LeetCode #491: Non-decreasing Subsequences -- Python mirror of the ★ arm
# (backtracking); see non_decreasing_subsequences.kara.


def extend(nums, start, current, out):
    if len(current) >= 2:
        out.append(list(current))
    tried = set()
    for i in range(start, len(nums)):
        if nums[i] in tried:
            continue
        if len(current) == 0 or nums[i] >= current[-1]:
            tried.add(nums[i])
            current.append(nums[i])
            extend(nums, i + 1, current, out)
            current.pop()


def find_subsequences(nums):
    out = []
    extend(nums, 0, [], out)
    return out


def sorted_answer(nums):
    out = find_subsequences(nums)
    out.sort()
    return out


def show(name, nums):
    out = sorted_answer(nums)
    print(f"{name}: {nums} -> {len(out)}: {out}")


seed = 491


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    show("example 1", [4, 6, 7, 7])
    show("example 2", [4, 4, 3, 2, 1])
    show("one number", [5])
    show("all equal", [2, 2, 2, 2])
    show("falling", [5, 4, 3, 2, 1])
    show("negatives", [-1, -3, -1, 0, -3])
    show("rising", [1, 2, 3, 4])
    # 300 random arrays of 1 to 12 numbers from -3 to 3.
    count = 300
    total = 0
    checksum = 0
    for _ in range(count):
        size = 1 + next_random() % 12
        nums = [next_random() % 7 - 3 for _ in range(size)]
        out = sorted_answer(nums)
        total += len(out)
        for s in out:
            for x in s:
                checksum = (checksum * 31 + x + 4) % 1000000007
            checksum = (checksum * 31 + 9) % 1000000007
    print(f"{count} random arrays: {total} subsequences, checksum {checksum}")


main()
