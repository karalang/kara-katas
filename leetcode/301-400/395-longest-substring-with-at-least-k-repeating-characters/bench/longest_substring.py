# Benchmark for #395: mirror of longest_substring.kara (divide and conquer).


def longest(b, lo, hi, k):
    if hi - lo < k:
        return 0
    count = [0] * 26
    for i in range(lo, hi):
        count[b[i] - 97] += 1
    best = 0
    start = lo
    split = False
    for i in range(lo, hi):
        if count[b[i] - 97] < k:
            split = True
            best = max(best, longest(b, start, i, k))
            start = i + 1
    if not split:
        return hi - lo
    return max(best, longest(b, start, hi, k))


def longest_substring(s, k):
    return longest(s, 0, len(s), k)


seed = 395


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    buf = bytearray()
    for _ in range(1000000):
        x = step() % 26
        y = step() % 26
        buf.append(min(x, y) + 97)
    pool = bytes(buf)
    total = 0
    checksum = 0
    for _ in range(10000):
        hi = step()
        a = (hi * 32768 + step()) % (1000000 - 10000)
        k = 1 + step() % 30
        r = longest_substring(memoryview(pool)[a:a + 10000], k)
        total += r
        checksum = (checksum * 31 + r) % 1000000007
    print(f"10000 windows: total {total}, checksum {checksum}")


main()
