"""LeetCode #1156: Swap For Longest Repeated Character Substring -- the
Python mirror of max_rep_opt1.kara.

The text as runs of one letter: a run can grow by one, with a letter
swapped in from elsewhere, and two runs of one letter split by a single
other letter can join through it. Neither can use more of the letter than
the text holds, which is what the swap draws on."""


def max_rep_opt1(text):
    b = text.encode()
    count = [0] * 26
    for c in b:
        count[c - 97] += 1
    runs = []
    i = 0
    while i < len(b):
        j = i
        while j < len(b) and b[j] == b[i]:
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


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(text):
    print(f"{text}  ->  {max_rep_opt1(text)}")


def random_text(n, letters):
    return "".join(chr(97 + next_random() % letters) for _ in range(n))


def main():
    global seed
    for t in ["ababa", "aaabaaa", "aaabbaaa", "aaaaa", "abcdef", "a", "ab", "aba", "aab",
              "baaab", "aaabaaab", "abaaac", "bbababaaaa"]:
        show(t)
    seed = 1156
    total = 0
    check = 0
    for _ in range(2000):
        n = 1 + next_random() % 40
        letters = 1 + next_random() % 4
        answer = max_rep_opt1(random_text(n, letters))
        total += answer
        check = (check * 31 + answer) % 1000000007
    print(f"2000 random texts: total {total}, checksum {check}")
    print(f"20000 random over 2: {max_rep_opt1(random_text(20000, 2))}")
    print(f"20000 random over 26: {max_rep_opt1(random_text(20000, 26))}")
    same = ["a"] * 20000
    print(f"20000 of one letter: {max_rep_opt1(''.join(same))}")
    split = list(same)
    split[10000] = "b"
    split[19999] = "c"
    print(f"one letter split once, another at the end: {max_rep_opt1(''.join(split))}")


if __name__ == "__main__":
    main()
