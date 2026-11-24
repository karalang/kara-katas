# LeetCode #1332: Remove Palindromic Subsequences -- Python mirror of the
# ★ arm: one step when the string reads the same from both ends, else two.


def remove_palindrome_sub(s):
    n = len(s)
    for i in range(n // 2):
        if s[i] != s[n - 1 - i]:
            return 2
    return 1


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def letter(r):
    return 'a' if r % 2 == 0 else 'b'


def draw(n, kind):
    letters = []
    for i in range(n):
        if kind == 0 or i < (n + 1) // 2:
            letters.append(letter(next_random()))
        else:
            letters.append(letters[n - 1 - i])
    if kind == 2:
        at = next_random() % n
        letters[at] = 'b' if letters[at] == 'a' else 'a'
    return ''.join(letters)


def main():
    global seed
    ex = [remove_palindrome_sub(x) for x in ("ababa", "abb", "baabb")]
    print(f"{ex[0]} {ex[1]} {ex[2]}")
    short = [remove_palindrome_sub(x) for x in ("a", "b", "ab", "bb")]
    print(" ".join(str(x) for x in short))
    all_a = "a" * 1000
    pal = ''.join('b' if min(i, 999 - i) % 7 == 3 else 'a' for i in range(1000))
    broken = 'b' + pal[1:]
    print(f"1000 letters: {remove_palindrome_sub(all_a)} {remove_palindrome_sub(pal)} {remove_palindrome_sub(broken)}")
    seed = 1332
    check = 0
    ones = 0
    for t in range(600):
        n = 1 + next_random() % 1000 if t % 20 == 0 else 1 + next_random() % 12
        s = draw(n, t % 3)
        steps = remove_palindrome_sub(s)
        if steps == 1:
            ones += 1
        check = (check * 131 + steps + n) % 1000000007
    print(f"600 random strings: {ones} palindromes, checksum {check}")


main()
