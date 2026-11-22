# LeetCode #2802: Find The K-th Lucky Number -- the bench in Python: the
# ★ arm over 200000 k up to 10^9, all drawn first, then each answered 10
# times.


def kth_lucky_number(k):
    n = k + 1
    top = 1
    while top * 2 <= n:
        top *= 2
    lucky = ""
    bit = top // 2
    while bit > 0:
        lucky += "4" if n & bit == 0 else "7"
        bit //= 2
    return lucky


seed = 2802


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def digest(s):
    h = 0
    for b in s.encode():
        h = (h * 131 + b) % 1000000007
    return h


def main():
    count = 200000
    rounds = 10
    ks = [wide() % 1000000000 + 1 for _ in range(count)]
    total = 0
    check = 0
    for r in range(rounds):
        for k in ks:
            s = kth_lucky_number(k)
            total += len(s)
            check = (check * 31 + digest(s) + r) % 1000000007
    print(f"{count} k up to 10^9, {rounds} rounds: lengths sum to {total}, checksum {check}")


main()
