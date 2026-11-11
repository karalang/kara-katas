# LeetCode #2111: Minimum Operations to Make the Array K-Increasing -- the
# benchmark, the same algorithm as increasing.kara: each chain's patience
# tails, the first tail above each value found with `bisect_right`.

from bisect import bisect_right


def k_increasing(arr, k):
    changes = 0
    for r in range(k):
        tails = []
        length = 0
        i = r
        while i < len(arr):
            x = arr[i]
            at = bisect_right(tails, x)
            if at == len(tails):
                tails.append(x)
            else:
                tails[at] = x
            length += 1
            i += k
        changes += length - len(tails)
    return changes


seed = 2111


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    arrays = []
    for _ in range(10):
        arr = []
        for _ in range(100000):
            hi = next_random()
            lo = next_random()
            arr.append((hi * 32768 + lo) % 100000 + 1)
        arrays.append(arr)
    total = 0
    check = 0
    for rnd in range(10):
        for a in range(10):
            at = rnd * 9973 + a
            arrays[a][at] = arrays[a][at] % 100000 + 1
            got = k_increasing(arrays[a], rnd + 1)
            total += got
            check = (check * 31 + got) % 1000000007
    print(f"100 solves: {total} operations, checksum {check}")


main()
