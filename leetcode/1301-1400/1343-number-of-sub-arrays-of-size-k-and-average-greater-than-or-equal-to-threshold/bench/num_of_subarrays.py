# LeetCode #1343 bench in Python: the ★ arm (a sliding window of the last
# k values, counted when its sum reaches k * threshold) on the same 10
# arrays of 10^5 values and 60 passes.


def num_of_subarrays(arr, k, threshold):
    need = k * threshold
    s = 0
    count = 0
    for i in range(len(arr)):
        s += arr[i]
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
    n = 100000
    arrays = [[1 + next_random() % 10000 for _ in range(n)] for _ in range(10)]
    check = 0
    for pass_ in range(60):
        for a in range(10):
            arr = arrays[a]
            arr[check % n] = 1 + (check // 7) % 10000
            k = 1 + check % 1000
            threshold = 4500 + check % 400
            answer = num_of_subarrays(arr, k, threshold)
            check = (check * 31 + answer + pass_) % 1000000007
    print(f"60 passes over 10 arrays of 10^5: checksum {check}")


main()
