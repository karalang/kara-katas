# LeetCode #422: Valid Word Square -- mirror of valid_word_square.kara
# (every cell against its mirror).


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


def show(text):
    answer = "true" if valid_word_square(text.split()) else "false"
    print(f'"{text}": {answer}')


show("abcd bnrt crmy dtye")
show("abcd bnrt crm dt")
show("ball area read lady")
show("a")
show("ab")
show("ab b")
show("ab ba")
show("abc b")
show("aa a a")
show("abc bde ce")
valid = 0
checksum = 0
for case in range(2000):
    n = 1 + step() % 12
    grid = [0] * (n * n)
    for i in range(n):
        for j in range(i, n):
            c = step() % 2
            grid[i * n + j] = c
            grid[j * n + i] = c
    lengths = [n]
    for i in range(1, n):
        lengths.append(max(1, lengths[i - 1] - step() % 3))
    kept = []
    for i in range(n):
        height = 0
        while height < n and lengths[height] > i:
            height += 1
        kept.append(min(lengths[i], height))
    lengths = kept
    words = ["".join(chr(97 + grid[i * n + j]) for j in range(lengths[i])) for i in range(n)]
    spoil = step() % 6
    row = step() % n
    if spoil == 1:
        at = step() % lengths[row]
        w = words[row]
        words[row] = w[:at] + chr(195 - ord(w[at])) + w[at + 1:]
    elif spoil == 2 and lengths[row] > 1:
        words[row] = words[row][:-1]
    elif spoil == 3:
        words[row] = words[row] + "a"
    elif spoil == 4:
        words.append("a")
    answer = valid_word_square(words)
    if answer:
        valid += 1
    checksum = (checksum * 31 + (case + 1 if answer else 0)) % 1000000007
print(f"2000 random squares: {valid} valid, checksum {checksum}")
