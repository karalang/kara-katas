# LeetCode #358: Rearrange String k Distance Apart -- mirror of rearrange.kara.
import heapq
from collections import deque


def rearrange(s, k):
    counts = [0] * 26
    for ch in s:
        counts[ord(ch) - 97] += 1
    # heapq is smallest-first: (-copies left, letter) pops the most copies,
    # then the smallest letter.
    ready = [(-counts[c], c) for c in range(26) if counts[c] > 0]
    heapq.heapify(ready)
    cooling = deque()
    out = []
    for _ in range(len(s)):
        if not ready:
            return ""
        neg, c = heapq.heappop(ready)
        left = -neg
        out.append(chr(c + 97))
        cooling.append((left - 1, c))
        if len(cooling) >= k:
            left, c = cooling.popleft()
            if left > 0:
                heapq.heappush(ready, (-left, c))
    return "".join(out)


def show(label, s, k):
    print(f'{label}: "{rearrange(s, k)}"')


def main():
    show("example 1", "aabbcc", 3)
    show("example 2", "aaabc", 3)
    show("example 3", "aaadbbcc", 2)

    show("k = 0", "aabbbc", 0)
    show("k = 1", "aaabbc", 1)
    show("one letter", "z", 5)
    show("one letter repeated, k = 1", "aaaa", 1)
    show("one letter repeated, k = 2", "aaaa", 2)
    show("k equals the length", "abcd", 4)
    show("k beyond the length", "abc", 9)
    show("ties go to the smaller letter", "ddccbbaa", 2)
    show("tight: the most frequent letter just fits", "aaabbbccd", 3)
    show("every letter fills its slots", "aaabbbcccdd", 4)
    show("one copy too many", "aaab", 2)

    seed = 358
    possible = 0
    checksum = 0
    for _ in range(2000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        n = (seed // 65536) % 25
        seed = (seed * 1103515245 + 12345) % 2147483648
        width = (seed // 65536) % 5 + 2
        seed = (seed * 1103515245 + 12345) % 2147483648
        k = (seed // 65536) % 5
        chars = []
        for _ in range(n):
            seed = (seed * 1103515245 + 12345) % 2147483648
            chars.append(chr((seed // 65536) % width + 97))
        s = "".join(chars)
        r = rearrange(s, k)
        if len(r) == len(s):
            possible += 1
        for ch in r:
            checksum = (checksum * 31 + ord(ch)) % 1000000007
        checksum = (checksum * 31 + 7) % 1000000007
    print(f"2000 random strings: {possible} can be arranged, checksum {checksum}")


main()
