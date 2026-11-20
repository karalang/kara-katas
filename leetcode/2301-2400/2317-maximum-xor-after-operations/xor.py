# LeetCode #2317: Maximum XOR After Operations -- the Python mirror of
# the ★ arm. The operation can clear any of a number's bits and set
# none, so the most is the OR of all the numbers.

seed = 2317


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def maximum_xor(nums):
    every = 0
    for x in nums:
        every |= x
    return every


for nums in [[3, 2, 4, 6], [1, 2, 3, 9, 2], [0], [12345], [5, 5], [100000000, 67108864, 33554432]]:
    print(maximum_xor(nums))
big = []
for _ in range(100000):
    hi = next_random()
    value = (hi * 32768 + next_random()) % 100000001
    big.append(value & (next_random() * 4096))
print(maximum_xor(big))
check = 0
ones = 0
for _ in range(1000):
    n = next_random() % 30 + 1
    top = 1 << (next_random() % 27 + 1)
    nums = []
    for _ in range(n):
        hi = next_random()
        nums.append((hi * 32768 + next_random()) % top)
    best = maximum_xor(nums)
    check = (check * 31 + best) % 1000000007
    ones += bin(best).count("1")
print(f"1000 arrays: checksum {check}, {ones} bits set in all")
