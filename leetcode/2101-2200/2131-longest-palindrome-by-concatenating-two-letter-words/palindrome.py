# LeetCode #2131: Longest Palindrome by Concatenating Two Letter Words --
# the mirror of palindrome.kara: the words counted in a 26 by 26 table,
# mirrored pairs four letters each, and one doubled word in the middle.


def longest_palindrome(words):
    count = [0] * (26 * 26)
    for w in words:
        count[(ord(w[0]) - 97) * 26 + (ord(w[1]) - 97)] += 1
    length = 0
    middle = False
    for x in range(26):
        length += count[x * 26 + x] // 2 * 4
        if count[x * 26 + x] % 2 == 1:
            middle = True
        for y in range(x + 1, 26):
            length += min(count[x * 26 + y], count[y * 26 + x]) * 4
    if middle:
        length += 2
    return length


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def show(words):
    print(f"[{', '.join(words)}] -> {longest_palindrome(words)}")


def main():
    show(["lc", "cl", "gg"])
    show(["ab", "ty", "yt", "lc", "cl", "ab"])
    show(["cc", "ll", "xx"])
    show(["aa"])
    show(["aa", "aa"])
    show(["ab", "ba", "ba"])
    show(["ab"])
    letters = "abcdefghijklmnopqrstuvwxyz"
    seed = [2131]
    total = 0
    check = 0
    for rnd in range(2000):
        n = next_random(seed) % 12 + 1
        k = [2, 3, 5][rnd % 3]
        words = []
        for _ in range(n):
            a = next_random(seed) % k
            b = next_random(seed) % k
            words.append(letters[a] + letters[b])
        length = longest_palindrome(words)
        total += length
        check = (check * 31 + length) % 1000000007
    print(f"2000 lists: {total} letters in all, checksum {check}")
    same = ["aa"] * 100000
    turns = ["ab" if i % 2 == 0 else "ba" for i in range(100000)]
    rand = []
    for _ in range(100000):
        a = next_random(seed) % 26
        b = next_random(seed) % 26
        rand.append(letters[a] + letters[b])
    x = longest_palindrome(same)
    y = longest_palindrome(turns)
    z = longest_palindrome(rand)
    print(f"100000 words: {x} of one, {y} in turn, {z} at random")


main()
