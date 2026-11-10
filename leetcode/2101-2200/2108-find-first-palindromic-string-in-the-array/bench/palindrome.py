# LeetCode #2108: Find First Palindromic String in the Array -- the
# benchmark, the same algorithm as palindrome.kara: each word's bytes read
# from both ends towards the middle.


def is_palindrome(w):
    b = w.encode()
    i = 0
    j = len(b) - 1
    while i < j:
        if b[i] != b[j]:
            return False
        i += 1
        j -= 1
    return True


def first_palindrome(words):
    for w in words:
        if is_palindrome(w):
            return w
    return ""


seed = 2108


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    lists = []
    for _ in range(200):
        words = []
        for _ in range(100):
            letters = [next_random() % 26 for _ in range(50)]
            letters += letters[::-1]
            if next_random() % 200 != 0:
                at = 25 + next_random() % 50
                letters[at] = (letters[at] + 1 + next_random() % 25) % 26
            words.append("".join(alphabet[l] for l in letters))
        lists.append(words)
    found = 0
    letters_total = 0
    check = 0
    for _ in range(50):
        for words in lists:
            got = first_palindrome(words)
            if len(got) > 0:
                found += 1
            letters_total += len(got)
            for c in got[:3]:
                check = (check * 31 + ord(c)) % 1000000007
            check = (check * 31 + len(got)) % 1000000007
    print(f"10000 searches: {found} found, {letters_total} letters, checksum {check}")


main()
