"""LeetCode 211 — Design Add and Search Words Data Structure (Python mirror).

Index-pool trie (all nodes in one list, children by integer index, root = 0)
with a recursive DFS search: a '.' wildcard tries every child. Mirrors the Kara
version.
"""


class TrieNode:
    def __init__(self):
        self.children = {}   # char -> node index
        self.is_end = False


def child_of(nodes, idx, c):
    return nodes[idx].children.get(c, -1)


def add_word(nodes, word):
    cur = 0
    for c in word:
        child = child_of(nodes, cur, c)
        if child == -1:
            new_idx = len(nodes)
            nodes.append(TrieNode())
            nodes[cur].children[c] = new_idx
            cur = new_idx
        else:
            cur = child
    nodes[cur].is_end = True


def dfs(nodes, idx, cs, pos):
    if pos == len(cs):
        return nodes[idx].is_end
    c = cs[pos]
    if c == '.':
        for child in nodes[idx].children.values():
            if dfs(nodes, child, cs, pos + 1):
                return True
        return False
    child = child_of(nodes, idx, c)
    if child == -1:
        return False
    return dfs(nodes, child, cs, pos + 1)


def search(nodes, word):
    return dfs(nodes, 0, list(word), 0)


def show(b):
    print("true" if b else "false")


def main():
    dict_nodes = [TrieNode()]  # root at index 0

    add_word(dict_nodes, "bad")
    add_word(dict_nodes, "dad")
    add_word(dict_nodes, "mad")

    show(search(dict_nodes, "pad"))
    show(search(dict_nodes, "bad"))
    show(search(dict_nodes, ".ad"))
    show(search(dict_nodes, "b.."))
    show(search(dict_nodes, "..."))
    show(search(dict_nodes, "...."))
    show(search(dict_nodes, "b.d"))
    show(search(dict_nodes, ".a."))
    show(search(dict_nodes, ".."))

    add_word(dict_nodes, "a")
    show(search(dict_nodes, "a"))
    show(search(dict_nodes, "."))
    show(search(dict_nodes, ".."))


main()
