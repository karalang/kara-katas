# LeetCode #1096: Brace Expansion II -- Python mirror of the ★ arm: a
# recursive descent over the grammar, each union and concatenation a set
# of words, the answer sorted. Same cases and output as
# brace_expansion_ii.kara.


def union_of(s, at):
    words, at = concat_of(s, at)
    while at < len(s) and s[at] == ",":
        more, at = concat_of(s, at + 1)
        words |= more
    return words, at


def concat_of(s, at):
    words = {""}
    while at < len(s) and s[at] not in ",}":
        if s[at] == "{":
            part, at = union_of(s, at + 1)
            at += 1
        else:
            part = {s[at]}
            at += 1
        words = {a + b for a in words for b in part}
    return words, at


def brace_expansion_ii(expression):
    words, _ = union_of(expression, 0)
    return sorted(words)


seed = 1096


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_expression(depth, k):
    s = ""
    parts = next_random() % 3 + 1
    for _ in range(parts):
        if depth == 0 or next_random() % 2 == 0:
            for _ in range(next_random() % 2 + 1):
                s += chr(ord("a") + next_random() % k)
        else:
            s += "{"
            n = next_random() % 2 + 2
            for i in range(n):
                if i > 0:
                    s += ","
                s += random_expression(depth - 1, k)
            s += "}"
    return s


def checksum(words):
    h = 0
    for w in words:
        for b in w.encode():
            h = (h * 131 + b) % 1000000007
        h = (h * 131 + 1) % 1000000007
    return h


def main():
    cases = [
        "{a,b}{c,{d,e}}",
        "{{a,z},a{b,c},{ab,z}}",
        "a",
        "abc",
        "{a,b,c}",
        "{a,a,a}",
        "{c,b,a}{b,a}",
        "{a{b,c}}{{d}}",
        "{a,ab}{c,bc}",
        "{{{{a}}}}",
        "{z,y}x{w,v}",
        "{a,b}c{d,e}f",
    ]
    for e in cases:
        words = brace_expansion_ii(e)
        print(f"{e} -> [{','.join(words)}]")
    total = 0
    check = 0
    tried = 0
    while tried < 2000:
        depth = next_random() % 4
        k = next_random() % 4 + 2
        e = random_expression(depth, k)
        if len(e) > 60:
            continue
        tried += 1
        words = brace_expansion_ii(e)
        total += len(words)
        check = (check * 31 + checksum(words)) % 1000000007
    print(f"2000 random expressions: {total} words, checksum {check}")
    wide = "{a,b,c}" * 8
    words = brace_expansion_ii(wide)
    print(f"{len(wide)} characters: {len(words)} words, first {words[0]}, last {words[-1]}, checksum {checksum(words)}")
    deep = "{a,{b,{c,{d,{e,{f,{g,{h,{i,{j,{k,{l,{m,n}}}}}}}}}}}}}{x,y}"
    words = brace_expansion_ii(deep)
    print(f"{len(deep)} characters: {len(words)} words, checksum {checksum(words)}")


main()
