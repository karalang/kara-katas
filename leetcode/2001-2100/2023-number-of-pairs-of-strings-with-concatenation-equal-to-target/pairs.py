# LeetCode #2023: Number of Pairs of Strings With Concatenation Equal to
# Target -- a Python mirror of the ★ arm (pairs.kara): count each string in
# a dict, then cut the target at every point. Same output, byte for byte.


def num_of_pairs(nums, target):
    count = {}
    for s in nums:
        count[s] = count.get(s, 0) + 1
    pairs = 0
    for k in range(1, len(target)):
        a = target[:k]
        b = target[k:]
        ca = count.get(a, 0)
        if a == b:
            pairs += ca * (ca - 1)
        else:
            pairs += ca * count.get(b, 0)
    return pairs


seed = 2023


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def digits(length, top):
    return "".join(chr(ord("1") + next_random() % top) for _ in range(length))


def show(nums):
    return "[" + ", ".join(nums) + "]"


def main():
    examples = [
        (["777", "7", "77", "77"], "7777"),
        (["123", "4", "12", "34"], "1234"),
        (["1", "1", "1"], "11"),
        (["1", "2"], "12"),
        (["12", "12"], "1212"),
        (["1", "11", "111"], "1111"),
        (["5", "55"], "555"),
        (["21", "12", "2", "1"], "2112"),
    ]
    for nums, target in examples:
        print(f"{show(nums)}, {target} -> {num_of_pairs(nums, target)}")
    total = 0
    check = 0
    for _ in range(3000):
        n = next_random() % 9 + 2
        nums = []
        for _ in range(n):
            length = next_random() % 4 + 1
            nums.append(digits(length, 2))
        if next_random() % 2 == 0:
            i = next_random() % n
            j = next_random() % n
            target = nums[i] + nums[j]
        else:
            length = next_random() % 7 + 2
            target = digits(length, 2)
        pairs = num_of_pairs(nums, target)
        total += pairs
        check = (check * 31 + pairs) % 1000000007
    print(f"3000 problems of up to 10 strings: {total} pairs, checksum {check}")
    total = 0
    check = 0
    for p in range(5):
        if p < 4:
            nums = ["7" * (next_random() % 100 + 1) for _ in range(100)]
        else:
            nums = []
            for _ in range(100):
                length = next_random() % 3 + 1
                nums.append(digits(length, 3))
        target = "7" * [2, 51, 100, 199][p] if p < 4 else nums[7] + nums[7]
        pairs = num_of_pairs(nums, target)
        total += pairs
        check = (check * 31 + pairs) % 1000000007
    print(f"5 problems of 100 strings: {total} pairs, checksum {check}")


main()
