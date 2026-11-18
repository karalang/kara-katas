# LeetCode #2270: Number of Ways to Split Array -- the Python mirror of
# the ★ arm, `split.kara`, line for line. Its output is byte-identical.


def ways_to_split_array(nums):
    total = sum(nums)
    left = 0
    ways = 0
    for i in range(len(nums) - 1):
        left += nums[i]
        if left >= total - left:
            ways += 1
    return ways


seed = 2270


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def values(n, spread):
    return [next_random() % (2 * spread + 1) - spread for _ in range(n)]


def show(v):
    return "[" + ", ".join(map(str, v)) + "]"


def main():
    examples = [
        [10, 4, -8, 7],
        [2, 3, 1, 0],
        [1, 2],
        [5, 5],
        [-1, -2, -3, -4],
        [1, 2, 3, 4, 5, 6],
        [100000, -1, -1, -1, 99999],
    ]
    for nums in examples:
        print(f"{show(nums)} -> {ways_to_split_array(nums)}")
    check = 0
    for t in range(2000):
        n = next_random() % 39 + 2
        nums = values(n, [1, 10, 1000, 100000][t % 4])
        check = (check * 31 + ways_to_split_array(nums)) % 1000000007
    print(f"2000 arrays: checksum {check}")
    rand = values(100000, 100000)
    high = [100000] * 100000
    swing = [-100000 if i % 2 == 0 else 100000 for i in range(100000)]
    answers = [ways_to_split_array(rand), ways_to_split_array(high), ways_to_split_array(swing)]
    print(f"10^5 values: {show(answers)}")


main()
