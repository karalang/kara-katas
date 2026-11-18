# LeetCode #1189 bench: the ★ arm in Python, over the same 200 texts of 10^4
# letters and 200 rounds as the Kāra bench.


def max_number_of_balloons(text):
    count = [0] * 26
    for b in text.encode():
        count[b - 97] += 1
    letter = lambda c: count[ord(c) - 97]
    return min(letter("b"), letter("a"), letter("l") // 2, letter("o") // 2, letter("n"))


seed = 1189


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_text(n, letters):
    return "".join(letters[next_random() % len(letters)] for _ in range(n))


alphabets = ["abcdefghijklmnopqrstuvwxyz", "balloon", "balonxy"]
texts = [random_text(10000, alphabets[i % 3]) for i in range(200)]
check = 0
for _ in range(200):
    for t in texts:
        check = (check * 131 + max_number_of_balloons(t) + 1) % 1000000007
print(f"200 rounds of 200 texts of 10000 letters: checksum {check}")
