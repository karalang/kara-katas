# LeetCode #2750: Ways to Split Array Into Good Subarrays -- the ★ arm in
# Python (splits.kara): the product of the distances between neighbouring
# 1s, mod 10^9 + 7, and 0 with no 1 at all.

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


def random_bits(n, percent):
    return [1 if next_random() % 100 < percent else 0 for _ in range(n)]


def main():
    print(number_of_good_subarray_splits([0, 1, 0, 0, 1]))
    print(number_of_good_subarray_splits([0, 1, 0]))
    print(number_of_good_subarray_splits([0] * 10))
    print(number_of_good_subarray_splits([1] * 100000))
    print(number_of_good_subarray_splits([1 - i % 2 for i in range(100000)]))
    total = check = 0
    for _ in range(3000):
        n = next_random() % 20 + 1
        percent = next_random() % 100
        ways = number_of_good_subarray_splits(random_bits(n, percent))
        total += ways
        check = (check * 31 + ways) % 1000000007
    print(f"3000 small arrays: ways sum to {total}, checksum {check}")
    total = check = 0
    for _ in range(20):
        percent = next_random() % 30 + 1
        ways = number_of_good_subarray_splits(random_bits(100000, percent))
        total += ways
        check = (check * 31 + ways) % 1000000007
    print(f"20 arrays of 100000: ways sum to {total}, checksum {check}")


main()
