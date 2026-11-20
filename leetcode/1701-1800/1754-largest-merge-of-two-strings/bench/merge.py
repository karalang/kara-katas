# LeetCode #1754: Largest Merge Of Two Strings -- the bench (merge.kara in
# Python): the larger rest goes first.


def largest_merge(word1, word2):
    merge = []
    i = j = 0
    while i < len(word1) or j < len(word2):
        if word1[i:] > word2[j:]:
            merge.append(word1[i])
            i += 1
        else:
            merge.append(word2[j])
            j += 1
    return "".join(merge)


seed = 1754


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# `n` letters, `a` but for a `b` one time in 300, so that the two rests
# often tie for a long way
def word(n):
    return "".join("b" if next_random() % 300 == 0 else "a" for _ in range(n))


count, rounds, n = 200, 20, 3000
pairs = []
for _ in range(count):
    word1 = word(n)
    word2 = word(n)
    pairs.append((word1, word2))
check = 0
for r in range(rounds):
    for word1, word2 in pairs:
        merge = largest_merge(word1, word2)
        check = (check * 31 + r) % 1000000007
        for b in merge.encode():
            check = (check * 31 + b) % 1000000007
print(f"{count} pairs of {n} letters, {rounds} rounds: checksum {check}")
