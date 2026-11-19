# LeetCode #1653: Minimum Deletions to Make String Balanced -- the bench's
# Python mirror: the ★ arm on 500 random strings of 100000 a's and b's,
# each with its own chance of a b, all drawn first.


def minimum_deletions(s):
    deletions = 0
    bs = 0
    for c in s:
        if c == "b":
            bs += 1
        else:
            deletions = min(deletions + 1, bs)
    return deletions


seed = 1653


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


strings = []
for _ in range(500):
    percent = next_random() % 101
    strings.append("".join("b" if next_random() % 100 < percent else "a" for _ in range(100000)))
check = 0
total = 0
for s in strings:
    deletions = minimum_deletions(s)
    total += deletions
    check = (check * 31 + deletions + 1) % 1000000007
print(f"500 strings of 100000 letters: deletions sum to {total}, checksum {check}")
