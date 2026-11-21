# LeetCode #2364: Count Number of Bad Pairs -- the Python mirror of the ★
# arm: each place's key nums[j] - j counted in a map as the places go by,
# the places before j with the same key its good pairs, and the bad pairs
# all n (n - 1) / 2 less the good ones.


def count_bad_pairs(nums):
    n = len(nums)
    seen = {}
    good = 0
    for j in range(n):
        key = nums[j] - j
        before = seen.get(key, 0)
        good += before
        seen[key] = before + 1
    return n * (n - 1) // 2 - good


SEED = [2364]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


def main():
    # LeetCode's two examples; one value; 10^5 places in a run rising by
    # one, every pair good; 10^5 equal values, every pair bad; 10^5 values
    # in four interleaved keys; then 2000 random arrays of 1 to 40
    # values, each the place plus a small offset or a random value up to
    # 10^9
    print(count_bad_pairs([4, 1, 3, 3]))
    print(count_bad_pairs([1, 2, 3, 4, 5]))
    print(count_bad_pairs([7]))
    print(count_bad_pairs([i + 1000 for i in range(100000)]))
    print(count_bad_pairs([1000000000] * 100000))
    print(count_bad_pairs([i + (i % 4) * 7 for i in range(100000)]))
    check = 0
    none_bad = 0
    for _ in range(2000):
        n = 1 + next_random() % 40
        spread = 1 + next_random() % 6
        nums = []
        for i in range(n):
            if next_random() % 8 == 0:
                hi = next_random()
                nums.append(1 + (hi * 32768 + next_random()) % 1000000000)
            else:
                nums.append(1 + i + next_random() % spread)
        bad = count_bad_pairs(nums)
        check = (check * 31 + bad) % 1000000007
        if bad == 0:
            none_bad += 1
    print(f"2000 arrays: checksum {check}, {none_bad} with no bad pair")


if __name__ == "__main__":
    main()
