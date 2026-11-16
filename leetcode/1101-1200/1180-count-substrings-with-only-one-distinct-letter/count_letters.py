# LeetCode #1180: Count Substrings with Only One Distinct Letter -- a Python
# mirror of the ★ arm (count_letters.kara): one pass, the length of the run
# of equal letters ending at each position added at every step. With `lit`
# it instead counts every substring whose letters form a set of one, as the
# statement reads, and prints the same.
import sys

LIT = len(sys.argv) > 1 and sys.argv[1] == "lit"


def count_letters(s):
    total = 0
    run = 0
    last = ""
    for c in s:
        if c == last:
            run += 1
        else:
            run = 1
            last = c
        total += run
    return total


def literal(s):
    n = len(s)
    return sum(1 for i in range(n) for j in range(i + 1, n + 1) if len(set(s[i:j])) == 1)


solve = literal if LIT else count_letters
seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_string(n, m):
    return "".join(chr(97 + next_random() % m) for _ in range(n))


def main():
    global seed
    print(f"example 1: {solve('aaaba')}")
    print(f"example 2: {solve('aaaaaaaaaa')}")
    small = ["a", "ab", "abcdefghijklmnopqrstuvwxyz", "zzzzabczzzz", "aabaabaa"]
    print("small: [" + ", ".join(str(solve(s)) for s in small) + "]")
    seed = 1180
    total = 0
    check = 0
    for _ in range(300):
        n = 1 + next_random() % 40
        m = 1 + next_random() % 3
        a = solve(random_string(n, m))
        total += a
        check = (check * 131 + a) % 1000000007
    print(f"300 random strings: {total} in all, checksum {check}")
    print(f"1000 of one letter: {count_letters('q' * 1000)}")
    total = 0
    check = 0
    for _ in range(2000):
        m = 2 + next_random() % 3
        a = count_letters(random_string(1000, m))
        total += a
        check = (check * 131 + a) % 1000000007
    print(f"2000 strings of 1000 letters: {total} in all, checksum {check}")


main()
