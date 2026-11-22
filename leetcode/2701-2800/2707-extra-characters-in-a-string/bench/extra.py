# LeetCode #2707: Extra Characters in a String -- the bench (extra.kara in
# Python): the fewest extra characters of each suffix, from the end back,
# with the dictionary a set asked about every slice.


def min_extra_char(s, dictionary):
    words = set(dictionary)
    n = len(s)
    best = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        best[i] = best[i + 1] + 1
        for j in range(i + 1, n + 1):
            if s[i:j] in words and best[j] < best[i]:
                best[i] = best[j]
    return best[0]


seed = 2707


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(n):
    return "".join(chr(97 + next_random() % 3) for _ in range(n))


cases, rounds = 10000, 5
problems = []
for _ in range(cases):
    s = random_word(50)
    dictionary = []
    for _ in range(50):
        n = next_random() % 5 + 1
        word = random_word(n)
        if word not in dictionary:
            dictionary.append(word)
    problems.append((s, dictionary))
total = 0
check = 0
for r in range(rounds):
    for s, dictionary in problems:
        extra = min_extra_char(s, dictionary)
        total += extra
        check = (check * 31 + extra + r) % 1000000007
print(f"{cases} strings of 50 letters against up to 50 words, {rounds} rounds: extra characters sum to {total}, checksum {check}")
