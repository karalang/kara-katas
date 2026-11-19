# LeetCode #1647: Minimum Deletions to Make Character Frequencies Unique --
# the bench's Python mirror: the ★ arm on 500 random strings of 100000
# letters, each from the first 1 to 26 of the alphabet, all drawn first.


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


seed = 1647


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


strings = []
for _ in range(500):
    letters = next_random() % 26 + 1
    strings.append("".join(chr(ord("a") + next_random() % letters) for _ in range(100000)))
check = 0
total = 0
for s in strings:
    deletions = min_deletions(s)
    total += deletions
    check = (check * 31 + deletions + 1) % 1000000007
print(f"500 strings of 100000 letters: deletions sum to {total}, checksum {check}")
