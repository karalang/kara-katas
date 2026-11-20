# LeetCode #1255: Maximum Score Words Formed by Letters -- the Python
# mirror of max_score_words.kara: backtracking, every word left out or,
# when the letters on hand cover it, taken, and the better kept.


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


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(longest, alphabet):
    n = next_random() % longest + 1
    return ''.join(chr(ord('a') + next_random() % alphabet) for _ in range(n))


def random_case(count, longest, pool, alphabet):
    words = [random_word(longest, alphabet) for _ in range(count)]
    letters = sorted(chr(ord('a') + next_random() % alphabet) for _ in range(pool))
    score = [next_random() % 11 for _ in range(26)]
    return words, letters, score


def scores(text):
    return [int(s.strip()) for s in text.split(",")]


def main():
    global seed
    a = max_score_words(["dog", "cat", "dad", "good"], list("aacdddgoo"), scores("1,0,9,5,0,0,3,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0"))
    b = max_score_words(["xxxz", "ax", "bx", "cx"], list("zabcxxx"), scores("4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,10"))
    c = max_score_words(["leetcode"], list("letcod"), scores("0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0"))
    print(a, b, c)
    seed = 1255
    total = check = 0
    for _ in range(300):
        count = next_random() % 14 + 1
        longest = next_random() % 15 + 1
        pool = next_random() % 100 + 1
        alphabet = next_random() % 24 + 3
        words, letters, score = random_case(count, longest, pool, alphabet)
        best_score = max_score_words(words, letters, score)
        total += best_score
        check = (check * 131 + best_score) % 1000000007
    print(f"300 random cases: total {total}, checksum {check}")
    words = [''.join(chr(ord('a') + next_random() % 4) for _ in range(15)) for _ in range(14)]
    letters = [chr(ord('a') + next_random() % 4) for _ in range(100)]
    score = [i % 4 + 1 for i in range(26)]
    print(f"14 words of 15 letters: best {max_score_words(words, letters, score)}")


main()
