# LeetCode #2452: Words Within Two Edits of Dictionary -- Python mirror of
# the ★ arm (edits.kara): each query against each word, the differing
# places counted until a third rules the word out.


def within_two(query, word):
    differ = 0
    for j in range(len(query)):
        if query[j] != word[j]:
            differ += 1
            if differ > 2:
                return False
    return True


def two_edit_words(queries, dictionary):
    answers = []
    for q in queries:
        for w in dictionary:
            if within_two(q, w):
                answers.append(q)
                break
    return answers


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(length, letters):
    return "".join(chr(97 + next_random() % letters) for _ in range(length))


def changed(word, changes, letters):
    b = list(word)
    for _ in range(changes):
        place = next_random() % len(b)
        b[place] = chr(97 + next_random() % letters)
    return "".join(b)


def show(words):
    return "[" + ", ".join(words) + "]"


def fold(check, answers):
    for w in answers:
        for b in w.encode():
            check = (check * 31 + b) % 1000000007
        check = (check * 31 + 1) % 1000000007
    return check


def main():
    global seed
    print(f"example 1: {show(two_edit_words(['word', 'note', 'ants', 'wood'], ['wood', 'joke', 'moat']))}")
    print(f"example 2: {show(two_edit_words(['yes'], ['not']))}")
    print(f"one letter: {show(two_edit_words(['a', 'z'], ['q']))}")
    print(f"two letters: {show(two_edit_words(['ab', 'zz'], ['yx']))}")
    print(f"three letters: {show(two_edit_words(['abc', 'xyc', 'xyz'], ['abd', 'abc']))}")
    seed = 2452
    for letters in [26, 2]:
        dictionary = [random_word(100, letters) for _ in range(100)]
        queries = []
        for _ in range(100):
            base = dictionary[next_random() % 100]
            changes = next_random() % 5
            queries.append(changed(base, changes, letters))
        answers = two_edit_words(queries, dictionary)
        print(f"100 of 100 letters from {letters}: {len(answers)} words, checksum {fold(0, answers)}")
    check = 0
    total = 0
    for _ in range(3000):
        length = 1 + next_random() % 6
        q = 1 + next_random() % 5
        d = 1 + next_random() % 5
        queries = [random_word(length, 3) for _ in range(q)]
        dictionary = [random_word(length, 3) for _ in range(d)]
        answers = two_edit_words(queries, dictionary)
        total += len(answers)
        check = fold(check, answers)
        check = (check * 31 + 2) % 1000000007
    print(f"3000 random: {total} words, checksum {check}")


main()
