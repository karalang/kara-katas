# LeetCode #1106: Parsing A Boolean Expression -- the bench in Python: the
# ★ arm (recursive descent from a shared position) over 32 expressions of
# up to about 2 * 10^4 characters, each round flipping one value in every
# expression and parsing it again.
import sys

sys.setrecursionlimit(10000)


def parse(s, at):
    c = s[at[0]]
    at[0] += 1
    if c == 't':
        return True
    if c == 'f':
        return False
    at[0] += 1
    values = []
    while True:
        values.append(parse(s, at))
        nxt = s[at[0]]
        at[0] += 1
        if nxt == ')':
            break
    if c == '!':
        return not values[0]
    if c == '&':
        return all(values)
    return any(values)


seed = 1106


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_expr(out, budget, depth):
    if budget <= 1 or depth == 0:
        out.append('t' if next_random() % 2 == 0 else 'f')
        return
    op = next_random() % 3
    if op == 0:
        out.append('!')
        out.append('(')
        random_expr(out, budget - 1, depth - 1)
        out.append(')')
        return
    k = next_random() % 4 + 1
    out.append('&' if op == 1 else '|')
    out.append('(')
    for i in range(k):
        if i > 0:
            out.append(',')
        random_expr(out, (budget - 1) // k, depth - 1)
    out.append(')')


def main():
    cases = []
    values = []
    length = 0
    for _ in range(32):
        e = []
        random_expr(e, 6000, 20)
        values.append([i for i in range(len(e)) if e[i] == 't' or e[i] == 'f'])
        length += len(e)
        cases.append(e)
    trues = 0
    check = 0
    for rnd in range(200):
        for j in range(len(cases)):
            vs = values[j]
            i = vs[(rnd * 7919 + j * 104729) % len(vs)]
            cases[j][i] = 'f' if cases[j][i] == 't' else 't'
            v = parse(cases[j], [0])
            if v:
                trues += 1
            check = (check * 31 + (2 if v else 1)) % 1000000007
    print(f"200 rounds over 32 expressions of {length} characters: {trues} true, checksum {check}")


main()
