# Benchmark for #457: mirror of circular_loop.kara (the ★ arm, slow and
# fast pointers) on the same workload.


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
            # Python's % already gives a result in 0..n-1.
            s = (slow + a[slow]) % n
            f1 = (fast + a[fast]) % n
            if a[f1] == 0 or (a[f1] > 0) != forward:
                break
            f2 = (f1 + a[f1]) % n
            if a[f2] == 0 or (a[f2] > 0) != forward:
                break
            slow = s
            fast = f2
            if slow == fast:
                if (slow + a[slow]) % n != slow:
                    return True
                break
        # Nothing on this path reaches a valid cycle: clear it.
        i = start
        while a[i] != 0 and (a[i] > 0) == forward:
            nxt = (i + a[i]) % n
            a[i] = 0
            i = nxt
    return False


# ---- benchmark --------------------------------------------------------

seed = 457


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    arrays = 10
    n = 1000000
    rounds = 5
    all_nums = []
    for _ in range(arrays):
        nums = []
        for _ in range(n):
            step = 1 + next_random() % 1000
            if next_random() % 2 == 0:
                nums.append(step)
            else:
                nums.append(-step)
        all_nums.append(nums)
    found = 0
    checksum = 0
    for _ in range(rounds):
        for a in range(arrays):
            hi = next_random()
            lo = next_random()
            k = (hi * 65536 + lo) % (n - 1)
            one, two = all_nums[a][k], all_nums[a][k + 1]
            if next_random() % 2 == 0:
                all_nums[a][k] = 1
                all_nums[a][k + 1] = n - 1
            has = circular_array_loop(all_nums[a])
            all_nums[a][k] = one
            all_nums[a][k + 1] = two
            if has:
                found += 1
            checksum = (checksum * 31 + (k + 1 if has else 0)) % 1000000007
    print(f"{rounds} rounds on {arrays} arrays of {n}: {found} with a loop, checksum {checksum}")


main()
