# LeetCode #1822: Sign of the Product of an Array -- the bench in Python:
# the ★ arm over 300000 calls on runs of 500 to 999 numbers cut from one
# list of 2000 numbers from -100 to 100 but zero, built once, each run's
# start and length drawn from the checksum so far.


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


base = []
for _ in range(2000):
    x = next_random() % 200 - 100
    base.append(x + 1 if x >= 0 else x)
check = 0
for call in range(300000):
    start = (check + call) % 1000
    n = 500 + (check * 7 + call) % 500
    check = (check * 3 + array_sign(base[start:start + n]) + 1) % 1000000007
print(f"300000 calls: checksum {check}")
