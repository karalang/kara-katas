# LeetCode 241 — Different Ways to Add Parentheses (oracle mirror).
def tokenize(expr):
    tok = []; i = 0; n = len(expr)
    while i < n:
        c = expr[i]
        if c in "+-*": tok.append(c); i += 1
        else:
            v = 0
            while i < n and expr[i].isdigit(): v = v*10 + int(expr[i]); i += 1
            tok.append(v)
    return tok

def ways(tok, lo, hi):
    if lo == hi: return [tok[lo]]
    res = []
    for k in range(lo+1, hi, 2):
        op = tok[k]
        for l in ways(tok, lo, k-1):
            for r in ways(tok, k+1, hi):
                res.append(l+r if op=="+" else l-r if op=="-" else l*r)
    return res

def report(expr):
    vals = sorted(ways(tokenize(expr), 0, len(tokenize(expr))-1))
    print(" ".join(str(x) for x in vals))

for e in ["2-1-1", "2*3-4*5", "11", "1+2*3", "2*3*4"]: report(e)
