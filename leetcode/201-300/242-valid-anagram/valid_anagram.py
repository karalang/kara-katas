# LeetCode 242 — Valid Anagram (oracle mirror).
def is_anagram(s, t):
    if len(s) != len(t): return False
    count = [0]*26
    for cs, ct in zip(s, t):
        count[ord(cs)-97] += 1
        count[ord(ct)-97] -= 1
    return all(c == 0 for c in count)
def report(s, t): print("true" if is_anagram(s, t) else "false")
for s, t in [("anagram","nagaram"),("rat","car"),("ab","ba"),("a","ab"),("listen","silent"),("abc","abd")]:
    report(s, t)
