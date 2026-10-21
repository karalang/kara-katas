# LeetCode 830 — Positions of Large Groups, by two pointers.
#
# Mirrors large_group_positions.kara: from the start i of each group, j
# runs on while the letter stays the same, and the group is kept when it
# holds 3 or more.

def large_group_positions(s):
    n = len(s)
    groups = []
    i = 0
    while i < n:
        j = i
        while j < n and s[j] == s[i]:
            j += 1
        if j - i >= 3:
            groups.append([i, j - 1])
        i = j
    return groups

seed = 0

def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536

def random_string(n, letters):
    return ''.join(chr(ord('a') + next_random() % letters) for _ in range(n))

def show(s):
    print(f'"{s}" -> {large_group_positions(s)}')

def summary(label, s):
    groups = large_group_positions(s)
    check = 0
    for g in groups:
        check = (check * 131 + g[0] * 1009 + g[1]) % 1000000007
    print(f"{label}: {len(groups)} groups, checksum {check}")

for s in ["abbxxxxzzy", "abc", "abcdddeeeeaabbbcd", "aba", "a", "aa", "aaa", "aaab", "baaa", "aaabbb", "aabbbaaaa"]:
    show(s)
seed = 830
summary("1000 letters of 2", random_string(1000, 2))
summary("1000 letters of 3", random_string(1000, 3))
summary("1000 letters of 1", random_string(1000, 1))
total = 0
check = 0
for _ in range(300):
    n = 1 + next_random() % 30
    letters = 1 + next_random() % 3
    for g in large_group_positions(random_string(n, letters)):
        total += 1
        check = (check * 131 + g[0] * 1009 + g[1]) % 1000000007
print(f"300 random strings: {total} groups, checksum {check}")
