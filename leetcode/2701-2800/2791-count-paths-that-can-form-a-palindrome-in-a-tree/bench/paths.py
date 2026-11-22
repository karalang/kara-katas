# LeetCode #2791: Count Paths That Can Form a Palindrome in a Tree -- the
# bench in Python: the ★ arm over 20 random trees of 10^5 nodes with
# letters from a to z, all drawn first, then each answered 5 times.


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


def main():
    count = 20
    rounds = 5
    n = 100000
    cases = []
    for _ in range(count):
        parent = [-1]
        for i in range(1, n):
            parent.append(wide() % i)
        s = "".join(ALPHABET[next_random() % 26] for _ in range(n))
        cases.append((parent, s))
    total = 0
    check = 0
    for r in range(rounds):
        for parent, s in cases:
            a = count_palindrome_paths(parent, s)
            total += a
            check = (check * 31 + a + r) % 1000000007
    print(f"{count} trees of 10^5, {rounds} rounds: paths sum to {total}, checksum {check}")


main()
