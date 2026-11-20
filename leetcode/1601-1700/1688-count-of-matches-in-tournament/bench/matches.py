# LeetCode #1688: Count of Matches in Tournament -- the bench's Python
# mirror: the ★ arm on 500000 random n up to 10^9, all drawn first, each
# answered 40 times.


def matches(n):
    teams = n
    played = 0
    while teams > 1:
        played += teams // 2
        teams = (teams + 1) // 2
    return played


seed = 1688


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, rounds = 500000, 40
    values = []
    for _ in range(count):
        hi = next_random()
        values.append((hi * 32768 + next_random()) % 1000000000 + 1)
    total = 0
    check = 0
    for r in range(rounds):
        for n in values:
            answer = matches(n)
            total += answer
            check = (check * 31 + answer + r) % 1000000007
    print(f"{count} values of n, {rounds} rounds: {total} matches, checksum {check}")


main()
