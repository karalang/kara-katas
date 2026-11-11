# LeetCode #2114: Maximum Number of Words Found in Sentences -- the Python
# mirror of words.kara (the ★ arm): each sentence's spaces counted, plus
# one, and the largest taken. O(total length).


def most_words_found(sentences):
    most = 0
    for s in sentences:
        most = max(most, s.count(" ") + 1)
    return most


# ---- test harness ----------------------------------------------------------

def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def show(v):
    return "[" + ", ".join(v) + "]"


def main():
    examples = [
        ["alice and bob love leetcode", "i think so too", "this is great thanks very much"],
        ["please wait", "continue to fight", "continue to win"],
        ["hello"],
        ["a b c", "d e f g h"],
        ["one two", "one", "one two three four"],
    ]
    for sentences in examples:
        print(f"{show(sentences)} -> {most_words_found(sentences)}")
    seed = [2114]
    total = 0
    check = 0
    for _ in range(3000):
        count = next_random(seed) % 10 + 1
        sentences = []
        for _ in range(count):
            words = next_random(seed) % 12 + 1
            s = ""
            for w in range(words):
                if w > 0:
                    s += " "
                length = next_random(seed) % 6 + 1
                for _ in range(length):
                    s += chr(ord("a") + next_random(seed) % 26)
            sentences.append(s)
        got = most_words_found(sentences)
        total += got
        check = (check * 31 + got) % 1000000007
    print(f"3000 lists: {total} words, checksum {check}")
    short = ["a " * 49 + "a" for _ in range(100)]
    long = ["z" * 100 for _ in range(100)]
    print(f"one-letter words -> {most_words_found(short)}")
    print(f"one long word -> {most_words_found(long)}")


main()
