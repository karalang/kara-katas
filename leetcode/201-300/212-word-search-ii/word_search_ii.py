"""LeetCode 212 — Word Search II (Python mirror / oracle).

Trie of the words + one DFS over the board, descending the trie in lockstep and
pruning where no edge exists; visited cells are marked in place and restored.
Index-pool trie (root = 0). Results sorted for a canonical order. Mirrors the
Kara version.
"""


class TrieNode:
    def __init__(self):
        self.children = {}   # char -> node index
        self.is_end = False


def child_of(nodes, idx, c):
    return nodes[idx].children.get(c, -1)


def insert(nodes, word):
    cur = 0
    for ch in word:
        child = child_of(nodes, cur, ch)
        if child == -1:
            idx = len(nodes)
            nodes.append(TrieNode())
            nodes[cur].children[ch] = idx
            cur = idx
        else:
            cur = child
    nodes[cur].is_end = True


def dfs(board, r, c, rows, cols, nodes, node, path, results):
    ch = board[r][c]
    if ch == '#':
        return
    nxt = child_of(nodes, node, ch)
    if nxt == -1:
        return

    path.append(ch)
    if nodes[nxt].is_end:
        nodes[nxt].is_end = False
        results.append("".join(path))

    board[r][c] = '#'
    if r > 0:
        dfs(board, r - 1, c, rows, cols, nodes, nxt, path, results)
    if r + 1 < rows:
        dfs(board, r + 1, c, rows, cols, nodes, nxt, path, results)
    if c > 0:
        dfs(board, r, c - 1, rows, cols, nodes, nxt, path, results)
    if c + 1 < cols:
        dfs(board, r, c + 1, rows, cols, nodes, nxt, path, results)
    board[r][c] = ch

    path.pop()


def find_words(board, words):
    nodes = [TrieNode()]
    for word in words:
        insert(nodes, word)

    results = []
    rows = len(board)
    if rows == 0:
        return results
    cols = len(board[0])

    path = []
    for r in range(rows):
        for c in range(cols):
            dfs(board, r, c, rows, cols, nodes, 0, path, results)
    results.sort()
    return results


def report(board, words):
    res = find_words(board, words)
    print(" ".join(res) if res else "[]")


def main():
    report([list("oaan"), list("etae"), list("ihkr"), list("iflv")],
           ["oath", "pea", "eat", "rain"])
    report([list("ab"), list("cd")], ["abcb"])
    report([list("ab"), list("cd")], ["ab", "cb", "ad", "bd", "xyz"])
    report([list("a")], ["a", "aa"])
    report([list("abc"), list("hid"), list("gfe")], ["abcdefghi", "abed"])


main()
