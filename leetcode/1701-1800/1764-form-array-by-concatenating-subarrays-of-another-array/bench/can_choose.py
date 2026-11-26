# LeetCode #1764: Form Array by Concatenating Subarrays of Another Array --
# the bench in Python, mirroring can_choose.kara: greedy, each group
# matched at the first place it fits, compared value by value.
import sys

def can_choose(groups, nums):
    at = 0
    for group in groups:
        n = len(group)
        while True:
            if at + n > len(nums):
                return False
            if all(nums[at + i] == group[i] for i in range(n)):
                break
            at += 1
        at += n
    return True

seed = 1764
def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536

def random_values(n, values):
    return [next_random() % values for _ in range(n)]

def random_case(k, most, values, gap, break_one):
    groups, nums = [], []
    for _ in range(k):
        filler = next_random() % (gap + 1)
        nums.extend(random_values(filler, values))
        n = 1 + next_random() % most
        group = random_values(n, values)
        nums.extend(group)
        groups.append(group)
    if break_one:
        g = next_random() % k
        at = next_random() % len(groups[g])
        groups[g][at] = next_random() % values
    return groups, nums

def main():
    calls = int(sys.argv[1]) if len(sys.argv) > 1 else 200000
    cases = [random_case(10, 40, 2, 60, i % 2 == 1) for i in range(200)]
    check = 0
    for call in range(calls):
        g, n = cases[(check + call * 7919) % 200]
        check = (check * 31 + (1 if can_choose(g, n) else 0) + call % 7) % 1000000007
    print(f"{calls} calls over 200 cases: checksum {check}")

main()
