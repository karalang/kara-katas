# LeetCode #1310: XOR Queries of a Subarray -- the Python mirror of the ★ arm
# (the XOR of every prefix, a range's XOR from two prefixes), with the same
# harness.


def xor_queries(arr, queries):
    prefix = [0] * (len(arr) + 1)
    for i, x in enumerate(arr):
        prefix[i + 1] = prefix[i] ^ x
    return [prefix[r + 1] ^ prefix[l] for l, r in queries]


seed = 1310


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(v):
    return ",".join(str(x) for x in v)


def main():
    e1 = xor_queries([1, 3, 4, 8], [[0, 1], [1, 2], [0, 3], [3, 3]])
    e2 = xor_queries([4, 8, 2, 10], [[2, 3], [1, 3], [0, 0], [0, 3]])
    one = xor_queries([7], [[0, 0]])
    big = xor_queries([1000000000, 1000000000, 999999999], [[0, 1], [0, 2], [1, 2]])
    print(f"{show(e1)} {show(e2)} {show(one)} {show(big)}")
    total = 0
    check = 0
    for i in range(1000):
        top = 2 if i % 3 == 0 else 1001 if i % 3 == 1 else 1000000001
        n = 1 + next_random() % 300
        arr = []
        for _ in range(n):
            hi = next_random()
            arr.append((hi * 65536 + next_random()) % top)
        q = 1 + next_random() % 300
        queries = []
        for _ in range(q):
            a = next_random() % n
            b = next_random() % n
            queries.append([a, b] if a <= b else [b, a])
        got = xor_queries(arr, queries)
        total += len(got)
        for x in got:
            check = (check * 31 + x) % 1000000007
    print(f"1000 random arrays: {total} answers, checksum {check}")


main()
