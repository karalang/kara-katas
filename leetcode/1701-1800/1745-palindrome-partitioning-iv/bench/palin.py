# LeetCode #1745: Palindrome Partitioning IV -- the bench (palin.kara in
# Python): a table of palindromes, then every pair of cuts.


def check_partitioning(s):
    b = s.encode()
    n = len(b)
    is_ = [[False] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            is_[i][j] = b[i] == b[j] and (j - i < 2 or is_[i + 1][j - 1])
    for i in range(1, n - 1):
        if is_[0][i - 1]:
            for j in range(i, n - 1):
                if is_[i][j] and is_[j + 1][n - 1]:
                    return True
    return False


seed = 1745


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def letter():
    return "a" if next_random() % 2 == 0 else "b"


def palindrome(n):
    half = [letter() for _ in range((n + 1) // 2)]
    return "".join(half) + "".join(reversed(half[: n // 2]))


count, rounds, n = 20, 5, 2000
strings = []
for k in range(count):
    if k % 2 == 0:
        a = next_random() % (n - 2) + 1
        b = next_random() % (n - a - 1) + 1
        s = palindrome(a)
        s += palindrome(b)
        s += palindrome(n - a - b)
        strings.append(s)
    else:
        strings.append("".join(letter() for _ in range(n)))
yes = 0
check = 0
for r in range(rounds):
    for k, s in enumerate(strings):
        bit = 1 if check_partitioning(s) else 0
        yes += bit
        check = (check * 3 + bit + k + r) % 1000000007
print(f"{count} strings of {n} letters, {rounds} rounds: {yes} split, checksum {check}")
