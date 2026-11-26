# LeetCode #1451 Rearrange Words in a Sentence: the bench, a mirror of
# arrange_words.kara.


def arrange_words(text):
    # the words lowered, sorted by length with ties kept in order by the
    # stable sort, joined, and the first letter raised
    words = [w.lower() for w in text.split(" ")]
    words.sort(key=len)
    joined = " ".join(words)
    return joined[:1].upper() + joined[1:]


def main():
    # 200 texts of 15000 words of 1 to 10 letters, the constraints' most,
    # each arranged and its letters folded to a checksum
    seed = 1451
    check = 0
    for _ in range(200):
        letters = []
        for i in range(15000):
            if i > 0:
                letters.append(" ")
            seed = (seed * 1103515245 + 12345) % 2147483648
            length = 1 + seed // 65536 % 10
            for j in range(length):
                seed = (seed * 1103515245 + 12345) % 2147483648
                c = chr(97 + seed // 65536 % 26)
                letters.append(c.upper() if i == 0 and j == 0 else c)
        for b in arrange_words("".join(letters)).encode():
            check = (check * 131 + b) % 1000000007
    print(f"200 texts of 15000 words: checksum {check}")


main()
