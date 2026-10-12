# Benchmark for #448: mirror of find_disappeared.kara (marking by sign)
# on one random array of 1,000,000 numbers with 300,000 missing, built
# once, copied and searched 20 times over.


def find_disappeared_numbers(nums):
    for i in range(len(nums)):
        x = abs(nums[i])
        if nums[x - 1] > 0:
            nums[x - 1] = -nums[x - 1]
    return [i + 1 for i in range(len(nums)) if nums[i] > 0]


seed = 448


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_index(below):
    return (next_random() * 32768 + next_random()) % below


def main():
    n, d, rounds = 1000000, 300000, 20
    # The first d of a shuffled 1..n twice, the next n - 2d once.
    values = list(range(1, n + 1))
    for i in range(n):
        j = i + random_index(n - i)
        values[i], values[j] = values[j], values[i]
    nums = values[: n - d] + values[:d]
    for i in range(n):
        j = i + random_index(n - i)
        nums[i], nums[j] = nums[j], nums[i]
    found = 0
    checksum = 0
    for round in range(rounds):
        missing = find_disappeared_numbers(list(nums))
        found += len(missing)
        for x in missing:
            checksum = (checksum * 31 + x + round) % 1000000007
    print(f"{rounds} rounds on {n} numbers: {found} missing, checksum {checksum}")


main()
