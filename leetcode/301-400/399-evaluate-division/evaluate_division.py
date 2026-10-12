# LeetCode #399: Evaluate Division -- mirror of evaluate_division.kara
# (union-find with weights).


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
    for a, b in equations:
        for name in (a, b):
            if name not in index:
                index[name] = len(parent)
                parent.append(len(parent))
                weight.append(1.0)
    for k in range(len(equations)):
        a = index[equations[k][0]]
        b = index[equations[k][1]]
        ra = find(parent, weight, a)
        rb = find(parent, weight, b)
        if ra != rb:
            weight[ra] = values[k] * weight[b] / weight[a]
            parent[ra] = rb
    answers = []
    for a, b in queries:
        if a in index and b in index:
            i = index[a]
            j = index[b]
            ri = find(parent, weight, i)
            rj = find(parent, weight, j)
            answers.append(weight[i] / weight[j] if ri == rj else -1.0)
        else:
            answers.append(-1.0)
    return answers


seed = 399


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def pairs(names):
    return [(names[i], names[i + 1]) for i in range(0, len(names) - 1, 2)]


def show(equations, values, queries):
    answers = calc_equation(pairs(equations), values, pairs(queries))
    print("[" + ", ".join(f"{x:.5f}" for x in answers) + "]")


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
    show(["a", "b", "b", "c"], [2.0, 3.0], ["a", "c", "b", "a", "a", "e", "a", "a", "x", "x"])
    show(["a", "b", "b", "c", "bc", "cd"], [1.5, 2.5, 5.0], ["a", "c", "c", "b", "bc", "cd", "cd", "bc"])
    show(["a", "b"], [0.5], ["a", "b", "b", "a", "a", "c", "x", "y"])
    show(["a", "b", "c", "d"], [2.0, 4.0], ["a", "d", "d", "c", "b", "a", "c", "c"])
    show(["a", "b", "b", "c", "a", "c"], [2.0, 2.0, 4.0], ["a", "c", "c", "a", "b", "b"])
    names = [f"x{i}" for i in range(10)]
    chain = []
    for i in range(9):
        chain.append(names[i])
        chain.append(names[i + 1])
    show(chain, [2.0] * 9, ["x0", "x9", "x9", "x0", "x3", "x7", "x5", "x5"])
    answered = 0
    unknown = 0
    checksum = 0
    for _ in range(300):
        m = 2 + step() % 11
        hidden = [step() % 9 - 4 for _ in range(m)]
        count = 1 + step() % 15
        equations = []
        values = []
        for _ in range(count):
            a = step() % m
            b = step() % m
            equations.append((f"v{a}", f"v{b}"))
            values.append(pow2(hidden[a] - hidden[b]))
        queries = []
        for _ in range(10):
            a = step() % (m + 2)
            b = step() % (m + 2)
            queries.append((f"v{a}", f"v{b}"))
        for x in calc_equation(equations, values, queries):
            if x < 0.0:
                unknown += 1
                checksum = (checksum * 31 + 1) % 1000000007
            else:
                answered += 1
                checksum = (checksum * 31 + exponent(x) + 50) % 1000000007
    print(f"300 random systems: {answered} answered, {unknown} unknown, checksum {checksum}")


main()
