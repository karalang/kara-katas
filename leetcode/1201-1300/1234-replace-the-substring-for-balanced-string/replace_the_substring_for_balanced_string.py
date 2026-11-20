# LeetCode #1234: Replace the Substring for Balanced String -- Python mirror
# of the ★ arm: a sliding window, shrunk while no letter outside it
# appears more than n / 4 times.


def balanced_string(s):
    n = len(s)
    k = n // 4
    index = {"Q": 0, "W": 1, "E": 2, "R": 3}
    outside = [0, 0, 0, 0]
    for c in s:
        outside[index[c]] += 1
    if all(c == k for c in outside):
        return 0
    best = n
    left = 0
    for right in range(n):
        outside[index[s[right]]] -= 1
        while left <= right and all(c <= k for c in outside):
            best = min(best, right - left + 1)
            outside[index[s[left]]] += 1
            left += 1
    return best


# ---- test harness ---------------------------------------------------------

def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def letters(n, lean, seed):
    out = []
    for _ in range(n):
        r = next_random(seed) % (4 + lean)
        out.append("Q" if r >= 4 or r == 0 else "W" if r == 1 else "E" if r == 2 else "R")
    return "".join(out)


def main():
    print(balanced_string("QWER"))
    print(balanced_string("QQWE"))
    print(balanced_string("QQQW"))
    print(balanced_string("QQQQ"))
    seed = [1234]
    check = 0
    for _ in range(1000):
        n = (next_random(seed) % 10 + 1) * 4
        s = letters(n, next_random(seed) % 5, seed)
        check = (check * 131 + balanced_string(s)) % 1000000007
    print(f"1000 random strings: checksum {check}")
    a = balanced_string(letters(100000, 0, seed))
    b = balanced_string(letters(100000, 2, seed))
    print(f"10^5 letters: {a}, {b}, {balanced_string('QWER' * 25000)}")


main()
