# Benchmark for #422: mirror of valid_word_square.kara (every cell
# against its mirror). A flip rebuilds the row, as the Kāra program does.
import sys


def valid_word_square(words):
    n = len(words)
    for i in range(n):
        row = words[i]
        for j in range(len(row)):
            if j >= n:
                return False
            mirror = words[j]
            if i >= len(mirror) or mirror[i] != row[j]:
                return False
    return True


seed = 422


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def flip(words, i, j):
    w = words[i]
    words[i] = w[:j] + chr(195 - ord(w[j])) + w[j + 1:]


rounds = int(sys.argv[1]) if len(sys.argv) > 1 else 6000
n = 500
grid = [0] * (n * n)
for i in range(n):
    for j in range(i, n):
        c = step() % 2
        grid[i * n + j] = c
        grid[j * n + i] = c
lengths = [n]
for i in range(1, n):
    drop = 1 if step() % 4 == 0 else 0
    lengths.append(max(1, lengths[i - 1] - drop))
words = []
for i in range(n):
    height = 0
    while height < n and lengths[height] > i:
        height += 1
    words.append("".join(chr(97 + grid[i * n + j]) for j in range(min(lengths[i], height))))
cells = sum(len(w) for w in words)
valid = 0
checksum = 0
for r in range(rounds):
    i = step() % n
    j = step() % len(words[i])
    flip(words, i, j)
    if r % 3 != 0:
        flip(words, j, i)
    answer = valid_word_square(words)
    if answer:
        valid += 1
    checksum = (checksum * 31 + (r + 1 if answer else 0)) % 1000000007
    if r % 3 == 0:
        flip(words, i, j)
print(f"{rounds} rounds on {n} words, {cells} letters: {valid} valid, checksum {checksum}")
