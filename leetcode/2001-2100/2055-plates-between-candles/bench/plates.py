# LeetCode #2055: Plates Between Candles -- Python mirror of the ★ arm's
# benchmark (plates.kara): the same 50 strings and five million queries,
# the same plate counts and nearest candles.

seed = 2055


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    hi = next_random()
    return hi * 32768 + next_random()


def plates_between_candles(s, queries):
    n = len(s)
    plates = [0] * (n + 1)
    before = [-1] * n
    last = -1
    for i in range(n):
        plates[i + 1] = plates[i] + (1 if s[i] == "*" else 0)
        if s[i] == "|":
            last = i
        before[i] = last
    after = [n] * n
    nxt = n
    for i in range(n - 1, -1, -1):
        if s[i] == "|":
            nxt = i
        after[i] = nxt
    answers = []
    for left, right in queries:
        first = after[left]
        last = before[right]
        answers.append(plates[last] - plates[first] if first < last else 0)
    return answers


def main():
    total = check = 0
    for t in range(50):
        every = t + 1
        s = "".join("|" if next_random() % every == 0 else "*" for _ in range(100000))
        queries = []
        for _ in range(100000):
            a = wide() % 100000
            b = wide() % 100000
            queries.append((min(a, b), max(a, b)))
        for a in plates_between_candles(s, queries):
            total += a
            check = (check * 31 + a + 1) % 1000000007
    print(f"50 strings: sum {total}, checksum {check}")


main()
