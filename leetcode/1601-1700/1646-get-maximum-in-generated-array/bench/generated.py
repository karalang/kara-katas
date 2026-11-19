# LeetCode #1646: Get Maximum in Generated Array -- the bench's Python
# mirror: the ★ arm on 4000000 random n from 0 to 100, all drawn first.

CASES = 4000000


def get_maximum_generated(n):
    if n == 0:
        return 0
    nums = [0] * (n + 1)
    nums[1] = 1
    best = 1
    for i in range(2, n + 1):
        nums[i] = nums[i // 2] if i % 2 == 0 else nums[i // 2] + nums[i // 2 + 1]
        best = max(best, nums[i])
    return best


seed = 1646


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


ns = [next_random() % 101 for _ in range(CASES)]
check = 0
total = 0
for n in ns:
    found = get_maximum_generated(n)
    total += found
    check = (check * 31 + found + 1) % 1000000007
print(f"{CASES} random n up to 100: maxima sum to {total}, checksum {check}")
