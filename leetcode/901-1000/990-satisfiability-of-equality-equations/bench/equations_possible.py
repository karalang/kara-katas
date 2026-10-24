# LeetCode #990: Satisfiability of Equality Equations -- bench, the ★
# arm (union-find with path halving), the same algorithm and workload
# as equations_possible.kara.


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


# n equations over the 26 letters, each `!=` with chance `unequal` in 256
def random_equations(n, unequal):
    out = []
    for _ in range(n):
        a = chr(97 + next_random() % 26)
        op = "!=" if next_random() % 256 < unequal else "=="
        b = chr(97 + next_random() % 26)
        out.append(a + op + b)
    return out


def main():
    rounds = 6000
    sets = [random_equations(500, i % 2) for i in range(20)]
    sat = 0
    check = 0
    for r in range(rounds):
        for i in range(20):
            ok = equations_possible(sets[(r + i) % 20])
            if ok:
                sat += 1
            check = (check * 31 + (2 if ok else 1)) % 1000000007
    print(f"{rounds} rounds over 20 sets of 500 equations: {sat} satisfiable, checksum {check}")


main()
