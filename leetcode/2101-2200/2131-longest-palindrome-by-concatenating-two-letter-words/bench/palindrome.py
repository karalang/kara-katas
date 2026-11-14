# LeetCode #2131: Longest Palindrome by Concatenating Two Letter Words --
# the benchmark, the same algorithm as palindrome.kara.


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


seed = 2131


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def word():
    letters = "abcdefgh"
    a = next_random() % 8
    b = next_random() % 8
    return letters[a] + letters[b]


def main():
    lists = [[word() for _ in range(100000)] for _ in range(20)]
    total = 0
    check = 0
    for rnd in range(10):
        for k in range(20):
            hi = next_random()
            at = (hi * 32768 + next_random()) % 100000
            lists[k][at] = word()
            length = longest_palindrome(lists[k])
            total += length
            check = (check * 31 + length + rnd) % 1000000007
    print(f"200 solves: {total} letters in all, checksum {check}")


main()
