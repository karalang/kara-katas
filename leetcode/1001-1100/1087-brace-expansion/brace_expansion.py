# LeetCode #1087: Brace Expansion -- mirrors brace_expansion.kara (the ★
# arm): the pattern read into its groups, each sorted, and the words built
# by a depth-first walk taking each group's letters in order.


def groups_of(s):
    groups = []
    open_group = None
    for c in s:
        if c == '{':
            open_group = []
        elif c == '}':
            open_group.sort()
            groups.append(open_group)
            open_group = None
        elif c == ',':
            pass
        elif open_group is not None:
            open_group.append(c)
        else:
            groups.append([c])
    return groups


def walk(groups, at, word, out):
    if at == len(groups):
        out.append("".join(word))
        return
    for c in groups[at]:
        word.append(c)
        walk(groups, at + 1, word, out)
        word.pop()


def expand(s):
    out = []
    walk(groups_of(s), 0, [], out)
    return out


# ---- test harness ---------------------------------------------------------

class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


# A pattern of up to `most` characters: letters alone, and groups of 1 to
# `k` different letters in braces, the letters drawn from the first `k`.
def random_pattern(rng, most, k):
    s = ""
    parts = rng.next() % 8 + 1
    for _ in range(parts):
        if rng.next() % 2 == 0:
            c = chr(ord('a') + rng.next() % k)
            if len(s) + 1 <= most:
                s += c
        else:
            want = rng.next() % k + 1
            letters = []
            while len(letters) < want:
                c = chr(ord('a') + rng.next() % k)
                if c not in letters:
                    letters.append(c)
            group = "{" + ",".join(letters) + "}"
            if len(s) + len(group) <= most:
                s += group
    if s == "":
        s = "a"
    return s


def written(words):
    return "[" + ",".join(words) + "]"


def fold(h, text):
    for b in text.encode():
        h = (h * 131 + b) % 1000000007
    return h


def main():
    cases = [
        "{a,b}c{d,e}f",
        "abcd",
        "{a,b}{z,x,y}",
        "k{a,b,c,d,e,f,g}",
        "{a}b",
        "{x,a}",
        "a{b,c}d{e,f}g{h,i}",
        "{z,y,x,w}{v,u}t",
        "{c,b,a}{c,b,a}",
        "z",
    ]
    for s in cases:
        print(f"{s} -> {written(expand(s))}")
    rng = Rng(1087)
    words = 0
    h = 0
    for t in range(300):
        s = random_pattern(rng, 50, t % 6 + 1)
        out = expand(s)
        words += len(out)
        h = fold(h, written(out))
    print(f"300 random patterns: {words} words, checksum {h}")
    big = "{c,a,b}{f,e,d}{i,g,h}{l,j,k}{o,n,m}{r,q,p}{u,s,t}"
    out = expand(big)
    print(f"{big} -> {len(out)} words, first {out[0]}, last {out[-1]}, checksum {fold(0, written(out))}")


main()
