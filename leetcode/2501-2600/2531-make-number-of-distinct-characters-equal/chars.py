# LeetCode #2531: Make Number of Distinct Characters Equal -- Python mirror
# of the ★ arm (chars.kara): the counts of each letter, and each pair of a
# letter from word1 and one from word2 swapped on the counts, compared,
# and put back.


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


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def random_word(seed, length, letters):
    return "".join(chr(97 + next_random(seed) % letters) for _ in range(length))


def main():
    fixed = [
        ("ac", "b"),
        ("abcc", "aab"),
        ("abcde", "fghij"),
        ("a", "a"),
        ("a", "bb"),
        ("aa", "bcd"),
        ("abcdefghijklmnopqrstuvwxyz", "a"),
        ("ab", "abcd"),
    ]
    for word1, word2 in fixed:
        print(f"{word1} {word2} -> {'true' if is_it_possible(word1, word2) else 'false'}")
    seed = [2531]
    for count, most, letters in [(3000, 8, 6), (300, 2000, 26)]:
        yes = 0
        check = 0
        for _ in range(count):
            pick = next_random(seed) % letters + 1
            word1 = random_word(seed, next_random(seed) % most + 1, pick)
            word2 = random_word(seed, next_random(seed) % most + 1, next_random(seed) % letters + 1)
            answer = is_it_possible(word1, word2)
            if answer:
                yes += 1
            check = (check * 31 + (2 if answer else 1)) % 1000000007
        print(f"{count} random pairs of up to {most} letters: {yes} possible, checksum {check}")


main()
