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


def show(text, rows, cols):
    sentence = text.split()
    print(f'"{text}" on {rows}x{cols}: {words_typing(sentence, rows, cols)}')


show("hello world", 2, 8)
show("a bcd e", 3, 6)
show("i had apple pie", 4, 5)
show("abc", 5, 3)
show("abcd", 5, 3)
show("a", 1, 1)
show("a b", 1, 2)
show("a b", 1, 3)
show("try to be better", 10000, 9001)
show("f p a", 8, 7)
total = 0
checksum = 0
for _ in range(1000):
    n = 1 + step() % 8
    sentence = []
    for _ in range(n):
        length = 1 + step() % 6
        sentence.append("".join(chr(97 + step() % 26) for _ in range(length)))
    rows = 1 + step() % 40
    cols = 1 + step() % 20
    answer = words_typing(sentence, rows, cols)
    total += answer
    checksum = (checksum * 31 + answer) % 1000000007
print(f"1000 random sentences: total {total}, checksum {checksum}")
