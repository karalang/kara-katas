# LeetCode #2151: Maximum Good People Based on Statements -- the Python
# mirror of statements.kara's ★ arm.


def maximum_good(statements):
    n = len(statements)
    best = 0
    for mask in range(1 << n):
        holds = True
        for i in range(n):
            if (mask >> i) & 1 == 1:
                for j in range(n):
                    say = statements[i][j]
                    if say != 2 and say != (mask >> j) & 1:
                        holds = False
        if holds:
            best = max(best, bin(mask).count("1"))
    return best


seed = 2151


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def draw(n, truthful):
    hidden = next_random() % (1 << n)
    statements = []
    for i in range(n):
        row = []
        for j in range(n):
            if i == j:
                say = 2
            elif truthful and (hidden >> i) & 1 == 1:
                say = 2 if next_random() % 3 == 0 else (hidden >> j) & 1
            else:
                say = next_random() % 3
            row.append(say)
        statements.append(row)
    return statements


def fmt(statements):
    return "[" + ", ".join("[" + ", ".join(map(str, row)) + "]" for row in statements) + "]"


def show(statements):
    print(f"{fmt(statements)} -> {maximum_good(statements)}")


def main():
    show([[2, 1, 2], [1, 2, 2], [2, 0, 2]])
    show([[2, 0], [0, 2]])
    show([[2]])
    show([[2, 2, 2], [2, 2, 2], [2, 2, 2]])
    show([[2, 1], [1, 2]])
    show([[2, 0], [1, 2]])
    total = 0
    check = 0
    for rnd in range(2000):
        n = next_random() % 6 + 2
        statements = draw(n, rnd % 2 == 1)
        good = maximum_good(statements)
        total += good
        check = (check * 31 + good + n) % 1000000007
    print(f"2000 villages: {total} good in all, checksum {check}")
    silent = [[2] * 15 for _ in range(15)]
    truthful = draw(15, True)
    rand = draw(15, False)
    print(f"15 people: {maximum_good(silent)} all silent, {maximum_good(truthful)} truthful, {maximum_good(rand)} at random")


main()
