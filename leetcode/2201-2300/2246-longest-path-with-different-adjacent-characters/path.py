# LeetCode #2246: Longest Path With Different Adjacent Characters -- the
# Python mirror of path.kara: children listed, the nodes in breadth-first
# order taken back to front, each node's longest changing chain down and
# its two longest through children of another letter. O(n).


def longest_path(parent, s):
    n = len(parent)
    children = [[] for _ in range(n)]
    for v in range(1, n):
        children[parent[v]].append(v)
    order = [0]
    nxt = 0
    while nxt < len(order):
        v = order[nxt]
        nxt += 1
        order.extend(children[v])
    down = [1] * n
    best = 1
    for v in reversed(order):
        first = second = 0
        for c in children[v]:
            if s[c] == s[v]:
                continue
            if down[c] > first:
                second = first
                first = down[c]
            elif down[c] > second:
                second = down[c]
        down[v] = first + 1
        best = max(best, first + second + 1)
    return best


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    high = next_random()
    return high * 32768 + next_random()


def random_tree(n, letters):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    order = list(range(n))
    for i in range(n - 1, 1, -1):
        j = wide_random() % i + 1
        order[i], order[j] = order[j], order[i]
    parent = [-1] * n
    for i in range(1, n):
        parent[order[i]] = order[wide_random() % i]
    s = "".join(alphabet[next_random() % letters] for _ in range(n))
    return parent, s


def main():
    global seed
    examples = [
        ([-1, 0, 0, 1, 1, 2], "abacbe"),
        ([-1, 0, 0, 0], "aabc"),
        ([-1], "z"),
        ([-1, 0, 1, 2], "aaaa"),
        ([-1, 0, 1, 2], "abab"),
        ([-1, 0, 0, 0, 0], "abcde"),
    ]
    for parent, s in examples:
        print(f"{parent} {s} -> {longest_path(parent, s)}")
    seed = 2246
    check = 0
    most = 0
    for _ in range(2000):
        n = next_random() % 30 + 1
        letters = next_random() % 4 + 1
        parent, s = random_tree(n, letters)
        longest = longest_path(parent, s)
        most = max(most, longest)
        check = (check * 31 + longest) % 1000000007
    print(f"2000 trees: longest {most}, checksum {check}")
    parent, s = random_tree(100000, 26)
    print(f"10^5 nodes: {longest_path(parent, s)}")
    parent = [i - 1 for i in range(100000)]
    s = "".join("a" if i % 2 == 0 else "b" for i in range(100000))
    print(f"a path of 10^5: {longest_path(parent, s)}")


main()
