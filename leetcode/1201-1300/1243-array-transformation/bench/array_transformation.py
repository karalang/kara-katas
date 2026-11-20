# LeetCode #1243: the benchmark, mirroring the Kāra file.


def transform_array(arr):
    cur = arr
    while True:
        nxt = list(cur)
        for i in range(1, len(cur) - 1):
            if cur[i] < cur[i - 1] and cur[i] < cur[i + 1]:
                nxt[i] += 1
            elif cur[i] > cur[i - 1] and cur[i] > cur[i + 1]:
                nxt[i] -= 1
        if nxt == cur:
            return cur
        cur = nxt


def main():
    seed = 1243
    arrays = []
    for _ in range(5000):
        a = []
        for _ in range(100):
            seed = (seed * 1103515245 + 12345) % 2147483648
            a.append(seed // 65536 % 100 + 1)
        arrays.append(a)
    check = 0
    for _ in range(10):
        for a in arrays:
            for v in transform_array(list(a)):
                check = (check * 131 + v) % 1000000007
    print(f"10 rounds of 5000 arrays of 100 values: checksum {check}")


main()
