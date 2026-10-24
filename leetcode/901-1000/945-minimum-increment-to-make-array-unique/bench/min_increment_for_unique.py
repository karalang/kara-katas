# Benchmark: LeetCode #945 Minimum Increment to Make Array Unique -- the
# ★ arm, sorted and raised, on arrays of 100000 values, LeetCode's
# longest. Mirrors min_increment_for_unique.kara, .c, .rs and go-seq/.


def min_increment_for_unique(nums):
    a = sorted(nums)
    moves = 0
    floor = -1
    for v in a:
        end = max(v, floor + 1)
        moves += end - v
        floor = end
    return moves


seed = 945


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds, count, n = 5, 20, 100000
    arrays = []
    for _ in range(count):
        range_ = 70001 + next_random() * 4 % 30001
        nums = []
        for _ in range(n):
            wide = next_random() * 32768
            wide += next_random()
            nums.append(wide % range_)
        arrays.append(nums)
    total = 0
    check = 0
    for r in range(rounds):
        for i in range(count):
            m = min_increment_for_unique(arrays[(r + i) % count])
            total += m
            check = (check * 1000003 + m) % 1000000007
    print(f"{rounds} rounds over {count} arrays of {n} values: {total} moves, checksum {check}")


main()
