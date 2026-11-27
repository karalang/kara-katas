# LeetCode #1807: Evaluate the Bracket Pairs of a String -- the ★ arm in
# Python: the knowledge put in a dict, and one walk of `s`, the text outside
# brackets copied, a key gathered inside them, and the key's value, or `?`,
# written at its `)`.


def evaluate(s, knowledge):
    values = {}
    for k, v in knowledge:
        values[k] = v
    out = []
    key = []
    inside = False
    for c in s:
        if c == "(":
            inside = True
        elif c == ")":
            out.append(values.get("".join(key), "?"))
            key = []
            inside = False
        elif inside:
            key.append(c)
        else:
            out.append(c)
    return "".join(out)


seed = 1807


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def word(most, letters):
    n = 1 + next_random() % most
    return "".join(chr(97 + next_random() % letters) for _ in range(n))


def fold(text):
    h = 0
    for b in text.encode():
        h = (h * 131 + b) % 1000000007
    return h


def main():
    # LeetCode's three examples
    print(evaluate("(name)is(age)yearsold", [("name", "bob"), ("age", "two")]))
    print(evaluate("hi(name)", [("a", "b")]))
    print(evaluate("(a)(a)(a)aaa", [("a", "yes")]))
    # the edges
    print(
        evaluate("plain", [("plain", "x")]),
        evaluate("(a)b(c)", []),
        evaluate("(x)(y)", [("x", "y"), ("y", "x")]),
        evaluate("(k)", [("k", "abcdefghij")]),
    )
    # the constraints' most
    knowledge = []
    seen = set()
    while len(knowledge) < 100000:
        k = word(10, 4)
        if k not in seen:
            seen.add(k)
            knowledge.append((k, word(10, 26)))
    s = []
    length = 0
    while length < 99980:
        if next_random() % 2 == 0:
            piece = word(3, 26)
        else:
            piece = "(" + word(10, 4) + ")"
        s.append(piece)
        length += len(piece)
    s = "".join(s)
    big = evaluate(s, knowledge)
    print(f"the most: {len(s)} characters to {len(big)}, fold {fold(big)}")
    # 3000 random cases
    check = 0
    for _ in range(3000):
        know = []
        keys = set()
        for _ in range(next_random() % 9):
            k = word(3, 3)
            if k not in keys:
                keys.add(k)
                know.append((k, word(4, 26)))
        text = []
        for _ in range(1 + next_random() % 12):
            if next_random() % 2 == 0:
                text.append(word(3, 26))
            else:
                text.append("(" + word(3, 3) + ")")
        check = (check * 31 + fold(evaluate("".join(text), know))) % 1000000007
    print(f"3000 random cases: checksum {check}")


main()
