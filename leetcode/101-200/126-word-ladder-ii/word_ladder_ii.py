"""LeetCode #126: Word Ladder II — Python reference / oracle.

Find ALL shortest transformation sequences beginWord -> endWord, changing one
letter per step, every intermediate in wordList. BFS builds a level graph +
predecessors; DFS reconstructs every shortest path. To keep the oracle
deterministic without pinning a path order, we print per-case
  count=<#paths> len=<path length> hash=<order-independent path digest>
and fold a global sink. (Same output discipline as #113.)
"""

MOD = 1000000007


def neighbors(word, word_set):
    out = []
    for i in range(len(word)):
        for c in range(26):
            ch = chr(ord('a') + c)
            if ch == word[i]:
                continue
            cand = word[:i] + ch + word[i + 1:]
            if cand in word_set:
                out.append(cand)
    return out


def find_ladders(begin, end, word_list):
    word_set = set(word_list)
    if end not in word_set:
        return []
    # BFS building predecessors of each word at its shortest depth.
    preds = {}                      # word -> list of predecessor words
    cur = {begin}
    visited = {begin}
    found = False
    while cur and not found:
        nxt = set()
        # words discovered this level are only committed to `visited` after the
        # whole level, so multiple predecessors at the same level are captured.
        for word in sorted(cur):
            for nb in neighbors(word, word_set):
                if nb in visited:
                    continue
                if nb not in preds:
                    preds[nb] = []
                preds[nb].append(word)
                nxt.add(nb)
                if nb == end:
                    found = True
        visited |= nxt
        cur = nxt
    if not found:
        return []
    # DFS back from end to begin via preds.
    paths = []
    path = [end]

    def dfs(word):
        if word == begin:
            paths.append(list(reversed(path)))
            return
        for p in preds.get(word, []):
            path.append(p)
            dfs(p)
            path.pop()

    dfs(end)
    return paths


def path_hash(path):
    h = 0
    for w in path:
        for ch in w:
            h = (h * 131 + (ord(ch) - ord('a') + 1)) % MOD
        h = (h * 131 + 27) % MOD          # word separator
    return h


def summarize(begin, end, word_list):
    paths = find_ladders(begin, end, word_list)
    count = len(paths)
    length = len(paths[0]) if paths else 0
    # Order-independent digest: sum of per-path hashes.
    digest = 0
    for p in paths:
        digest = (digest + path_hash(p)) % MOD
    return count, length, digest


def main():
    cases = [
        ("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]),
        ("hit", "cog", ["hot", "dot", "dog", "lot", "log"]),          # end absent -> 0
        ("a", "c", ["a", "b", "c"]),
        ("red", "tax", ["ted", "tex", "red", "tax", "tad", "den", "rex", "pee"]),
        # a/b hypercube: 6 shortest paths of length 4 (flip each of 3 positions once).
        ("aaa", "bbb", ["aaa", "baa", "aba", "aab", "bba", "bab", "abb", "bbb"]),
    ]
    sink = 0
    for begin, end, wl in cases:
        count, length, digest = summarize(begin, end, wl)
        print(f"{begin}->{end}: count={count} len={length} hash={digest}")
        sink = (sink * 1000003 + count * 7 + length * 13 + digest) % MOD
    print(f"sink: {sink}")


if __name__ == "__main__":
    main()
