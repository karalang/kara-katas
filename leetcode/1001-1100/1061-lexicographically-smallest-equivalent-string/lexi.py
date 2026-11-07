# LeetCode #1061: Lexicographically Smallest Equivalent String -- the Python
# mirror of lexi.kara (the ★ arm): a union-find over the 26 letters whose
# root is always the smallest letter of its class.


def find(parent, x):
    root = x
    while parent[root] != root:
        root = parent[root]
    y = x
    while parent[y] != root:
        nxt = parent[y]
        parent[y] = root
        y = nxt
    return root


def smallest_equivalent(s1, s2, base):
    parent = list(range(26))
    for a, b in zip(s1.encode(), s2.encode()):
        ra = find(parent, a - ord("a"))
        rb = find(parent, b - ord("a"))
        if ra < rb:
            parent[rb] = ra
        else:
            parent[ra] = rb
    out = []
    for c in base.encode():
        out.append(chr(ord("a") + find(parent, c - ord("a"))))
    return "".join(out)


# ---- test harness ---------------------------------------------------------

seed = 1061


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(n, k):
    return "".join(chr(ord("a") + next_random() % k) for _ in range(n))


def mix(check, base, answer):
    moved = 0
    for x, y in zip(base.encode(), answer.encode()):
        check = (check * 31 + y) % 1000000007
        if x != y:
            moved += 1
    return check, moved


def main():
    examples = [
        ("parker", "morris", "parser"),
        ("hello", "world", "hold"),
        ("leetcode", "programs", "sourcecode"),
        ("a", "b", "b"),
        ("abc", "abc", "xyz"),
        ("abc", "bcd", "dcba"),
        ("z", "a", "zoo"),
        ("aabbcc", "bcdefa", "fed"),
        ("zyx", "wvu", "uvwxyz"),
        ("abcdefghijklmnopqrstuvwxy", "bcdefghijklmnopqrstuvwxyz", "thequickbrownfoxjumpsoverthelazydog"),
    ]
    for s1, s2, base in examples:
        print(f"{s1} {s2} {base} -> {smallest_equivalent(s1, s2, base)}")

    def batch(cases, n_of, k, base_len_of, base_k):
        check = 0
        moved = 0
        for i in range(cases):
            n = n_of(i)
            s1 = random_word(n, k)
            s2 = random_word(n, k)
            base = random_word(base_len_of(i), base_k)
            check, m = mix(check, base, smallest_equivalent(s1, s2, base))
            moved += m
        return moved, check

    moved, check = batch(3000, lambda i: next_random() % 8 + 1, 6, lambda i: next_random() % 10 + 1, 8)
    print(f"3000 pairs of 1 to 8 letters over 6: {moved} letters moved, checksum {check}")
    moved, check = batch(3000, lambda i: next_random() % 4 + 1, 26, lambda i: next_random() % 30 + 1, 26)
    print(f"3000 pairs of 1 to 4 letters over 26: {moved} letters moved, checksum {check}")
    moved, check = batch(100, lambda i: 1 + i % 20, 26, lambda i: 1000, 26)
    print(f"100 bases of 1000 letters: {moved} letters moved, checksum {check}")
    s1 = random_word(1000, 26)
    s2 = random_word(1000, 26)
    base = random_word(1000, 26)
    c, m = mix(0, base, smallest_equivalent(s1, s2, base))
    print(f"1000 pairs over 26, a base of 1000: {m} letters moved, checksum {c}")
    up = "".join(chr(ord("z") - i) for i in range(25))
    down = "".join(chr(ord("y") - i) for i in range(25))
    print(f"{up} {down} zebra -> {smallest_equivalent(up, down, 'zebra')}")


main()
