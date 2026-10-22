# Benchmark for #852: Peak Index in a Mountain Array -- Python twin of the
# Kāra ★ arm (binary search on the slope).


def peak_index_in_mountain_array(arr):
    lo = 0
    hi = len(arr) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < arr[mid + 1]:
            lo = mid + 1
        else:
            hi = mid
    return lo


seed = 852


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count = 64
    rounds = 30000000
    n = 100000
    arrays = []
    for g in range(count):
        step = 1 + g % 10
        peak = 1 + (next_random() * 32768 + next_random()) % (n - 2)
        arr = []
        v = 0
        low = 0
        for i in range(n):
            if i > 0:
                if i <= peak:
                    v += 1 + next_random() % step
                else:
                    v -= 1 + next_random() % step
            arr.append(v)
            low = min(low, v)
        arrays.append([x - low for x in arr])
    total = 0
    checksum = 0
    for round_ in range(rounds):
        p = peak_index_in_mountain_array(arrays[round_ % count])
        total += p
        checksum = (checksum * 31 + p) % 1000000007
    print(f"{rounds} rounds of {count} mountains: peaks sum to {total}, checksum {checksum}")


main()
