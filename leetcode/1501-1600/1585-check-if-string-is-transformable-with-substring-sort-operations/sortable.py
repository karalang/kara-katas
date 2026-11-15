# LeetCode #1585: Check If String Is Transformable With Substring Sort
# Operations -- the Python mirror of the ★ arm: each digit of t matched to
# the first unused copy in s (a deque of positions per digit), failing when
# a smaller digit's first unused copy lies before it. O(10 n)
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


# ---- the harness: the same in every arm

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def draw(n, digits, sorts):
    s = [chr(48 + next_random() % digits) for _ in range(n)]
    t = list(s)
    for _ in range(next_random() % (sorts + 1)):
        a = (next_random() * 32768 + next_random()) % n
        b = (next_random() * 32768 + next_random()) % n
        lo, hi = min(a, b), max(a, b)
        t[lo : hi + 1] = sorted(t[lo : hi + 1])
    if next_random() % 2 == 0:
        a = (next_random() * 32768 + next_random()) % n
        b = (next_random() * 32768 + next_random()) % n
        t[a], t[b] = t[b], t[a]
    return "".join(s), "".join(t)


def batch(count, most, digits, sorts):
    check = 0
    yes = 0
    for _ in range(count):
        n = (next_random() * 32768 + next_random()) % most + 1
        s, t = draw(n, digits, sorts)
        ok = is_transformable(s, t)
        if ok:
            yes += 1
        check = mix(check, 1 if ok else 0)
    print(f"{count} problems of up to {most} digits: {yes} transformable, checksum {check}")


def main():
    global seed
    examples = [
        ("84532", "34852"),
        ("34521", "23415"),
        ("12345", "12435"),
        ("1", "2"),
        ("7", "7"),
        ("98765", "56789"),
        ("10", "01"),
        ("221", "212"),
    ]
    for s, t in examples:
        print(f"{s} {t} -> {'true' if is_transformable(s, t) else 'false'}")
    seed = 1585
    batch(3000, 8, 3, 3)
    batch(300, 1000, 10, 20)
    batch(10, 100000, 10, 100)


main()
