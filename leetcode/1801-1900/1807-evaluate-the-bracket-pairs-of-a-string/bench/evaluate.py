# LeetCode #1807: Evaluate the Bracket Pairs of a String -- the bench in
# Python: the ★ arm over 40 strings of 10^5 characters and 40 knowledge
# lists of 2 * 10^4 pairs built once, 200 calls.


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


def main():
    texts = []
    lists = []
    for _ in range(40):
        s = []
        length = 0
        while length < 99980:
            if next_random() % 2 == 0:
                piece = word(3, 26)
            else:
                piece = "(" + word(8, 4) + ")"
            s.append(piece)
            length += len(piece)
        texts.append("".join(s))
        knowledge = []
        seen = set()
        while len(knowledge) < 20000:
            k = word(8, 4)
            if k not in seen:
                seen.add(k)
                knowledge.append((k, word(10, 26)))
        lists.append(knowledge)
    check = 0
    for call in range(200):
        s = texts[(check + call) % 40]
        knowledge = lists[(check * 7 + call) % 40]
        out = evaluate(s, knowledge)
        check = (check * 31 + len(out) + ord(out[len(out) // 2])) % 1000000007
    print(f"200 calls over 40 strings of 10^5 characters: checksum {check}")


main()
