# LeetCode #1216 bench, in Python: the ★ arm (the longest palindromic
# subsequence, one row at a time) on 48 strings of 1000 letters drawn once
# from 2, 4, 8 or 26 letters, each asked with k = 200, 400, 600 and 800;
# every answer folded into a checksum.

seed = 1216


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def is_valid_palindrome(s, k):
    b = s.encode()
    n = len(b)
    row = [0] * n
    for i in range(n - 1, -1, -1):
        row[i] = 1
        diagonal = 0
        for j in range(i + 1, n):
            below = row[j]
            row[j] = diagonal + 2 if b[i] == b[j] else max(row[j], row[j - 1])
            diagonal = below
    return n - row[n - 1] <= k


def main():
    alphabets = [2, 4, 8, 26]
    texts = []
    for t in range(48):
        letters = alphabets[t % 4]
        texts.append("".join(chr(97 + next_random() % letters) for _ in range(1000)))
    check = 0
    yes = 0
    for s in texts:
        for k in (200, 400, 600, 800):
            answer = is_valid_palindrome(s, k)
            yes += answer
            check = (check * 131 + (2 if answer else 1) + k) % 1000000007
    print(f"48 strings of 1000 letters, 4 budgets each: {yes} true, checksum {check}")


main()
