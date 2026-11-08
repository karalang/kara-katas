# LeetCode #2014: Longest Subsequence Repeated k Times -- a mirror of the ★
# arm, longest.kara.
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
        counts[ord(c) - ord("a")] += 1
    letters = [chr(ord("a") + i) for i in range(26) if counts[i] >= k]
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


def mix(check, answer):
    check = (check * 31 + len(answer)) % 1000000007
    for c in answer:
        check = (check * 31 + ord(c)) % 1000000007
    return check


def random_text(n, letters, width, keep, noise):
    pattern = []
    for _ in range(next_random() % width + 1):
        pattern.append(chr(ord("a") + next_random() % letters))
    text = []
    at = 0
    while len(text) < n:
        if next_random() % 10 < keep:
            text.append(pattern[at])
        if len(text) < n and next_random() % 10 < noise:
            text.append(chr(ord("a") + next_random() % letters))
        at = (at + 1) % len(pattern)
    return "".join(text)


def main():
    examples = [
        ("letsleetcode", 2),
        ("bb", 2),
        ("ab", 2),
        ("bbabbabbbbabaababab", 3),
        ("zzzzzzzzzzzzzzz", 2),
        ("abcabcabcabc", 4),
        ("cbacbacba", 3),
        ("aabbaabb", 3),
    ]
    for s, k in examples:
        print(f'"{s}", k = {k} -> "{longest_subsequence_repeated_k(s, k)}"')
    total = check = 0
    for _ in range(2000):
        k = next_random() % 5 + 2
        n = next_random() % min(8 * k - 2, 30) + 2
        letters = next_random() % 5 + 1
        width = next_random() % 4 + 1
        keep = next_random() % 5 + 6
        noise = next_random() % 5
        s = random_text(n, letters, width, keep, noise)
        answer = longest_subsequence_repeated_k(s, k)
        total += len(answer)
        check = mix(check, answer)
    print(f"2000 strings of 2 to 31 letters: total length {total}, checksum {check}")
    total = check = 0
    for a in range(6):
        k = [251, 260, 300, 400, 251, 285][a]
        letters = [3, 8, 26, 2, 5, 12][a]
        s = random_text(2000, letters, 7, 9, 2)
        answer = longest_subsequence_repeated_k(s, k)
        total += len(answer)
        check = mix(check, answer)
    print(f"6 strings of 2000 letters: total length {total}, checksum {check}")


main()
