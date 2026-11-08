# LeetCode #1525: Number of Good Ways to Split a String -- mirrors
# splits.kara, the ★ arm: distinct letters in every prefix and every
# suffix, compared at each split.


def num_splits(s):
    n = len(s)
    left = [0] * n
    seen = set()
    for i in range(n):
        seen.add(s[i])
        left[i] = len(seen)
    right = [0] * n
    seen = set()
    for i in range(n - 1, -1, -1):
        seen.add(s[i])
        right[i] = len(seen)
    return sum(1 for i in range(1, n) if left[i - 1] == right[i])


seed = 1525


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def batch(count, most, letters):
    check = 0
    for _ in range(count):
        n = (next_random() * 32768 + next_random()) % most + 1
        s = "".join(chr(97 + next_random() % letters) for _ in range(n))
        check = mix(check, num_splits(s))
    print(f"{count} strings of 1 to {most} letters over {letters}: checksum {check}")


for s in ["aacaba", "abcd", "aaaaa", "acbadbaada", "a"]:
    print(f"{s} -> {num_splits(s)}")
batch(3000, 12, 4)
batch(300, 300, 26)
batch(30, 100000, 26)
