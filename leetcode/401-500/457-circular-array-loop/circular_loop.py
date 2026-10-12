# LeetCode #457: Circular Array Loop -- mirror of circular_loop.kara
# (slow and fast pointers), with the same harness.


def next_index(a, i):
    # Python's % already gives a result in 0..n-1.
    return (i + a[i]) % len(a)


def circular_array_loop(nums):
    a = list(nums)
    n = len(a)
    for start in range(n):
        if a[start] == 0:
            continue
        forward = a[start] > 0
        slow = start
        fast = start
        while True:
            s = next_index(a, slow)
            f1 = next_index(a, fast)
            if a[f1] == 0 or (a[f1] > 0) != forward:
                break
            f2 = next_index(a, f1)
            if a[f2] == 0 or (a[f2] > 0) != forward:
                break
            slow = s
            fast = f2
            if slow == fast:
                if next_index(a, slow) != slow:
                    return True
                break
        # Nothing on this path reaches a valid cycle: clear it.
        i = start
        while a[i] != 0 and (a[i] > 0) == forward:
            nxt = next_index(a, i)
            a[i] = 0
            i = nxt
    return False


# ---- test harness ---------------------------------------------------------


def listed(nums):
    return ",".join(str(x) for x in nums)


def show(nums):
    print(f"[{listed(nums)}]: {'true' if circular_array_loop(nums) else 'false'}")


seed = 457


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    show([2, -1, 1, 2, 2])
    show([-1, -2, -3, -4, -5, 6])
    show([1, -1, 5, 1, 4])
    show([1])
    show([1, 1])
    show([-1, -1])
    show([1, -1])
    show([2, 2, 2])
    show([3, 1, 2])
    show([-2, 1, -1, -2, -2])
    show([1000, -1000, 999])
    # 300 random arrays of 1 to 200 steps, each of size 1 to 3, 10 or
    # 1,000, forward with probability 1/2, 3/4, 15/16 or 1.
    count = 300
    found = 0
    checksum = 0
    for case in range(count):
        n = 1 + next_random() % 200
        size = [3, 10, 1000][next_random() % 3]
        backward = [2, 4, 16, 0][next_random() % 4]
        nums = []
        for _ in range(n):
            step = 1 + next_random() % size
            if backward > 0 and next_random() % backward == 0:
                nums.append(-step)
            else:
                nums.append(step)
        has = circular_array_loop(nums)
        if has:
            found += 1
        checksum = (checksum * 31 + (case + 1 if has else 0)) % 1000000007
    print(f"{count} random arrays: {found} with a loop, checksum {checksum}")


main()
