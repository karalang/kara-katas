# LeetCode #2014: Longest Subsequence Repeated k Times -- the ★ arm's
# benchmark, a mirror of longest.kara.
from collections import deque


def repeats(s, t, k):
    i = 0
    found = 0
    for c in s:
        if c == t[i]:
            i += 1
            if i == len(t):
                found += 1
                if found == k:
                    return True
                i = 0
    return False


def longest_subsequence_repeated_k(s, k):
    counts = [0] * 26
    for c in s:
        counts[ord(c) - 97] += 1
    letters = [chr(97 + i) for i in range(26) if counts[i] >= k]
    queue = deque([""])
    best = ""
    while queue:
        t = queue.popleft()
        for c in letters:
            nxt = t + c
            if repeats(s, nxt, k):
                best = nxt
                queue.append(nxt)
    return best


seed = 2014


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_text(n, letters):
    pattern = [chr(97 + next_random() % letters) for _ in range(next_random() % 7 + 1)]
    text = []
    at = 0
    while len(text) < n:
        if next_random() % 10 < 9:
            text.append(pattern[at])
        if len(text) < n and next_random() % 10 < 1:
            text.append(chr(97 + next_random() % letters))
        at = (at + 1) % len(pattern)
    return "".join(text)


def main():
    cases = []
    for c in range(200):
        k = 251 + next_random() % 50
        cases.append((random_text(2000, c % 8 + 2), k))
    calls = total = check = 0
    for _ in range(5):
        for s, k in cases:
            answer = longest_subsequence_repeated_k(s, k)
            calls += 1
            total += len(answer)
            for c in answer:
                check = (check * 31 + ord(c)) % 1000000007
            check = (check * 31 + len(answer)) % 1000000007
    print(f"{calls} calls: total length {total}, checksum {check}")


main()
