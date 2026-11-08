# LeetCode #1512: Number of Good Pairs -- the Python mirror of the ★ arm:
# walking left to right, each number pairs with every earlier copy of
# itself; the counts sit in a table of 101.


def num_identical_pairs(nums):
    seen = [0] * 101
    pairs = 0
    for x in nums:
        pairs += seen[x]
        seen[x] += 1
    return pairs


seed = 1512


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def batch(count, most, top):
    check = 0
    for _ in range(count):
        n = next_random() % most + 1
        nums = [next_random() % top + 1 for _ in range(n)]
        check = mix(check, num_identical_pairs(nums))
    return check


print(f"[1, 2, 3, 1, 1, 3] -> {num_identical_pairs([1, 2, 3, 1, 1, 3])}")
print(f"[1, 1, 1, 1] -> {num_identical_pairs([1, 1, 1, 1])}")
print(f"[1, 2, 3] -> {num_identical_pairs([1, 2, 3])}")
print(f"[7] -> {num_identical_pairs([7])}")
print(f"100 copies of 100 -> {num_identical_pairs([100] * 100)}")
print(f"3000 arrays of 1 to 100 numbers up to 10: checksum {batch(3000, 100, 10)}")
print(f"300 arrays of 1 to 100 numbers up to 100: checksum {batch(300, 100, 100)}")
print(f"3 arrays of 1 to 100000 numbers up to 100: checksum {batch(3, 100000, 100)}")
