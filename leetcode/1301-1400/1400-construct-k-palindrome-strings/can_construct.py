# LeetCode #1400: Construct K Palindrome Strings -- Python mirror of the ★
# arm: k palindromes can be made exactly when there are at least k
# letters and at most k letters that appear an odd number of times.


def can_construct(s, k):
    if len(s) < k:
        return False
    count = [0] * 26
    for b in s.encode():
        count[b - 97] += 1
    odd = sum(1 for c in count if c % 2 == 1)
    return odd <= k


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def drawn(n, letters):
    return "".join(chr(97 + next_random() % letters) for _ in range(n))


def show(b):
    return "true" if b else "false"


def main():
    global seed
    shown = [
        can_construct("annabelle", 2),
        can_construct("leetcode", 3),
        can_construct("true", 4),
        can_construct("ab", 3),
        can_construct("a", 1),
        can_construct("abcdefghijklmnopqrstuvwxyz", 26),
    ]
    print(" ".join(show(b) for b in shown))
    seed = 1400
    wide = drawn(100000, 26)
    narrow = drawn(100000, 3)
    yes = 0
    for k in range(1, 31):
        if can_construct(wide, k):
            yes += 1
        if can_construct(narrow, k):
            yes += 1
    print(f"10^5 letters: {yes} of 60 true, {show(can_construct(wide, 100000))} {show(can_construct(narrow, 100001))}")
    check = 0
    count = 0
    for _ in range(2000):
        n = 1 + next_random() % 20
        letters = 1 + next_random() % 26
        s = drawn(n, letters)
        k = 1 + next_random() % 25
        got = can_construct(s, k)
        if got:
            count += 1
        check = (check * 131 + (k if got else 0)) % 1000000007
    print(f"2000 random cases: {count} true, checksum {check}")


main()
