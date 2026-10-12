# LeetCode #453: Minimum Moves to Equal Array Elements -- mirror of
# min_moves.kara (sum minus n times the minimum), with the same harness.


def min_moves(nums):
    smallest = nums[0]
    total = 0
    for x in nums:
        smallest = min(smallest, x)
        total += x
    return total - len(nums) * smallest


# ---- test harness ---------------------------------------------------------


def listed(nums):
    return ",".join(str(x) for x in nums)


def show(nums):
    print(f"[{listed(nums)}]: {min_moves(nums)} moves")


seed = 453


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    show([1, 2, 3])
    show([1, 1, 1])
    show([5])
    show([3, 1])
    show([-1000000000, 1000000000])
    show([1000000000, 1000000000, -1000000000])
    show([0, 0, 0, 0, 100])
    show([7, 3, 9, 3, 12, 5])
    # 300 random arrays of 1 to 200 numbers, spread over 1, 10, 1,000
    # or the full range from -10^9 to 10^9.
    count = 300
    total = 0
    checksum = 0
    for _ in range(count):
        n = 1 + next_random() % 200
        spread = [1, 10, 1000, 2000000001][next_random() % 4]
        nums = []
        for _ in range(n):
            r = next_random() * 65536
            r += next_random()
            # Kara's % truncates toward zero; r is never negative here.
            nums.append(r % spread - spread // 2)
        moves = min_moves(nums)
        total += moves
        checksum = (checksum * 31 + moves % 1000000007) % 1000000007
    print(f"{count} random arrays: {total} moves, checksum {checksum}")


main()
