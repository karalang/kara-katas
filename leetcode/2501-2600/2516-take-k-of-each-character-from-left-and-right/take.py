# LeetCode #2516: Take K of Each Character From Left and Right -- Python
# mirror of the ★ arm (take.kara): the longest middle window that leaves
# k of each letter outside it, found by sliding; and its harness, line
# for line.


def take_characters(s, k):
    n = len(s)
    total = [0, 0, 0]
    for ch in s:
        total[ord(ch) - 97] += 1
    if total[0] < k or total[1] < k or total[2] < k:
        return -1
    inside = [0, 0, 0]
    left = 0
    longest = 0
    for right in range(n):
        c = ord(s[right]) - 97
        inside[c] += 1
        while total[c] - inside[c] < k:
            inside[ord(s[left]) - 97] -= 1
            left += 1
        longest = max(longest, right - left + 1)
    return n - longest


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def letters(n):
    return "".join(chr(97 + next_random() % 3) for _ in range(n))


def main():
    global seed
    cases = [("aabaaaacaabc", 2), ("a", 1), ("a", 0), ("abc", 1), ("aabbcc", 2), ("ccbbaa", 1), ("abacabac", 2), ("bcbbbbca", 1)]
    for s, k in cases:
        print(f"\"{s}\" k {k} -> {take_characters(s, k)}")
    seed = 2516
    for most in [20, 2000]:
        misses = 0
        total = 0
        check = 0
        for _ in range(2000):
            n = next_random() % most + 1
            s = letters(n)
            k = next_random() % 5 if most == 20 else next_random() % (n // 3 + 1)
            a = take_characters(s, k)
            if a == -1:
                misses += 1
            else:
                total += a
            check = (check * 31 + a + 1) % 1000000007
        print(f"2000 random of up to {most} letters: {misses} misses, total {total}, checksum {check}")
    s = letters(100000)
    print(f"10^5 random, k 33000: {take_characters(s, 33000)}")
    print(f"10^5 random, k 0: {take_characters(s, 0)}")
    print(f"10^5 a's, k 1: {take_characters('a' * 100000, 1)}")
    abc = "abc" * 33333
    print(f"abc 33333 times, k 33333: {take_characters(abc, 33333)}")
    print(f"abc 33333 times, k 33332: {take_characters(abc, 33332)}")


main()
