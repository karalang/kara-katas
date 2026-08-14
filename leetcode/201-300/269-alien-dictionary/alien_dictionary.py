"""LeetCode 269 — Alien Dictionary (Python mirror / oracle).

Mirrors alien_dictionary.kara algorithm-for-algorithm: derive one edge per
adjacent pair from the first differing position, reject a word followed by its
own prefix, then run Kahn's algorithm always taking the smallest ready letter,
which makes the answer the unique lexicographically least valid order.
"""


def alien_order(words):
    present = [False] * 26
    for w in words:
        for b in w.encode():
            present[b - 97] = True

    indeg = [0] * 26
    adj = [[False] * 26 for _ in range(26)]

    for p in range(len(words) - 1):
        a = [b - 97 for b in words[p].encode()]
        c = [b - 97 for b in words[p + 1].encode()]
        found = False
        for k in range(min(len(a), len(c))):
            if a[k] != c[k]:
                if not adj[a[k]][c[k]]:
                    adj[a[k]][c[k]] = True
                    indeg[c[k]] += 1
                found = True
                break
        if not found and len(a) > len(c):
            return ""

    done = [False] * 26
    remaining = sum(1 for d in range(26) if present[d])

    out = []
    while len(out) < remaining:
        pick = -1
        for s in range(26):
            if present[s] and not done[s] and indeg[s] == 0:
                pick = s
                break
        if pick < 0:
            return ""
        done[pick] = True
        out.append(chr(pick + 97))
        for t in range(26):
            if adj[pick][t]:
                indeg[t] -= 1
    return "".join(out)


def report(label, words):
    print(f'{label} -> "{alien_order(words)}"')


def main():
    report("[wrt,wrf,er,ett,rftt]", ["wrt", "wrf", "er", "ett", "rftt"])
    report("[z,x]", ["z", "x"])
    report("[abc,ab]", ["abc", "ab"])
    report("[ab,abc]", ["ab", "abc"])
    report("[z,x,z]", ["z", "x", "z"])
    report("[ab,adc]", ["ab", "adc"])
    report("[zy,zx]", ["zy", "zx"])
    report("[aaa]", ["aaa"])
    report("[]", [])


main()
