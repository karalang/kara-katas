# LeetCode #2810: Faulty Keyboard -- the bench in Python: the ★ arm over
# 20000 strings of 100 letters, about a fifth of them i, all drawn first,
# then each typed 10 times.


def final_string(s):
    screen = ""
    for c in s:
        if c == "i":
            screen = screen[::-1]
        else:
            screen += c
    return screen


seed = 2810


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def digest(s):
    h = 0
    for b in s.encode():
        h = (h * 131 + b) % 1000000007
    return h


def main():
    count = 20000
    rounds = 10
    letters = "abcdefghijklmnopqrstuvwxyz"
    cases = []
    for _ in range(count):
        s = []
        for _ in range(100):
            r = next_random() % 125
            s.append("i" if r < 25 else letters[r % 26])
        cases.append("".join(s))
    total = 0
    check = 0
    for r in range(rounds):
        for s in cases:
            out = final_string(s)
            total += len(out)
            check = (check * 31 + digest(out) + r) % 1000000007
    print(f"{count} strings of 100, {rounds} rounds: lengths sum to {total}, checksum {check}")


main()
