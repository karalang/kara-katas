# LeetCode #990: Satisfiability of Equality Equations -- mirror of the
# ★ arm (equations_possible.kara), union-find with path halving.


def find(parent, x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def equations_possible(equations):
    parent = list(range(26))
    for e in equations:
        if e[1] == "=":
            a = find(parent, ord(e[0]) - 97)
            b = find(parent, ord(e[3]) - 97)
            parent[a] = b
    for e in equations:
        if e[1] == "!" and find(parent, ord(e[0]) - 97) == find(parent, ord(e[3]) - 97):
            return False
    return True


seed = 990


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def letter(i):
    return chr(97 + i)


# n equations over the first `letters` letters, each `!=` with chance
# `unequal` in 16
def random_equations(n, letters, unequal):
    out = []
    for _ in range(n):
        a = letter(next_random() % letters)
        op = "!=" if next_random() % 16 < unequal else "=="
        b = letter(next_random() % letters)
        out.append(a + op + b)
    return out


def shown(es):
    return "[" + ", ".join('"' + e + '"' for e in es) + "]"


def tf(b):
    return "true" if b else "false"


def main():
    cases = [
        ["a==b", "b!=a"],
        ["b==a", "a==b"],
        ["a==b", "b==c", "a==c"],
        ["a==b", "b!=c", "c==a"],
        ["c==c", "b==d", "x!=z"],
        ["a!=a"],
        ["a==a"],
        ["a==b", "c==d", "b==c", "a!=d"],
        ["a!=b", "b!=c", "c!=a"],
        ["a!=b", "a==c", "c==b"],
    ]
    for es in cases:
        print(f"{shown(es)} -> {tf(equations_possible(es))}")
    chain = [letter(i % 25) + "==" + letter(i % 25 + 1) for i in range(499)] + ["a!=z"]
    print(f"500 equations, a chain from a to z and then a!=z -> {tf(equations_possible(chain))}")
    halves = [letter(2 * (i % 13)) + "==" + letter(2 * ((i + 1) % 13)) for i in range(250)]
    halves += [letter(2 * (i % 13)) + "!=" + letter(2 * (i % 13) + 1) for i in range(250)]
    print(f"500 equations, the even letters equal and each unequal to the next -> {tf(equations_possible(halves))}")
    for count, most, letters, unequal in [(300, 5, 3, 4), (3000, 50, 26, 1), (300, 500, 26, 1), (3, 500, 26, 0)]:
        sat = 0
        total = 0
        check = 0
        for _ in range(count):
            n = most if count == 3 else 1 + next_random() % most
            es = random_equations(n, letters, unequal)
            ok = equations_possible(es)
            total += n
            if ok:
                sat += 1
            check = (check * 31 + (2 if ok else 1)) % 1000000007
        print(f"{count} random sets of up to {most} equations over {letters} letters, {unequal} in 16 unequal: {total} equations, {sat} satisfiable, checksum {check}")


main()
