# LeetCode #1745: Palindrome Partitioning IV -- mirrors palin.kara (the ★
# arm).


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


def letter(letters):
    return chr(ord("a") + next_random() % letters)


def palindrome(n, letters):
    half = [letter(letters) for _ in range((n + 1) // 2)]
    return "".join(half) + "".join(reversed(half[: n // 2]))


def batch(count, most, letters):
    yes = 0
    check = 0
    for k in range(count):
        n = next_random() % (most - 2) + 3
        if k % 2 == 0:
            a = next_random() % (n - 2) + 1
            b = next_random() % (n - a - 1) + 1
            s = palindrome(a, letters)
            s += palindrome(b, letters)
            s += palindrome(n - a - b, letters)
        else:
            s = "".join(letter(letters) for _ in range(n))
        bit = 1 if check_partitioning(s) else 0
        yes += bit
        check = (check * 2 + bit + n) % 1000000007
    print(f"{count} strings of up to {most} letters from {letters}: {yes} split, checksum {check}")


for s in ["abcbdd", "bcbddxy", "abc", "aaaa", "abcbaz", "juchzcedhfesefhdecz"]:
    print("true" if check_partitioning(s) else "false")
batch(3000, 10, 2)
batch(1000, 40, 3)
batch(20, 2000, 26)
