# Benchmark for #491: Python mirror of the ★ arm (backtracking); see
# non_decreasing_subsequences.kara.


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


def main():
    # 3000 arrays of 15 numbers, the k-th from k / 2 to k / 2 + 3, so
    # they mostly rise, built once, then each solved once.
    seed = 491

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    arrays = [[k // 2 + next_random() % 4 for k in range(15)] for _ in range(3000)]
    total = 0
    checksum = 0
    for nums in arrays:
        out = find_subsequences(nums)
        total += len(out)
        for s in out:
            for x in s:
                checksum = (checksum * 31 + x + 7) % 1000000007
            checksum = (checksum * 31 + 15) % 1000000007
    print(f"3000 arrays of 15: {total} subsequences, checksum {checksum}")


main()
