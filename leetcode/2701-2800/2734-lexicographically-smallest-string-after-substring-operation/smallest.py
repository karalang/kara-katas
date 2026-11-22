# LeetCode #2734: Lexicographically Smallest String After Substring
# Operation -- Python mirror of smallest.kara (the ★ arm): the run from
# the first letter that is not an 'a' up to the next 'a' moved back a
# letter, or the last letter of a string of 'a's made 'z'.


def smallest_string(s):
    b = bytearray(s, "ascii")
    n = len(b)
    i = 0
    while i < n and b[i] == ord("a"):
        i += 1
    if i == n:
        b[n - 1] = ord("z")
    else:
        while i < n and b[i] != ord("a"):
            b[i] -= 1
            i += 1
    return b.decode("ascii")


seed = 2734


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(n, rare):
    word = []
    for _ in range(n):
        if next_random() % rare == 0:
            word.append("a")
        else:
            word.append(chr(ord("b") + next_random() % 25))
    return "".join(word)


def main():
    for s in ["cbabc", "acbbc", "leetcode", "a", "aaaa", "b", "aazzz", "abcadef"]:
        print(smallest_string(s))
    total = 0
    check = 0
    for _ in range(5000):
        n = next_random() % 30 + 1
        rare = next_random() % 4 + 1
        answer = smallest_string(random_word(n, rare))
        for ch in answer:
            total += ord(ch) - ord("a")
            check = (check * 31 + ord(ch) - ord("a")) % 1000000007
        check = (check * 31 + 26) % 1000000007
    print(f"5000 words: letters sum to {total}, checksum {check}")


main()
