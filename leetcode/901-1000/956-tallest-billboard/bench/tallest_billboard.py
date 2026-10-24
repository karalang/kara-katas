# LeetCode #956: Tallest Billboard -- Python mirror of the Kara bench
# program (the shorter side by difference).


def tallest_billboard(rods):
    total = sum(rods)
    best = [-1] * (total + 1)
    best[0] = 0
    for r in rods:
        prev = list(best)
        for d in range(total + 1):
            short = prev[d]
            if short < 0:
                continue
            if d + r <= total and short > best[d + r]:
                best[d + r] = short
            nd = abs(d - r)
            ns = short + min(d, r)
            if ns > best[nd]:
                best[nd] = ns
    return best[0]


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    rounds, count, n = 30, 200, 20
    seed = [956]
    sets = [[1 + next_random(seed) % 250 for _ in range(n)] for _ in range(count)]
    total = 0
    check = 0
    for r in range(rounds):
        for i in range(count):
            k = (r + i) % count
            h = tallest_billboard(sets[k])
            total += h
            check = (check * 31 + h) % 1000000007
    print(f"{rounds} rounds over {count} sets of {n} rods up to 250: heights adding to {total}, checksum {check}")


main()
