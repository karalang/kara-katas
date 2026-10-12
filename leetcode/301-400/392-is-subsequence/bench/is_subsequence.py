# Benchmark for #392: mirror of is_subsequence.kara (two pointers).


def is_subsequence(s, t):
    i = 0
    n = len(s)
    for b in t:
        if i < n and s[i] == b:
            i += 1
    return i == n


seed = 392


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def big():
    hi = step()
    return hi * 32768 + step()


def main():
    pool = bytes(step() % 26 + 97 for _ in range(1000000))
    yes = 0
    checksum = 0
    for _ in range(20000):
        a = big() % (1000000 - 100)
        length = step() % 10001
        b = big() % (1000000 - length)
        r = is_subsequence(pool[a:a + 100], memoryview(pool)[b:b + length])
        if r:
            yes += 1
        checksum = (checksum * 3 + (1 if r else 2)) % 1000000007
    print(f"20000 pairs: {yes} subsequences, checksum {checksum}")


main()
