# LeetCode #2055: Plates Between Candles -- Python mirror of the ★ arm
# (plates.kara): the plates counted before each place, the nearest candle
# at or before and at or after it, and each query's plates the difference
# of the counts at its first and last candle. Output is byte-identical to
# the Kāra arms.


def plates_between_candles(s, queries):
    n = len(s)
    plates = [0] * (n + 1)
    candle_before = [-1] * n
    last = -1
    for i in range(n):
        plates[i + 1] = plates[i] + (1 if s[i] == "*" else 0)
        if s[i] == "|":
            last = i
        candle_before[i] = last
    candle_after = [n] * n
    nxt = n
    for i in range(n - 1, -1, -1):
        if s[i] == "|":
            nxt = i
        candle_after[i] = nxt
    answers = []
    for left, right in queries:
        first = candle_after[left]
        last = candle_before[right]
        answers.append(plates[last] - plates[first] if first < last else 0)
    return answers


# ---- test harness ---------------------------------------------------------

seed = 2055


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def draw(n, every):
    return "".join("|" if next_random() % every == 0 else "*" for _ in range(n))


def ask(n, q):
    queries = []
    for _ in range(q):
        a = next_random() % n
        b = next_random() % n
        queries.append((min(a, b), max(a, b)))
    return queries


def fold(check, answers):
    c = check
    for a in answers:
        c = (c * 31 + a + 1) % 1000000007
    return c


def show(xs):
    return "[" + ", ".join(str(x) for x in xs) + "]"


def main():
    examples = [
        ("**|**|***|", [(2, 5), (5, 9)]),
        ("***|**|*****|**||**|*", [(1, 17), (4, 5), (14, 17), (5, 11), (15, 16)]),
        ("|*|", [(0, 2), (0, 1), (1, 2)]),
        ("***", [(0, 2)]),
        ("||||", [(0, 3), (1, 2)]),
        ("*|*|*|*", [(0, 6), (1, 5), (2, 4), (3, 3)]),
    ]
    for s, queries in examples:
        print(f'"{s}" {show(f"({a}, {b})" for a, b in queries)} -> {show(plates_between_candles(s, queries))}')
    total = check = 0
    for _ in range(2000):
        n = next_random() % 38 + 3
        every = next_random() % 5 + 1
        s = draw(n, every)
        q = next_random() % 20 + 1
        answers = plates_between_candles(s, ask(n, q))
        total += sum(answers)
        check = fold(check, answers)
    print(f"2000 strings: sum {total}, checksum {check}")
    total = check = 0
    for t in range(10):
        s = draw(2000, [1, 2, 3, 5, 8, 13, 21, 30, 4, 10][t])
        answers = plates_between_candles(s, ask(2000, 2000))
        total += sum(answers)
        check = fold(check, answers)
    print(f"10 strings of 2000: sum {total}, checksum {check}")


main()
