# LeetCode #937: Reorder Data in Log Files -- two lists and a sort
# (Python mirror).


def reorder_log_files(logs):
    letters = []
    digits = []
    for log in logs:
        cut = log.index(" ")
        contents = log[cut + 1:]
        if "0" <= contents[0] <= "9":
            digits.append(log)
        else:
            letters.append((contents, log[:cut], log))
    letters.sort(key=lambda e: (e[0], e[1]))
    return [e[2] for e in letters] + digits


# ---- test harness ---------------------------------------------------------

seed = 937


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(logs):
    return "[" + ",".join('"' + log + '"' for log in logs) + "]"


def fold(check, logs):
    h = check
    for log in logs:
        for b in log.encode():
            h = (h * 131 + b) % 1000000007
        h = (h * 131 + 10) % 1000000007
    return h


def random_word(length, letters):
    w = ""
    for _ in range(length):
        if letters == 0:
            w += chr(48 + next_random() % 10)
        else:
            w += chr(97 + next_random() % letters)
    return w


def random_id():
    length = 1 + next_random() % 4
    w = ""
    for _ in range(length):
        c = next_random() % 6
        w += chr(97 + c if c < 3 else 45 + c)
    return w


def long_log(letters):
    log = random_word(3, 3)
    left = 96
    while left > 0:
        w = 1 + next_random() % 9
        if w > left or left - w < 2:
            w = left
        log = log + " " + random_word(w, letters)
        left -= w + 1
    assert len(log) == 100
    return log


def main():
    cases = [
        ["dig1 8 1 5 1", "let1 art can", "dig2 3 6", "let2 own kit dig", "let3 art zero"],
        ["a1 9 2 3 1", "g1 act car", "zo4 4 7", "ab1 off key dog", "a8 act zoo"],
        ["d3 7", "d1 0 0", "d2 12 3"],
        ["b2 same words", "a10 same words", "a9 same words"],
        ["x1 art can", "x2 art", "x3 art c", "x4 arta"],
        ["z 1", "y a", "x 2", "w b"],
        ["only one"],
    ]
    for c in cases:
        print(f"{show(c)} -> {show(reorder_log_files(c))}")
    total = 0
    check = 0
    for _ in range(300):
        n = 1 + next_random() % 100
        logs = []
        for _ in range(n):
            log = random_id()
            letters = 3 if next_random() % 2 == 0 else 0
            words = 1 + next_random() % 4
            for _ in range(words):
                length = 1 + next_random() % 3
                log = log + " " + random_word(length, letters)
            logs.append(log)
        total += n
        check = fold(check, reorder_log_files(logs))
    print(f"300 random lists: {total} logs, checksum {check}")
    big = [long_log(5 if i % 2 == 0 else 0) for i in range(100)]
    out = reorder_log_files(big)
    print(f"100 logs of 100 characters: first {out[0][:3]}, last {out[99][:3]}, checksum {fold(0, out)}")
    words = long_log(5)[3:]
    same = [random_word(3, 3) + words for _ in range(100)]
    out = reorder_log_files(same)
    print(f"100 logs with the same contents: first {out[0][:3]}, last {out[99][:3]}, checksum {fold(0, out)}")


main()
