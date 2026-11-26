# LeetCode #1768: Merge Strings Alternately -- the bench in Python,
# mirroring merge_alternately.kara: one index walking both words, a letter
# from each word that still has one.

def merge_alternately(word1, word2):
    merged = []
    for i in range(max(len(word1), len(word2))):
        if i < len(word1):
            merged.append(word1[i])
        if i < len(word2):
            merged.append(word2[i])
    return "".join(merged)

seed = 1768
def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536

def main():
    words = []
    for _ in range(1000):
        n = 1 + next_random() % 100
        words.append("".join(chr(97 + next_random() % 26) for _ in range(n)))
    check = 0
    for call in range(2000000):
        a = (check + call * 7919) % 1000
        b = (check // 3 + call * 104729) % 1000
        merged = merge_alternately(words[a], words[b])
        at = check % len(merged)
        check = (check * 31 + len(merged) + ord(merged[at])) % 1000000007
    print(f"2000000 calls over 1000 words: checksum {check}")

main()
