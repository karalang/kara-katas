# LeetCode #2367: Number of Arithmetic Triplets -- the Python mirror of
# the ★ arm: a triplet fixed by its first value x exists exactly when
# x + diff and x + 2 diff are values too, looked up in a set.


def arithmetic_triplets(nums, diff):
    values = set(nums)
    count = 0
    for x in nums:
        if x + diff in values and x + 2 * diff in values:
            count += 1
    return count


SEED = [2367]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


def main():
    # LeetCode's two examples; three values; every value from 0 to 199
    # with a diff of 1 and of 50; then 3000 random sets of 3 to 40 values
    # from 0 to 0 to 200, with a diff of 1 to 50
    print(arithmetic_triplets([0, 1, 4, 6, 7, 10], 3))
    print(arithmetic_triplets([4, 5, 6, 7, 8, 9], 2))
    print(arithmetic_triplets([1, 3, 5], 2))
    every = list(range(200))
    print(f"{arithmetic_triplets(every, 1)} {arithmetic_triplets(every, 50)}")
    check = 0
    none = 0
    for _ in range(3000):
        top = 3 + next_random() % 198
        n = 3 + next_random() % min(top - 2, 38)
        taken = [False] * (top + 1)
        count = 0
        while count < n:
            v = next_random() % (top + 1)
            if not taken[v]:
                taken[v] = True
                count += 1
        nums = [v for v in range(top + 1) if taken[v]]
        diff = 1 + next_random() % 50
        t = arithmetic_triplets(nums, diff)
        check = (check * 31 + t) % 1000000007
        if t == 0:
            none += 1
    print(f"3000 sets: checksum {check}, {none} with no triplet")


if __name__ == "__main__":
    main()
