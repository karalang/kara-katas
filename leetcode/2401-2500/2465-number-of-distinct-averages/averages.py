# LeetCode #2465: Number of Distinct Averages -- the Python mirror of
# averages.kara: sorted, the `i`th smallest paired with the `i`th
# largest, and the pairs' sums put in a set.


def distinct_averages(nums):
    s = sorted(nums)
    n = len(s)
    return len({s[i] + s[n - 1 - i] for i in range(n // 2)})


# ---- test harness ---------------------------------------------------------

seed = 2465


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(values):
    return "[" + ", ".join(str(v) for v in values) + "]"


def main():
    cases = [
        [4, 1, 4, 0, 3, 5],
        [1, 100],
        [7, 7, 7, 7],
        [0, 100, 0, 100],
        [1, 2, 3, 4, 5, 6],
        [0, 1, 1, 3],
    ]
    for nums in cases:
        print(f"{show(nums)} -> {distinct_averages(nums)}")
    print(f"0 to 99: {distinct_averages(list(range(100)))}")
    for top in (101, 4):
        nums = [next_random() % top for _ in range(100)]
        print(f"100 random below {top}: {distinct_averages(nums)}")
    check = 0
    for _ in range(3000):
        n = 2 * (1 + next_random() % 10)
        nums = [next_random() % 101 for _ in range(n)]
        check = (check * 31 + distinct_averages(nums)) % 1000000007
    print(f"3000 random: checksum {check}")


if __name__ == "__main__":
    main()
