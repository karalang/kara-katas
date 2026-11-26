# The Python mirror of ways.kara.


def ways(pizza, k):
    rows = len(pizza)
    cols = len(pizza[0])
    apples = [[0] * (cols + 1) for _ in range(rows + 1)]
    for r in range(rows - 1, -1, -1):
        for c in range(cols - 1, -1, -1):
            here = 1 if pizza[r][c] == "A" else 0
            apples[r][c] = here + apples[r + 1][c] + apples[r][c + 1] - apples[r + 1][c + 1]
    w = [[0] * (cols + 1) for _ in range(rows + 1)]
    for r in range(rows):
        for c in range(cols):
            if apples[r][c] > 0:
                w[r][c] = 1
    for _ in range(1, k):
        nxt = [[0] * (cols + 1) for _ in range(rows + 1)]
        for r in range(rows):
            for c in range(cols):
                total = 0
                for cut in range(r + 1, rows):
                    if apples[r][c] - apples[cut][c] > 0:
                        total += w[cut][c]
                for cut in range(c + 1, cols):
                    if apples[r][c] - apples[r][cut] > 0:
                        total += w[r][cut]
                nxt[r][c] = total % 1000000007
        w = nxt
    return w[0][0]


def main():
    seed = 1444
    check = 0
    for _ in range(200):
        seed = (seed * 1103515245 + 12345) % 2147483648
        rate = 5 + seed // 65536 % 46
        pizza = []
        for _ in range(50):
            line = []
            for _ in range(50):
                seed = (seed * 1103515245 + 12345) % 2147483648
                line.append("A" if seed // 65536 % 100 < rate else ".")
            pizza.append("".join(line))
        check = (check * 131 + ways(pizza, 10)) % 1000000007
    print(f"200 pizzas of 50 by 50: checksum {check}")


main()
