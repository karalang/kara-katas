# LeetCode #2708: Maximum Strength of a Group -- the bench (strength.kara
# in Python): every non-zero number multiplied in, and an odd negative,
# the one nearest zero, divided back out.


def max_strength(nums):
    if len(nums) == 1:
        return nums[0]
    product = 1
    taken = 0
    negatives = 0
    nearest = -10
    for v in nums:
        if v != 0:
            product *= v
            taken += 1
        if v < 0:
            negatives += 1
            nearest = max(nearest, v)
    if negatives % 2 == 1:
        product //= nearest
        taken -= 1
    return product if taken > 0 else 0


seed = 2708


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def trunc_mod(a, m):
    # Kara's and C's remainder takes the dividend's sign
    r = abs(a) % m
    return -r if a < 0 else r


groups, rounds = 1000000, 10
everything = []
for _ in range(groups):
    n = next_random() % 13 + 1
    everything.append([next_random() % 19 - 9 for _ in range(n)])
total = 0
check = 0
for r in range(rounds):
    for nums in everything:
        strength = max_strength(nums)
        total += trunc_mod(strength, 1000)
        check = (check * 31 + strength % 1000000007 + r) % 1000000007
print(f"{groups} groups of 1 to 13, {rounds} rounds: strengths mod 1000 sum to {total}, checksum {check}")
