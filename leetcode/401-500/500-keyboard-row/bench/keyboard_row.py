# Benchmark for #500: Python mirror of the ★ arm (a row number for every
# letter); see keyboard_row.kara.


def find_words(words):
    rows = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]
    row_of = [0] * 26
    for r in range(3):
        for ch in rows[r]:
            row_of[ord(ch) - ord("a")] = r
    out = []
    for word in words:
        first = -1
        one_row = True
        for ch in word.lower():
            r = row_of[ord(ch) - ord("a")]
            if first < 0:
                first = r
            elif r != first:
                one_row = False
                break
        if one_row:
            out.append(word)
    return out


seed = 500


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 20,000 lists of 20 words of 1 to 100 letters, each word from one
    # row (2 in 3) or the whole alphabet, a letter upper case with odds
    # 1 in 4, built once. Then each list is solved once.
    rows = ["qwertyuiop", "asdfghjkl", "zxcvbnm", "abcdefghijklmnopqrstuvwxyz"]
    pools = [list(r) for r in rows]
    lists = 20000
    all_lists = []
    for _ in range(lists):
        words = []
        for _ in range(20):
            pool = 3 if next_random() % 3 == 0 else next_random() % 3
            length = 1 + next_random() % 100
            letters = []
            for _ in range(length):
                ch = pools[pool][next_random() % len(pools[pool])]
                if next_random() % 4 == 0:
                    letters.append(ch.upper())
                else:
                    letters.append(ch)
            words.append("".join(letters))
        all_lists.append(words)
    kept = 0
    letters = 0
    checksum = 0
    for k in range(lists):
        for word in find_words(all_lists[k]):
            kept += 1
            letters += len(word)
            checksum = (checksum * 31 + len(word) + ord(word[0])) % 1000000007
    print(f"{lists} lists of 20 words: {kept} words kept, {letters} letters, checksum {checksum}")


main()
