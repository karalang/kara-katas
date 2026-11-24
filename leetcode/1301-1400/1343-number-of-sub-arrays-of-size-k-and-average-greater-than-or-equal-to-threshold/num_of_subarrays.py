# LeetCode #1343: Number of Sub-arrays of Size K and Average Greater than
# or Equal to Threshold -- Python mirror of the ★ arm: a sliding window of
# the last k values, counted when its sum reaches k * threshold.


def num_of_subarrays(arr, k, threshold):
    need = k * threshold
    s = 0
    count = 0
    for i, x in enumerate(arr):
        s += x
        if i >= k:
            s -= arr[i - k]
        if i >= k - 1 and s >= need:
            count += 1
    return count


seed = 1343


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    e1 = num_of_subarrays([2, 2, 2, 2, 5, 5, 5, 8], 3, 4)
    e2 = num_of_subarrays([11, 13, 17, 23, 29, 31, 7, 5, 2, 3], 3, 5)
    one = num_of_subarrays([7], 1, 7)
    big = [1 + next_random() % 10000 for _ in range(100000)]
    print(f"{e1} {e2} {one} {num_of_subarrays(big, 1000, 4700)} {num_of_subarrays(big, 1, 0)} {num_of_subarrays(big, 100000, 4697)}")
    check = 0
    for t in range(1000):
        n = 1 + next_random() % 300 if t % 10 == 0 else 1 + next_random() % 20
        top = 10 if t % 2 == 0 else 10000
        arr = [1 + next_random() % top for _ in range(n)]
        k = 1 + next_random() % n
        threshold = next_random() % (top + 1)
        check = (check * 131 + num_of_subarrays(arr, k, threshold)) % 1000000007
    print(f"1000 random arrays: checksum {check}")


main()
