# Benchmark for #442: mirror of find_duplicates.kara (marking by sign) on
# one random array of 1,000,000 numbers with 300,000 duplicates, built
# once, copied and searched 20 times over.


def find_duplicates(nums):
    duplicates = []
    for i in range(len(nums)):
        x = abs(nums[i])
        if nums[x - 1] < 0:
            duplicates.append(x)
        else:
            nums[x - 1] = -nums[x - 1]
    return duplicates


seed = 442


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
        duplicates = find_duplicates(list(nums))
        found += len(duplicates)
        for x in duplicates:
            checksum = (checksum * 31 + x + round) % 1000000007
    print(f"{rounds} rounds on {n} numbers: {found} duplicates, checksum {checksum}")


main()
