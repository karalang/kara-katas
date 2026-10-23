# LeetCode #907: Sum of Subarray Minimums -- bench program, Python.
#
# How far each element reaches, over 1,000,000 numbers from 1 to 30000
# built once. Each round sums the subarray minimums, folds the sum into a
# checksum and changes one number.


def sum_subarray_mins(arr):
    n = len(arr)
    left = [0] * n
    right = [0] * n
    stack = []
    for i in range(n):
        while stack and arr[stack[-1]] >= arr[i]:
            stack.pop()
        left[i] = i - stack[-1] if stack else i + 1
        stack.append(i)
    stack.clear()
    for k in range(n):
        i = n - 1 - k
        while stack and arr[stack[-1]] > arr[i]:
            stack.pop()
        right[i] = stack[-1] - i if stack else n - i
        stack.append(i)
    total = 0
    for i in range(n):
        total = (total + arr[i] * left[i] % 1000000007 * right[i]) % 1000000007
    return total


seed = 907


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    n = 1000000
    rounds = 40
    arr = [1 + next_random() % 30000 for _ in range(n)]
    check = 0
    for r in range(rounds):
        got = sum_subarray_mins(arr)
        check = (check * 31 + got) % 1000000007
        arr[r * 7919 % n] = 1 + next_random() % 30000
    print(f"{rounds} rounds over {n} numbers: checksum {check}")


main()
