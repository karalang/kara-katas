# LeetCode #1805: Number of Different Integers in a String -- the bench in
# Python: the ★ arm over 64 random words of 1000 characters built once,
# 20000 calls.


def num_different_integers(word):
    seen = set()
    run = []
    in_run = False
    for c in word:
        if c.isdigit():
            in_run = True
            if not (not run and c == "0"):
                run.append(c)
        elif in_run:
            seen.add("".join(run))
            run = []
            in_run = False
    if in_run:
        seen.add("".join(run))
    return len(seen)


seed = 1805


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    words = []
    for _ in range(64):
        word = []
        for _ in range(1000):
            if next_random() % 2 == 0:
                word.append(str(next_random() % 4))
            else:
                word.append(chr(97 + next_random() % 26))
        words.append("".join(word))
    check = 0
    for call in range(20000):
        word = words[(check + call) % 64]
        check = (check * 31 + num_different_integers(word)) % 1000000007
    print(f"20000 calls over 64 words of 1000 characters: checksum {check}")


main()
