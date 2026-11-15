# LeetCode #2172: Maximum AND Sum of Array -- the Python mirror of
# and_sum.kara: the slots' fill in base 3, each fill's best pushed forward
# to the fills one number more.


def maximum_and_sum(nums, num_slots):
    powers = [3 ** k for k in range(num_slots)]
    p = 3 ** num_slots
    best = [-1] * p
    best[0] = 0
    answer = 0
    for fill in range(p):
        if best[fill] < 0:
            continue
        placed = 0
        rest = fill
        while rest > 0:
            placed += rest % 3
            rest //= 3
        if placed == len(nums):
            answer = max(answer, best[fill])
            continue
        for slot in range(num_slots):
            if fill // powers[slot] % 3 < 2:
                nxt = fill + powers[slot]
                s = best[fill] + (nums[placed] & (slot + 1))
                if s > best[nxt]:
                    best[nxt] = s
    return answer


# ---- test harness ---------------------------------------------------------

seed = 2172


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(nums, num_slots):
    print(f"[{', '.join(map(str, nums))}], {num_slots} -> {maximum_and_sum(nums, num_slots)}")


def main():
    show([1, 2, 3, 4, 5, 6], 3)
    show([1, 3, 10, 4, 7, 1], 9)
    show([5], 1)
    show([1, 3], 1)
    show([15] * 18, 9)
    show([1, 2, 3, 4, 5, 6, 7, 8, 9], 9)
    total = 0
    check = 0
    for _ in range(2000):
        num_slots = next_random() % 6 + 1
        n = next_random() % (2 * num_slots) + 1
        nums = [next_random() % 15 + 1 for _ in range(n)]
        best = maximum_and_sum(nums, num_slots)
        total += best
        check = (check * 31 + best + n) % 1000000007
    print(f"2000 cases: {total} in all, checksum {check}")
    largest = []
    for _ in range(3):
        nums = [next_random() % 15 + 1 for _ in range(18)]
        largest.append(maximum_and_sum(nums, 9))
    print(f"9 slots, 18 numbers: [{', '.join(map(str, largest))}]")


main()
