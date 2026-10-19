# LeetCode 796 -- Rotate String, in s written twice. Python mirror of
# the ★ arm and its harness.


def rotate_string(s, goal):
    return len(s) == len(goal) and goal in s + s


seed = 796


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(s, goal):
    answer = "true" if rotate_string(s, goal) else "false"
    print(f's = "{s}", goal = "{goal}" -> {answer}')


def main():
    show("abcde", "cdeab")
    show("abcde", "abced")
    show("a", "a")
    show("aa", "a")
    show("abab", "baba")
    show("abc", "abc")
    show("aab", "abb")
    rotations = 0
    check = 0
    for i in range(300):
        letters = 1 + next_random() % 4
        n = 1 + next_random() % 100
        s = "".join(chr(97 + next_random() % letters) for _ in range(n))
        kind = next_random() % 3
        if kind == 2:
            goal = "".join(chr(97 + next_random() % letters) for _ in range(n))
        else:
            k = next_random() % n
            change = next_random() % n if kind == 1 else -1
            goal = ""
            for j in range(n):
                c = s[(j + k) % n]
                goal += chr(97 + (ord(c) - 97 + 1) % letters) if j == change else c
        if rotate_string(s, goal):
            rotations += 1
            check = (check * 131 + i) % 1000000007
    print(f"300 random cases: {rotations} rotations, checksum {check}")


main()
