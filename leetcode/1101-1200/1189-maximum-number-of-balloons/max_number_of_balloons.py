# LeetCode #1189: Maximum Number of Balloons -- the ★ arm in Python: a count
# of each letter, then the least of what each letter of "balloon" makes.
# It also checks every answer of the 2000 random texts against the statement
# read literally: take the word's letters out of the text while they are
# all there.


def max_number_of_balloons(text):
    count = [0] * 26
    for b in text.encode():
        count[b - 97] += 1
    letter = lambda c: count[ord(c) - 97]
    return min(letter("b"), letter("a"), letter("l") // 2, letter("o") // 2, letter("n"))


def literal(text):
    left = list(text)
    words = 0
    while True:
        for c in "balloon":
            if c not in left:
                return words
            left.remove(c)
        words += 1


seed = 1189


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_text(n, letters):
    return "".join(letters[next_random() % len(letters)] for _ in range(n))


cases = ["nlaebolko", "loonbalxballpoon", "leetcode", "balloon", "baloon", "lnolaoblnoobllaobaonlbllno", "ballooballoo", "b", "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"]
for c in cases:
    assert literal(c) == max_number_of_balloons(c)
    print(f"{c}: {max_number_of_balloons(c)}")
check = total = 0
for _ in range(2000):
    n = next_random() % 60 + 1
    text = random_text(n, "balonxy")
    words = max_number_of_balloons(text)
    assert literal(text) == words, text
    total += words
    check = (check * 131 + words + 1) % 1000000007
print(f"2000 random texts: {total} words, checksum {check}")
print(f"10000 letters of 26: {max_number_of_balloons(random_text(10000, 'abcdefghijklmnopqrstuvwxyz'))}")
print(f"10000 letters of balloon: {max_number_of_balloons(random_text(10000, 'balloon'))}")
