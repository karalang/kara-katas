# LeetCode #1063: Number of Valid Subarrays -- the Python mirror of
# num_valid.kara (the ★ arm): a stack of the numbers no later number has
# gone below yet, each number ending one valid subarray per start on it.


def valid_subarrays(nums):
    stack = []
    count = 0
    for x in nums:
        while stack and stack[-1] > x:
            stack.pop()
        stack.append(x)
        count += len(stack)
    return count


seed = 1063


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_array(n, k):
    return [next_random() % k for _ in range(n)]


def show(nums):
    return "[" + ", ".join(str(x) for x in nums) + "]"


def main():
    examples = [[1, 4, 2, 5, 3], [3, 2, 1], [2, 2, 2], [7], [1, 2], [2, 1], [0, 0, 1, 0], [5, 1, 5, 1, 5], [1, 3, 2, 4, 3, 5], [100000, 0, 100000]]
    for nums in examples:
        print(f"{show(nums)} -> {valid_subarrays(nums)}")
    total = 0
    check = 0
    for _ in range(3000):
        n = next_random() % 12 + 1
        k = next_random() % 4 + 1
        answer = valid_subarrays(random_array(n, k))
        total += answer
        check = (check * 31 + answer) % 1000000007
    print(f"3000 arrays of 1 to 12 numbers below 1 to 4: sum {total}, checksum {check}")
    total = 0
    check = 0
    for i in range(300):
        n = next_random() % 251 + 50
        answer = valid_subarrays(random_array(n, 2 + i * 7 % 100000))
        total += answer
        check = (check * 31 + answer) % 1000000007
    print(f"300 arrays of 50 to 300 numbers: sum {total}, checksum {check}")
    rising = list(range(2000))
    falling = [2000 - i for i in range(2000)]
    equal = [7] * 2000
    zigzag = [i if i % 2 == 0 else 100000 - i for i in range(2000)]
    print(f"2000 rising: {valid_subarrays(rising)}")
    print(f"2000 falling: {valid_subarrays(falling)}")
    print(f"2000 equal: {valid_subarrays(equal)}")
    print(f"2000 random below 100001: {valid_subarrays(random_array(2000, 100001))}")
    print(f"2000 zigzag: {valid_subarrays(zigzag)}")


main()
