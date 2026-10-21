# LeetCode 828 — Count Unique Characters of All Substrings of a Given
# String, by each character's contribution.
#
# Mirrors unique_letter_string.kara: a character at i is unique in
# (i - prev) * (next - i) substrings, prev and next the copies of its
# letter beside it, and one pass keeps the last two positions of each letter.

def unique_letter_string(s):
    n = len(s)
    last = [-1] * 26
    before = [-1] * 26
    total = 0
    for i in range(n):
        c = ord(s[i]) - ord('A')
        if last[c] >= 0:
            total += (last[c] - before[c]) * (i - last[c])
        before[c] = last[c]
        last[c] = i
    for c in range(26):
        if last[c] >= 0:
            total += (last[c] - before[c]) * (n - last[c])
    return total

seed = 0

def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536

def random_string(n, letters):
    return ''.join(chr(ord('A') + next_random() % letters) for _ in range(n))

def show(s):
    print(f'"{s}" -> {unique_letter_string(s)}')

show("ABC")
show("ABA")
show("LEETCODE")
show("A")
show("AA")
show("AAAA")
show("ABAB")
show("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
show("ZYXWVUTSRQPONMLKJIHGFEDCBAZ")
seed = 828
print(f"100000 letters of 26 -> {unique_letter_string(random_string(100000, 26))}")
print(f"100000 letters of 2 -> {unique_letter_string(random_string(100000, 2))}")
print(f"100000 letters of 1 -> {unique_letter_string(random_string(100000, 1))}")
total = 0
check = 0
for _ in range(300):
    n = 1 + next_random() % 30
    letters = 1 + next_random() % 6
    r = unique_letter_string(random_string(n, letters))
    total += r
    check = (check * 131 + r) % 1000000007
print(f"300 random strings: total {total}, checksum {check}")
