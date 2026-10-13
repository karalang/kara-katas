# LeetCode #503: Next Greater Element II -- Python mirror of the ★ arm (a
# stack of indices, twice around); see next_greater_elements.kara.


def next_greater_elements(nums):
    n = len(nums)
    answer = [-1] * n
    waiting = []
    for i in range(2 * n):
        x = nums[i % n]
        while waiting:
            top = waiting[-1]
            if nums[top] >= x:
                break
            answer[top] = x
            waiting.pop()
        if i < n:
            waiting.append(i)
    return answer


# ---- test harness ---------------------------------------------------------

seed = 503


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def rem(a, b):
    # Kāra's % truncates toward zero, as C's does; Python's floors.
    r = abs(a) % b
    return -r if a < 0 else r


def fmt(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def show(name, nums):
    print(f"{name}: {fmt(nums)} -> {fmt(next_greater_elements(nums))}")


def main():
    show("example 1", [1, 2, 1])
    show("example 2", [1, 2, 3, 4, 3])
    show("one number", [5])
    show("all equal", [3, 3, 3])
    show("falling", [5, 4, 3, 2, 1])
    show("rising", [1, 2, 3, 4, 5])
    show("the extremes", [-1000000000, 1000000000, -1000000000])
    show("the largest twice", [2, 9, 1, 9, 3])
    # 300 random arrays of 1 to 30 numbers from 0 to 9 or from the
    # whole range -10^9 to 10^9, in turn.
    count = 300
    total = 0
    found = 0
    checksum = 0
    for c in range(count):
        size = 1 + next_random() % 30
        nums = []
        for _ in range(size):
            if c % 2 == 0:
                nums.append(next_random() % 10)
            else:
                hi = next_random()
                nums.append((hi * 65536 + next_random()) % 2000000001 - 1000000000)
        for a in next_greater_elements(nums):
            total += 1
            if a != -1:
                found += 1
            checksum = (checksum * 31 + rem(a, 1000000007) + 1000000007) % 1000000007
    print(f"{count} random arrays: {total} numbers, {found} with a greater one, checksum {checksum}")


main()
