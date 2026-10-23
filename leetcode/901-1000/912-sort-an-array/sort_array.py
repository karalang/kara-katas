# LeetCode #912: Sort an Array -- Python mirror of the heap sort in
# sort_array.kara, with the same test harness.


def sift_down(a, start, end):
    root = start
    while True:
        child = 2 * root + 1
        if child >= end:
            return
        if child + 1 < end and a[child + 1] > a[child]:
            child += 1
        if a[root] >= a[child]:
            return
        a[root], a[child] = a[child], a[root]
        root = child


def sort_array(nums):
    a = list(nums)
    n = len(a)
    parent = n // 2 - 1
    while parent >= 0:
        sift_down(a, parent, n)
        parent -= 1
    end = n - 1
    while end > 0:
        a[0], a[end] = a[end], a[0]
        sift_down(a, 0, end)
        end -= 1
    return a


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def join(v):
    return ",".join(str(x) for x in v)


def show(nums):
    print(f"[{join(nums)}] -> [{join(sort_array(nums))}]")


def fold(nums):
    s = sort_array(nums)
    check = len(s)
    for x in s:
        check = (check * 1000003 + x + 50000) % 1000000007
    return check


def main():
    global seed
    show([5, 2, 3, 1])
    show([5, 1, 1, 2, 0, 0])
    show([1])
    show([50000, -50000])
    show([-3, -1, -2, 0, 2, 1, 3])
    show([1, 2, 3, 4, 5, 6, 7, 8])
    show([8, 7, 6, 5, 4, 3, 2, 1])
    show([4, 4, 4, 4, 4])
    show([255, 256, 0, -1, 257, -256, 50000, -50000, 65535 - 50000])
    seed = 912
    check = 0
    for c in range(300):
        n = 1 + next_random() % 2000
        span = 10 if c % 3 == 0 else 1000 if c % 3 == 1 else 100001
        low = -50000 + next_random() % (100002 - span)
        nums = [low + next_random() % span for _ in range(n)]
        check = (check * 31 + fold(nums)) % 1000000007
    print(f"300 arrays: checksum {check}")
    rand = []
    falling = []
    equal = []
    for i in range(50000):
        rand.append(next_random() % 100001 - 50000)
        falling.append(50000 - 2 * i)
        equal.append(i // 1000 if i % 1000 == 0 else 7)
    print(f"50000 random: checksum {fold(rand)}")
    print(f"50000 falling: checksum {fold(falling)}")
    print(f"50000 nearly equal: checksum {fold(equal)}")


main()
