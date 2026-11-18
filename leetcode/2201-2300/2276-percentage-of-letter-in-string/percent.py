# LeetCode #2276: Percentage of Letter in String -- the Python mirror of
# the ★ arm, `percent.kara`, line for line. Its output is byte-identical.


def percentage_letter(s, letter):
    count = 0
    for c in s:
        if c == letter:
            count += 1
    return count * 100 // len(s)


seed = 2276


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def letters(n, k):
    return "".join(chr(97 + next_random() % k) for _ in range(n))


def show(v):
    return "[" + ", ".join(map(str, v)) + "]"


def main():
    examples = [
        ("foobar", "o"),
        ("jjjj", "k"),
        ("a", "a"),
        ("ab", "a"),
        ("abc", "a"),
        ("aab", "a"),
        ("zzzzzzzzzy", "y"),
    ]
    for s, letter in examples:
        print(f"{s} {letter} -> {percentage_letter(s, letter)}")
    check = 0
    for t in range(3000):
        n = next_random() % 100 + 1
        s = letters(n, [2, 3, 26][t % 3])
        letter = chr(97 + next_random() % 3)
        check = (check * 31 + percentage_letter(s, letter)) % 1000000007
    print(f"3000 strings: checksum {check}")
    rand = letters(100, 4)
    allq = "q" * 100
    once = "x" * 99 + "q"
    answers = [percentage_letter(rand, "a"), percentage_letter(allq, "q"), percentage_letter(once, "q")]
    print(f"100 letters: {show(answers)}")


main()
