# LeetCode #1827: Minimum Operations to Make the Array Increasing -- the bench
# in Python: the ★ arm over 10000 calls on runs of 2500 to 4999 numbers cut
# from one list of 10^4 numbers from 1 to 10^4, built once, each run's start
# and length drawn from the checksum so far.


def min_operations(nums):
    operations = 0
    last = 0
    for x in nums:
        if x <= last:
            last += 1
            operations += last - x
        else:
            last = x
    return operations


seed = 1827


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


base = [1 + next_random() % 10000 for _ in range(10000)]
check = 0
for call in range(10000):
    start = (check + call) % 5000
    length = 2500 + (check * 7 + call) % 2500
    run = base[start:start + length]
    check = (check * 31 + min_operations(run)) % 1000000007
print(f"10000 calls: checksum {check}")
