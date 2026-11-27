# LeetCode #1829: Maximum XOR for Each Query -- the ★ arm in Python


def get_maximum_xor(nums, maximum_bit):
    mask = (1 << maximum_bit) - 1
    total = 0
    for x in nums:
        total ^= x
    answer = []
    for i in range(len(nums) - 1, -1, -1):
        answer.append(total ^ mask)
        total ^= nums[i]
    return answer


seed = 1829


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


print(show(get_maximum_xor([0, 1, 1, 3], 2)), show(get_maximum_xor([2, 3, 4, 7], 3)), show(get_maximum_xor([0, 1, 2, 2, 5, 7], 3)))
print(show(get_maximum_xor([0], 1)), show(get_maximum_xor([7], 3)), show(get_maximum_xor([5, 5, 5, 5], 3)), show(get_maximum_xor([0, 1, 1048575], 20)))
big = []
for _ in range(100000):
    hi = next_random()
    big.append((hi * 32768 + next_random()) % 1048576)
big.sort()
answer = get_maximum_xor(big, 20)
print(f"the most: {sum(answer)} {answer[0]} {answer[99999]}")
check = 0
for _ in range(3000):
    bits = 1 + next_random() % 5
    n = 1 + next_random() % 10
    nums = sorted(next_random() % (1 << bits) for _ in range(n))
    for k in get_maximum_xor(nums, bits):
        check = (check * 31 + k) % 1000000007
print(f"3000 random cases: checksum {check}")
