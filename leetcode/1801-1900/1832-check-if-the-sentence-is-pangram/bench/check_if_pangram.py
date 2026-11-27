# LeetCode #1832: Check if the Sentence Is Pangram -- the bench in Python: the
# ★ arm over 100000 calls on runs of 500 to 999 letters cut from one string of
# 2000 letters, built once, each letter a z one time in 600 and otherwise one
# of a to y; each run's start and length are drawn from the checksum so far.
# Each call makes its run a string of its own.


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


letters = bytearray()
for _ in range(2000):
    if next_random() % 600 == 0:
        letters.append(122)
    else:
        letters.append(97 + next_random() % 25)
check = 0
pangrams = 0
for call in range(100000):
    start = (check + call) % 1000
    length = 500 + (check * 7 + call) % 500
    yes = check_if_pangram(letters[start:start + length].decode())
    if yes:
        pangrams += 1
    check = (check * 31 + (2 if yes else 1)) % 1000000007
print(f"100000 calls: {pangrams} pangrams, checksum {check}")
