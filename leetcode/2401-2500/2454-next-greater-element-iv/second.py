# LeetCode #2454: Next Greater Element IV -- Python mirror of second.kara:
# two monotonic stacks, the first waiting for one greater value and the
# second for another; each value answers the second's smaller tops, then
# moves the first's smaller tops, in their order, onto the second.


def second_greater_element(nums):
    n = len(nums)
    answer = [-1] * n
    first = []
    second = []
    for j in range(n):
        while len(second) > 0 and nums[second[-1]] < nums[j]:
            answer[second.pop()] = nums[j]
        cut = len(first)
        while cut > 0 and nums[first[cut - 1]] < nums[j]:
            cut -= 1
        for i in range(cut, len(first)):
            second.append(first[i])
        del first[cut:]
        first.append(j)
    return answer


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    a = next_random()
    return a * 32768 + next_random()


def fold(values):
    check = 0
    for v in values:
        check = (check * 31 + v + 1) % 1000000007
    return check


def show(values):
    return "[" + ", ".join(str(v) for v in values) + "]"


def main():
    global seed
    print(show(second_greater_element([2, 4, 0, 9, 6])))
    print(show(second_greater_element([3, 3])))
    print(show(second_greater_element([7])))
    print(show(second_greater_element([1, 2, 3, 4, 5])))
    print(show(second_greater_element([5, 4, 3, 2, 1])))
    print(show(second_greater_element([1, 5, 5, 1, 5, 2, 9])))
    print(show(second_greater_element([0, 1000000000, 0, 1000000000, 1000000000])))
    seed = 2454
    wide = [wide_random() % 1000000001 for _ in range(2000)]
    print(f"2000 values up to 10^9: checksum {fold(second_greater_element(wide))}")
    narrow = [next_random() % 4 for _ in range(2000)]
    print(f"2000 values up to 3: checksum {fold(second_greater_element(narrow))}")
    check = 0
    for _ in range(3000):
        n = 1 + next_random() % 8
        nums = [next_random() % 10 for _ in range(n)]
        check = (check * 31 + fold(second_greater_element(nums))) % 1000000007
    print(f"3000 random: checksum {check}")


main()
