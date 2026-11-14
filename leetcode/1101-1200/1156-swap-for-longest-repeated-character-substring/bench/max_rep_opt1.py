"""LeetCode #1156 bench -- mirrors max_rep_opt1.kara: the same 64 texts,
the same passes, the ★ arm's runs."""


def max_rep_opt1(text):
    b = text.encode()
    count = [0] * 26
    for c in b:
        count[c - 97] += 1
    runs = []
    i = 0
    n = len(b)
    while i < n:
        j = i
        while j < n and b[j] == b[i]:
            j += 1
        runs.append((b[i], j - i))
        i = j
    best = 0
    for r in range(len(runs)):
        c, length = runs[r]
        have = count[c - 97]
        best = max(best, min(length + 1, have))
        if r + 2 < len(runs) and runs[r + 1][1] == 1 and runs[r + 2][0] == c:
            best = max(best, min(length + runs[r + 2][1] + 1, have))
    return best


seed = 1156


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    passes = 100
    texts = []
    for t in range(64):
        b = []
        while len(b) < 20000:
            if t % 4 == 3:
                b.extend([97] * (1 + next_random() % 40))
                b.append(98 + next_random() % 25)
            else:
                b.append(97 + next_random() % [2, 3, 26][t % 4])
        texts.append(bytes(b[:20000]).decode())
    check = 0
    for p in range(passes):
        for text in texts:
            check = (check * 31 + max_rep_opt1(text) + p) % 1000000007
    print(f"{passes} passes over 64 texts of 20000 letters: checksum {check}")


if __name__ == "__main__":
    main()
