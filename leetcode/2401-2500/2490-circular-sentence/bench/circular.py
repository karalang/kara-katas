# LeetCode #2490: Circular Sentence -- Python mirror of the ★ arm's
# benchmark (circular.kara): the same 200 sentences and 2300 passes, each
# letter changed and changed back, the sentence joined afresh for every
# answer.


def is_circular_sentence(sentence):
    n = len(sentence)
    if sentence[0] != sentence[n - 1]:
        return False
    for i in range(1, n - 1):
        if sentence[i] == " " and sentence[i - 1] != sentence[i + 1]:
            return False
    return True


seed = 2490


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def letter(k):
    return chr(ord("a") + k % 26)


def sentence():
    text = []
    first = letter(next_random())
    last = first
    while len(text) < 490:
        if text:
            text.append(" ")
        text.append(last)
        for _ in range(next_random() % 8):
            text.append(letter(next_random()))
        last = text[-1]
    text.append(" ")
    text.append(last)
    text.append(first)
    return text


def main():
    passes = 2300
    sentences = [sentence() for _ in range(200)]
    check = 0
    circular = 0
    for p in range(passes):
        for s in range(200):
            words = sentences[s]
            n = len(words)
            at = check % n
            was = words[at]
            if was != " ":
                words[at] = letter(check // n + p)
            answer = is_circular_sentence("".join(words))
            words[at] = was
            if answer:
                circular += 1
            check = (check * 31 + (1 if answer else 2) + p) % 1000000007
    print(f"{passes} passes over 200 sentences: {circular} circular, checksum {check}")


main()
