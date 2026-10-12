# Benchmark for #421: mirror of maximum_xor.kara (prefix bits).
import sys


def find_maximum_xor(nums):
    answer = 0
    mask = 0
    bit = 30
    while bit >= 0:
        mask |= 1 << bit
        prefixes = set()
        for x in nums:
            prefixes.add(x & mask)
        candidate = answer | (1 << bit)
        for p in prefixes:
            if p ^ candidate in prefixes:
                answer = candidate
                break
        bit -= 1
    return answer


seed = 421


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random31():
    high = step()
    low = step()
    bit = step() % 2
    return high * 65536 + low * 2 + bit


rounds = int(sys.argv[1]) if len(sys.argv) > 1 else 100
n = 20000
nums = [random31() for _ in range(n)]
total = 0
checksum = 0
for r in range(rounds):
    nums[r * 7919 % n] = random31()
    answer = find_maximum_xor(nums)
    total += answer
    checksum = (checksum * 31 + answer) % 1000000007
print(f"{rounds} rounds on {n} numbers: total {total}, checksum {checksum}")
