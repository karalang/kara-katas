# LeetCode #1209 bench, in Python: the ★ arm (a stack of runs, each a
# letter and how many times it has come in a row, a run popped when it
# reaches k) on 12 strings of 100000 letters drawn once, then 10 rounds
# over the strings with k = 2, 3 and 4, each answer's length and last
# letter folded into a checksum.

seed = 1209


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_text(n, letters):
    return "".join(chr(97 + next_random() % letters) for _ in range(n))


def remove_duplicates(s, k):
    runs = []
    for c in s:
        if runs and runs[-1][0] == c:
            runs[-1][1] += 1
            if runs[-1][1] == k:
                runs.pop()
        else:
            runs.append([c, 1])
    return "".join(c * n for c, n in runs)


def main():
    texts = []
    for i in range(12):
        if i < 4:
            texts.append(random_text(100000, 2))
        elif i < 8:
            texts.append(random_text(100000, 3))
        else:
            half = random_text(50000, 26)
            texts.append(half + half[::-1])
    check = 0
    for rnd in range(10):
        for s in texts:
            for k in range(2, 5):
                answer = remove_duplicates(s, k)
                last = ord(answer[-1]) if answer else 0
                check = (check * 131 + len(answer) + last + rnd) % 1000000007
    print(f"10 rounds over 12 strings of 100000 letters: checksum {check}")


main()
