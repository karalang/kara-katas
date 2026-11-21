# LeetCode #2472: Maximum Number of Non-overlapping Palindrome Substrings
# -- the bench, the ★ arm in Python: the greedy over starts, a palindrome
# of `k` letters from here taken first, else one of `k + 1`, each checked
# by two indices walked inward. The string is a list of letters.


def is_palindrome(c, lo, hi):
    while lo < hi:
        if c[lo] != c[hi]:
            return False
        lo += 1
        hi -= 1
    return True


def max_palindromes(c, k):
    n = len(c)
    count = 0
    i = 0
    while i + k <= n:
        if is_palindrome(c, i, i + k - 1):
            count += 1
            i += k
        elif i + k < n and is_palindrome(c, i, i + k):
            count += 1
            i += k + 1
        else:
            i += 1
    return count


seed = 2472


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 20 strings of 2000 letters from "ab" built once; then 2400 passes,
    # each setting one letter of every string from the checksum so far,
    # then answering it with `k` from 2 to 6 by the pass, folding the
    # count plus the pass into the checksum
    n = 2000
    texts = [["ab"[next_random() % 2] for _ in range(n)] for _ in range(20)]
    check = 0
    for p in range(2400):
        k = 2 + p % 5
        for a, c in enumerate(texts):
            c[(check + a) % n] = "ab"[check % 2]
            check = (check * 31 + max_palindromes(c, k) + p) % 1000000007
    print(f"2400 passes over 20 strings of 2000: checksum {check}")


main()
