# Benchmark: LeetCode #1089 Duplicate Zeros -- mirrors duplicate_zeros.kara:
# count the zeros, then walk back from the end writing each digit at its
# place shifted by the zeros up to it, over 200 random arrays of 10^4
# digits built once, each copied and duplicated in each of 100 rounds.


def duplicate_zeros(arr):
    n = len(arr)
    zeros = 0
    for x in arr:
        if x == 0:
            zeros += 1
    for i in range(n - 1, -1, -1):
        if i + zeros < n:
            arr[i + zeros] = arr[i]
        if arr[i] == 0:
            zeros -= 1
            if i + zeros < n:
                arr[i + zeros] = 0


seed = 1089


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    arrays = []
    for _ in range(200):
        arr = []
        for _ in range(10000):
            r = next_random() % 15
            arr.append(0 if r < 5 else r - 5)
        arrays.append(arr)
    zeros = 0
    check = 0
    for rnd in range(100):
        for k, a in enumerate(arrays):
            work = list(a)
            duplicate_zeros(work)
            at = (rnd * 7919 + k * 31) % 10000
            if work[at] == 0:
                zeros += 1
            check = (check * 31 + work[at] * 10 + work[9999]) % 1000000007
    print(f"100 rounds over 200 arrays of 10^4 digits: {zeros} zeros sampled, checksum {check}")


main()
