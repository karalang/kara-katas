# LeetCode #1128: Number of Equivalent Domino Pairs -- the bench in Python,
# the ★ arm with a list of 100 counts, the same 16 sets and 300 rounds.


def num_equiv_domino_pairs(dominoes):
    count = [0] * 100
    pairs = 0
    for a, b in dominoes:
        key = min(a, b) * 10 + max(a, b)
        pairs += count[key]
        count[key] += 1
    return pairs


seed = 1128


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    sets = []
    for _ in range(16):
        dominoes = []
        for _ in range(40000):
            a = next_random() % 9 + 1
            b = next_random() % 9 + 1
            dominoes.append([a, b])
        sets.append(dominoes)
    total = 0
    check = 0
    for rnd in range(300):
        for j in range(len(sets)):
            at = (rnd * 7919 + j * 104729) % 40000
            side = rnd % 2
            sets[j][at][side] = sets[j][at][side] % 9 + 1
            answer = num_equiv_domino_pairs(sets[j])
            total += answer
            check = (check * 31 + answer) % 1000000007
    print(f"300 rounds over 16 sets of 4 * 10^4 dominoes: pairs total {total}, checksum {check}")


main()
