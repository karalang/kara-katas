# LeetCode #727: Minimum Window Subsequence -- forward, then back.
# Benchmark mirror of the Kara star arm: walk s1 forward matching s2 in
# order, walk back from where the last letter matched to find the
# latest start, keep the window if shorter, and begin again one place
# after its start.


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def random_word(n, kinds, seed):
    return "".join(chr(ord("a") + next_random(seed) % kinds) for _ in range(n))


def min_window(s1, s2):
    n, m = len(s1), len(s2)
    best_start, best_len = -1, n + 1
    i = 0
    while i < n:
        j = 0
        while i < n:
            if s1[i] == s2[j]:
                j += 1
                if j == m:
                    break
            i += 1
        if j < m:
            break
        end = i
        k = m - 1
        p = end
        while k >= 0:
            if s1[p] == s2[k]:
                k -= 1
            p -= 1
        start = p + 1
        if end - start + 1 < best_len:
            best_len = end - start + 1
            best_start = start
        i = start + 1
    if best_start < 0:
        return ""
    return s1[best_start:best_start + best_len]


def main():
    seed = [727]
    texts = [random_word(20000, 8, seed) for _ in range(10)]
    total = 0
    for _ in range(300):
        for d in range(10):
            word = random_word(20, 8, seed)
            total += len(min_window(texts[d], word))
    print(f"300 rounds of 10 texts of 20000 letters: sum {total}")


main()
