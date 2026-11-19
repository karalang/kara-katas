# LeetCode #1654: Minimum Jumps to Reach Home -- the bench's Python mirror:
# the ★ arm on 5000 random problems with a, b and x up to 2000 and up to
# 1000 forbidden positions, all drawn first.

from collections import deque


def minimum_jumps(forbidden, a, b, x):
    limit = max(x, max(forbidden, default=0)) + a + b
    blocked = [False] * (limit + 1)
    for f in forbidden:
        blocked[f] = True
    seen = [[False, False] for _ in range(limit + 1)]
    queue = deque([(0, False, 0)])
    seen[0][0] = True
    while queue:
        p, back, jumps = queue.popleft()
        if p == x:
            return jumps
        forward = p + a
        if forward <= limit and not blocked[forward] and not seen[forward][0]:
            seen[forward][0] = True
            queue.append((forward, False, jumps + 1))
        backward = p - b
        if not back and backward >= 0 and not blocked[backward] and not seen[backward][1]:
            seen[backward][1] = True
            queue.append((backward, True, jumps + 1))
    return -1


seed = 1654


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


problems = []
for _ in range(5000):
    a = next_random() % 2000 + 1
    b = next_random() % 2000 + 1
    x = next_random() % 2001
    m = next_random() % 1001
    taken = [False] * 2001
    forbidden = []
    for _ in range(m):
        f = next_random() % 2000 + 1
        if f != x and not taken[f]:
            taken[f] = True
            forbidden.append(f)
    problems.append((forbidden, a, b, x))
check = 0
total = 0
unreachable = 0
for forbidden, a, b, x in problems:
    answer = minimum_jumps(forbidden, a, b, x)
    if answer < 0:
        unreachable += 1
    total += answer
    check = (check * 31 + answer + 2) % 1000000007
print(f"5000 problems up to 2000: jumps sum to {total}, {unreachable} unreachable, checksum {check}")
