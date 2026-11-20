# LeetCode #1255 bench, in Python: the ★ arm (backtracking, every word in
# turn left out or, when the letters on hand cover it, taken) on 100
# random cases built once, each 14 words of 1 to 15 letters and 100
# letters to spend from the first 6 letters of the alphabet; each asked
# 3 times, every best score folded into a checksum.


def best(i, words, left, score):
    if i == len(words):
        return 0
    top = best(i + 1, words, left, score)
    need = words[i]
    if all(need[c] <= left[c] for c in range(26)):
        for c in range(26):
            left[c] -= need[c]
        gain = sum(need[c] * score[c] for c in range(26))
        top = max(top, gain + best(i + 1, words, left, score))
        for c in range(26):
            left[c] += need[c]
    return top


def max_score_words(words, letters, score):
    counts = []
    for w in words:
        n = [0] * 26
        for ch in w:
            n[ord(ch) - ord('a')] += 1
        counts.append(n)
    left = [0] * 26
    for ch in letters:
        left[ord(ch) - ord('a')] += 1
    return best(0, counts, left, score)


seed = 1255


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    cases = []
    for _ in range(100):
        words = []
        for _ in range(14):
            n = next_random() % 15 + 1
            words.append(''.join(chr(ord('a') + next_random() % 6) for _ in range(n)))
        letters = [chr(ord('a') + next_random() % 6) for _ in range(100)]
        score = [next_random() % 11 for _ in range(26)]
        cases.append((words, letters, score))
    check = 0
    for _ in range(3):
        for words, letters, score in cases:
            check = (check * 131 + max_score_words(words, letters, score)) % 1000000007
    print(f"3 rounds of 100 cases of 14 words: checksum {check}")


main()
