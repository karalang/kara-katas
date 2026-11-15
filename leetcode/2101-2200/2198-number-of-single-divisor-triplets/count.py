# LeetCode #2198: Number of Single Divisor Triplets -- Python mirror of
# count.kara (the ★ arm): the numbers tallied by value, and every ordered
# triple (a, b, c) of the values the array holds tried; when exactly one
# of the three divides a + b + c, its index triples are counted.
# O(n + 100^3).


def single_divisor_triplet(nums):
    count = [0] * 101
    for x in nums:
        count[x] += 1
    total = 0
    for a in range(1, 101):
        if count[a] == 0:
            continue
        for b in range(1, 101):
            if count[b] == 0:
                continue
            for c in range(1, 101):
                if count[c] == 0:
                    continue
                s = a + b + c
                by_a = s % a == 0
                by_b = s % b == 0
                by_c = s % c == 0
                if (by_a and not by_b and not by_c) or (by_b and not by_a and not by_c) or (by_c and not by_a and not by_b):
                    second = count[b] - 1 if b == a else count[b]
                    third = count[c] - (1 if c == a else 0) - (1 if c == b else 0)
                    total += count[a] * second * third
    return total


# ---- test harness ---------------------------------------------------------

seed = 2198


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(nums):
    print(f"[{', '.join(map(str, nums))}] -> {single_divisor_triplet(nums)}")


def main():
    show([4, 6, 7, 3, 2])
    show([1, 2, 2])
    show([1, 1, 1])
    show([2, 3, 4])
    show([3, 3, 3, 3, 1])
    show(list(range(1, 101)))
    check = 0
    for rnd in range(200):
        n = next_random() % 58 + 3
        top = [6, 20, 100][rnd % 3]
        nums = [next_random() % top + 1 for _ in range(n)]
        check = (check * 31 + single_divisor_triplet(nums)) % 1000000007
    print(f"200 arrays: checksum {check}")
    wide = []
    two = []
    for i in range(100000):
        wide.append(next_random() % 100 + 1)
        two.append(2 if i % 3 == 0 else 4)
    print(f"10^5 numbers: {single_divisor_triplet(wide)}; two values: {single_divisor_triplet(two)}")


main()
