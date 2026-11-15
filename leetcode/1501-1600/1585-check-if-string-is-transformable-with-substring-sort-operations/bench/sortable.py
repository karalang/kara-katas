# LeetCode #1585 bench: the same first-unused-copy match, in Python.
from collections import deque


def is_transformable(s, t):
    at = [deque() for _ in range(10)]
    for i, c in enumerate(s):
        at[ord(c) - 48].append(i)
    for c in t:
        d = ord(c) - 48
        if not at[d]:
            return False
        p = at[d].popleft()
        for e in range(d):
            if at[e] and at[e][0] < p:
                return False
    return True


seed = 1585


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def main():
    n = 100000
    problems = []
    for k in range(40):
        s = [48 + next_random() % 10 for _ in range(n)]
        t = list(s)
        for _ in range(2000):
            a = (next_random() * 32768 + next_random()) % (n - 50)
            b = a + next_random() % 50 + 1
            t[a:b] = sorted(t[a:b])
        if k % 2 == 1:
            a = (next_random() * 32768 + next_random()) % n
            b = (next_random() * 32768 + next_random()) % n
            t[a], t[b] = t[b], t[a]
        problems.append((bytes(s).decode(), bytes(t).decode()))
    check = 0
    yes = 0
    for s, t in problems:
        ok = is_transformable(s, t)
        if ok:
            yes += 1
        check = mix(check, 1 if ok else 0)
    print(f"40 problems of 100000 digits: {yes} transformable, checksum {check}")


main()
