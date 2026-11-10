# LeetCode #2108: Find First Palindromic String in the Array -- Python
# mirror of palindrome.kara: each word in order, its bytes read from both
# ends towards the middle. O(total letters).


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


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def draw(n, longest, letters):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    words = []
    for _ in range(n):
        length = next_random() % longest + 1
        words.append("".join(alphabet[next_random() % letters] for _ in range(length)))
    return words


def main():
    global seed
    examples = [
        ["abc", "car", "ada", "racecar", "cool"],
        ["notapalindrome", "racecar"],
        ["def", "ghi"],
        ["z"],
        ["abca", "abba", "aba"],
        ["ab", "ba", "abc", "cbc"],
        ["xyx", "xyx"],
    ]
    for words in examples:
        print(f'[{", ".join(words)}] -> "{first_palindrome(words)}"')
    seed = 2108
    found = 0
    letters_total = 0
    check = 0
    for _ in range(3000):
        n = next_random() % 20 + 1
        longest = next_random() % 6 + 1
        letters = next_random() % 4 + 2
        words = draw(n, longest, letters)
        got = first_palindrome(words)
        if len(got) > 0:
            found += 1
        letters_total += len(got)
        check = (check * 31 + len(got)) % 1000000007
        for c in got:
            check = (check * 31 + ord(c)) % 1000000007
    print(f"3000 lists: {found} with a palindrome, {letters_total} letters, checksum {check}")
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    big = [alphabet[i % 26] * 99 + alphabet[(i + 1) % 26] for i in range(99)]
    big.append("a" + "b" * 98 + "a")
    print(f"largest, the last -> {len(first_palindrome(big))} letters")
    big[99] = "a" + "b" * 98 + "c"
    print(f'largest, none -> "{first_palindrome(big)}"')


main()
