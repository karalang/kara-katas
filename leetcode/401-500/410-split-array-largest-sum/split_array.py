# LeetCode #410: Split Array Largest Sum -- mirror of split_array.kara
# (binary search on the answer).


def pieces_needed(nums, cap):
    pieces = 1
    s = 0
    for x in nums:
        if s + x > cap:
            pieces += 1
            s = x
        else:
            s += x
    return pieces


def split_array(nums, k):
    lo = 0
    hi = 0
    for x in nums:
        if x > lo:
            lo = x
        hi += x
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if pieces_needed(nums, mid) <= k:
            hi = mid
        else:
            lo = mid + 1
    return lo


seed = 410


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(nums, k):
    print(f"[{', '.join(str(x) for x in nums)}], k = {k}: {split_array(nums, k)}")


show([7, 2, 5, 10, 8], 2)
show([1, 2, 3, 4, 5], 2)
show([1, 4, 4], 3)
show([5], 1)
show([0, 0, 0], 2)
show([3, 1, 4, 1, 5, 9, 2, 6], 1)
show([3, 1, 4, 1, 5, 9, 2, 6], 8)
show([1000000, 1000000, 1000000], 2)
show([2, 3, 1, 2, 4, 3], 5)
show([10, 5, 13, 4, 8, 4, 5, 11, 14, 9, 16, 10, 20, 8], 8)
total = 0
checksum = 0
for _ in range(2000):
    n = 1 + step() % 40
    nums = [step() % 100 for _ in range(n)]
    k = 1 + step() % n
    answer = split_array(nums, k)
    total += answer
    checksum = (checksum * 31 + answer) % 1000000007
print(f"2000 random arrays: total {total}, checksum {checksum}")
