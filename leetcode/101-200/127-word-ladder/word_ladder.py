"""LeetCode #127: Word Ladder — Python oracle.

Length of the SHORTEST transformation sequence begin -> end (one letter per
step, every intermediate in the word list), counting both endpoints; 0 if none.
BFS by levels. Deterministic scalar output, so the mirror comparison is exact.
"""

from collections import deque


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


def ladder_length(begin, end, word_list):
    word_set = set(word_list)
    if end not in word_set:
        return 0
    q = deque([begin])
    visited = {begin}
    steps = 1
    while q:
        for _ in range(len(q)):
            word = q.popleft()
            if word == end:
                return steps
            for nb in neighbors(word, word_set):
                if nb not in visited:
                    visited.add(nb)
                    q.append(nb)
        steps += 1
    return 0


def main():
    cases = [
        ("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]),   # 5
        ("hit", "cog", ["hot", "dot", "dog", "lot", "log"]),          # 0 (no end)
        ("a", "c", ["a", "b", "c"]),                                  # 2
        ("red", "tax", ["ted", "tex", "red", "tax", "tad", "den", "rex", "pee"]),  # 4
        ("aaa", "bbb", ["aaa", "baa", "aba", "aab", "bba", "bab", "abb", "bbb"]),  # 4
        ("hot", "dog", ["hot", "dog", "dot"]),                        # 3
        ("lost", "cost", ["most", "fost", "cost", "lost", "mist", "fist", "list"]),  # 2
    ]
    MOD = 1000000007
    sink = 0
    for begin, end, wl in cases:
        n = ladder_length(begin, end, wl)
        print(f"{begin}->{end}: {n}")
        sink = (sink * 1000003 + n) % MOD
    print(f"sink: {sink}")


if __name__ == "__main__":
    main()
