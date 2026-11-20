# LeetCode #1668: Maximum Repeating Substring -- the bench's Python mirror:
# the ★ arm on 400000 problems, words of 1 to 6 letters and sequences of
# about 100 built of whole copies of the word and single letters, all
# drawn first.


def max_repeating(sequence, word):
    k = 0
    repeated = word
    while repeated in sequence:
        k += 1
        repeated += word
    return k


# ---- the harness --------------------------------------------------------

seed = 1668


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_text(n, kinds):
    return "".join(chr(ord("a") + next_random() % kinds) for _ in range(n))


def random_sequence(word, n, kinds):
    text = ""
    while len(text) < n:
        if next_random() % 2 == 0:
            text += word
        else:
            text += random_text(1, kinds)
    return text


problems = 400000
cases = []
for _ in range(problems):
    kinds = next_random() % 3 + 1
    word = random_text(next_random() % 6 + 1, kinds)
    sequence = random_sequence(word, 100, kinds)
    cases.append((sequence, word))
total = 0
check = 0
for sequence, word in cases:
    k = max_repeating(sequence, word)
    total += k
    check = (check * 31 + k) % 1000000007
print(f"{problems} problems of about 100 letters: answers sum to {total}, checksum {check}")
