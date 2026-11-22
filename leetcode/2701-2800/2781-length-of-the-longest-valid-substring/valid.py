# LeetCode #2781: Length of the Longest Valid Substring -- the ★ arm in
# Python (valid.kara): the forbidden words in a set, the substrings
# ending at each j of up to 10 letters asked from the shortest, and the
# window's start moved past any found.


def longest_valid_substring(word, forbidden):
    banned = set(forbidden)
    n = len(word)
    start = 0
    best = 0
    for j in range(n):
        i = j
        while i >= start and i + 10 > j:
            if word[i:j + 1] in banned:
                start = i + 1
                break
            i -= 1
        best = max(best, j + 1 - start)
    return best


seed = 2781


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(n, letters):
    return "".join(chr(ord("a") + next_random() % letters) for _ in range(n))


def random_words(count, shortest, longest, letters):
    words = []
    for _ in range(count):
        n = shortest + next_random() % (longest - shortest + 1)
        words.append(random_word(n, letters))
    return words


def main():
    print(longest_valid_substring("cbaaaabc", ["aaa", "cb"]))
    print(longest_valid_substring("leetcode", ["de", "le", "e"]))
    print(longest_valid_substring("a", ["a"]))
    print(longest_valid_substring("a", ["b"]))
    many = "a" * 100000
    print(longest_valid_substring(many, ["aa"]))
    print(longest_valid_substring(many, ["b"]))
    total = 0
    check = 0
    for _ in range(3000):
        n = next_random() % 30 + 1
        word = random_word(n, 3)
        count = next_random() % 10 + 1
        forbidden = random_words(count, 1, 4, 3)
        a = longest_valid_substring(word, forbidden)
        total += a
        check = (check * 31 + a + 1) % 1000000007
    print(f"3000 small cases: lengths sum to {total}, checksum {check}")
    total = 0
    check = 0
    for _ in range(3):
        word = random_word(100000, 5)
        forbidden = random_words(100000, 8, 10, 5)
        a = longest_valid_substring(word, forbidden)
        total += a
        check = (check * 31 + a + 1) % 1000000007
    print(f"3 cases of 10^5: lengths sum to {total}, checksum {check}")


main()
