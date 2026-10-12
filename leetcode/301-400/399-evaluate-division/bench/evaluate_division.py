# Benchmark for #399: mirror of evaluate_division.kara (union-find with weights).
import sys

sys.setrecursionlimit(10000)


def find(parent, weight, i):
    p = parent[i]
    if p == i:
        return i
    root = find(parent, weight, p)
    weight[i] = weight[i] * weight[p]
    parent[i] = root
    return root


def calc_equation(equations, values, queries):
    index = {}
    parent = []
    weight = []

    def intern(name):
        i = index.get(name)
        if i is not None:
            return i
        i = len(parent)
        index[name] = i
        parent.append(i)
        weight.append(1.0)
        return i

    for k in range(len(equations)):
        a = intern(equations[k][0])
        b = intern(equations[k][1])
        ra = find(parent, weight, a)
        rb = find(parent, weight, b)
        if ra != rb:
            weight[ra] = values[k] * weight[b] / weight[a]
            parent[ra] = rb
    answers = []
    for a, b in queries:
        answer = -1.0
        if a in index and b in index:
            i = index[a]
            j = index[b]
            if find(parent, weight, i) == find(parent, weight, j):
                answer = weight[i] / weight[j]
        answers.append(answer)
    return answers


seed = 3991


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def pow2(k):
    x = 1.0
    for _ in range(abs(k)):
        x = x * 2.0
    return 1.0 / x if k < 0 else x


def exponent(x):
    v = x
    k = 0
    while v >= 2.0:
        v = v / 2.0
        k += 1
    while v < 1.0:
        v = v * 2.0
        k -= 1
    return k


def main():
    systems = int(sys.argv[1]) if len(sys.argv) > 1 else 100000
    answered = 0
    checksum = 0
    for _ in range(systems):
        m = 2 + step() % 39
        hidden = [step() % 9 - 4 for _ in range(m)]
        equations = []
        values = []
        for _ in range(20):
            a = step() % m
            b = step() % m
            equations.append((f"v{a}", f"v{b}"))
            values.append(pow2(hidden[a] - hidden[b]))
        queries = []
        for _ in range(20):
            a = step() % (m + 2)
            b = step() % (m + 2)
            queries.append((f"v{a}", f"v{b}"))
        for x in calc_equation(equations, values, queries):
            if x < 0.0:
                checksum = (checksum * 31 + 1) % 1000000007
            else:
                answered += 1
                checksum = (checksum * 31 + exponent(x) + 50) % 1000000007
    print(f"{systems} systems: {answered} answered, checksum {checksum}")


main()
