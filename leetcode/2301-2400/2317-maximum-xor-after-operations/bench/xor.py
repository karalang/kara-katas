# LeetCode #2317: Maximum XOR After Operations -- the bench, the ★ arm in
# Python. The operation can clear any of a number's bits and set none, so
# the most is the OR of all the numbers.

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


arrays = []
for a in range(20):
    mask = 0
    for _ in range(a + 4):
        mask |= 1 << (next_random() % 27)
    nums = []
    for _ in range(100000):
        hi = next_random()
        nums.append((hi * 32768 + next_random()) % 100000001 & mask)
    arrays.append(nums)
check = 0
for p in range(100):
    for a in range(20):
        check = (check * 31 + maximum_xor(arrays[(a + p) % 20])) % 1000000007
print(f"100 passes over 20 arrays of 10^5 numbers: checksum {check}")
