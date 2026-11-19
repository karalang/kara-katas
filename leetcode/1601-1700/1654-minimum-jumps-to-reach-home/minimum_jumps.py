# LeetCode #1654: Minimum Jumps to Reach Home -- the Python mirror of the
# ★ arm: a breadth-first search over (position, whether the last jump was
# backward), positions capped at the largest of x and the forbidden ones
# plus a + b.

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


# ---- the harness: the same as every arm's ---------------------------------

seed = 1654


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def batch(count, most):
    check = 0
    total = 0
    unreachable = 0
    for _ in range(count):
        a = next_random() % most + 1
        b = next_random() % most + 1
        x = next_random() % (most + 1)
        m = next_random() % (most // 2 + 1)
        forbidden = []
        for _ in range(m):
            f = next_random() % most + 1
            if f != x and f not in forbidden:
                forbidden.append(f)
        answer = minimum_jumps(forbidden, a, b, x)
        if answer < 0:
            unreachable += 1
        total += answer
        check = (check * 31 + answer + 2) % 1000000007
    print(f"{count} problems up to {most}: jumps sum to {total}, {unreachable} unreachable, checksum {check}")


print(minimum_jumps([14, 4, 18, 1, 15], 3, 15, 9))
print(minimum_jumps([8, 3, 16, 6, 12, 20], 15, 13, 11))
print(minimum_jumps([1, 6, 2, 14, 5, 17, 4], 16, 9, 7))
print(minimum_jumps([5], 3, 2, 0))
print(minimum_jumps([], 4, 1, 4))
print(minimum_jumps([], 5, 3, 2))
batch(3000, 12)
batch(300, 200)
batch(20, 2000)
