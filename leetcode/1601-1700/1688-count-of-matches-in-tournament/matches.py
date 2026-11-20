# LeetCode #1688: Count of Matches in Tournament -- mirrors matches.kara,
# the ★ arm: the rounds played out.


def matches(n):
    teams = n
    played = 0
    while teams > 1:
        played += teams // 2
        teams = (teams + 1) // 2
    return played


class Seed:
    def __init__(self, v):
        self.v = v

    def next(self):
        self.v = (self.v * 1103515245 + 12345) % 2147483648
        return self.v // 65536


def main():
    print(matches(7))
    print(matches(14))
    print(matches(1))
    print(matches(200))
    total = 0
    check = 0
    for n in range(1, 201):
        answer = matches(n)
        total += answer
        check = (check * 31 + answer) % 1000000007
    print(f"n from 1 to 200: {total} matches, checksum {check}")
    seed = Seed(1688)
    total = 0
    check = 0
    for _ in range(3000):
        hi = seed.next()
        n = (hi * 32768 + seed.next()) % 1000000000 + 1
        answer = matches(n)
        total += answer
        check = (check * 31 + answer) % 1000000007
    print(f"3000 n up to 1000000000: {total} matches, checksum {check}")


main()
