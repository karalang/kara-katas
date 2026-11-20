# LeetCode #2354: Number of Excellent Pairs -- the bench, the ★ arm in
# Python: the distinct values tallied by their count of set bits, then
# every two tallies whose bits reach k multiplied.


def count_excellent_pairs(nums, k):
    by_bits = [0] * 31
    for x in set(nums):
        by_bits[bin(x).count("1")] += 1
    total = 0
    for a in range(31):
        for b in range(31):
            if a + b >= k:
                total += by_bits[a] * by_bits[b]
    return total


SEED = [2354]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


def main():
    # array a holds 10^5 values from 1 to 10^9, from 1 to 10^(4 + a / 2)
    # distinct; pass p asks for k = 1 + (7 p + a) mod 60
    arrays = []
    spread = 10000
    for a in range(10):
        nums = []
        for _ in range(100000):
            high = next_random()
            nums.append(1 + (high * 32768 + next_random()) % spread * 99991 % 1000000000)
        arrays.append(nums)
        if a % 2 == 1:
            spread *= 10
    check = 0
    for p in range(20):
        for a in range(10):
            k = 1 + (7 * p + a) % 60
            check = (check * 31 + count_excellent_pairs(arrays[a], k) + p) % 1000000007
    print(f"20 passes over 10 arrays of 10^5 values: checksum {check}")


main()
