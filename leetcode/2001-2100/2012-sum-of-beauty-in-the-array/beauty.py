# LeetCode #2012: Sum of Beauty in the Array -- a mirror of the ★ arm,
# beauty.kara.


def sum_of_beauties(nums):
    n = len(nums)
    min_after = [0] * n
    min_after[n - 1] = nums[n - 1]
    for i in range(n - 2, -1, -1):
        min_after[i] = min(min_after[i + 1], nums[i])
    max_before = nums[0]
    total = 0
    for i in range(1, n - 1):
        if max_before < nums[i] < min_after[i + 1]:
            total += 2
        elif nums[i - 1] < nums[i] < nums[i + 1]:
            total += 1
        max_before = max(max_before, nums[i])
    return total


seed = 2012


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, answer):
    return (check * 31 + answer) % 1000000007


def random_nums(n, top, rise):
    nums = []
    for i in range(n):
        if i > 0 and next_random() % 10 < rise:
            nums.append(min(nums[i - 1] + next_random() % 3 + 1, top))
        else:
            nums.append(next_random() % top + 1)
    return nums


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    examples = [
        [1, 2, 3],
        [2, 4, 6, 4],
        [3, 2, 1],
        [1, 2, 3, 4, 5],
        [5, 1, 2, 3, 4],
        [1, 1, 1],
        [1, 3, 2, 4, 3, 5],
        [2, 1, 3, 2, 4, 3],
    ]
    for nums in examples:
        print(f"{show(nums)} -> {sum_of_beauties(nums)}")
    total = 0
    check = 0
    for _ in range(3000):
        n = next_random() % 10 + 3
        top = next_random() % 20 + 1
        rise = next_random() % 11
        answer = sum_of_beauties(random_nums(n, top, rise))
        total += answer
        check = mix(check, answer)
    print(f"3000 arrays of 3 to 12 values: sum {total}, checksum {check}")
    total = 0
    check = 0
    for a in range(6):
        top = [100, 100000][a % 2]
        rise = [0, 5, 9][a % 3]
        answer = sum_of_beauties(random_nums(3000, top, rise))
        total += answer
        check = mix(check, answer)
    print(f"6 arrays of 3000 values: sum {total}, checksum {check}")


main()
