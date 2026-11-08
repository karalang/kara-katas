# LeetCode #2009: Minimum Number of Operations to Make Array Continuous --
# the ★ arm's benchmark, a mirror of continuous.kara.


def min_operations(nums):
    n = len(nums)
    values = sorted(nums)
    w = 0
    for v in values:
        if w == 0 or values[w - 1] != v:
            values[w] = v
            w += 1
    del values[w:]
    kept = 0
    right = 0
    for left in range(len(values)):
        while right < len(values) and values[right] <= values[left] + n - 1:
            right += 1
        kept = max(kept, right - left)
    return n - kept


seed = 2009


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    arrays = []
    for a in range(200):
        top = 2000 * (a + 1)
        nums = []
        for _ in range(2000):
            hi = next_random()
            nums.append((hi * 32768 + next_random()) % top + 1)
        arrays.append(nums)
    calls = 0
    total = 0
    check = 0
    for _ in range(25):
        for a in range(len(arrays)):
            answer = min_operations(arrays[a])
            calls += 1
            total += answer
            check = (check * 31 + answer) % 1000000007
    print(f"{calls} calls: sum {total}, checksum {check}")


main()
