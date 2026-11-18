# LeetCode #1190: Reverse Substrings Between Each Pair of Parentheses -- the
# ★ arm in Python: each bracket paired with its match, then one walk that
# jumps to the match at a bracket and turns around. It also checks every
# answer against the statement read literally: the innermost pair's letters
# reversed and its brackets dropped, until no pair is left.
import re


def reverse_parentheses(s):
    n = len(s)
    pair = [0] * n
    open_ = []
    for i, c in enumerate(s):
        if c == "(":
            open_.append(i)
        elif c == ")":
            j = open_.pop()
            pair[i] = j
            pair[j] = i
    out = []
    i, step = 0, 1
    while i < n:
        if s[i] in "()":
            i = pair[i]
            step = -step
        else:
            out.append(s[i])
        i += step
    return "".join(out)


def literal(s):
    inner = re.compile(r"\(([a-z]*)\)")
    while "(" in s:
        s = inner.sub(lambda m: m.group(1)[::-1], s, count=1)
    return s


seed = 1190


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_case(n, letters):
    s = []
    open_ = 0
    for _ in range(n):
        r = next_random() % 4
        if r == 0:
            s.append("(")
            open_ += 1
        elif r == 1 and open_ > 0:
            s.append(")")
            open_ -= 1
        else:
            s.append(letters[next_random() % len(letters)])
    s.append(")" * open_)
    return "".join(s)


def digest(s):
    h = 0
    for b in s.encode():
        h = (h * 131 + b) % 1000000007
    return h


def solve(s):
    out = reverse_parentheses(s)
    assert out == literal(s), s
    return out


cases = ["(abcd)", "(u(love)i)", "(ed(et(oc))el)", "a", "()", "((ab))", "a(bcdefghijkl(mno)p)q", "ta()usw((((a))))", "(a)(b)(c)"]
for c in cases:
    print(f'"{c}" -> "{solve(c)}"')
letters = "abcdefghijklmnopqrstuvwxyz"
check = total = 0
for _ in range(2000):
    n = next_random() % 40 + 1
    out = solve(random_case(n, letters))
    total += len(out)
    check = (check * 131 + digest(out)) % 1000000007
print(f"2000 random strings: {total} letters, checksum {check}")
deep = "".join(letters[i % 26] + "(" for i in range(500)) + "".join(letters[(i * 7) % 26] + ")" for i in range(500))
out = solve(deep)
print(f"500 nested pairs: {len(out)} letters, digest {digest(out)}")
out = solve(random_case(2000, letters))
print(f"2000 random characters: {len(out)} letters, digest {digest(out)}")
