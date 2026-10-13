# Benchmark for #462: mirror of min_moves2.kara (the star arm: sort, take
# the median) on the same workload.


def min_moves2(nums):
    nums.sort()
    median = nums[len(nums) // 2]
    moves = 0
    for x in nums:
        moves += abs(x - median)
    return moves


def main():
    n = 1000000
    rounds = 10
    seed = 462
    spread = 1000000000

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    def random_number():
        a = next_random()
        b = next_random()
        c = next_random()
        return ((a * 32768 + b) * 32768 + c) % (2 * spread + 1) - spread

    nums = [random_number() for _ in range(n)]
    total = 0
    checksum = 0
    for _ in range(rounds):
        hi = next_random()
        lo = next_random()
        k = (hi * 65536 + lo) % n
        nums[k] = random_number()
        moves = min_moves2(list(nums))
        total += moves
        checksum = (checksum * 31 + moves % 1000003) % 1000000007
    print(f"{rounds} rounds on {n} numbers: {total} moves in all, checksum {checksum}")


main()
