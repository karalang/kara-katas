# LeetCode #679: 24 Game -- backtracking over pairs, in floating point.
# Mirrors the ★ arm (twenty_four_game.kara) and its test harness.


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


def b(x):
    return "true" if x else "false"


def show(cards):
    print(f"{cards} -> {b(judge_point24(cards))}")


def hands():
    for a in range(1, 10):
        for b_ in range(a, 10):
            for c in range(b_, 10):
                for d in range(c, 10):
                    yield a, b_, c, d


def main():
    for h in [[4, 1, 8, 7], [1, 2, 1, 2], [3, 3, 8, 8], [1, 5, 5, 5],
              [1, 3, 4, 6], [1, 4, 5, 6], [6, 6, 6, 6], [1, 1, 1, 1],
              [9, 9, 9, 9], [1, 1, 1, 8], [1, 1, 2, 6], [3, 3, 7, 7]]:
        show(h)
    solvable = 0
    count = 0
    by_low = [0] * 10
    total = 0
    for a, b_, c, d in hands():
        count += 1
        code = a * 1000 + b_ * 100 + c * 10 + d
        if judge_point24([a, b_, c, d]):
            solvable += 1
            by_low[a] += 1
            total = (total * 31 + code) % 1000000007
        else:
            total = (total * 31 + 7) % 1000000007
    lows = " ".join(str(by_low[a]) for a in range(1, 10))
    print(f"{solvable} of {count} hands solvable; by smallest card: {lows}")
    print(f"checksum {total}")
    agree = 0
    orders = [[0, 1, 2, 3], [3, 2, 1, 0], [1, 3, 0, 2], [2, 0, 3, 1]]
    for hand in hands():
        want = judge_point24(list(hand))
        if all(judge_point24([hand[o[0]], hand[o[1]], hand[o[2]], hand[o[3]]]) == want
               for o in orders):
            agree += 1
    print(f"{agree} of {count} hands agree in four orders")


main()
