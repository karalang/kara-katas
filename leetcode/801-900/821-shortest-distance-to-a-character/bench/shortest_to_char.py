# Benchmark for #821: Shortest Distance to a Character -- the ★ arm (two sweeps).
#
# Mirrors shortest_to_char.kara: a sweep from the left keeps the last `c`
# seen and a sweep from the right the first, and each place keeps the
# nearer of the two.


def shortest_to_char(s, c):
    chars = list(s)
    n = len(chars)
    answer = [0] * n
    last = -n
    for i in range(n):
        if chars[i] == c:
            last = i
        answer[i] = i - last
    last = 2 * n
    for i in range(n - 1, -1, -1):
        if chars[i] == c:
            last = i
        answer[i] = min(answer[i], last - i)
    return answer


class Random:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def main():
    count = 64
    rounds = 50000
    rng = Random(821)
    strings = []
    targets = []
    for _ in range(count):
        strings.append("".join(chr(ord("a") + rng.next() % 26) for _ in range(10000)))
        targets.append(chr(ord("a") + rng.next() % 26))
    total = 0
    checksum = 0
    for r in range(rounds):
        g = r % count
        answer = shortest_to_char(strings[g], targets[g])
        total += sum(answer)
        checksum = (checksum * 131 + answer[r % 10000]) % 1000000007
    print(f"{rounds} rounds of {count} strings: total {total}, checksum {checksum}")


main()
