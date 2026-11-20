# LeetCode #2354: Number of Excellent Pairs -- the Python mirror of the ★
# arm: the distinct values counted by their number of set bits, then every
# two counts whose bits reach k multiplied.


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
    # LeetCode's two examples; one value with k at its bits doubled and one
    # past; 10^5 values that are all 2^30 - 1; 10^5 values over 2000
    # distinct with k from 1 to 60
    print(count_excellent_pairs([1, 2, 3, 1], 3))
    print(count_excellent_pairs([5, 1, 1], 10))
    print(count_excellent_pairs([7], 6))
    print(count_excellent_pairs([7], 7))
    print(count_excellent_pairs([1073741823] * 100000, 60))
    many = [i * 7919 % 2000 * 524309 % 1000000000 + 1 for i in range(100000)]
    print(" ".join(str(count_excellent_pairs(many, k)) for k in range(1, 61, 7)))
    # 2000 random arrays of 1 to 30 values from 1 to 2^b, b from 1 to 30,
    # and k from 1 to 2 b + 1
    check = 0
    total = 0
    none = 0
    for _ in range(2000):
        n = 1 + next_random() % 30
        b = 1 + next_random() % 30
        nums = [1 + (next_random() * 32768 + next_random()) % (1 << b) for _ in range(n)]
        k = 1 + next_random() % (2 * b + 1)
        p = count_excellent_pairs(nums, k)
        check = (check * 31 + p) % 1000000007
        total += p
        if p == 0:
            none += 1
    print(f"2000 arrays: checksum {check}, pairs {total}, {none} with none")


main()
