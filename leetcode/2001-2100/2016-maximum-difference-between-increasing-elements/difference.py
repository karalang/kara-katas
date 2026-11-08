# LeetCode #2016: Maximum Difference Between Increasing Elements -- a mirror
# of the ★ arm, difference.kara.


def maximum_difference(nums):
    smallest = nums[0]
    best = -1
    for x in nums[1:]:
        if x > smallest:
            best = max(best, x - smallest)
        smallest = min(smallest, x)
    return best


seed = 2016


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, answer):
    return (check * 31 + answer + 1) % 1000000007


def random_values(n, top, fall):
    nums = []
    for i in range(n):
        if i > 0 and next_random() % 10 < fall:
            step = next_random() % 3
            nums.append(max(nums[i - 1] - step, 1))
        else:
            a = next_random()
            nums.append((a * 32768 + next_random()) % top + 1)
    return nums


def main():
    examples = [
        [7, 1, 5, 4],
        [9, 4, 3, 2],
        [1, 5, 2, 10],
        [5, 5],
        [1, 2],
        [1000000000, 1],
        [3, 3, 3, 4],
        [6, 1, 6, 1, 6],
        [2, 9, 1, 8, 1, 7],
    ]
    for nums in examples:
        print(f"[{', '.join(map(str, nums))}] -> {maximum_difference(nums)}")
    total = check = 0
    for _ in range(3000):
        n = next_random() % 11 + 2
        top = next_random() % 20 + 1
        fall = next_random() % 11
        answer = maximum_difference(random_values(n, top, fall))
        total += answer
        check = mix(check, answer)
    print(f"3000 arrays of 2 to 12 values: sum {total}, checksum {check}")
    total = check = 0
    for a in range(6):
        top = [100, 1000000000, 1000, 1000000000, 50, 7][a]
        fall = [5, 9, 10, 8, 3, 0][a]
        answer = maximum_difference(random_values(1000, top, fall))
        total += answer
        check = mix(check, answer)
    print(f"6 arrays of 1000 values: sum {total}, checksum {check}")


main()
