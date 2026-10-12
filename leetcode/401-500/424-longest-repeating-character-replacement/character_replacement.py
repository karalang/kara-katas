# LeetCode #424: Longest Repeating Character Replacement -- mirror of
# character_replacement.kara (a window that never shrinks).


def character_replacement(s, k):
    count = [0] * 26
    best = 0
    left = 0
    for right in range(len(s)):
        c = ord(s[right]) - 65
        count[c] += 1
        best = max(best, count[c])
        if right - left + 1 - best > k:
            count[ord(s[left]) - 65] -= 1
            left += 1
    return len(s) - left


seed = 424


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(s, k):
    print(f'"{s}", k = {k}: {character_replacement(s, k)}')


show("ABAB", 2)
show("AABABBA", 1)
show("A", 0)
show("A", 1)
show("ABCDE", 0)
show("ABCDE", 2)
show("AAAA", 0)
show("AAAB", 0)
show("ABBBA", 1)
show("BAAAB", 2)
total = 0
checksum = 0
for _ in range(2000):
    n = 1 + step() % 60
    alphabet = 1 + step() % 5
    s = ""
    while len(s) < n:
        letter = chr(65 + step() % alphabet)
        run = 1 + step() % 5
        for _ in range(run):
            if len(s) < n:
                s += letter
    k = step() % 7
    answer = character_replacement(s, k)
    total += answer
    checksum = (checksum * 31 + answer) % 1000000007
print(f"2000 random strings: total {total}, checksum {checksum}")
