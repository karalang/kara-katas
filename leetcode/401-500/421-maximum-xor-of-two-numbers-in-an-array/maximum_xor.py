# LeetCode #421: Maximum XOR of Two Numbers in an Array -- mirror of
# maximum_xor.kara (prefix bits).


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


def show(nums):
    print(f"[{', '.join(str(x) for x in nums)}]: {find_maximum_xor(nums)}")


show([3, 10, 5, 25, 2, 8])
show([14, 70, 53, 83, 49, 91, 36, 80, 92, 51, 66, 70])
show([0])
show([7, 7, 7])
show([0, 2147483647])
show([1, 2, 4, 8, 16, 32])
show([1073741824, 1073741823, 0])
show([8, 9, 10, 11, 12, 13, 14, 15])
show([5, 6])
show([2147483647, 2147483646, 1073741824, 536870912])
total = 0
checksum = 0
for _ in range(2000):
    n = 1 + step() % 50
    limit = 1 << (1 + step() % 31)
    nums = []
    for _ in range(n):
        high = step()
        low = step()
        bit = step() % 2
        nums.append((high * 65536 + low * 2 + bit) % limit)
    answer = find_maximum_xor(nums)
    total += answer
    checksum = (checksum * 31 + answer) % 1000000007
print(f"2000 random arrays: total {total}, checksum {checksum}")
