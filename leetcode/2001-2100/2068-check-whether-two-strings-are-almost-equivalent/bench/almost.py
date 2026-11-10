# LeetCode #2068: Check Whether Two Strings are Almost Equivalent -- Python
# mirror of the ★ arm's benchmark (almost.kara): every pair of 1500 words
# of 100 letters, each a common word of `a`, `b` and `c` with up to 30
# letters changed.


def check_almost_equivalent(word1, word2):
    diff = [0] * 26
    for b in word1.encode():
        diff[b - 97] += 1
    for b in word2.encode():
        diff[b - 97] -= 1
    return all(abs(d) <= 3 for d in diff)


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    letters = "abc"
    seed = [2068]
    base = [letters[next_random(seed) % 3] for _ in range(100)]
    words = []
    for _ in range(1500):
        word = base[:]
        for _ in range(next_random(seed) % 31):
            i = next_random(seed) % 100
            word[i] = letters[next_random(seed) % 3]
        words.append("".join(word))
    yes = 0
    check = 0
    for i in range(1500):
        for j in range(i + 1, 1500):
            if check_almost_equivalent(words[i], words[j]):
                yes += 1
                check = (check * 31 + i * 1500 + j) % 1000000007
    print(f"1124250 pairs: {yes} almost equivalent, checksum {check}")


main()
