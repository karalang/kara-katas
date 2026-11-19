# LeetCode #1657: Determine if Two Strings Are Close -- the bench's Python
# mirror: the ★ arm on 400 random pairs of words of 100000 letters, each
# pair from the first 1 to 26 of the alphabet, half of the second words
# made close by construction, all drawn first.


def close_strings(word1, word2):
    count1 = [0] * 26
    count2 = [0] * 26
    for c in word1:
        count1[ord(c) - ord("a")] += 1
    for c in word2:
        count2[ord(c) - ord("a")] += 1
    for i in range(26):
        if (count1[i] == 0) != (count2[i] == 0):
            return False
    return sorted(count1) == sorted(count2)


seed = 1657


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(n, letters):
    return "".join(chr(ord("a") + next_random() % letters) for _ in range(n))


pairs = []
for _ in range(400):
    alphabet = next_random() % 26 + 1
    word1 = random_word(100000, alphabet)
    if next_random() % 2 == 0:
        word2 = random_word(100000, alphabet)
    else:
        a = chr(ord("a") + next_random() % alphabet)
        b = chr(ord("a") + next_random() % alphabet)
        word2 = "".join(b if c == a else a if c == b else c for c in reversed(word1))
    pairs.append((word1, word2))
check = 0
close = 0
for word1, word2 in pairs:
    answer = close_strings(word1, word2)
    if answer:
        close += 1
    check = (check * 31 + (2 if answer else 1)) % 1000000007
print(f"400 pairs of 100000 letters: {close} close, checksum {check}")
