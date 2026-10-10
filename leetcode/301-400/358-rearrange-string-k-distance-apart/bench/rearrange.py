# Benchmark for #358 -- mirror of rearrange.kara.
import heapq
from collections import deque


def rearrange(s, k):
    counts = [0] * 26
    for ch in s:
        counts[ord(ch) - 97] += 1
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


def main():
    seed = 358
    possible = 0
    checksum = 0
    for _ in range(200):
        seed = (seed * 1103515245 + 12345) % 2147483648
        width = (seed // 65536) % 23 + 4
        seed = (seed * 1103515245 + 12345) % 2147483648
        k = (seed // 65536) % 8 + 1
        chars = []
        for _ in range(50000):
            seed = (seed * 1103515245 + 12345) % 2147483648
            draw = seed // 65536
            c = 0 if draw % 8 == 0 else (draw // 8) % width
            chars.append(chr(c + 97))
        s = "".join(chars)
        r = rearrange(s, k)
        if len(r) == len(s):
            possible += 1
        for ch in r:
            checksum = (checksum * 31 + ord(ch)) % 1000000007
        checksum = (checksum * 31 + 7) % 1000000007
    print(f"{possible} of 200 strings can be arranged, checksum {checksum}")


main()
