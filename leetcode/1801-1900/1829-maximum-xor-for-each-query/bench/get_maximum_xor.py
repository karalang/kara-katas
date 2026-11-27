# LeetCode #1829: Maximum XOR for Each Query -- the bench in Python: the ★ arm
# over 200 calls on the first 50000 to 99999 of one sorted list of 10^5
# numbers below 2^20, built once, each run's length drawn from the checksum so
# far, and maximumBit 20. Each call copies its run, as the arm takes its list
# by value.


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


base = []
for _ in range(100000):
    hi = next_random()
    base.append((hi * 32768 + next_random()) % 1048576)
base.sort()
check = 0
for call in range(200):
    n = 50000 + (check + call) % 50000
    answer = get_maximum_xor(base[:n], 20)
    check = (check * 31 + sum(answer) % 1000000007) % 1000000007
print(f"200 calls: checksum {check}")
