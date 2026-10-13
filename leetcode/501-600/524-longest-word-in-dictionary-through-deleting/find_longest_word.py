# LeetCode #524: Longest Word in Dictionary through Deleting -- Python
# mirror of the ★ arm (check every word); see
# find_longest_word.kara. Same algorithm, same harness, same output.


def is_subsequence(word, s):
    i = 0
    for c in s:
        if i < len(word) and word[i] == c:
            i += 1
    return i == len(word)


def find_longest_word(s, dictionary):
    best = ""
    for word in dictionary:
        if len(word) > len(best) or (len(word) == len(best) and word < best):
            if is_subsequence(word, s):
                best = word
    return best


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(length, letters):
    return "".join(chr(97 + next_random() % letters) for _ in range(length))


def random_subsequence(s, keep):
    word = "".join(c for c in s if next_random() % keep == 0)
    return word if word else s[0]


def show(s, dictionary):
    print(f'{s}, [{", ".join(dictionary)}]: "{find_longest_word(s, dictionary)}"')


def main():
    global seed
    show("abpcplea", ["ale", "apple", "monkey", "plea"])
    show("abpcplea", ["a", "b", "c"])
    show("abc", ["d", "abcd", "ca"])
    show("bab", ["ba", "ab"])
    show("abc", ["abc", "ab", "abc"])
    show("aaa", ["aaaa", "aa"])
    show("z", ["z"])
    show("xyzxyz", ["zz", "yy", "xx", "zyx"])
    seed = 524
    empty = 0
    checksum = 0
    for _ in range(1000):
        letters = 1 + next_random() % 4
        s = random_word(1 + next_random() % 60, letters)
        dictionary = []
        count = 1 + next_random() % 30
        for _ in range(count):
            if next_random() % 3 == 0:
                dictionary.append(random_subsequence(s, 1 + next_random() % 8))
            else:
                dictionary.append(random_word(1 + next_random() % 8, letters))
        answer = find_longest_word(s, dictionary)
        if len(answer) == 0:
            empty += 1
        for c in answer:
            checksum = (checksum * 31 + ord(c)) % 1000000007
        checksum = (checksum * 31 + len(answer)) % 1000000007
    print(f"1000 random cases: {empty} with none, checksum {checksum}")
    s = random_word(1000, 26)
    dictionary = []
    for i in range(1000):
        if i % 2 == 0:
            dictionary.append(random_subsequence(s, 2 + next_random() % 3))
        else:
            dictionary.append(random_word(1 + next_random() % 1000, 26))
    answer = find_longest_word(s, dictionary)
    print(f"1000 words against 1000 letters: {len(answer)} letters, starting {answer[0:10]}")


main()
