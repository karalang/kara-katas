# LeetCode #1668: Maximum Repeating Substring -- the Python mirror of the
# ★ arm: the repeated word grown while the sequence holds it.


def max_repeating(sequence, word):
    k = 0
    repeated = word
    while repeated in sequence:
        k += 1
        repeated += word
    return k


# ---- the harness: the same as the Kāra arms -------------------------------

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


def batch(count, longest, widest):
    total = 0
    check = 0
    for _ in range(count):
        kinds = next_random() % 3 + 1
        word = random_text(next_random() % widest + 1, kinds)
        sequence = random_sequence(word, next_random() % longest + 1, kinds)
        k = max_repeating(sequence, word)
        total += k
        check = (check * 31 + k + len(sequence)) % 1000000007
    print(f"{count} problems of up to {longest} letters: answers sum to {total}, checksum {check}")


print(max_repeating("ababc", "ab"))
print(max_repeating("ababc", "ba"))
print(max_repeating("ababc", "ac"))
print(max_repeating("aaabaaaabaaabaaaabaaaabaaaabaaaaba", "aaaba"))
print(max_repeating("ab", "abc"))
print(max_repeating("kara", "kara"))
batch(3000, 12, 3)
batch(3000, 100, 6)
batch(300, 100, 100)
