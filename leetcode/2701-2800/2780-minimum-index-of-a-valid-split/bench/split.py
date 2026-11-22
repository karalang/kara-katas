# LeetCode #2780: Minimum Index of a Valid Split -- the bench in Python:
# the ★ arm over 20 arrays of 10^5 numbers up to 10^9, each with a
# dominant number, all drawn first, then each answered 100 times.


def minimum_index(nums):
    n = len(nums)
    x = 0
    votes = 0
    for v in nums:
        if votes == 0:
            x = v
        votes += 1 if v == x else -1
    total = sum(1 for v in nums if v == x)
    left = 0
    for i in range(n - 1):
        if nums[i] == x:
            left += 1
        if 2 * left > i + 1 and 2 * (total - left) > n - i - 1:
            return i
    return -1


seed = 2780


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def dominated(n, others, top):
    x = wide() % top + 1
    many = n // 2 + 1 + wide() % (n - n // 2)
    nums = [x] * many
    while len(nums) < n:
        v = wide() % others + 1
        if v != x:
            nums.append(v)
    for i in range(n - 1, 0, -1):
        j = wide() % (i + 1)
        nums[i], nums[j] = nums[j], nums[i]
    return nums


def main():
    count = 20
    rounds = 100
    cases = [dominated(100000, 1000000000, 1000000000) for _ in range(count)]
    total = 0
    check = 0
    for r in range(rounds):
        for nums in cases:
            a = minimum_index(nums)
            total += a
            check = (check * 31 + a + 1 + r) % 1000000007
    print(f"{count} arrays of 10^5, {rounds} rounds: indices sum to {total}, checksum {check}")


main()
