# Benchmark for #818: Race Car -- the ★ arm (the best run to each distance).
#
# Mirrors racecar.kara: one table of the best run to every distance up to
# the target, each entry the better of overshooting and stopping short.


def racecar(target):
    best = [0] * (target + 1)
    for t in range(1, target + 1):
        n = t.bit_length()
        full = (1 << n) - 1
        if t == full:
            best[t] = n
            continue
        shortest = n + 1 + best[full - t]
        short = (1 << (n - 1)) - 1
        for m in range(n - 1):
            back = (1 << m) - 1
            steps = (n - 1) + 1 + m + 1 + best[t - short + back]
            if steps < shortest:
                shortest = steps
        best[t] = shortest
    return best[target]


def main():
    rounds = 40000
    seed = 818
    total = 0
    checksum = 0
    for _ in range(rounds):
        seed = (seed * 1103515245 + 12345) % 2147483648
        t = 1 + (seed // 65536) % 10000
        answer = racecar(t)
        total += answer
        checksum = (checksum * 131 + answer) % 1000000007
    print(f"{rounds} rounds of targets up to 10000: total {total}, checksum {checksum}")


main()
