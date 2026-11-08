# LeetCode #1063: Number of Valid Subarrays -- the benchmark, the same
# left-to-right stack as num_valid.kara.
seed = 1063


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_array(n, k):
    return [next_random() % k for _ in range(n)]


def valid_subarrays(nums):
    stack = []
    count = 0
    for x in nums:
        while stack and stack[-1] > x:
            stack.pop()
        stack.append(x)
        count += len(stack)
    return count


def main():
    # 20 arrays of 100000 numbers below 2 to 685902, built once, then each
    # answered on 50 of its suffixes
    arrays = [random_array(100000, 2 + a * a * a * 100) for a in range(20)]
    calls = total = check = 0
    for nums in arrays:
        for p in range(50):
            answer = valid_subarrays(nums[p * 100 :])
            total += answer
            check = (check * 31 + answer) % 1000000007
            calls += 1
    print(f"{calls} calls: answers sum {total}, checksum {check}")


main()
