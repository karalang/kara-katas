# LeetCode #1224: Maximum Equal Frequency -- the Python mirror of the ★
# arm: walk the prefixes keeping each number's count and how many numbers
# have each count, and test the three shapes a removable prefix can have.

seed = 1224


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def max_equal_freq(nums):
    top = max(nums)
    count = [0] * (top + 1)
    with_count = [0] * (len(nums) + 1)
    most = 0
    best = 0
    for k, x in enumerate(nums):
        with_count[count[x]] -= 1
        count[x] += 1
        with_count[count[x]] += 1
        most = max(most, count[x])
        length = k + 1
        if most == 1 or with_count[most] * most + 1 == length or (with_count[most - 1] + 1) * (most - 1) + 1 == length:
            best = length
    return best


def main():
    print(max_equal_freq([2, 2, 1, 1, 5, 3, 3, 5]))
    print(max_equal_freq([1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5]))
    print(max_equal_freq([1, 1]))
    print(max_equal_freq([1, 2, 3, 4, 5, 6, 7, 8, 9]))
    total = 0
    check = 0
    for _ in range(1000):
        n = next_random() % 30 + 2
        values = next_random() % 6 + 1
        nums = [next_random() % values + 1 for _ in range(n)]
        answer = max_equal_freq(nums)
        total += answer
        check = (check * 131 + answer) % 1000000007
    print(f"1000 random arrays of 2 to 31 numbers: lengths total {total}, checksum {check}")
    rising = list(range(1, 100001))
    blocks = []
    for v in range(1, 317):
        blocks.extend([v] * 316)
    blocks.append(317)
    wide = [next_random() % 100000 + 1 for _ in range(100000)]
    print(f"10^5 numbers: all different {max_equal_freq(rising)}, 316 blocks of 316 and one more {max_equal_freq(blocks)}, random {max_equal_freq(wide)}")


main()
