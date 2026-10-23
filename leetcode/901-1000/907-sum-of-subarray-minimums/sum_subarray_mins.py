# LeetCode #907: Sum of Subarray Minimums -- Python mirror of how far each
# element reaches in sum_subarray_mins.kara, with the same test harness.


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


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(arr):
    listed = ",".join(str(x) for x in arr)
    print(f"arr = [{listed}] -> {sum_subarray_mins(arr)}")


def main():
    global seed
    show([3, 1, 2, 4])
    show([11, 81, 94, 43, 3])
    show([1])
    show([2, 2, 2])
    show([1, 2, 3, 4, 5])
    show([5, 4, 3, 2, 1])
    show([3, 1, 3, 1, 3])
    show([30000, 1, 30000])
    seed = 907
    check = 0
    for c in range(300):
        length = 1 + next_random() % 1000
        top = 3 if c % 3 == 0 else 100 if c % 3 == 1 else 30000
        arr = [1 + next_random() % top for _ in range(length)]
        check = (check * 1000003 + sum_subarray_mins(arr)) % 1000000007
    print(f"300 cases: checksum {check}")
    random = []
    rising = []
    flat = []
    for i in range(30000):
        random.append(1 + next_random() % 30000)
        rising.append(i + 1)
        flat.append(30000)
    print(f"30000 random numbers -> {sum_subarray_mins(random)}")
    print(f"1 to 30000 rising -> {sum_subarray_mins(rising)}")
    print(f"30000 copies of 30000 -> {sum_subarray_mins(flat)}")


main()
