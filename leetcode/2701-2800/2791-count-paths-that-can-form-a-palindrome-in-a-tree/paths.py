# LeetCode #2791: Count Paths That Can Form a Palindrome in a Tree -- the
# ★ arm in Python (paths.kara): each node's mask of letter parities from
# the root, and each node paired with the earlier ones whose mask is the
# same or one bit away, counted in a dict.


def count_palindrome_paths(parent, s):
    n = len(parent)
    letters = [ord(c) - 97 for c in s]
    children = [[] for _ in range(n)]
    for i in range(1, n):
        children[parent[i]].append(i)
    mask = [0] * n
    todo = [0]
    while todo:
        u = todo.pop()
        for c in children[u]:
            mask[c] = mask[u] ^ (1 << letters[c])
            todo.append(c)
    seen = {}
    paths = 0
    for m in mask:
        paths += seen.get(m, 0)
        for b in range(26):
            paths += seen.get(m ^ (1 << b), 0)
        seen[m] = seen.get(m, 0) + 1
    return paths


seed = 2791


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def random_tree(n, letters):
    parent = [-1]
    for i in range(1, n):
        parent.append(wide() % i)
    s = "".join(ALPHABET[next_random() % letters] for _ in range(n))
    return parent, s


def main():
    print(count_palindrome_paths([-1, 0, 0, 1, 1, 2], "acaabc"))
    print(count_palindrome_paths([-1, 0, 0, 0, 0], "aaaaa"))
    n = 100000
    print(count_palindrome_paths([i - 1 for i in range(n)], "a" * n))
    star = [-1 if i == 0 else 0 for i in range(n)]
    print(count_palindrome_paths(star, "".join(ALPHABET[i % 26] for i in range(n))))
    total = 0
    check = 0
    for _ in range(3000):
        m = next_random() % 12 + 1
        parent, s = random_tree(m, 3)
        a = count_palindrome_paths(parent, s)
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"3000 small trees: paths sum to {total}, checksum {check}")
    total = 0
    check = 0
    for _ in range(20):
        parent, s = random_tree(n, 26)
        a = count_palindrome_paths(parent, s)
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"20 trees of 10^5: paths sum to {total}, checksum {check}")


main()
