# LeetCode #2009: Minimum Number of Operations to Make Array Continuous --
# a mirror of the ★ arm, continuous.kara.


def min_operations(nums):
    n = len(nums)
    values = sorted(set(nums))
    kept = 0
    right = 0
    for left in range(len(values)):
        while right < len(values) and values[right] <= values[left] + n - 1:
            right += 1
        kept = max(kept, right - left)
    return n - kept


seed = 2009


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, answer):
    return (check * 31 + answer) % 1000000007


def random_nums(n, top):
    nums = []
    for _ in range(n):
        a = next_random()
        nums.append((a * 32768 + next_random()) % top + 1)
    return nums


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    examples = [
        [4, 2, 5, 3],
        [1, 2, 3, 5, 6],
        [1, 10, 100, 1000],
        [7],
        [5, 5, 5, 5],
        [1, 3, 5, 7, 9],
        [8, 5, 9, 9, 8, 4],
        [1000000000, 1, 999999999, 2],
    ]
    for nums in examples:
        print(f"{show(nums)} -> {min_operations(nums)}")
    total = 0
    check = 0
    for _ in range(3000):
        n = next_random() % 12 + 1
        top = next_random() % 30 + 1
        answer = min_operations(random_nums(n, top))
        total += answer
        check = mix(check, answer)
    print(f"3000 arrays of 1 to 12 values: sum {total}, checksum {check}")
    total = 0
    check = 0
    for a in range(6):
        top = [5000, 1000000, 1000000000][a % 3]
        answer = min_operations(random_nums(3000, top))
        total += answer
        check = mix(check, answer)
    print(f"6 arrays of 3000 values: sum {total}, checksum {check}")


main()
