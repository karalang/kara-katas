# LeetCode #645: Set Mismatch -- Python mirror of the ★ arm.
#
# One pass counts how often each value appears: the one seen twice is the
# copy and the one never seen is the value it replaced.


def find_error_nums(nums):
    n = len(nums)
    seen = [0] * (n + 1)
    for x in nums:
        seen[x] += 1
    twice = 0
    missing = 0
    for v in range(1, n + 1):
        if seen[v] == 2:
            twice = v
        elif seen[v] == 0:
            missing = v
    return [twice, missing]


def next_random(rng):
    rng[0] = (rng[0] * 1103515245 + 12345) % 2147483648
    return rng[0] // 65536


def show(nums):
    text = ",".join(str(x) for x in nums)
    got = find_error_nums(nums)
    print(f"[{text}] -> [{got[0]},{got[1]}]")


def mismatched(n, rng):
    nums = list(range(1, n + 1))
    for i in range(n - 1):
        j = i + next_random(rng) % (n - i)
        nums[i], nums[j] = nums[j], nums[i]
    frm = next_random(rng) % n
    to = next_random(rng) % (n - 1)
    if to >= frm:
        to += 1
    nums[to] = nums[frm]
    return nums


def main():
    show([1, 2, 2, 4])
    show([1, 1])
    show([2, 2])
    show([1, 2, 3, 3])
    show([3, 2, 3, 4, 6, 5])
    show([1, 5, 3, 2, 2, 7, 6, 4, 9, 10])
    show([1, 2, 3, 4, 1])
    show([5, 2, 3, 4, 5])
    rng = [645]
    twice_sum = 0
    missing_sum = 0
    gaps = 0
    for _ in range(300):
        n = 2 + next_random(rng) % 39
        got = find_error_nums(mismatched(n, rng))
        twice_sum += got[0]
        missing_sum += got[1]
        gaps += abs(got[0] - got[1])
    print(f"300 random cases: copies add to {twice_sum}, missing values to {missing_sum}, gaps to {gaps}")
    for _ in range(3):
        got = find_error_nums(mismatched(10000, rng))
        print(f"10000 values -> [{got[0]},{got[1]}]")


main()
