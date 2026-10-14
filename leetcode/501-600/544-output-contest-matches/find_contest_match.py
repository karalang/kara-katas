# LeetCode #544: Output Contest Matches -- Python mirror of the ★ arm
# (rounds, in place); see find_contest_match.kara.


def find_contest_match(n):
    teams = [str(t) for t in range(1, n + 1)]
    m = n
    while m > 1:
        for i in range(m // 2):
            teams[i] = f"({teams[i]},{teams[m - 1 - i]})"
        m //= 2
    return teams[0]


# ---- test harness ----------------------------------------------------------


def sum_of(s):
    h = 0
    for b in s.encode():
        h = (h * 131 + b) % 1000000007
    return h


def main():
    for n in [2, 4, 8, 16]:
        print(f"{n} teams: {find_contest_match(n)}")
    n = 2
    while n <= 4096:
        s = find_contest_match(n)
        print(f"{n} teams: {len(s)} bytes, checksum {sum_of(s)}")
        n *= 2


main()
