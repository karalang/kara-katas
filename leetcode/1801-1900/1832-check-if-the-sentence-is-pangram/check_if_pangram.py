# LeetCode #1832: Check if the Sentence Is Pangram -- the ★ arm in Python


def check_if_pangram(sentence):
    seen = 0
    for b in sentence.encode():
        seen |= 1 << (b - 97)
    return seen == (1 << 26) - 1


seed = 1832


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def sentence(n, span):
    return "".join(chr(97 + next_random() % span) for _ in range(n))


def show(b):
    return "true" if b else "false"


print(show(check_if_pangram("thequickbrownfoxjumpsoverthelazydog")), show(check_if_pangram("leetcode")))
late = "abcdefghijklmnopqrstuvwxy" * 39 + "z"
print(show(check_if_pangram("abcdefghijklmnopqrstuvwxyz")), show(check_if_pangram("abcdefghijklmnopqrstuvwxy")), show(check_if_pangram("q")), show(check_if_pangram(late)))
whole = sentence(1000, 26)
short = sentence(1000, 25)
print(f"the most: {show(check_if_pangram(whole))} {show(check_if_pangram(short))} {show(check_if_pangram('e' * 1000))}")
pangrams = 0
check = 0
for _ in range(3000):
    n = 20 + next_random() % 81
    span = 24 + next_random() % 3
    yes = check_if_pangram(sentence(n, span))
    if yes:
        pangrams += 1
    check = (check * 31 + (2 if yes else 1)) % 1000000007
print(f"3000 random sentences: {pangrams} pangrams, checksum {check}")
