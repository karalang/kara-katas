# LeetCode #2453: Destroy Sequential Targets -- bench, Python mirror of
# targets.kara: a dict counts each residue class, and a second pass keeps
# the least value of a largest class.


def destroy_targets(nums, space):
    count = {}
    for x in nums:
        count[x % space] = count.get(x % space, 0) + 1
    best = 0
    answer = 0
    for x in nums:
        c = count[x % space]
        if c > best or (c == best and x < answer):
            best = c
            answer = x
    return answer


seed = 2453


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    n = 100000
    arrays = []
    for _ in range(10):
        nums = []
        for _ in range(n):
            hi = next_random()
            nums.append(1 + (hi * 32768 + next_random()) % 1000000000)
        arrays.append(nums)
    check = 0
    for p in range(50):
        for a in range(10):
            arrays[a][(p * 7919 + a) % n] = 1 + check % 1000000000
            space = 1 + (p * 7919 + a * 104729) % 100000
            check = (check * 31 + destroy_targets(arrays[a], space) + p) % 1000000007
    print(f"50 passes over 10 arrays of 10^5 values: checksum {check}")


main()
