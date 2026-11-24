# LeetCode #1338 bench, Python mirror of the Kāra bench: the ★ arm on 20
# arrays of 10^5 values built once, then 30 passes, each setting one value
# of every array from the checksum so far, answering every array.


def min_set_size(arr):
    counts = {}
    for x in arr:
        counts[x] = counts.get(x, 0) + 1
    sizes = sorted(counts.values(), reverse=True)
    removed = 0
    chosen = 0
    for s in sizes:
        if 2 * removed >= len(arr):
            break
        removed += s
        chosen += 1
    return chosen


seed = 1338


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    n = 100000
    arrays = []
    for t in range(20):
        top = 100000 if t % 2 == 0 else 1000
        arr = []
        for _ in range(n):
            a = next_random()
            arr.append(1 + (a * 32768 + next_random()) % top)
        arrays.append(arr)
    check = 0
    for p in range(30):
        for t in range(20):
            at = check % n
            arrays[t][at] = 1 + check // 3 % 1000
            answer = min_set_size(arrays[t])
            check = (check * 31 + answer + p) % 1000000007
    print(f"30 passes over 20 arrays of 10^5: checksum {check}")


main()
