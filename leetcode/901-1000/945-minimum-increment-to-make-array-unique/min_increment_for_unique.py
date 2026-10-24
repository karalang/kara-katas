# LeetCode #945: Minimum Increment to Make Array Unique -- sorted, raised.
# Mirrors min_increment_for_unique.kara (the ★ arm) and its harness.


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


def show(nums):
    return "[" + ",".join(str(v) for v in nums) + "]"


def moves_text(m):
    return "1 move" if m == 1 else f"{m} moves"


def main():
    examples = [
        [1, 2, 2],
        [3, 2, 1, 2, 1, 7],
        [0],
        [5, 5, 5, 5],
        [1, 2, 3],
        [100000, 100000],
        [0, 0, 2, 2],
        [4, 0, 4, 1, 1, 2],
    ]
    for nums in examples:
        print(f"{show(nums)}: {moves_text(min_increment_for_unique(nums))}")
    values = 0
    moves = 0
    check = 0
    for _ in range(300):
        n = 1 + next_random() % 50
        nums = [next_random() % 31 for _ in range(n)]
        m = min_increment_for_unique(nums)
        values += n
        moves += m
        check = (check * 31 + m) % 1000000007
    print(f"300 random arrays of {values} values: {moves} moves, checksum {check}")
    random = []
    for _ in range(100000):
        wide = next_random() * 32768
        wide += next_random()
        random.append(wide % 100001)
    print(f"100000 random values: {min_increment_for_unique(random)} moves")
    distinct = [99999 - v for v in range(100000)]
    print(f"100000 distinct values, falling: {min_increment_for_unique(distinct)} moves")
    pairs = [v // 2 * 2 for v in range(100000)]
    print(f"each even number from 0 to 99998 twice: {min_increment_for_unique(pairs)} moves")
    same = [100000] * 65536
    print(f"65536 times 100000: {min_increment_for_unique(same)} moves")


main()
