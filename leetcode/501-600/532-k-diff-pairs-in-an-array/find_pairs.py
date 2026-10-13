# LeetCode #532: K-diff Pairs in an Array -- Python mirror of the ★ arm
# (count each number); see find_pairs.kara. Same algorithm, same
# harness, same output.


def find_pairs(nums, k):
    counts = {}
    for x in nums:
        counts[x] = counts.get(x, 0) + 1
    pairs = 0
    for v, c in counts.items():
        if k == 0:
            if c >= 2:
                pairs += 1
        elif v + k in counts:
            pairs += 1
    return pairs


# ---- test harness ---------------------------------------------------------

seed = 532


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(name, nums, k):
    print(f"{name}: {nums}, k = {k} -> {find_pairs(nums, k)}")


def main():
    show("example 1", [3, 1, 4, 1, 5], 2)
    show("example 2", [1, 2, 3, 4, 5], 1)
    show("example 3", [1, 3, 1, 5, 4], 0)
    show("no repeats, k = 0", [4, 2, 9], 0)
    show("all equal, k = 0", [7, 7, 7, 7], 0)
    show("all equal, k = 1", [7, 7, 7, 7], 1)
    show("one number", [5], 0)
    show("negatives", [-1, -2, -3, -1], 1)
    show("the extremes", [0, 10000000, -10000000], 10000000)
    total = checksum = 0
    for t in range(300):
        half = 10 if t % 3 == 0 else 100 if t % 3 == 1 else 10000000
        size = 1 + next_random() % 50
        nums = []
        for _ in range(size):
            high = next_random()
            nums.append((high * 32768 + next_random()) % (2 * half + 1) - half)
        k = abs(nums[0]) if t % 3 == 2 else next_random() % 5
        answer = find_pairs(nums, k)
        total += answer
        checksum = (checksum * 31 + answer) % 1000000007
    print(f"300 random arrays: {total} pairs, checksum {checksum}")
    nums = [next_random() % 10001 - 5000 for _ in range(10000)]
    print(f"10000 numbers: k = 0 -> {find_pairs(nums, 0)}, k = 1 -> {find_pairs(nums, 1)}, k = 7 -> {find_pairs(nums, 7)}")


main()
