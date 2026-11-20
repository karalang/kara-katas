# LeetCode #1664: Ways to Make a Fair Array -- the Python mirror of the ★
# arm (one pass with running sums).


def ways_to_make_fair(nums):
    total = [0, 0]
    for i, x in enumerate(nums):
        total[i % 2] += x
    before = [0, 0]
    ways = 0
    for i, x in enumerate(nums):
        p = i % 2
        after = [total[0] - before[0], total[1] - before[1]]
        after[p] -= x
        if before[0] + after[1] == before[1] + after[0]:
            ways += 1
        before[p] += x
    return ways


# ---- the harness: the same in every arm --------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def batch(count, longest, top):
    total = 0
    check = 0
    for _ in range(count):
        n = (next_random() * 32768 + next_random()) % longest + 1
        nums = [next_random() % top + 1 for _ in range(n)]
        answer = ways_to_make_fair(nums)
        total += answer
        check = (check * 31 + answer + 1) % 1000000007
    print(f"{count} arrays of up to {longest} values up to {top}: {total} fair removals, checksum {check}")


print(ways_to_make_fair([2, 1, 6, 4]))
print(ways_to_make_fair([1, 1, 1]))
print(ways_to_make_fair([1, 2, 3]))
print(ways_to_make_fair([7]))
print(ways_to_make_fair([5, 5]))
print(ways_to_make_fair([1, 1, 1, 1, 1, 1, 1]))
seed = 1664
batch(3000, 8, 3)
batch(300, 1000, 10)
batch(10, 100000, 2)
