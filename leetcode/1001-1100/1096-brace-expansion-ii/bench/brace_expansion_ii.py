# Benchmark: LeetCode #1096 Brace Expansion II -- Python mirror of
# brace_expansion_ii.kara: the stack arm, two lists of words sorted and
# deduplicated at each `}`, over 64 expressions of up to 60 characters
# built once, each round changing one letter in every expression.


def join(words, part):
    out = []
    for a in words:
        for b in part:
            out.append(a + b)
    return out


def dedup(words):
    out = []
    for w in words:
        if not out or out[-1] != w:
            out.append(w)
    return out


def brace_expansion_ii(expression):
    stack = []
    union = []
    concat = [""]
    for c in expression:
        if c == "{":
            stack.append((union, concat))
            union = []
            concat = [""]
        elif c == ",":
            union.extend(concat)
            concat = [""]
        elif c == "}":
            union.extend(concat)
            union.sort()
            union = dedup(union)
            outer_union, outer_concat = stack.pop()
            concat = join(outer_concat, union)
            union = outer_union
        else:
            concat = join(concat, [c])
    union.extend(concat)
    union.sort()
    return dedup(union)


seed = 1096


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def letter():
    return chr(ord("a") + next_random() % 6)


def option():
    if next_random() % 4 == 0:
        a = letter()
        b = letter()
        c = letter()
        return "{" + a + "," + b + "}" + c
    return "".join(letter() for _ in range(next_random() % 2 + 1))


def main():
    expressions = []
    while len(expressions) < 64:
        s = ""
        for _ in range(5):
            options = [option() for _ in range(next_random() % 2 + 2)]
            s += "{" + ",".join(options) + "}"
        if len(s) <= 60:
            expressions.append(list(s))
    total = 0
    check = 0
    for rnd in range(200):
        for j, e in enumerate(expressions):
            at = (rnd * 7 + j * 13) % len(e)
            if e[at].islower():
                e[at] = chr(ord("a") + (rnd + j) % 6)
            words = brace_expansion_ii("".join(e))
            total += len(words)
            check = (check * 31 + len(words)) % 1000000007
            for b in (words[0] + words[-1]).encode():
                check = (check * 131 + b) % 1000000007
    print(f"200 rounds over 64 expressions: {total} words, checksum {check}")


main()
