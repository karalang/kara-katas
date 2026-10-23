# LeetCode #896: Monotonic Array -- Python mirror of the one-pass solution
# in is_monotonic.kara, with the same test harness.
#
# Walk the neighbours once. A step up rules out non-increasing, a step
# down rules out non-decreasing, and an equal step rules out neither;
# the array is monotonic when at least one of the two survives. O(n).


def is_monotonic(nums):
    rising = True
    falling = True
    for i in range(1, len(nums)):
        if nums[i] > nums[i - 1]:
            falling = False
        if nums[i] < nums[i - 1]:
            rising = False
    return rising or falling


# ---- test harness ----------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def text(b):
    return "true" if b else "false"


def show(nums):
    print(f"nums = [{', '.join(str(x) for x in nums)}] -> {text(is_monotonic(nums))}")


# `len` random numbers spread over `span` values centred on 0, sorted up
# for kind 1, 3 and 5 and down for kind 2 and 4; kinds 3 and 4 then swap
# two random places, and kind 5 sets one random place to a random number
def random_case(kind, length, span):
    nums = []
    for _ in range(length):
        r = next_random() * 32768
        r += next_random()
        nums.append(r % span - span // 2)
    if kind >= 1:
        nums.sort()
    if kind == 2 or kind == 4:
        nums.reverse()
    if kind == 3 or kind == 4:
        i = next_random() % length
        j = next_random() % length
        nums[i], nums[j] = nums[j], nums[i]
    if kind == 5:
        i = next_random() % length
        r = next_random() * 32768
        r += next_random()
        nums[i] = r % span - span // 2
    return nums


def main():
    global seed
    show([1, 2, 2, 3])
    show([6, 5, 4, 4])
    show([1, 3, 2])
    show([5])
    show([2, 2, 2])
    show([3, 3, 1, 1, 2])
    show([-100000, 100000])
    show([1, 2, 1, 2])
    # random cases of up to 1000 numbers, a third of them up to 5, half
    # of them from at most 3 values, the rest from LeetCode's whole range
    seed = 896
    monotonic = 0
    check = 0
    for c in range(300):
        kind = next_random() % 6
        length = 1 + next_random() % 5 if c % 3 == 0 else 1 + next_random() % 1000
        span = 1 + next_random() % 3 if c % 2 == 0 else 200001
        nums = random_case(kind, length, span)
        got = is_monotonic(nums)
        if got:
            monotonic += 1
        check = (check * 131 + length * 2 + (1 if got else 0)) % 1000000007
    print(f"300 cases of up to 1000 numbers: {monotonic} monotonic, checksum {check}")
    # LeetCode's largest: 100000 numbers sorted up, down, and each with
    # two places swapped
    big = [text(is_monotonic(random_case(kind, 100000, 200001))) for kind in range(1, 5)]
    print(f"4 cases of 100000 numbers: [{', '.join(big)}]")


main()
