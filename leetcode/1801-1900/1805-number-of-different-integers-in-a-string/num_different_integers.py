# LeetCode #1805: Number of Different Integers in a String -- the ★ arm in
# Python: one walk of the word, a run of digits gathered until a letter
# ends it, its leading zeros left out as they come, and the runs counted
# once each in a set.


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


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    # LeetCode's three examples
    print(
        num_different_integers("a123bc34d8ef34"),
        num_different_integers("leet1234code234"),
        num_different_integers("a1b01c001"),
    )
    # the edges
    long = "9" * 400 + "x" + "0" * 5 + "9" * 400
    print(*[num_different_integers(w) for w in ["abc", "0", "0a00b000", long, "x10y010z100"]])
    # the constraints' most
    print(
        "the most:",
        num_different_integers("1" * 1000),
        num_different_integers("q" * 1000),
        num_different_integers("7z" * 500),
    )
    # 3000 random words
    seed = [1805]
    check = 0
    for _ in range(3000):
        n = 1 + next_random(seed) % 30
        chance = next_random(seed) % 4
        word = []
        for _ in range(n):
            if next_random(seed) % 4 < chance:
                word.append(str(next_random(seed) % 3))
            else:
                word.append(chr(97 + next_random(seed) % 3))
        check = (check * 31 + num_different_integers("".join(word))) % 1000000007
    print(f"3000 random words: checksum {check}")


main()
