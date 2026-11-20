# LeetCode #1754: Largest Merge Of Two Strings -- mirrors merge.kara (the
# ★ arm): the larger rest goes first.


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


def word(most, letters):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    n = next_random() % most + 1
    return "".join(alphabet[next_random() % letters] for _ in range(n))


def batch(count, most, letters):
    check = 0
    first_a = 0
    for _ in range(count):
        word1 = word(most, letters)
        word2 = word(most, letters)
        merge = largest_merge(word1, word2)
        for b in merge.encode():
            check = (check * 31 + b) % 1000000007
        if merge.startswith("a"):
            first_a += 1
    print(f"{count} pairs of up to {most} letters from {letters}: {first_a} start with a, checksum {check}")


print(largest_merge("cabaa", "bcaaa"))
print(largest_merge("abcabc", "abdcaba"))
print(largest_merge("a", "b"))
print(largest_merge("abc", "abc"))
print(largest_merge("ba", "bab"))
print(largest_merge("aaaab", "aaaac"))
batch(3000, 6, 2)
batch(1000, 100, 3)
batch(10, 3000, 2)
