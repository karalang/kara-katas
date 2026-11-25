# LeetCode #1299 bench: the ★ arm (one walk from the right end, each place
# given the greatest seen so far) over 50 arrays of 10^4 numbers up to 10^5,
# built once; then 1000 passes, each setting one number of every array from the
# checksum so far, answering it, and folding two of its answers, chosen by the
# checksum, into the checksum.


def replace_elements(arr):
    n = len(arr)
    out = [-1] * n
    greatest = -1
    for i in range(n - 1, -1, -1):
        out[i] = greatest
        if arr[i] > greatest:
            greatest = arr[i]
    return out


seed = 1299


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    arrays = []
    for _ in range(50):
        arr = []
        for _ in range(10000):
            hi = next_random()
            arr.append(1 + (hi * 32768 + next_random()) % 100000)
        arrays.append(arr)
    check = 0
    for p in range(1000):
        for arr in arrays:
            arr[check % 10000] = 1 + check * 7919 % 100000
            out = replace_elements(arr)
            check = (check * 31 + out[check % 10000] + out[(check // 7) % 10000] + p) % 1000000007
    print(f"1000 passes over 50 arrays of 10^4: checksum {check}")


main()
