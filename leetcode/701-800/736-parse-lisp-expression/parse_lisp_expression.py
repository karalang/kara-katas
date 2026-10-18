# LeetCode #736: Parse Lisp Expression -- tokens, recursion and a stack
# of scopes.
# Mirror of the Kara star arm: split the text into tokens, then evaluate
# by recursion, keeping one dict of assignments for each let that is
# open.


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
    if kind in (2, 3):
        a = random_expr(seed, depth - 1, names)
        b = random_expr(seed, depth - 1, names)
        op = "add" if kind == 2 else "mult"
        return f"({op} {a} {b})"
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


def show(e):
    print(f"{e} -> {evaluate(e)}")


def main():
    show("(let x 2 (mult x (let x 3 y 4 (add x y))))")
    show("(let x 3 x 2 x)")
    show("(let x 1 y 2 x (add x y) (add x y))")
    show("(add 1 2)")
    show("(mult 3 (add 2 3))")
    show("(let a1 3 b2 (add a1 1) b2)")
    show("(let x 2 (add (let x 3 (let x 4 x)) x))")
    show("(let x -2 y x y)")
    show("(mult -3 (add 4 -6))")
    show("-7")
    deep = "(let v0 1"
    for i in range(1, 80):
        deep = f"{deep} (let v{i} (add v{i - 1} 1)"
    deep = f"{deep} v79" + ")" * 80
    print(f"80 nested lets, {len(deep)} characters -> {evaluate(deep)}")
    chain = "150"
    for k in range(149, 0, -1):
        chain = f"(add {k} {chain})"
    print(f"adds of 1 to 150, {len(chain)} characters -> {evaluate(chain)}")
    doubling = "(let x 1" + " (let x (add x x)" * 30 + " x" + ")" * 31
    print(f"x doubled in 30 lets that each hide the last, {len(doubling)} characters -> {evaluate(doubling)}")
    seed = [736]
    total = 0
    chars = 0
    for _ in range(300):
        depth = 1 + next_random(seed) % 3
        e = random_expr(seed, depth, [])
        chars += len(e)
        v = evaluate(e)
        total = (total * 131 + v % 1000000007) % 1000000007
    print(f"300 random expressions, {chars} characters: checksum {total}")


main()
