# LeetCode #2452: Words Within Two Edits of Dictionary -- the bench, the
# ★ arm: each query against each word, the differing places counted
# until a third rules the word out.


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


seed = 2452


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word():
    return [97 + next_random() % 4 for _ in range(100)]


def main():
    dictionaries = []
    queries = []
    for _ in range(100):
        words = [random_word() for _ in range(100)]
        asks = []
        for _ in range(100):
            b = list(words[next_random() % 100])
            for _ in range(next_random() % 5):
                place = next_random() % 100
                b[place] = 97 + next_random() % 4
            asks.append(b)
        dictionaries.append([bytes(w).decode() for w in words])
        queries.append(asks)
    check = 0
    for p in range(45):
        for c in range(100):
            place = next_random() % 100
            queries[c][p % 100][place] = 97 + next_random() % 4
            asks = [bytes(q).decode() for q in queries[c]]
            kept = two_edit_words(asks, dictionaries[c])
            check = (check * 31 + len(kept) + p) % 1000000007
    print(f"45 passes over 100 cases of 100 queries: checksum {check}")


main()
