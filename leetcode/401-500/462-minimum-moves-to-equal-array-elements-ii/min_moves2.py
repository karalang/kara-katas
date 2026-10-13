# LeetCode #462: Minimum Moves to Equal Array Elements II -- Python mirror
# of min_moves2.kara (the star arm, the median of the sorted numbers).


def min_moves2(nums):
    s = sorted(nums)
    median = s[len(s) // 2]
    moves = 0
    for x in s:
        moves += abs(x - median)
    return moves


def show(nums):
    moves = min_moves2(list(nums))
    print(f"[{', '.join(str(x) for x in nums)}] -> {moves}")


seed = 462


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    show([1, 2, 3])
    show([1, 10, 2, 9])
    show([7])
    show([4, -4])
    show([5, 5, 5, 5])
    show([-1000000000, 1000000000, 0])
    show([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5])
    show([1, 1, 1, 1000000000])
    count = 300
    total = 0
    checksum = 0
    for _ in range(count):
        n = 1 + next_random() % 200
        spread = [5, 1000, 1000000000][next_random() % 3]
        nums = []
        for _ in range(n):
            a = next_random()
            b = next_random()
            c = next_random()
            r = ((a * 32768 + b) * 32768 + c) % (2 * spread + 1)
            nums.append(r - spread)
        moves = min_moves2(nums)
        total += moves
        checksum = (checksum * 31 + moves % 1000003) % 1000000007
    print(f"{count} random arrays: {total} moves in all, checksum {checksum}")


main()
