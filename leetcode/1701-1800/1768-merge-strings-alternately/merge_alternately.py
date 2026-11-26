# LeetCode #1768: Merge Strings Alternately -- the ★ arm in Python: one
# index walking both words, a letter from each word that still has one.

def merge_alternately(word1, word2):
    merged = []
    for i in range(max(len(word1), len(word2))):
        if i < len(word1):
            merged.append(word1[i])
        if i < len(word2):
            merged.append(word2[i])
    return "".join(merged)

seed = 0
def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536

def random_word(n, letters):
    return "".join(chr(97 + next_random() % letters) for _ in range(n))

def digest(s):
    check = len(s)
    for b in s.encode():
        check = (check * 31 + b) % 1000000007
    return check

def main():
    global seed
    print(merge_alternately("abc", "pqr"), merge_alternately("ab", "pqrs"), merge_alternately("abcd", "pq"))
    print(merge_alternately("a", "b"), merge_alternately("a", "bcd"), merge_alternately("abcd", "e"), merge_alternately("zz", "zz"))
    seed = 1768
    long1 = random_word(100, 26)
    long2 = random_word(100, 26)
    one = random_word(1, 26)
    both = merge_alternately(long1, long2)
    lopsided = merge_alternately(one, long1)
    print(f"the most: {len(both)} {digest(both)}, {len(lopsided)} {digest(lopsided)}")
    check = 0
    for _ in range(3000):
        n1 = 1 + next_random() % 20
        n2 = 1 + next_random() % 20
        w1 = random_word(n1, 26)
        w2 = random_word(n2, 26)
        check = (check * 31 + digest(merge_alternately(w1, w2))) % 1000000007
    print(f"3000 random pairs: checksum {check}")

main()
