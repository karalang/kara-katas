# LeetCode #1574: Shortest Subarray to be Removed to Make Array Sorted --
# bench: the ★ arm (a sorted prefix joined to a sorted suffix by two
# pointers) over 20 arrays of 500000 values, each a rising first half, a
# stretch of random values and a rising second half that starts low, built
# once; then 3 rounds answering all 20, 60 answers.


def shortest(arr):
    n = len(arr)
    left = 0
    while left + 1 < n and arr[left] <= arr[left + 1]:
        left += 1
    if left == n - 1:
        return 0
    right = n - 1
    while right > 0 and arr[right - 1] <= arr[right]:
        right -= 1
    best = min(n - left - 1, right)
    j = right
    for i in range(left + 1):
        while j < n and arr[j] < arr[i]:
            j += 1
        best = min(best, j - i - 1)
    return best


seed = 1574


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def main():
    n = 500000
    arrays = []
    for _ in range(20):
        middle = next_random() % 1000 + 1
        start = (n - middle) // 2
        arr = []
        v = 0
        for i in range(n):
            if i == start + middle:
                v = next_random() % 1000
            if start <= i < start + middle:
                arr.append(next_random() % 4000000)
            else:
                v += next_random() % 8
                arr.append(v)
        arrays.append(arr)
    check = 0
    total = 0
    for _ in range(3):
        for arr in arrays:
            length = shortest(arr)
            total += length
            check = mix(check, length)
    print(f"60 answers over 20 arrays of {n} values: lengths total {total}, checksum {check}")


main()
