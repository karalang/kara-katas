# LeetCode #1309 bench in Python: the ★ arm (the code read from the right, a
# `#` taking the two digits before it) on the same 200 codes and 500 passes.


def freq_alphabets(s):
    b = s.encode()
    letters = []
    i = len(b) - 1
    while i >= 0:
        if b[i] == 35:
            i -= 3
            number = (b[i + 1] - 48) * 10 + (b[i + 2] - 48)
        else:
            i -= 1
            number = b[i + 1] - 48
        letters.append(chr(97 + number - 1))
    letters.reverse()
    return "".join(letters)


seed = 1309


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def encode(letters):
    return "".join(f"{k + 1}" if k < 9 else f"{k + 1}#" for k in letters)


def main():
    texts = []
    codes = []
    for _ in range(200):
        letters = [next_random() % 26 for _ in range(300)]
        codes.append(encode(letters))
        texts.append(letters)
    check = 0
    for pass_no in range(500):
        t = check % 200
        texts[t][(check // 200) % 300] = (check // 7) % 26
        codes[t] = encode(texts[t])
        for c in range(200):
            got = freq_alphabets(codes[c]).encode()
            check = (check * 31 + got[check % len(got)] + len(got) + pass_no) % 1000000007
    print(f"500 passes over 200 codes: checksum {check}")


main()
