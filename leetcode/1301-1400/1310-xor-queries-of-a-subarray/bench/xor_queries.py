# LeetCode #1310 bench, Python: the ★ arm (a prefix XOR, each answer the XOR
# of the prefixes at the range's two ends) on the same 10 arrays and 100
# passes.


def xor_queries(arr, queries):
    prefix = [0] * (len(arr) + 1)
    for i in range(len(arr)):
        prefix[i + 1] = prefix[i] ^ arr[i]
    return [prefix[q[1] + 1] ^ prefix[q[0]] for q in queries]


seed = 1310


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    n = 30000
    m = 30000
    arrays = []
    ranges = []
    for _ in range(10):
        arr = []
        for _ in range(n):
            hi = next_random()
            lo = next_random()
            arr.append(1 + (hi * 65536 + lo) % 1000000000)
        arrays.append(arr)
        queries = []
        for _ in range(m):
            a = next_random() % n
            b = next_random() % n
            queries.append([a, b] if a <= b else [b, a])
        ranges.append(queries)
    check = 0
    for p in range(100):
        for a in range(10):
            arrays[a][check % n] = 1 + (check // 7) % 1000000000
            x = (check // 11) % n
            y = (check // 13) % n
            ranges[a][check % m] = [x, y] if x <= y else [y, x]
            got = xor_queries(arrays[a], ranges[a])
            check = (check * 31 + got[(check // 3) % m]) % 1000000007
            check = (check * 31 + got[(check // 17) % m] + p) % 1000000007
    print(f"100 passes over 10 arrays of 3 * 10^4: checksum {check}")


main()
