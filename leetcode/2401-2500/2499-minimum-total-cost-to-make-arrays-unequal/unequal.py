# LeetCode #2499: Minimum Total Cost to Make Arrays Unequal -- Python
# mirror of the ★ arm (unequal.kara): a count per agreeing value, the
# mode, and the lowest helping places for the places short.


def minimum_total_cost(nums1, nums2):
    n = len(nums1)
    count = [0] * (n + 1)
    equal = 0
    cost = 0
    for i in range(n):
        if nums1[i] == nums2[i]:
            count[nums1[i]] += 1
            equal += 1
            cost += i
    mode = 0
    for v in range(1, n + 1):
        if count[v] > count[mode]:
            mode = v
    short = 2 * count[mode] - equal
    for j in range(n):
        if short <= 0:
            break
        if nums1[j] != nums2[j] and nums1[j] != mode and nums2[j] != mode:
            cost += j
            short -= 1
    return -1 if short > 0 else cost


# ---- test harness -----------------------------------------------------------

seed = 2499


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    hi = next_random()
    return hi * 32768 + next_random()


def random_pair(n, top, agree_in):
    nums1 = []
    nums2 = []
    for _ in range(n):
        a = wide() % top + 1
        nums1.append(a)
        if next_random() % 4 < agree_in:
            nums2.append(a)
        else:
            nums2.append(wide() % top + 1)
    return nums1, nums2


def main():
    cases = [
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),
        ([2, 2, 2, 1, 3], [1, 2, 2, 3, 3]),
        ([1, 2, 2], [1, 2, 2]),
        ([1], [1]),
        ([1], [2]),
        ([1, 1], [2, 2]),
        ([1, 2], [1, 2]),
        ([3, 3, 3, 1, 2], [3, 3, 3, 2, 1]),
        ([1, 1, 1, 2, 3, 4], [1, 1, 5, 2, 4, 3]),
    ]
    for nums1, nums2 in cases:
        print(f"{len(nums1)} places -> {minimum_total_cost(nums1, nums2)}")
    for agree_in in range(5):
        able = 0
        check = 0
        for t in range(2000):
            n = next_random() % 40 + 1
            top = min(n, 3) if t % 2 == 0 else n
            nums1, nums2 = random_pair(n, top, agree_in)
            cost = minimum_total_cost(nums1, nums2)
            if cost >= 0:
                able += 1
            check = (check * 31 + cost + 1) % 1000000007
        print(f"2000 random, agreeing {agree_in} in 4: {able} can, checksum {check}")
    n = 100000
    same = list(range(1, n + 1))
    two1, two2 = random_pair(n, 2, 3)
    third1, third2, most1, most2 = [], [], [], []
    for i in range(n):
        if i % 3 == 0:
            third1.append(7)
            third2.append(7)
        else:
            third1.append(wide() % n + 1)
            third2.append(wide() % n + 1)
        if i % 3 != 2:
            most1.append(7)
            most2.append(7)
        else:
            most1.append(wide() % n + 1)
            most2.append(wide() % n + 1)
    print(f"10^5 same -> {minimum_total_cost(same, same)}")
    print(f"10^5 two values -> {minimum_total_cost(two1, two2)}")
    print(f"10^5 a third of 7s -> {minimum_total_cost(third1, third2)}")
    print(f"10^5 two thirds of 7s -> {minimum_total_cost(most1, most2)}")


if __name__ == "__main__":
    main()
