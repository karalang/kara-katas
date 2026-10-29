# LeetCode #1016: Binary String With Substrings Representing 1 To N --
# bench
# Mirrors query.kara; see ../README.md § Benchmarks.


def query_string(s, n):
    if n - n // 2 > 2 * len(s):
        return False
    x = n
    while x > n // 2:
        if f"{x:b}" not in s:
            return False
        x -= 1
    return True


seed = 1016


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    strings = 200
    length = 1000
    most = 400
    holds = 0
    check = 0
    for _ in range(strings):
        s = "".join("1" if next_random() % 2 == 1 else "0" for _ in range(length))
        for n in range(1, most + 1):
            answer = query_string(s, n)
            if answer:
                holds += 1
            check = (check * 2 + (1 if answer else 0)) % 1000000007
    print(f"{strings} strings of {length} bits, n = 1..{most}: {holds} hold, checksum {check}")


main()
