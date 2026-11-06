# LeetCode #1055: Shortest Way to Form String -- Python mirror of
# bench/shortest_way.kara.

seed = 1055


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def shortest_way(source, target):
    pieces = 0
    i = 0
    m = len(target)
    while i < m:
        start = i
        for c in source:
            if i < m and target[i] == c:
                i += 1
        if i == start:
            return -1
        pieces += 1
    return pieces


def random_word(n):
    return "".join(chr(97 + next_random() % 20) for _ in range(n))


def main():
    count, rounds = 100, 10
    pairs = []
    for _ in range(count):
        source = random_word(1000)
        target = random_word(10000)
        pairs.append((source, target))
    total = 0
    check = 0
    for _ in range(rounds):
        for source, target in pairs:
            answer = shortest_way(source, target)
            total += answer
            check = (check * 131 + answer) % 1000000007
    print(f"{count} pairs of 1000 and 10000 letters, {rounds} rounds: total {total}, checksum {check}")


main()
