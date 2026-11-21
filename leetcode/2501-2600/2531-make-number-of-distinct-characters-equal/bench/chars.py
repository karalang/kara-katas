# LeetCode #2531: Make Number of Distinct Characters Equal -- benchmark
# mirror of the ★ arm (chars.kara): 1000 pairs of words built once, then
# the passes, each asking every pair from an offset the checksum picks.


def distinct(counts):
    return sum(1 for c in counts if c > 0)


def is_it_possible(word1, word2):
    one = [0] * 26
    two = [0] * 26
    for b in word1.encode():
        one[b - 97] += 1
    for b in word2.encode():
        two[b - 97] += 1
    for a in range(26):
        for b in range(26):
            if one[a] > 0 and two[b] > 0:
                one[a] -= 1
                one[b] += 1
                two[b] -= 1
                two[a] += 1
                equal = distinct(one) == distinct(two)
                one[a] += 1
                one[b] -= 1
                two[b] += 1
                two[a] -= 1
                if equal:
                    return True
    return False


seed = 2531


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(length, letters):
    return "".join(chr(97 + next_random() % letters) for _ in range(length))


def main():
    pairs = []
    for _ in range(1000):
        word1 = random_word(next_random() % 1000 + 1, next_random() % 26 + 1)
        word2 = random_word(next_random() % 1000 + 1, next_random() % 26 + 1)
        pairs.append((word1, word2))
    passes = 24
    check = 0
    for p in range(passes):
        start = check % 1000
        for i in range(1000):
            word1, word2 = pairs[(start + i) % 1000]
            answer = is_it_possible(word1, word2)
            check = (check * 31 + (2 if answer else 1) + p) % 1000000007
    print(f"{passes} passes over 1000 pairs of words: checksum {check}")


main()
