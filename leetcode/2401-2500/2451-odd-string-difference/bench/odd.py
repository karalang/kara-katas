# LeetCode #2451: Odd String Difference -- the bench, the ★ arm: the
# common difference array read off the first three words, and the word
# whose array is not it.


def differences(word):
    b = word.encode()
    steps = []
    for j in range(1, len(b)):
        steps.append(b[j] - b[j - 1])
    return steps


def odd_string(words):
    a = differences(words[0])
    b = differences(words[1])
    c = differences(words[2])
    common = a if a == b or a == c else b
    for w in words:
        if differences(w) != common:
            return w
    return words[0]


seed = 2451


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def word_of(steps):
    at = low = high = 0
    for s in steps:
        at += s
        low = min(low, at)
        high = max(high, at)
    code = -low + next_random() % (26 - (high - low))
    letters = [97 + code]
    for s in steps:
        code += s
        letters.append(97 + code)
    return bytes(letters).decode()


def main():
    lists = []
    for _ in range(2000):
        common = [next_random() % 3 - 1 for _ in range(19)]
        other = list(common)
        other[18] += 1
        odd = next_random() % 100
        lists.append([word_of(other if i == odd else common) for i in range(100)])
    check = 0
    for p in range(110):
        for c in range(len(lists)):
            words = lists[c]
            j = (p + c) % 100
            words[0], words[j] = words[j], words[0]
            answer = odd_string(words)
            for x in answer.encode():
                check = (check * 31 + x + p) % 1000000007
    print(f"110 passes over 2000 lists of 100 words: checksum {check}")


main()
