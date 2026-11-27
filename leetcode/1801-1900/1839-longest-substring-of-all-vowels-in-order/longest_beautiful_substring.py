# LeetCode #1839: Longest Substring Of All Vowels in Order -- the ★ arm in
# Python


def longest_beautiful_substring(word):
    best = 0
    length = 1
    vowels = 1
    for i in range(1, len(word)):
        if word[i] < word[i - 1]:
            length = 1
            vowels = 1
        else:
            length += 1
            if word[i] > word[i - 1]:
                vowels += 1
        if vowels == 5:
            best = max(best, length)
    return best


seed = 1839


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def word(n):
    vowels = "aeiou"
    out = []
    at = 0
    for _ in range(n):
        roll = next_random() % 10
        if roll < 4:
            pass
        elif roll < 8:
            at = min(at + 1, 4)
        elif roll < 9:
            at = 0
        else:
            at = next_random() % 5
        out.append(vowels[at])
    return "".join(out)


def main():
    f = longest_beautiful_substring
    print(f"{f('aeiaaioaaaaeiiiiouuuooaauuaeiu')} {f('aeeeiiiioooauuuaeiou')} {f('a')}")
    print(f"{f('aeiou')} {f('uoiea')} {f('aeiiuu')} {f('eiouaeiou')} {f('aeiouaaeeiioouu')} {f('aaeiaeiouu')}")
    drawn = word(500000)
    whole = "a" * 100000 + "e" * 100000 + "i" * 100000 + "o" * 100000 + "u" * 100000
    print(f"the most: {f(drawn)} {f(whole)}")
    check = 0
    for _ in range(3000):
        n = 1 + next_random() % 30
        w = word(n)
        check = (check * 31 + f(w)) % 1000000007
    print(f"3000 random words: checksum {check}")


main()
