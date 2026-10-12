# Benchmark for #453: mirror of min_moves.kara (the ★ arm, sum minus n
# times the minimum) on the same workload.


def min_moves(nums):
    smallest = nums[0]
    total = 0
    for x in nums:
        if x < smallest:
            smallest = x
        total += x
    return total - len(nums) * smallest


# ---- benchmark --------------------------------------------------------

seed = 453


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_value():
    hi = next_random()
    lo = next_random()
    return (hi * 65536 + lo) % 2000000001 - 1000000000


def main():
    arrays = 10
    n = 1000000
    rounds = 20
    all_nums = []
    for _ in range(arrays):
        all_nums.append([random_value() for _ in range(n)])
    total = 0
    checksum = 0
    for _ in range(rounds):
        for a in range(arrays):
            hi = next_random()
            lo = next_random()
            at = (hi * 65536 + lo) % n
            all_nums[a][at] = random_value()
            moves = min_moves(all_nums[a])
            total += moves
            checksum = (checksum * 31 + moves % 1000000007) % 1000000007
    print(f"{rounds} rounds on {arrays} arrays of {n}: {total} moves, checksum {checksum}")


main()
