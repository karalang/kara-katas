# LeetCode #736: Parse Lisp Expression -- tokens, recursion and a stack
# of scopes.
# Benchmark mirror of the Kara star arm: split the text into tokens,
# then evaluate by recursion, keeping the assignments of each open let
# in a scope of its own and looking a name up from the innermost.


def tokenize(expression):
    tokens = []
    word = ""
    for c in expression:
        if c in "() ":
            if word:
                tokens.append(word)
                word = ""
            if c != " ":
                tokens.append(c)
        else:
            word += c
    if word:
        tokens.append(word)
    return tokens


def lookup(scopes, name):
    for scope in reversed(scopes):
        if name in scope:
            return scope[name]
    return 0


def evaluate_at(tokens, pos, scopes):
    t = tokens[pos[0]]
    pos[0] += 1
    if t != "(":
        if t[0] == "-" or t[0].isdigit():
            return int(t)
        return lookup(scopes, t)
    op = tokens[pos[0]]
    pos[0] += 1
    if op == "add":
        a = evaluate_at(tokens, pos, scopes)
        b = evaluate_at(tokens, pos, scopes)
        value = a + b
    elif op == "mult":
        a = evaluate_at(tokens, pos, scopes)
        b = evaluate_at(tokens, pos, scopes)
        value = a * b
    else:
        scopes.append({})
        while True:
            name = tokens[pos[0]]
            if name != "(" and tokens[pos[0] + 1] != ")":
                pos[0] += 1
                scopes[-1][name] = evaluate_at(tokens, pos, scopes)
            else:
                value = evaluate_at(tokens, pos, scopes)
                break
        scopes.pop()
    pos[0] += 1
    return value


def evaluate(expression):
    return evaluate_at(tokenize(expression), [0], [])


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def random_expr(seed, depth, names):
    kinds = 2 if depth == 0 else 5
    kind = next_random(seed) % kinds
    if kind == 0 or (kind == 1 and not names):
        return f"{next_random(seed) % 21 - 10}"
    if kind == 1:
        return names[next_random(seed) % len(names)]
    if kind == 2:
        a = random_expr(seed, depth - 1, names)
        b = random_expr(seed, depth - 1, names)
        return f"(add {a} {b})"
    if kind == 3:
        a = random_expr(seed, depth - 1, names)
        return f"(mult {a} {next_random(seed) % 5 - 2})"
    pool = ["x", "y", "z", "a1", "b2"]
    inner = list(names)
    text = "(let"
    count = 1 + next_random(seed) % 3
    for _ in range(count):
        name = pool[next_random(seed) % 5]
        v = random_expr(seed, depth - 1, inner)
        text = f"{text} {name} {v}"
        if name not in inner:
            inner.append(name)
    body = random_expr(seed, depth - 1, inner)
    return f"{text} {body})"



def main():
    seed = [736]
    exprs = []
    chars = 0
    while len(exprs) < 1000:
        e = random_expr(seed, 8, [])
        if 500 <= len(e) <= 2000:
            chars += len(e)
            exprs.append(e)
    total = 0
    for _ in range(40):
        for e in exprs:
            v = evaluate(e)
            total = (total * 31 + v % 1000000007) % 1000000007
    print(f"40 rounds of 1000 expressions of {chars} characters in all: checksum {total}")


main()
