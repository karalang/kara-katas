# LeetCode #2442: Count Number of Distinct Integers After Reverse
# Operations -- the bench, the ★ arm: the digits reversed by % 10 and
# // 10, and a table of flags up to the largest value.


def reversed_digits(x):
    r = 0
    y = x
    while y > 0:
        r = r * 10 + y % 10
        y //= 10
    return r


def count_distinct_integers(nums):
    values = nums[:]
    for x in nums:
        values.append(reversed_digits(x))
    largest = 0
    for v in values:
        largest = max(largest, v)
    seen = [False] * (largest + 1)
    count = 0
    for v in values:
        if not seen[v]:
            seen[v] = True
            count += 1
    return count


seed = 2442


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return 1 + (a * 32768 + next_random()) % 1000000


def main():
    arrays = [[wide() for _ in range(100000)] for _ in range(4)]
    check = 0
    for p in range(40):
        for c in range(len(arrays)):
            at = (p * 7919 + c * 104729) % 100000
            arrays[c][at] = wide()
            check = (check * 31 + count_distinct_integers(arrays[c]) + p) % 1000000007
    print(f"40 passes over 4 arrays of 10^5 values: checksum {check}")


main()
