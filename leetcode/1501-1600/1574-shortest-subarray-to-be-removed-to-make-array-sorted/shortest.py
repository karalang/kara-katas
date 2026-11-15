# LeetCode #1574: Shortest Subarray to be Removed to Make Array Sorted --
# the Python mirror of the ★ arm: what is kept is a sorted prefix and a
# sorted suffix that joins it; two pointers walk the longest sorted prefix
# and, for each end of it, move the start of the suffix right until its
# first value is not below the prefix's last. O(n)


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


# ---- the harness: the same in every arm

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def batch(count, most, falls, top):
    check = 0
    total = 0
    for _ in range(count):
        n = (next_random() * 32768 + next_random()) % most + 1
        odds = next_random() % falls + 1
        arr = []
        v = (next_random() * 32768 + next_random()) % top
        for _ in range(n):
            if next_random() % odds == 0:
                v = (next_random() * 32768 + next_random()) % top
            else:
                v = min(v + next_random() % 3, top - 1)
            arr.append(v)
        length = shortest(arr)
        total += length
        check = mix(check, length)
    print(f"{count} arrays of up to {most} values: lengths total {total}, checksum {check}")


def main():
    global seed
    examples = [
        [1, 2, 3, 10, 4, 2, 3, 5],
        [5, 4, 3, 2, 1],
        [1, 2, 3],
        [1],
        [2, 2, 2, 1, 1, 1],
        [1, 2, 3, 3, 10, 1, 3, 3, 5],
        [6, 3, 10, 11, 15, 20, 13, 3, 18, 12],
    ]
    for arr in examples:
        print(f"{arr} -> {shortest(arr)}")
    seed = 1574
    batch(3000, 10, 4, 6)
    batch(300, 1000, 200, 1000000000)
    batch(30, 100000, 20000, 1000000000)


main()
