# LeetCode #418: Sentence Screen Fitting -- mirror of sentence_screen.kara
# (one pointer into the text).


def words_typing(sentence, rows, cols):
    text = " ".join(sentence) + " "
    length = len(text)
    at = 0
    for _ in range(rows):
        at += cols
        if text[at % length] == " ":
            at += 1
        else:
            while at > 0 and text[(at - 1) % length] != " ":
                at -= 1
    return at // length


seed = 418


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    calls = 10000
    pool = []
    for _ in range(200):
        length = 1 + step() % 10
        pool.append("".join(chr(97 + step() % 26) for _ in range(length)))
    total = 0
    checksum = 0
    for _ in range(calls):
        n = 1 + step() % 100
        sentence = [pool[step() % 200] for _ in range(n)]
        rows = 1 + step() % 20000
        cols = 10 + step() % 19991
        answer = words_typing(sentence, rows, cols)
        total += answer
        checksum = (checksum * 31 + answer) % 1000000007
    print(f"{calls} calls: total {total}, checksum {checksum}")


main()
