# LeetCode #2246: Longest Path With Different Adjacent Characters -- the
# benchmark's Python mirror of path.kara: child lists, breadth-first
# order taken back to front, each node's two longest chains through
# children of another letter.


def longest_path(parent, s):
    n = len(parent)
    children = [[] for _ in range(n)]
    for v in range(1, n):
        children[parent[v]].append(v)
    order = [0]
    nxt = 0
    while nxt < len(order):
        order.extend(children[order[nxt]])
        nxt += 1
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


seed = 2246


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    high = next_random()
    return high * 32768 + next_random()


def main():
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    check = 0
    for _ in range(40):
        parent = [-1] * 100000
        for v in range(1, 100000):
            parent[v] = wide_random() % v
        s = "".join(alphabet[next_random() % 26] for _ in range(100000))
        check = (check * 31 + longest_path(parent, s)) % 1000000007
    print(f"40 trees of 100000 nodes: checksum {check}")


main()
