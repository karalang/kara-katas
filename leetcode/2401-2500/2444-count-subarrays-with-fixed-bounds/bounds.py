# LeetCode #2444: Count Subarrays With Fixed Bounds -- Python mirror of
# the ★ arm (bounds.kara): one pass keeping the last value outside the
# bounds, the last min_k and the last max_k.


def count_subarrays(nums, min_k, max_k):
    count = 0
    bad = -1
    last_min = -1
    last_max = -1
    for i, x in enumerate(nums):
        if x < min_k or x > max_k:
            bad = i
        if x == min_k:
            last_min = i
        if x == max_k:
            last_max = i
        count += max(min(last_min, last_max) - bad, 0)
    return count


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    global seed
    print(f"example 1: {count_subarrays([1, 3, 5, 2, 7, 5], 1, 5)}")
    print(f"example 2: {count_subarrays([1, 1, 1, 1], 1, 1)}")
    print(f"bounds reversed: {count_subarrays([2, 1, 2], 2, 1)}")
    print(f"one value: {count_subarrays([1000000], 1000000, 1000000)}")
    n = 5000
    print(f"all equal: {count_subarrays([7] * n, 7, 7)}")
    seed = 2444
    small = [1 + next_random() % 5 for _ in range(n)]
    print(f"1 to 5: {count_subarrays(small, 1, 5)}")
    wide = []
    for i in range(n):
        if i % 50 == 49:
            v = 1000000
        else:
            a = next_random()
            v = 200000 + (a * 32768 + next_random()) % 600001
        wide.append(v)
    wide[10] = 200000
    wide[20] = 800000
    wide[3000] = 800000
    wide[3001] = 200000
    print(f"wide: {count_subarrays(wide, 200000, 800000)}")
    check = 0
    total = 0
    for _ in range(3000):
        length = 1 + next_random() % 10
        nums = [1 + next_random() % 4 for _ in range(length)]
        low = 1 + next_random() % 4
        high = 1 + next_random() % 4
        answer = count_subarrays(nums, low, high)
        check = (check * 31 + answer) % 1000000007
        total += answer
    print(f"3000 random: checksum {check}, total {total}")


main()
