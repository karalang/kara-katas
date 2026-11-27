# LeetCode #1816: Truncate Sentence -- the bench in Python: the ★ arm over
# 2 * 10^6 calls on 1000 sentences of 20 to 100 words, built once, each
# sentence and its k drawn from the checksum so far.


def truncate_sentence(s, k):
    return " ".join(s.split(" ")[:k])


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    seed = [1816]
    sentences = []
    for _ in range(1000):
        n = 20 + next_random(seed) % 81
        words = []
        for _ in range(n):
            m = 1 + next_random(seed) % 5
            words.append("".join(chr(97 + next_random(seed) % 26) for _ in range(m)))
        sentences.append((" ".join(words), n))
    check = 0
    for call in range(2000000):
        s, n = sentences[(check + call) % 1000]
        cut = truncate_sentence(s, 1 + (check + call) % n)
        check = (check * 31 + len(cut)) % 1000000007
    print(f"2000000 calls: checksum {check}")


main()
