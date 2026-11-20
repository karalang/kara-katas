# LeetCode #1234 bench: the ★ arm in Python, over the same 40 strings of
# 10^5 letters and 20 passes as the Kāra bench.

INDEX = {"Q": 0, "W": 1, "E": 2, "R": 3}


def balanced_string(s):
    n = len(s)
    k = n // 4
    outside = [0, 0, 0, 0]
    for c in s:
        outside[INDEX[c]] += 1
    if all(c == k for c in outside):
        return 0
    best = n
    left = 0
    for right in range(n):
        outside[INDEX[s[right]]] -= 1
        while left <= right and all(c <= k for c in outside):
            best = min(best, right - left + 1)
            outside[INDEX[s[left]]] += 1
            left += 1
    return best


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    seed = [1234]
    strings = []
    for t in range(40):
        lean = t % 4
        out = []
        for _ in range(100000):
            r = next_random(seed) % (4 + lean)
            out.append("Q" if r >= 4 or r == 0 else "W" if r == 1 else "E" if r == 2 else "R")
        strings.append("".join(out))
    check = 0
    for _ in range(20):
        for s in strings:
            check = (check * 131 + balanced_string(s)) % 1000000007
    print(f"40 strings of 10^5 letters, 20 passes: checksum {check}")


main()
