# LeetCode #1309: Decrypt String from Alphabet to Integer Mapping -- the
# Python mirror of the ★ arm (the code read from the right, a `#` taking the
# two digits before it), with the same harness.


def freq_alphabets(s):
    b = s.encode()
    letters = []
    i = len(b) - 1
    while i >= 0:
        if b[i] == ord("#"):
            i -= 3
            number = (b[i + 1] - 48) * 10 + (b[i + 2] - 48)
        else:
            i -= 1
            number = b[i + 1] - 48
        letters.append(chr(ord("a") + number - 1))
    letters.reverse()
    return "".join(letters)


seed = 1309


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    every = "12345678910#11#12#13#14#15#16#17#18#19#20#21#22#23#24#25#26#"
    print(" ".join(freq_alphabets(c) for c in ["10#11#12", "1326#", every, "1", "26#", "11110#"]))
    same = 0
    check = 0
    for i in range(3000):
        span = 2 if i % 3 == 0 else 10 if i % 3 == 1 else 26
        length = 1 + next_random() % 300
        text = []
        code = []
        for _ in range(length):
            k = next_random() % span
            text.append(chr(ord("a") + k))
            code.append(f"{k + 1}" if k < 9 else f"{k + 1}#")
        got = freq_alphabets("".join(code))
        if got == "".join(text):
            same += 1
        for c in got:
            check = (check * 31 + ord(c)) % 1000000007
    print(f"3000 random texts: {same} read back, checksum {check}")


main()
