# Benchmark for #658: binary search for the window, as the Kara ★ arm.


def find_closest_elements(arr, k, x):
    low, high = 0, len(arr) - k
    while low < high:
        middle = (low + high) // 2
        if x - arr[middle] > arr[middle + k] - x:
            low = middle + 1
        else:
            high = middle
    return arr[low:low + k]


seed = 658


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    n, queries = 1000000, 1000000
    arr = []
    for _ in range(n):
        hi = next_random()
        lo = next_random()
        arr.append((hi * 32768 + lo) % 2000001 - 1000000)
    arr.sort()
    checksum = 0
    for q in range(queries):
        k = 1 + q % 64
        hi = next_random()
        lo = next_random()
        x = (hi * 32768 + lo) % 2200001 - 1100000
        got = find_closest_elements(arr, k, x)
        checksum = (checksum * 31 + got[0] * 3 + got[-1] * 5 + len(got) + 10000000) % 1000000007
    print(f"{n} numbers, {queries} queries: checksum {checksum}")


main()
