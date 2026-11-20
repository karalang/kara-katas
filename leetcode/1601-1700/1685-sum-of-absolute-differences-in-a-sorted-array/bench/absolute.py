# LeetCode #1685: Sum of Absolute Differences in a Sorted Array -- the
# bench's Python mirror: the ★ arm on 50 random sorted arrays of 100000
# values, all drawn first, each answered 20 times.


def sum_differences(nums):
    n = len(nums)
    total = sum(nums)
    before = 0
    result = []
    for i in range(n):
        x = nums[i]
        after = total - before - x
        result.append(x * i - before + after - x * (n - 1 - i))
        before += x
    return result


seed = 1685


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, size, rounds = 50, 100000, 20
    arrays = []
    for _ in range(count):
        arrays.append(sorted(next_random() % 10000 + 1 for _ in range(size)))
    total = 0
    check = 0
    for r in range(rounds):
        for nums in arrays:
            answer = sum_differences(nums)
            first, middle, last = answer[0], answer[size // 2], answer[size - 1]
            total += middle
            check = (check * 31 + first + middle + last + r) % 1000000007
    print(f"{count} arrays of {size} values, {rounds} rounds: middles sum to {total}, checksum {check}")


main()
