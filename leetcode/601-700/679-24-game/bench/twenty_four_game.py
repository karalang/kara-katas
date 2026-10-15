# Benchmark for #679: the ★ arm, pairs combined in floating point.


def reach(values):
    n = len(values)
    if n == 1:
        return abs(values[0] - 24.0) < 0.000001
    for i in range(n):
        for j in range(i + 1, n):
            a = values[i]
            b = values[j]
            rest = [values[k] for k in range(n) if k != i and k != j]
            results = [a + b, a - b, b - a, a * b]
            if b != 0.0:
                results.append(a / b)
            if a != 0.0:
                results.append(b / a)
            for r in results:
                if reach(rest + [r]):
                    return True
    return False


def judge_point24(cards):
    return reach([float(c) for c in cards])


def main():
    solvable = 0
    total = 0
    for a in range(1, 14):
        for b in range(1, 14):
            for c in range(1, 14):
                for d in range(1, 14):
                    code = a * 1000 + b * 100 + c * 10 + d
                    if judge_point24([a, b, c, d]):
                        solvable += 1
                        total = (total * 31 + code) % 1000000007
                    else:
                        total = (total * 31 + 7) % 1000000007
    print(f"28561 hands: {solvable} solvable, checksum {total}")


main()
