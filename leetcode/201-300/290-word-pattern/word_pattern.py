# LeetCode 290 — Word Pattern (oracle mirror).
def word_pattern(pattern, s):
    words = s.split()
    if len(pattern) != len(words): return False
    p2w = {}; w2p = {}
    for c, w in zip(pattern, words):
        if c in p2w:
            if p2w[c] != w: return False
        else: p2w[c] = w
        if w in w2p:
            if w2p[w] != c: return False
        else: w2p[w] = c
    return True
def report(p, s): print("true" if word_pattern(p, s) else "false")
for p, s in [("abba","dog cat cat dog"),("abba","dog cat cat fish"),("aaaa","dog cat cat dog"),
             ("abba","dog dog dog dog"),("abc","b c a"),("ab","dog dog")]:
    report(p, s)
