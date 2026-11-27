# LeetCode #1822: Sign of the Product of an Array -- the ★ arm in Python


def array_sign(nums):
    sign = 1
    for x in nums:
        if x == 0:
            return 0
        if x < 0:
            sign = -sign
    return sign


seed = 1822


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


f = array_sign
print(f([-1, -2, -3, -4, 3, 2, 1]), f([1, 5, 0, 2, -3]), f([-1, 1, -1, 1, -1]))
print(f([7]), f([-7]), f([0]), f([-100, 100]), f([-100, -100, -100]), f([-1, -1, -1, 0]))
n = 1000
print(f"the most: {f([-100] * n)} {f([-100] * (n - 1) + [1])}")
check = 0
tally = [0, 0, 0]
for _ in range(3000):
    ln = 1 + next_random() % 12
    nums = []
    for _ in range(ln):
        x = next_random() % 201 - 100
        nums.append(0 if next_random() % 30 == 0 else x)
    sign = f(nums)
    tally[sign + 1] += 1
    check = (check * 3 + sign + 1) % 1000000007
print(f"3000 random cases: {tally[0]} negative, {tally[1]} zero, {tally[2]} positive, checksum {check}")
