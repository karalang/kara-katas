# LeetCode 792 -- Number of Matching Subsequences, every word at once.
# Python mirror of the ★ arm and its harness.


def num_matching_subseq(s, words):
    waiting = [[] for _ in range(26)]
    for i, word in enumerate(words):
        waiting[ord(word[0]) - 97].append((i, 0))
    count = 0
    for ch in s:
        c = ord(ch) - 97
        moving = waiting[c]
        waiting[c] = []
        for w, matched in moving:
            word = words[w]
            if matched + 1 == len(word):
                count += 1
            else:
                waiting[ord(word[matched + 1]) - 97].append((w, matched + 1))
    return count


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(length, letters):
    return "".join(chr(97 + next_random() % letters) for _ in range(length))


def show(s, words):
    answer = num_matching_subseq(s, words)
    print(f's = "{s}", words = [{", ".join(words)}] -> {answer}')


def main():
    global seed
    show("abcde", ["a", "bb", "acd", "ace"])
    show("dsahjpjauf", ["ahjpjau", "ja", "ahbwzgqnuk", "tnmlanowax"])
    show("a", ["a", "a", "b", "aa"])
    show("aaaaa", ["a", "aa", "aaa", "aaaaa", "aaaaaa"])
    show("abc", ["abc", "cba", "ac", "ca", "c"])
    seed = 792
    total = 0
    check = 0
    for _ in range(300):
        letters = 1 + next_random() % 26
        s = random_word(1 + next_random() % 300, letters)
        words = []
        for _ in range(1 + next_random() % 50):
            kind = next_random() % 4
            if kind == 0 and len(words) > 0:
                words.append(words[next_random() % len(words)])
            elif kind == 1:
                word = []
                for ch in s:
                    if len(word) == 50:
                        break
                    if next_random() % 3 == 0:
                        word.append(ch)
                if not word:
                    word.append(s[0])
                words.append("".join(word))
            else:
                words.append(random_word(1 + next_random() % 8, letters))
        answer = num_matching_subseq(s, words)
        total += answer
        check = (check * 131 + answer + 1) % 1000000007
    print(f"300 random cases: {total} matching words, checksum {check}")


main()
