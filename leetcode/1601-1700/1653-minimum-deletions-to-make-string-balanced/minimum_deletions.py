# LeetCode #1653: Minimum Deletions to Make String Balanced -- the Python
# mirror of the ★ arm: one pass, each a either deleted or kept with every
# b before it deleted.


def minimum_deletions(s):
    deletions = 0
    bs = 0
    for c in s:
        if c == "b":
            bs += 1
        else:
            deletions = min(deletions + 1, bs)
    return deletions


# ---- the harness: the same as every arm's ---------------------------------

seed = 1653


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def batch(count, most):
    check = 0
    total = 0
    for _ in range(count):
        n = (next_random() * 32768 + next_random()) % most + 1
        s = "".join("a" if next_random() % 2 == 0 else "b" for _ in range(n))
        answer = minimum_deletions(s)
        total += answer
        check = (check * 31 + answer + 1) % 1000000007
    print(f"{count} strings of up to {most} letters: deletions sum to {total}, checksum {check}")


print(minimum_deletions("aababbab"))
print(minimum_deletions("bbaaaaabb"))
print(minimum_deletions("a"))
print(minimum_deletions("bbbb"))
print(minimum_deletions("bbbaa"))
batch(3000, 10)
batch(1000, 1000)
batch(20, 100000)
