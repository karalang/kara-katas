# LeetCode #658: Find K Closest Elements -- binary search for the window.
# Mirrors the ★ arm (find_k_closest_elements.kara) and its test harness.


def find_closest_elements(arr, k, x):
    low, high = 0, len(arr) - k
    while low < high:
        middle = (low + high) // 2
        if x - arr[middle] > arr[middle + k] - x:
            low = middle + 1
        else:
            high = middle
    return arr[low:low + k]


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(arr, k, x):
    got = find_closest_elements(arr, k, x)
    print(f"[{','.join(map(str, arr))}], k = {k}, x = {x} -> [{','.join(map(str, got))}]")


def random_sorted(n, spread):
    arr = [next_random() % (2 * spread + 1) - spread for _ in range(n)]
    arr.sort()
    return arr


def checksum(got):
    h = 0
    for a in got:
        h = (h * 31 + a + 20000) % 1000000007
    return h


def main():
    global seed
    show([1, 2, 3, 4, 5], 4, 3)
    show([1, 1, 2, 3, 4, 5], 4, -1)
    show([7], 1, 100)
    show([-3, 0, 4], 3, 1)
    show([1, 2, 3, 4, 5], 2, 99)
    show([1, 3, 5, 7], 1, 4)
    show([2, 2, 2, 5, 5, 5], 4, 4)
    seed = 658
    s = 0
    total = 0
    for _ in range(300):
        n = 1 + next_random() % 50
        arr = random_sorted(n, 20)
        k = 1 + next_random() % n
        x = next_random() % 51 - 25
        got = find_closest_elements(arr, k, x)
        total += sum(got)
        s = (s * 7 + checksum(got)) % 1000000007
    print(f"300 random arrays: total {total}, checksum {s}")
    arr = random_sorted(10000, 10000)
    print(f"10000 numbers, k = 100, x = 17: checksum {checksum(find_closest_elements(arr, 100, 17))}")
    print(f"10000 numbers, k = 10000, x = 0: checksum {checksum(find_closest_elements(arr, 10000, 0))}")
    print(f"10000 numbers, k = 3, x = -10000: checksum {checksum(find_closest_elements(arr, 3, -10000))}")


main()
