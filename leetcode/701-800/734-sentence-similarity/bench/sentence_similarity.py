# LeetCode #734: Sentence Similarity -- a set of pairs.
# Benchmark mirror of the Kara star arm: put every pair in a set both
# ways round, then check the words place by place.


def are_sentences_similar(sentence1, sentence2, pairs):
    if len(sentence1) != len(sentence2):
        return False
    similar = set()
    for a, b in pairs:
        similar.add((a, b))
        similar.add((b, a))
    for a, b in zip(sentence1, sentence2):
        if a != b and (a, b) not in similar:
            return False
    return True


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    seed = [734]
    pairs = []
    for _ in range(1000):
        a = next_random(seed) % 5000
        b = next_random(seed) % 5000
        pairs.append((f"w{a}", f"w{b}"))
    s1, s2 = [], []
    for _ in range(1000):
        p = next_random(seed) % 1000
        if next_random(seed) % 2 == 0:
            s1.append(pairs[p][0])
            s2.append(pairs[p][1])
        else:
            s1.append(pairs[p][1])
            s2.append(pairs[p][0])
    similar = 0
    for _ in range(1000):
        j = next_random(seed) % 1000
        x = next_random(seed) % 5000
        saved = s2[j]
        s2[j] = f"w{x}"
        if are_sentences_similar(s1, s2, pairs):
            similar += 1
        s2[j] = saved
        if are_sentences_similar(s1, s2, pairs):
            similar += 1
    print(f"1000 rounds of 2 checks of 1000 words with 1000 pairs: {similar} similar")


main()
