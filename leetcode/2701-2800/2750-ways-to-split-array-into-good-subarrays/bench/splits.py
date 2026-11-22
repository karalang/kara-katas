# LeetCode #2750: Ways to Split Array Into Good Subarrays -- the bench
# (splits.kara in Python): the product of the distances between
# neighbouring 1s, mod 10^9 + 7.

MOD = 1000000007


def number_of_good_subarray_splits(nums):
    ways = 1
    last = None
    for i, x in enumerate(nums):
        if x == 1:
            if last is not None:
                ways = ways * (i - last) % MOD
            last = i
    return 0 if last is None else ways


seed = 2750


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, rounds = 50, 20
    arrays = []
    for _ in range(count):
        percent = next_random() % 30 + 1
        arrays.append([1 if next_random() % 100 < percent else 0 for _ in range(100000)])
    total = check = 0
    for r in range(rounds):
        for nums in arrays:
            ways = number_of_good_subarray_splits(nums)
            total += ways
            check = (check * 31 + ways + r) % 1000000007
    print(f"{count} arrays of 100000, {rounds} rounds: ways sum to {total}, checksum {check}")


main()
