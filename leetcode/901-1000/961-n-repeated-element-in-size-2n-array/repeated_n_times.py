# LeetCode #961: N-Repeated Element in Size 2N Array -- near neighbours.
#
# Mirrors repeated_n_times.kara: two copies of the repeated value are never
# more than three places apart, so compare each number with the next one,
# then the one after, then the one three on.


def repeated_n_times(nums):
    for k in range(1, 4):
        for i in range(len(nums) - k):
            if nums[i] == nums[i + k]:
                return nums[i]
    return -1


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_nums(n, top):
    used = [False] * (top + 1)
    r = next_random() % (top + 1)
    used[r] = True
    out = []
    while len(out) < n:
        v = next_random() % (top + 1)
        if not used[v]:
            used[v] = True
            out.append(v)
    out += [r] * n
    for i in range(len(out)):
        j = i + next_random() % (len(out) - i)
        out[i], out[j] = out[j], out[i]
    return out


def show(nums):
    return "[" + ",".join(str(x) for x in nums) + "]"


def main():
    global seed
    cases = [
        [1, 2, 3, 3],
        [2, 1, 2, 5, 3, 2],
        [5, 1, 5, 2, 5, 3, 5, 4],
        [9, 9, 1, 2],
        [9, 1, 2, 9],
        [1, 9, 2, 9],
        [0, 10000, 0, 1],
        [10000, 1, 2, 10000],
        [4, 7, 7, 5, 7, 1],
        [3, 1, 2, 4, 3, 3],
    ]
    for nums in cases:
        print(f"{show(nums)}: {repeated_n_times(nums)}")
    seed = 961
    count = 0
    total = 0
    check = 0
    for _ in range(300):
        n = 2 + next_random() % 9
        nums = random_nums(n, 10000)
        r = repeated_n_times(nums)
        count += 2 * n
        total += r
        check = (check * 31 + r) % 1000000007
    print(f"300 random cases of {count} numbers: the repeated ones sum to {total}, checksum {check}")
    big = random_nums(5000, 10000)
    print(f"10000 random numbers: {repeated_n_times(big)}")
    odd = []
    even = []
    for i in range(5000):
        odd += [i + 1, 0]
        even += [10000, i]
    print(f"0 at every other place, from the second: {repeated_n_times(odd)}")
    print(f"10000 at every other place, from the first: {repeated_n_times(even)}")
    front = [7777] * 5000 + list(range(5000))
    back = [i + 5001 for i in range(5000)] + [4242] * 5000
    print(f"7777 in the first half: {repeated_n_times(front)}")
    print(f"4242 in the second half: {repeated_n_times(back)}")
    print(f"[6,0,10000,6]: {repeated_n_times([6, 0, 10000, 6])}")


main()
