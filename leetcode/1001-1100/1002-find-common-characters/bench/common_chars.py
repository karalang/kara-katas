# Benchmark: LeetCode #1002 Find Common Characters -- the ★ arm, the
# least count of each letter, on lists of 100 words of 100 letters,
# LeetCode's largest. Mirrors common_chars.kara, .c, .rs and go-seq/.


def common_chars(words):
    least = [1000] * 26
    for word in words:
        count = [0] * 26
        for c in word:
            count[ord(c) - ord('a')] += 1
        for i in range(26):
            least[i] = min(least[i], count[i])
    ans = []
    for i in range(26):
        for _ in range(least[i]):
            ans.append(chr(i + ord('a')))
    return ans


seed = 1002


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds = 1000
    # 20 lists of 100 words of 100 letters, list t drawing its letters
    # from the first 2 + t % 10 of the alphabet
    lists = []
    for t in range(20):
        alphabet = 2 + t % 10
        words = []
        for _ in range(100):
            word = ""
            for _ in range(100):
                word += chr(97 + next_random() % alphabet)
            words.append(word)
        lists.append(words)
    found = 0
    check = 0
    for r in range(rounds):
        for i in range(20):
            ans = common_chars(lists[(r + i) % 20])
            found += len(ans)
            for s in ans:
                for c in s:
                    check = (check * 31 + ord(c)) % 1000000007
    print(f"{rounds} rounds over 20 lists of 100 words of 100 letters: "
          f"{found} common letters, checksum {check}")


main()
