# Benchmark for #544: Python mirror of the ★ arm (rounds, in place); see
# find_contest_match.kara.


def find_contest_match(n):
    teams = [str(t) for t in range(1, n + 1)]
    m = n
    while m > 1:
        for i in range(m // 2):
            teams[i] = f"({teams[i]},{teams[m - 1 - i]})"
        m //= 2
    return teams[0]


def main():
    # 200 rounds over every size the problem allows, 2 to 4,096 teams;
    # the length of each answer is summed, and one byte of it, picked
    # by the round and the size, goes into the checksum.
    total = 0
    checksum = 0
    for r in range(200):
        n = 2
        while n <= 4096:
            s = find_contest_match(n)
            b = ord(s[(r * 7919 + n * 13) % len(s)])
            total += len(s)
            checksum = (checksum * 31 + b) % 1000000007
            n *= 2
    print(f"200 rounds of 2 to 4096 teams: {total} bytes, checksum {checksum}")


main()
