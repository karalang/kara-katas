# Benchmark for #639: mirror of decode_ways_ii.kara (the ★ arm: the count
# of decodings of every prefix, two at a time) on the same workload.

M = 1000000007
ROUNDS = 600
STAR, ZERO, ONE, TWO, SIX = ord("*"), ord("0"), ord("1"), ord("2"), ord("6")


def alone(c):
    if c == STAR:
        return 9
    if c == ZERO:
        return 0
    return 1


def together(a, b):
    if a == STAR:
        if b == STAR:
            return 15
        return 2 if b <= SIX else 1
    if a == ONE:
        return 9 if b == STAR else 1
    if a == TWO:
        if b == STAR:
            return 6
        return 1 if b <= SIX else 0
    return 0


def num_decodings(s):
    before = 1
    last = alone(s[0])
    for i in range(1, len(s)):
        nxt = (last * alone(s[i]) + before * together(s[i - 1], s[i])) % M
        before = last
        last = nxt
    return last


seed = 639


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    texts = []
    for _ in range(20):
        s = bytearray()
        prev = ONE
        for _ in range(100000):
            c = STAR
            if next_random() % 10 >= 3:
                c = ONE + next_random() % 9
                if next_random() % 100 == 0 and prev in (ONE, TWO, STAR):
                    c = ZERO
            s.append(c)
            prev = c
        texts.append(bytes(s))
    total = 0
    checksum = 0
    for r in range(ROUNDS):
        count = num_decodings(texts[r % 20])
        total = (total + count) % M
        checksum = (checksum * 31 + count) % M
    print(f"20 strings of 100000 characters, {ROUNDS} rounds: total {total}, checksum {checksum}")


main()
