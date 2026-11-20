# LeetCode #1224 bench, Python mirror of the Kāra ★ arm: each number's
# count and how many numbers have each count, over 10 random arrays of 10^5
# numbers drawn once, 5 passes; checksum of the answers.

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
    arrays = []
    for a in range(10):
        values = 2 << a
        arrays.append([next_random() % values + 1 for _ in range(100000)])
    total = 0
    check = 0
    for _ in range(5):
        for nums in arrays:
            answer = max_equal_freq(nums)
            total += answer
            check = (check * 131 + answer) % 1000000007
    print(f"10 arrays of 10^5 numbers, 5 passes: lengths total {total}, checksum {check}")


main()
