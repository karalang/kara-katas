# LeetCode #1221 bench, Python mirror of the Kāra ★ arm: walk the string
# keeping L's count less R's and count the returns to zero, over 2000
# random balanced strings of 1000 letters drawn once, 20 passes; checksum
# of the answers.

seed = 1221


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def balanced_string_split(s):
    balance = 0
    pieces = 0
    for c in s:
        if c == 'L':
            balance += 1
        else:
            balance -= 1
        if balance == 0:
            pieces += 1
    return pieces


strings = []
for _ in range(2000):
    letters = ['L', 'R'] * 500
    k = len(letters) - 1
    while k > 0:
        j = next_random() % (k + 1)
        letters[k], letters[j] = letters[j], letters[k]
        k -= 1
    strings.append(''.join(letters))
total = 0
check = 0
for _ in range(20):
    for s in strings:
        answer = balanced_string_split(s)
        total += answer
        check = (check * 131 + answer) % 1000000007
print(f"2000 strings of 1000 letters, 20 passes: pieces total {total}, checksum {check}")
