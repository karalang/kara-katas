# LeetCode #2472: Maximum Number of Non-overlapping Palindrome Substrings
# -- the Python mirror of palindromes.kara: the greedy over starts, a
# palindrome of `k` letters from here taken first, else one of `k + 1`.


def is_palindrome(c, lo, hi):
    while lo < hi:
        if c[lo] != c[hi]:
            return False
        lo += 1
        hi -= 1
    return True


def max_palindromes(s, k):
    c = list(s)
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


# ---- test harness ---------------------------------------------------------

seed = 2472


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_text(n, kinds):
    letters = "abcdefghijklmnopqrstuvwxyz"
    return "".join(letters[next_random() % kinds] for _ in range(n))


def main():
    cases = [
        ("abaccdbbd", 3),
        ("adbcda", 2),
        ("abc", 1),
        ("aaaaaa", 2),
        ("racecar", 7),
        ("xabbay", 4),
        ("aabaaba", 3),
    ]
    for s, k in cases:
        print(f'"{s}", k {k} -> {max_palindromes(s, k)}')
    same = random_text(2000, 1)
    print(f"2000 of one letter, k 1 -> {max_palindromes(same, 1)}")
    print(f"2000 of one letter, k 7 -> {max_palindromes(same, 7)}")
    print(f"2000 of two letters, k 3 -> {max_palindromes(random_text(2000, 2), 3)}")
    print(f"2000 of 26 letters, k 2 -> {max_palindromes(random_text(2000, 26), 2)}")
    check = 0
    for _ in range(3000):
        n = 1 + next_random() % 40
        kinds = 1 + next_random() % 3
        s = random_text(n, kinds)
        k = 1 + next_random() % n
        check = (check * 31 + max_palindromes(s, k)) % 1000000007
    print(f"3000 random: checksum {check}")


main()
