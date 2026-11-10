# LeetCode #1106: Parsing A Boolean Expression -- Python mirror of the ★
# arm: recursive descent from a shared position. Same cases and output as
# parse_bool_expr.kara.

import sys

sys.setrecursionlimit(100000)


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


def parse_bool_expr(expression):
    return parse(expression, [0])


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_expr(budget, depth):
    if budget <= 1 or depth == 0 or next_random() % 4 == 0:
        return "t" if next_random() % 2 == 0 else "f"
    op = next_random() % 3
    if op == 0:
        return f"!({random_expr(budget - 1, depth - 1)})"
    k = next_random() % 4 + 1
    parts = [random_expr((budget - 1) // k, depth - 1) for _ in range(k)]
    sign = "&" if op == 1 else "|"
    return f"{sign}({','.join(parts)})"


def show(b):
    return "true" if b else "false"


def main():
    global seed
    cases = ["&(|(f))", "|(f,f,f,t)", "!(&(f,t))", "t", "f", "!(t)", "!(f)", "&(t,t,t)", "&(t,f,t)", "|(f)", "!(!(!(t)))", "|(&(t,f,t),!(t))", "&(|(f,t),!(&(f)),|(f,f,!(f)))"]
    for e in cases:
        print(f"{e} -> {show(parse_bool_expr(e))}")
    seed = 1106
    trues = 0
    length = 0
    for _ in range(2000):
        budget = next_random() % 60 + 1
        e = random_expr(budget, 8)
        length += len(e)
        if parse_bool_expr(e):
            trues += 1
    print(f"2000 random expressions, {length} characters: {trues} true")
    deep = "t"
    for i in range(6000):
        deep = f"!({deep})" if i % 3 == 0 else f"&({deep},t)" if i % 3 == 1 else f"|(f,{deep})"
        if len(deep) > 19990:
            break
    print(f"deep, {len(deep)} characters: {show(parse_bool_expr(deep))}")
    wide = "|(" + "f," * 9998 + "t)"
    print(f"wide, {len(wide)} characters: {show(parse_bool_expr(wide))}")


main()
