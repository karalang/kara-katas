# LeetCode #1647: Minimum Deletions to Make Character Frequencies Unique --
# the Python mirror of the ★ arm: the counts sorted from largest down,
# each capped at one less than the one before it kept.


def min_deletions(s):
    counts = [0] * 26
    for c in s:
        counts[ord(c) - ord("a")] += 1
    counts.sort(reverse=True)
    deletions = 0
    cap = counts[0]
    for c in counts:
        keep = min(c, cap)
        deletions += c - keep
        cap = max(keep - 1, 0)
    return deletions


# ---- the harness: the same as every arm's ---------------------------------

seed = 1647


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def batch(count, long, letters):
    check = 0
    total = 0
    for _ in range(count):
        n = (next_random() * 32768 + next_random()) % long + 1
        s = "".join(chr(ord("a") + next_random() % letters) for _ in range(n))
        deletions = min_deletions(s)
        total += deletions
        check = (check * 31 + deletions + 1) % 1000000007
    print(f"{count} strings of up to {long} letters from {letters}: deletions sum to {total}, checksum {check}")


print(min_deletions("aab"))
print(min_deletions("aaabbbcc"))
print(min_deletions("ceabaacb"))
print(min_deletions("z"))
print(min_deletions("abcdefghijklmnopqrstuvwxyz"))
print(min_deletions("aaaabbbbccccdddd"))
batch(3000, 10, 4)
batch(1000, 1000, 26)
batch(20, 100000, 26)
