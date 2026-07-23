"""LeetCode 208 — Implement Trie (Prefix Tree) (Python mirror / oracle).

Index-pool trie: all nodes in one list, children referenced by integer index
(root = 0). Mirrors the Kara version.
"""


class TrieNode:
    def __init__(self):
        self.children = {}   # char -> node index
        self.is_end = False


def child_of(nodes, idx, c):
    return nodes[idx].children.get(c, -1)


def insert(nodes, word):
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


def walk(nodes, s):
    cur = 0
    for c in s:
        child = child_of(nodes, cur, c)
        if child == -1:
            return -1
        cur = child
    return cur


def search(nodes, word):
    node = walk(nodes, word)
    if node == -1:
        return False
    return nodes[node].is_end


def starts_with(nodes, prefix):
    return walk(nodes, prefix) != -1


def show(b):
    print("true" if b else "false")


def main():
    trie = [TrieNode()]  # root at index 0

    insert(trie, "apple")
    show(search(trie, "apple"))
    show(search(trie, "app"))
    show(starts_with(trie, "app"))
    insert(trie, "app")
    show(search(trie, "app"))

    insert(trie, "application")
    insert(trie, "apply")
    show(search(trie, "apply"))
    show(search(trie, "appl"))
    show(starts_with(trie, "appl"))
    show(starts_with(trie, "banana"))
    show(search(trie, "banana"))

    insert(trie, "banana")
    show(search(trie, "banana"))
    show(starts_with(trie, "ban"))


main()
